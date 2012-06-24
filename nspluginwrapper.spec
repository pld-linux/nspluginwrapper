# TODO
# - create -plugin and -viewer packages (like upstream)
Summary:	Open Source compatibility plugin for Netscape 4 (NPAPI) plugins
Summary(pl):	Wtyczka Open Source dla kompatybilno�ci z wtyczkami Netscape'a 4 (NPAPI)
Name:		nspluginwrapper
Version:	0.9.91.2
Release:	0.1
License:	GPL v2
Group:		Applications/Multimedia
Source0:	http://gwenole.beauchesne.info/projects/nspluginwrapper/files/%{name}-%{version}.tar.bz2
# Source0-md5:	74e40fa501ded6f1670684b3e42464c7
URL:		http://gwenole.beauchesne.info/en/projects/nspluginwrapper
BuildRequires:	/usr/lib/libsupc++.a
BuildRequires:	gtk+2-devel
#Requires:	qemu
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

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DONT_STRIP=yes \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
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
