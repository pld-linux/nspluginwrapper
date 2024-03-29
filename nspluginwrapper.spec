# TODO
# - make it not to scan root user plugins:
#  # /usr/bin/nspluginwrapper -v -a -i
#  Auto-install plugins from /usr/lib/nspluginwrapper/plugins
#  Looking for plugins in /usr/lib/nspluginwrapper/plugins
#  Install plugin /usr/lib/nspluginwrapper/plugins/libflashplayer.so
#    into /usr/lib64/browser-plugins/npwrapper.libflashplayer.so
#  Auto-install plugins from /root/.mozilla/plugins
#  Looking for plugins in /root/.mozilla/plugins
Summary:	Open Source compatibility plugin for Netscape 4 (NPAPI) plugins
Summary(pl.UTF-8):	Wtyczka Open Source dla kompatybilności z wtyczkami Netscape'a 4 (NPAPI)
Name:		nspluginwrapper
Version:	1.4.4
Release:	0.4
License:	GPL v2
Group:		Applications/Multimedia
Source0:	http://nspluginwrapper.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	36f3e290fc4ce56f65ee695078961188
Patch0:		%{name}-plugindirs.patch
Patch1:		%{name}-biarch.patch
URL:		http://nspluginwrapper.org/
BuildRequires:	gcc-c++-multilib
BuildRequires:	gtk+2-devel >= 1:2.0
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.365
BuildRequires:	xorg-lib-libXt-devel
Requires:	browser-plugins >= 3.0
Requires:	linux32
# to have sound in flash player install 32bit alsa-lib
Requires:	libasound.so.2
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nspluginwrapper is an Open Source compatibility plugin for Netscape 4
(NPAPI) plugins. That is, it enables you to use plugins on platforms
they were not built for. For example, you can use the Adobe Flash
plugin with x86-64 compiled Mozilla browsers.

%description -l pl.UTF-8
nspluginwrapper to wtyczka Open Source dla kompatybilności z wtyczkami
Netscape'a 4 (NPAPI). Pozwala używać wtyczek na platformach, dla
których nie zostały zbudowane. Na przykład można używać wtyczki Adobe
Flash z przeglądarkami Mozilla zbudowanymi na architekturę x86-64.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
./configure \
	--enable-biarch
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

# we pretend we're browser for x86 ;)
install -d $RPM_BUILD_ROOT%{_prefix}/lib/%{name}/plugins
%browser_plugins_add_browser %{name} -p %{_prefix}/lib/%{name}/plugins -a i386 -b <<'EOF'
# use 64bit versions

# mplayerplug-in
mplayerplug-in*

# browser-plugin-helixplayer
nphelix.*

# browser-plugin-gplflash
libnpflash.so

# browser-plugin-gpac
nposmozilla.*

# browser-plugin-djvulibre
nsdejavu.so

# java-sun: libjavaplugin_oji.so is not a valid NPAPI plugin
libjavaplugin_oji.so

libcult3dplugin.so
kaffeineplugin.so
npfreewrl.so
EOF

%{__make} -j1 install \
	DONT_STRIP=yes \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

# uh.
# first we call update-browser-plugins to make links to our browser dir
# then we call nspluginwrapper -v -[ui] to create npwrapper.*.so plugins
# then we call update-browser-plugins once again to create links to 64bit browser plugins dir

%post
umask 022
%update_browser_plugins
if [ "$1" = 1 ]; then
	%{_bindir}/%{name} -v -a -i
else
	%{_bindir}/%{name} -v -a -u
fi
%update_browser_plugins

%preun
if [ "$1" = 0 ]; then
	rm -f %{_browserpluginsdir}/npwrapper.*.so
	%{_bindir}/%{name} -v -a -r
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog.pre-1-4 NEWS README TODO
%attr(755,root,root) %{_bindir}/nspluginplayer
%attr(755,root,root) %{_bindir}/nspluginwrapper
%dir %{_prefix}/lib/nspluginwrapper
%dir %{_prefix}/lib/nspluginwrapper/i386
%dir %{_prefix}/lib/nspluginwrapper/i386/linux
%attr(755,root,root) %{_prefix}/lib/nspluginwrapper/i386/linux/libnoxshm.so
%attr(755,root,root) %{_prefix}/lib/nspluginwrapper/i386/linux/npviewer
%attr(755,root,root) %{_prefix}/lib/nspluginwrapper/i386/linux/npviewer.bin
%dir %{_prefix}/lib/nspluginwrapper/noarch
%attr(755,root,root) %{_prefix}/lib/nspluginwrapper/noarch/npviewer.sh
%dir %{_prefix}/lib/nspluginwrapper/x86_64
%dir %{_prefix}/lib/nspluginwrapper/x86_64/linux
%attr(755,root,root) %{_prefix}/lib/nspluginwrapper/x86_64/linux/npconfig
%attr(755,root,root) %{_prefix}/lib/nspluginwrapper/x86_64/linux/npplayer
%attr(755,root,root) %{_prefix}/lib/nspluginwrapper/x86_64/linux/npwrapper.so

# you should put plugins here you want to be automatically used in 64bit browsers
%dir %{_prefix}/lib/%{name}/plugins
%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist
