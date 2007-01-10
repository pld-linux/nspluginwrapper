# TODO
# - create -plugin and -viewer packages (like upstream)
Summary:	Open Source compatibility plugin for Netscape 4 (NPAPI) plugins
Summary(pl):	Wtyczka Open Source dla kompatybilno¶ci z wtyczkami Netscape'a 4 (NPAPI)
Name:		nspluginwrapper
Version:	0.9.91.2
Release:	0.2
License:	GPL v2
Group:		Applications/Multimedia
Source0:	http://gwenole.beauchesne.info/projects/nspluginwrapper/files/%{name}-%{version}.tar.bz2
# Source0-md5:	74e40fa501ded6f1670684b3e42464c7
URL:		http://gwenole.beauchesne.info/en/projects/nspluginwrapper
BuildRequires:	/usr/lib/libsupc++.a
BuildRequires:	rpmbuild(macros) >= 1.357
Requires:	browser-plugins >= 2.0
BuildRequires:	gtk+2-devel
#Requires:	qemu
Requires:	linux32
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nspluginwrapper is an Open Source compatibility plugin for Netscape 4
(NPAPI) plugins. That is, it enables you to use plugins on platforms
they were not built for. For example, you can use the Adobe Flash
plugin with x86-64 compiled Mozilla browsers.

%description -l pl
nspluginwrapper to wtyczka Open Source dla kompatybilno¶ci z wtyczkami
Netscape'a 4 (NPAPI). Pozwala u¿ywaæ wtyczek na platformach, dla
których nie zosta³y zbudowane. Na przyk³ad mo¿na u¿ywaæ wtyczki Adobe
Flash z przegl±darkami Mozilla zbudowanymi na architekturê x86-64.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DONT_STRIP=yes \
	DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_browserpluginsdir}
ln -s %{_prefix}/lib/%{name}/%{_arch}/%{_os}/npwrapper.so $RPM_BUILD_ROOT%{_browserpluginsdir}/npwrapper.so

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_browser_plugins
if [ "$1" = 1 ]; then
	%{_bindir}/%{name} -v -a -i
else
	%{_bindir}/%{name} -v -a -u
fi

%preun
if [ "$1" = 0 ]; then
	%update_browser_plugins
	%{_bindir}/%{name} -v -a -r
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README TODO
%attr(755,root,root) %{_browserpluginsdir}/npwrapper.so
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
%attr(755,root,root) %{_prefix}/lib/nspluginwrapper/x86_64/linux/npconfig
%attr(755,root,root) %{_prefix}/lib/nspluginwrapper/x86_64/linux/npwrapper.so
