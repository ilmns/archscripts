#!/bin/bash

# Check for root privileges
if [ "$(id -u)" -ne 0 ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

set -e
set -o pipefail

log_file="install.log"
dry_run=false

log() {
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" | tee -a "$log_file"
}

# Initialize values for Finland, Helsinki
TIMEZONE_REGION="Europe"
TIMEZONE_CITY="Helsinki"
LOCALE="fi_FI.UTF-8"
KEYBOARD_LAYOUT="fi"

layout_keyboard() {
    log "Setting keyboard layout..."
    loadkeys "$1"
}

check_internet_connection() {
    log "Checking internet connection..."
    if ping -c 1 archlinux.org >/dev/null; then
        log "Internet connection is active."
    else
        log "Internet connection is not active. Please ensure a connection before proceeding."
        exit 1
    fi
}

synchronize_clock() {
    log "Updating system clock..."
    timedatectl set-ntp true
}

validate_input() {
    local prompt="$1"
    local pattern="$2"
    read -p "$prompt" INPUT
    while [[ ! $INPUT =~ $pattern ]]; do
        echo "Invalid input. Please try again."
        read -p "$prompt" INPUT
    done
    echo "$INPUT"
}

select_partition_layout() {
    local options=(
        "UEFI with GPT"
        "BIOS with MBR"
        "BIOS/GPT"
    )
    local layout
    PS3="Enter your desired disk partition layout: "
    select layout in "${options[@]}"; do
        case $layout in
            "UEFI with GPT")
                PARTITION_LAYOUT="mklabel gpt mkpart ESP fat32 1MiB 551MiB set 1 boot on mkpart primary linux-swap 551MiB 1551MiB mkpart primary ext4 1551MiB 100%"
                break
                ;;
            "BIOS with MBR")
                PARTITION_LAYOUT="mklabel msdos mkpart primary linux-swap 1MiB 551MiB mkpart primary ext4 551MiB 100%"
                break
                ;;
            "BIOS/GPT")
                PARTITION_LAYOUT="mklabel gpt mkpart none 1MiB 2MiB set 1 bios_grub on mkpart primary linux-swap 2MiB 514MiB mkpart primary ext4 514MiB 100%"
                break
                ;;
            *) echo "Invalid option. Please choose a valid partition layout." ;;
        esac
    done
}

disk_partition() {
    log "Disk partitioning for installation:"

    echo ""
    echo "Example Layouts for Filesystem:"
    echo ""

    echo "UEFI with GPT:"
    echo ""
    echo "Mount point 	Partition 	Partition type 	Suggested size"
    echo "/mnt/boot1 	/dev/efi_system_partition 	EFI system partition 	At least 300 MiB. If multiple kernels will be installed, then no less than 1 GiB."
    echo "[SWAP] 	/dev/swap_partition 	Linux swap 	More than 512 MiB"
    echo "/mnt 	/dev/root_partition 	Linux x86-64 root (/) 	Remainder of the device"
    echo ""

    echo "BIOS with MBR:"
    echo ""
    echo "Mount point 	Partition 	Partition type 	Suggested size"
    echo "[SWAP] 	/dev/swap_partition 	Linux swap 	More than 512 MiB"
    echo "/mnt 	/dev/root_partition 	Linux 	Remainder of the device"
    echo ""

    echo "BIOS/GPT:"
    echo ""
    echo "Mount point on the installed system 	Partition 	Partition type GUID 	Partition attributes 	Suggested size"
    echo "None 	/dev/sda1 	21686148-6449-6E6F-744E-656564454649: BIOS boot partition3 		1 MiB"
    echo "[SWAP] 	/dev/sda2 	0657FD6D-A4AB-43C4-84E5-0933C84B4F4F: Linux swap 		More than 512 MiB"
    echo "/ 	/dev/sda3 	4F68BCE3-E8CD-4DB1-96E7-FBCAF984B709: Linux x86-64 root (/) 		Remainder of the device"
    echo ""

    select_partition_layout

    if [ -n "$(lsblk | grep 'nvme')" ]; then
        log "Detected NVMe disk. Partitioning using nvme-cli..."
        nvme_disk=$(lsblk -d -o NAME | grep 'nvme' | head -n1)
        parted -s "/dev/$nvme_disk" $PARTITION_LAYOUT
        EFI_PARTITION="/dev/${nvme_disk}p1"
        SWAP_PARTITION="/dev/${nvme_disk}p2"
        ROOT_PARTITION="/dev/${nvme_disk}p3"
    else
        log "Partitioning for non-NVMe disk..."
        parted -s /dev/sda $PARTITION_LAYOUT
        EFI_PARTITION="/dev/sda1"
        SWAP_PARTITION="/dev/sda2"
        ROOT_PARTITION="/dev/sda3"
    fi

    mkfs.fat -F32 "$EFI_PARTITION"
    mkswap "$SWAP_PARTITION"
    swapon "$SWAP_PARTITION"
    mkfs.ext4 "$ROOT_PARTITION"
    mount "$ROOT_PARTITION" /mnt
    mkdir /mnt/boot
    mount "$EFI_PARTITION" /mnt/boot
}

base_system_install() {
    log "Installing base system..."
    if [ "$dry_run" = true ]; then
        log "Dry run: Skipping package installation"
    else
        pacstrap /mnt base linux linux-firmware base-devel vim nano networkmanager dhcpcd wpa_supplicant dialog
        genfstab -U /mnt >> /mnt/etc/fstab
        arch-chroot /mnt systemctl enable NetworkManager
    fi
}

configure_locale() {
    log "Configuring localization..."
    if [ "$dry_run" = true ]; then
        log "Dry run: Skipping locale configuration"
    else
        echo "$LOCALE UTF-8" > /mnt/etc/locale.gen
        arch-chroot /mnt locale-gen
        echo "LANG=$LOCALE" > /mnt/etc/locale.conf
        echo "KEYMAP=$KEYBOARD_LAYOUT" > /mnt/etc/vconsole.conf
    fi
}

configure_timezone() {
    log "Configuring timezone..."
    if [ "$dry_run" = true ]; then
        log "Dry run: Skipping timezone configuration"
    else
        arch-chroot /mnt ln -sf "/usr/share/zoneinfo/$TIMEZONE_REGION/$TIMEZONE_CITY" /mnt/etc/localtime
        arch-chroot /mnt hwclock --systohc
    fi
}

configure_network() {
    log "Configuring network..."
    HOSTNAME=$(validate_input "Enter your hostname: " '^[a-zA-Z0-9\-]+$')
    if [ "$dry_run" = true ]; then
        log "Dry run: Skipping network configuration"
    else
        echo "$HOSTNAME" > /mnt/etc/hostname
        printf "127.0.0.1\tlocalhost\n::1\t\tlocalhost\n127.0.1.1\t$HOSTNAME.localdomain\t$HOSTNAME" > /mnt/etc/hosts
    fi
}

set_password() {
    log "Setting root password..."
    if [ "$dry_run" = true ]; then
        log "Dry run: Skipping password configuration"
    else
        arch-chroot /mnt passwd

        log "Creating a new user and setting password..."
        USERNAME=$(validate_input "Enter the name for the new user: " '^[a-z_][a-z0-9_-]*[$]?$')
        arch-chroot /mnt useradd -m -G wheel "$USERNAME"
        arch-chroot /mnt passwd "$USERNAME"

        log "Setting sudo privileges..."
        echo "$USERNAME ALL=(ALL) ALL" | arch-chroot /mnt EDITOR='tee -a' visudo
    fi
}

configure_bootloader() {
    log "Installing and configuring bootloader..."
    if [ "$dry_run" = true ]; then
        log "Dry run: Skipping bootloader installation and configuration"
    else
        DRIVE_TYPE=$(lsblk -d -o NAME,TYPE | awk '/^sda|^nvme/{print $2}')
        if [ "$DRIVE_TYPE" = "disk" ]; then
            arch-chroot /mnt pacman -S --noconfirm grub
            arch-chroot /mnt grub-install --target=i386-pc "/dev/sda"
            arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg
        elif [ "$DRIVE_TYPE" = "disk/ssd" ] || [ "$DRIVE_TYPE" = "disk/nvme" ]; then
            arch-chroot /mnt pacman -S --noconfirm grub efibootmgr
            arch-chroot /mnt grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
            arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg
        else
            log "Unsupported drive type: $DRIVE_TYPE"
            log "Bootloader installation failed."
        fi
    fi
}

update_packages() {
    log "Updating packages..."
    if [ "$dry_run" = true ]; then
        log "Dry run: Skipping package updates"
    else
        arch-chroot /mnt pacman -Syu --noconfirm
        if [ "$DRIVE_TYPE" = "disk/ssd" ]; then
            arch-chroot /mnt pacman -S --noconfirm util-linux
        fi
    fi
}

print_usage() {
    echo "Usage: $0 [--dry-run] [--locale=<locale>] [--timezone=<timezone>] [--keyboard-layout=<layout>]"
}

# Start of the script

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            dry_run=true
            ;;
        --locale=*)
            LOCALE="${1#*=}"
            ;;
        --timezone=*)
            TIMEZONE="${1#*=}"
            ;;
        --keyboard-layout=*)
            KEYBOARD_LAYOUT="${1#*=}"
            ;;
        *)
            echo "Invalid argument: $1"
            print_usage
            exit 1
            ;;
    esac
    shift
done

# Pre-installation checks
check_internet_connection

# Logging
log "Welcome to the Arch Linux installation wizard!"

# Display dry run status if enabled
if [ "$dry_run" = true ]; then
    log "Dry run mode is enabled. No changes will be made."
fi

layout_keyboard "$KEYBOARD_LAYOUT"
synchronize_clock
disk_partition
base_system_install
configure_locale
configure_timezone
configure_network
set_password
configure_bootloader
update_packages
log "Installation is completed. Please remove the installation media before rebooting."
