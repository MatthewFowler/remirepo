#
# RPM spec file for php-psr-http-message
#
# Copyright (c) 2014-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     php-fig
%global github_name      http-message
%global github_version   0.10.1
%global github_commit    9723465b3e7c8ecb0436f066bfb8a13e1bac1789

%global composer_vendor  psr
%global composer_project http-message

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:      php-%{composer_vendor}-%{composer_project}
Version:   %{github_version}
Release:   1%{?github_release}%{?dist}
Summary:   Common interface for HTTP messages (PSR-7)

Group:     Development/Libraries
License:   MIT
URL:       https://github.com/%{github_owner}/%{github_name}
Source0:   %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

# phpcompatinfo (computed from version 0.10.1)
Requires:  php(language) >= 5.3.0

# Composer
Provides:  php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
This package holds all interfaces/classes/traits related to PSR-7.

Note that this is not a HTTP message implementation of its own. It is merely an
interface that describes a HTTP message. See the specification for more details.


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}/Psr/Http/Message
cp -rp src/* %{buildroot}%{phpdir}/Psr/Http/Message/


%check
# No tests provided by upstream


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%doc composer.json
%dir %{phpdir}/Psr
%dir %{phpdir}/Psr/Http
     %{phpdir}/Psr/Http/Message


%changelog
* Mon Apr 13 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.10.1-1
- Updated to 0.10.1 (BZ #1187918)

* Sun Apr 12 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.9.2-1
- Updated to 0.9.2 (BZ #1187918)

* Thu Jan 29 2015 Remi Collet <remi@fedoraproject.org> - 0.8.0-1
- Updated to 0.8.0

* Tue Jan 27 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.6.0-1
- Updated to 0.6.0 (BZ #1183600)

* Thu Nov 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.5.1-1
- Updated to 0.5.1 (BZ #1163322)

* Thu Nov  6 2014 Remi Collet <remi@fedoraproject.org> - 0.4.0-1
- backport for remi repository

* Thu Oct 30 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.4.0-1
- Initial package
