#!/bin/bash
# Usage:
#   It is expected that this script will be invoked using the syntax:
#       setupPortage.sh <EPREFIX>

# Check for proper number of command line args.
EXPECTED_ARGS=1
E_BADARGS=65

if [ $# -ne $EXPECTED_ARGS ]
then
    echo "Usage: `basename $0` <install directory>"
    exit $E_BADARGS
fi

# Get path of this script for calling other scripts
SELFPATH=`dirname "$0"`

# Use the first argument as the EPREFIX directory
export EPREFIX="$1"

# Create the target directory if it doesn't exist
mkdir -p $EPREFIX

# Add Prefix paths to the PATH
export PATH="$EPREFIX/usr/bin:$EPREFIX/bin:$EPREFIX/tmp/usr/bin:$EPREFIX/tmp/bin:$PATH"

# Use the bootstrap script for the initial set of packages
chmod 755 $SELFPATH/bootstrap-prefix.sh
$SELFPATH/bootstrap-prefix.sh $EPREFIX tree
$SELFPATH/bootstrap-prefix.sh $EPREFIX/tmp make
$SELFPATH/bootstrap-prefix.sh $EPREFIX/tmp wget
$SELFPATH/bootstrap-prefix.sh $EPREFIX/tmp sed
$SELFPATH/bootstrap-prefix.sh $EPREFIX/tmp python
$SELFPATH/bootstrap-prefix.sh $EPREFIX/tmp coreutils
$SELFPATH/bootstrap-prefix.sh $EPREFIX/tmp findutils
$SELFPATH/bootstrap-prefix.sh $EPREFIX/tmp tar
$SELFPATH/bootstrap-prefix.sh $EPREFIX/tmp patch259
$SELFPATH/bootstrap-prefix.sh $EPREFIX/tmp grep
$SELFPATH/bootstrap-prefix.sh $EPREFIX/tmp gawk
$SELFPATH/bootstrap-prefix.sh $EPREFIX/tmp bash
$SELFPATH/bootstrap-prefix.sh $EPREFIX portage

hash -r

# Emerge oneshots
emerge --oneshot sed
emerge --oneshot --nodeps bash
emerge --oneshot pax-utils
emerge --oneshot --nodeps xz-utils
emerge --oneshot --nodeps "<wget-1.13.4-r1"

emerge --oneshot --nodeps sys-apps/baselayout-prefix
emerge --oneshot --nodeps sys-devel/m4
emerge --oneshot --nodeps sys-devel/flex
emerge --oneshot --nodeps sys-devel/bison
emerge --oneshot --nodeps sys-devel/binutils-config

emerge --oneshot --nodeps sys-devel/binutils-apple
emerge --oneshot --nodeps sys-devel/gcc-config
emerge --oneshot --nodeps sys-devel/gcc-apple

emerge --oneshot sys-apps/coreutils
emerge --oneshot sys-apps/findutils
emerge --oneshot '<app-arch/tar-1.26-r1'
emerge --oneshot sys-apps/grep
emerge --oneshot sys-devel/patch
emerge --oneshot sys-apps/gawk
emerge --oneshot sys-devel/make
emerge --oneshot --nodeps sys-apps/file
emerge --oneshot --nodeps app-admin/eselect

# Emerge portage
env FEATURES="-collision-protect" emerge --oneshot sys-apps/portage

# Remove tmp directory
rm -Rf $EPREFIX/tmp/*
hash -r

# Update tree
emerge --sync

# Emerge system
env USE=-git emerge -u system

# TODO: Parse CPU info and use it to determine arch variable
echo 'USE="aac acpi -alsa flac -git gtk mp3 opengl pdf qt4 ssl truetype unicode x264 xvid"' >> $EPREFIX/etc/portage/make.conf
# -march=core2 for Core2Duo
echo 'CFLAGS="-O2 -pipe -march=core2"' >> $EPREFIX/etc/portage/make.conf
echo 'CXXFLAGS="${CFLAGS}"' >> $EPREFIX/etc/portage/make.conf

#emerge -e system
