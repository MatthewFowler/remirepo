#
# RPM spec file for php-guzzlehttp-streams
#
# Copyright (c) 2014-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     guzzle
%global github_name      streams
%global github_version   3.0.0
%global github_commit    47aaa48e27dae43d39fc1cea0ccf0d84ac1a2ba5

%global composer_vendor  guzzlehttp
%global composer_project streams

# "php": ">=5.4.0"
%global php_min_ver      5.4.0

# Build using "--without tests" to disable tests
%global with_tests       %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:     %global phpdir     %{_datadir}/php}
%{!?__phpunit:  %global __phpunit  %{_bindir}/phpunit}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Provides a simple abstraction over streams of data

Group:         Development/Libraries
License:       MIT
URL:           http://docs.guzzlephp.org/en/guzzle4/streams.html
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# Test suite start failing with upcoming 5.5.21RC1 / 5.6.5RC1
# https://github.com/guzzle/streams/issues/29
# https://github.com/guzzle/streams/commit/ad4c07ea55d02789a65ae75f6e4a9ee2cb9dab3f.patch
Patch0:        %{name}-ad4c07ea55d02789a65ae75f6e4a9ee2cb9dab3f.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
# composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: %{__phpunit}
# phpcompatinfo (computed from version 3.0.0)
BuildRequires: php-hash
BuildRequires: php-spl
BuildRequires: php-zlib
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 3.0.0)
Requires:      php-hash
Requires:      php-spl

Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.


%prep
%setup -qn %{github_name}-%{github_commit}

%patch0 -p1 -b .ad4c07ea55d02789a65ae75f6e4a9ee2cb9dab3f


%build
# Empty build section, nothing required


%install
mkdir -p  %{buildroot}%{phpdir}/GuzzleHttp/Stream
cp -pr src/* %{buildroot}%{phpdir}/GuzzleHttp/Stream/


%check
%if %{with_tests}
# Create autoloader
mkdir vendor
cat > vendor/autoload.php <<'AUTOLOAD'
<?php

spl_autoload_register(function ($class) {
    $src = str_replace(array('\\', '_'), '/', $class).'.php';
    @include_once $src;
});
AUTOLOAD

%{__phpunit} --include-path="%{buildroot}%{phpdir}"
%else
: Tests skipped
%endif


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.rst
%doc composer.json
%dir %{phpdir}/GuzzleHttp
     %{phpdir}/GuzzleHttp/Stream


%changelog
* Sun Feb 08 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 3.0.0-1
- Updated to 3.0.0 (BZ #1131103)

* Thu Jan 22 2015 Remi Collet <remi@fedoraproject.org> - 1.5.1-3
- add upstream patch for test suite against latest PHP
  see https://github.com/guzzle/streams/issues/29, thank Koschei

* Tue Aug 26 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.5.1-2
- Updated URL and description per upstream
- Fix test suite when previous version installed

* Sun Aug 17 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.5.1-1
- Updated to 1.5.1 (BZ #1128102)

* Fri Jun 06 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.4.0-1
- Updated to 1.4.0 (BZ #1124227)
- Added option to build without tests ("--without tests")
- Added %%license usage

* Fri Jun 06 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.0-2
- Updated URL
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide

* Fri May 23 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.0-1
- Initial package
