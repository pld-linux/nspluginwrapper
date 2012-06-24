# TODO
# - create -plugin and -viewer packages (like upstream)
Summary:	Open Source compatibility plugin for Netscape 4 (NPAPI) plugins
Summary(pl):	Wtyczka Open Source dla kompatybilno�ci z wtyczkami Netscape'a 4 (NPAPI)
Name:		nspluginwrapper
Version:	0.9.91.2
Release:	0.11
License:	GPL v2
Group:		Applications/Multimedia
Source0:	http://gwenole.beauchesne.info/projects/nspluginwrapper/files/%{name}-%{version}.tar.bz2
# Source0-md5:	74e40fa501ded6f1670684b3e42464c7
Patch0:		%{name}-plugindirs.patch
URL:		http://gwenole.beauchesne.info/en/projects/nspluginwrapper
BuildRequires:	/usr/lib/libsupc++.a
BuildRequires:	gtk+2-devel
BuildRequires:	rpmbuild(macros) >= 1.363
Requires:	browser-plugins >= 2.0
Requires:	linux32
#Requires:	qemu
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nspluginwrapper is an Open Source compatibility plugin for Netscape 4
(NPAPI) plugins. That is, it enables you to use plugins on platforms
they were not built for. For example, you can use the Adobe Flash
plugin with x86-64 compiled Mozilla browsers.

%description -l pl
nspluginwrapper to wtyczka Open Source dla kompatybilno�ci z wtyczkami
Netscape'a 4 (NPAPI). Pozwala u�ywa� wtyczek na platformach, dla
kt�rych nie zosta�y zbudowane. Na przyk�ad mo�na u�ywa� wtyczki Adobe
Flash z przegl�darkami Mozilla zbudowanymi na architektur� x86-64.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--with-biarch
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

# we pretend we're browser for x86 ;)
install -d $RPM_BUILD_ROOT%{_prefix}/lib/%{name}/plugins
%browser_plugins_add_browser %{name} -p %{_prefix}/lib/%{name}/plugins -a i386

%{__make} install \
	DONT_STRIP=yes \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 002
if [ "$1" = 1 ]; then
	%{_bindir}/%{name} -v -a -i
else
	%{_bindir}/%{name} -v -a -u
fi
%update_browser_plugins

%preun
if [ "$1" = 0 ]; then
	umask 002
	%{_bindir}/%{name} -v -a -r
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/nspluginwrapper
%dir %{_prefix}/lib/nspluginwrapper
%dir %{_prefix}/lib/nspluginwrapper/i386
%dir %{_prefix}/lib/nspluginwrapper/i386/linux
%attr(755,root,root) %{_prefix}/lib/nspluginwrapper/i386/linux/libxpcom.so
%attr(755,root,root) %{_prefix}/lib/nspluginwrapper/i386/linux/npviewer
%attr(755,root,root) %{_prefix}/lib/nspluginwrapper/i386/linux/npviewer.bin
%dir %{_prefix}/lib/nspluginwrapper/noarch
%attr(755,root,root) %{_prefix}/lib/nspluginwrapper/noarch/mkruntime
%attr(755,root,root) %{_prefix}/lib/nspluginwrapper/noarch/npviewer
%dir %{_prefix}/lib/nspluginwrapper/x86_64
%dir %attr(755,root,root) %{_prefix}/lib/nspluginwrapper/x86_64/linux
%attr(755,root,root) %{_prefix}/lib/nspluginwrapper/x86_64/linux/npconfig
%attr(755,root,root) %{_prefix}/lib/nspluginwrapper/x86_64/linux/npwrapper.so

# you should put plugins here you want to be automatically used in 64bit browsers
%dir %{_prefix}/lib/%{name}/plugins
%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist
