# spec file for php-true-punycode
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    59dca474914324763397be2ea3d6ad3bc48f4688
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     true
%global gh_project   php-punycode
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

# Notice: single file / class, so no need to provide an autoloader for now

Name:           php-true-punycode
Version:        1.0.1
Release:        1%{?dist}
Summary:        A Bootstring encoding of Unicode for IDNA

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-mbstring
BuildRequires:  %{_bindir}/phpunit

# From composer.json
#      "php": ">=5.3.0"
#      "ext-mbstring": "*"
Requires:       php(language) >= 5.3.3
Requires:       php-mbstring

Provides:       php-composer(true/punycode) = %{version}


%description
A Bootstring encoding of Unicode for Internationalized Domain Names
in Applications (IDNA).


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Nothing


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{_datadir}/php/True
cp -pr src/* %{buildroot}%{_datadir}/php/True


%check
%if %{with_tests}
: Run test suite
phpunit --bootstrap src/Punycode.php
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{_datadir}/php/True/


%changelog
* Wed Jan  7 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- initial package