# spec file for php-phpunit-environment
#
# Copyright (c) 2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    0d9bf79554d2a999da194a60416c15cf461eb67d
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   environment
%global php_home     %{_datadir}/php/SebastianBergmann
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-phpunit-environment
Version:        1.2.0
Release:        1%{?dist}
Summary:        Handle HHVM/PHP environments

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

Patch0:         %{gh_project}-upstream.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
%endif

# from composer.json
#        "php": ">=5.3.3"
Requires:       php(language) >= 5.3.3

Provides:       php-composer(sebastian/environment) = %{version}


%description
This component provides functionality that helps writing PHP code that
has runtime-specific (PHP / HHVM) execution paths.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1


%build
# Generate the Autoloader
phpab --output src/autoload.php src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/Environment


%if %{with_tests}
%check
if [ -d /usr/share/php/PHPUnit ]
then
  # Hack PHPUnit 4 autoloader to not use system library
  mkdir PHPUnit
  sed -e 's:SebastianBergmann/Environment:src:' \
    -e 's:dirname(__FILE__):"/usr/share/php/PHPUnit":' \
    /usr/share/php/PHPUnit/Autoload.php \
    >PHPUnit/Autoload.php
fi

# Ignore this test which requires a tty
# https://github.com/sebastianbergmann/environment/issues/5
rm -f tests/ConsoleTest.php

phpunit \
  --bootstrap src/autoload.php \
  -d date.timezone=UTC
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README.md composer.json
%dir %{php_home}
%{php_home}/Environment


%changelog
* Sat Oct 25 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0

* Wed Oct  8 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0

* Sun Oct  5 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- enable test suite

* Wed Jun 25 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-4
- composer dependencies

* Wed Apr 23 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- add generated autoload.php

* Tue Apr  1 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package