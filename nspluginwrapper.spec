Summary:	Open Source compatibility plugin for Netscape 4 (NPAPI) plugins
Name:		nspluginwrapper
Version:	0.9.90.1
Release:	0.1
License:	GPL v2
Group:		Applications/Multimedia
Source0:	http://www.gibix.net/projects/nspluginwrapper/files/%{name}-%{version}.tar.bz2
# Source0-md5:	34021feaf1a2ddbf718b20d9d1376c6e
URL:		http://www.gibix.net/dokuwiki/en:projects:nspluginwrapper
BuildRequires:	gtk+2-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/browser-plugins

# list of supported browsers, in free form text
%define		browsers	mozilla, mozilla-firefox, netscape, seamonkey

%description
nspluginwrapper is an Open Source compatibility plugin for Netscape 4 (NPAPI) plugins. That is, it enables you to use plugins on platforms they were not built for. For example, you can use the Adobe Flash plugin with x86-64 compiled Mozilla browsers.

%prep
%setup -q

%build
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
#%doc AUTHORS ChangeLog NEWS README TODO
#%attr(755,root,root) %{_bindir}/*
#%{_datadir}/%{name}
#%{_desktopdir}/*.desktop
#%{_mandir}/man1/*
#%{_pixmapsdir}/*
