Name: grub
Version: 0.97+
Release: b4
Summary: Grand Unified Boot Loader.
Group: System Environment/Base
License: GPLv2+

BuildRequires: binutils >= 2.9.1.0.23, ncurses-devel
BuildRequires: autoconf automake
BuildRequires: nasm
%ifarch x86_64
BuildRequires: glibc-devel(x86-32)
BuildRequires: libstdc++(x86-32)
BuildRequires: libgcc(x86-32)
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

URL: https://github.com/chenall/grub4dos
Source0: ftp://alpha.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2

%description
GRUB (Grand Unified Boot Loader) is an experimental boot loader
capable of booting into most free operating systems - Linux, FreeBSD,
NetBSD, GNU Mach, and others as well as most commercial operating
systems.

%prep
%setup -q
# This is from
# http://git.kernel.org/?p=boot/grub-fedora/grub-fedora.git;a=summary
#patch -p1 < berry/grub-fedora-9.patch
#patch -p1 < berry/grub-keystatus.patch

# Various bugfixes
# http://fedorapeople.org/~lkundrak/grub-fedora.git/
#patch -p1 < berry/0001-Get-rid-of-usr-bin-cmp-dependency.patch
#patch -p1 < berry/0002-Add-strspn-strcspn-and-strtok_r.patch
#patch -p1 < berry/0003-Allow-passing-multiple-image-files-to-the-initrd-com.patch
#patch -p1 < berry/0004-Obey-2.06-boot-protocol-s-cmdline_size.patch

#patch -p1 < berry/grub-0.97-printf_hex.patch
#patch -p1 < berry/grub-0.97-eficd.patch
#patch -p1 < berry/grub-0.97-xfs-buildfix.patch
#patch -p1 < berry/grub-0.97-efigraph-use-blt.patch
#patch -p1 < berry/grub-0.97-efislice.patch
#patch -p1 < berry/grub-0.97-efistatus.patch
#patch -p1 < berry/grub-0.97-fat-lowercase.patch
#patch -p1 < berry/grub-0.97-efipxe.patch
#patch -p1 < berry/grub-0.97-tolower.patch
#patch -p1 < berry/grub-low-memory.patch
#patch -p1 < berry/grub-install_virtio_blk_support.patch
#patch -p1 < berry/grub-fix-memory-corruption.patch
#patch -p1 < berry/grub-ext4-support.patch
#patch -p1 < berry/grub-0.97-xfs-writable-strings.patch
#patch -p1 < berry/grub-0.97-partitionable-md.patch
#patch -p1 < berry/grub-0.97-relocatable-kernel-on-x86_64-uefi.patch
#patch -p1 < berry/grub-0.97-use-gnuefi.patch

# for NTFS
patch -p1 < berry/ntfs-patch
patch -p1 < berry/fsys_ntfs.c.patch
#cp -a berry/fsys_ntfs.c stage2/

#sed -e "s:-Wl,-Bstatic -lncurses -ltinfo -Wl,-Bdynamic:-lncurses:" -i configure.in
#sed -e "s:-Wl,-Bstatic -lcurses -ltinfo -Wl,-Bdynamic:-lcurses:" -i configure.in

%build
autoupdate
autoreconf -i
#autoconf
GCCVERS=$(gcc --version | head -1 | cut -d\  -f3 | cut -d. -f1)
#CFLAGS="-Os -g -fno-strict-aliasing -Wall -Werror -Wno-shadow -Wno-unused"
#CFLAGS="-Os -fno-strict-aliasing -Wall -Werror -Wno-shadow -Wno-unused -Wno-misleading-indentation"
CFLAGS="-Os -fno-strict-aliasing -Wall"
if [ "$GCCVERS" == "4" ]; then
	CFLAGS="$CFLAGS -Wno-pointer-sign"
fi
export CFLAGS
#configure --sbindir=/sbin --disable-auto-linux-mem-opt --datarootdir=%{_datadir} --with-platform=efi
#make
#mv efi/grub.efi .
#make clean
#
#autoreconf
#autoconf
#CFLAGS="$CFLAGS -static"
#export CFLAGS
%configure --sbindir=/sbin --disable-auto-linux-mem-opt --datarootdir=%{_datadir}
make

%install
rm -fr $RPM_BUILD_ROOT
%makeinstall sbindir=${RPM_BUILD_ROOT}/sbin
mkdir -p ${RPM_BUILD_ROOT}/boot/grub
#mkdir -m 0755 -p ${RPM_BUILD_ROOT}/boot/efi/EFI/redhat/
#install -m 755 grub.efi ${RPM_BUILD_ROOT}/boot/efi/EFI/redhat/grub.efi

rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir

%clean
rm -fr $RPM_BUILD_ROOT

#%post
#if [ "$1" = 1 ]; then
#  /sbin/install-info --info-dir=%{_infodir} %{_infodir}/grub.info.gz || :
#  /sbin/install-info --info-dir=%{_infodir} %{_infodir}/multiboot.info.gz || :
#fi
#
#%preun
#if [ "$1" = 0 ] ;then
#  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/grub.info.gz || :
#  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/multiboot.info.gz || :
#fi

%files
%defattr(-,root,root)
#%doc AUTHORS ChangeLog NEWS README COPYING TODO docs/menu.lst
/boot/grub
#%attr(0755,root,root)/boot/efi/EFI/redhat
/sbin/grub
/sbin/grub-install
#/sbin/grub-terminfo
#/sbin/grub-md5-crypt
#{_bindir}/mbchk
#{_infodir}/grub*
#{_infodir}/multiboot*
#{_mandir}/man*/*
#{_datadir}/grub
%{_libdir}/grub

%changelog
* Mon Feb 11 2019 Yuichiro Nakada <berry@berry-lab.net>
- Update
* Wed Dec 30 2009 Yuichiro Nakada <berry@po.yui.mine.nu>
- Create for Berry Linux
