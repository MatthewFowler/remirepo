# spec file for php-pecl-yar
#
# Copyright (c) 2013-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package        php-pecl-yar}
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global with_zts   0%{?__ztsphp:1}
%global pecl_name  yar
%if "%{php_version}" < "5.6"
# After json, msgpack
%global ini_name   %{pecl_name}.ini
%else
# After 40-json, 40-msgpack
%global ini_name   50-%{pecl_name}.ini
%endif

Summary:        Light, concurrent RPC framework
Name:           %{?scl_prefix}php-pecl-%{pecl_name}
Version:        1.2.4
Release:        1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}.1
License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  curl-devel
BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-pecl-msgpack-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%if "%{php_version}" < "5.4"
# php 5.3.3 in EL-6 don't use arched virtual provides
# so only requires real packages instead
Requires:       %{?scl_prefix}php-common%{?_isa}
%else
Requires:       %{?scl_prefix}php-curl%{?_isa}
Requires:       %{?scl_prefix}php-json%{?_isa}
%endif
Requires:       %{?scl_prefix}php-pecl(msgpack)%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php53u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php54-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php54w-pecl-%{pecl_name} <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Yar (Yet another RPC framework) is a light, concurrent RPC framework,
supports multi package protocols (json, msgpack).

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection}.


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

# Don't install/register tests
sed -e 's/role="test"/role="src"/' -i package2.xml

cd NTS

# Add shebang
sed -e 's:<?php:#!%{_bindir}/php\n<?php:' \
     -i tools/yar_debug.php

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_YAR_VERSION/{s/.* "//;s/".*$//;p}' php_yar.h)
if test "x${extver}" != "x%{version}%{?prever:-%{prever}}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever:-%{prever}}.
   exit 1
fi
cd ..

sed -e 's:tools/yar_debug.inc:yar_debug.inc:' \
    -e 's:tools/yar_debug.php:yar_debug:' \
    -i package2.xml

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif

# Create configuration file
cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; Configuration
;yar.allow_persistent=0
;yar.connect_timeout=1000
;yar.content_type=application/octet-stream
;yar.debug=Off
;yar.expose_info=On
;yar.packager=msgpack
;yar.timeout=5000
;yar.transport=curl
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --enable-msgpack \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --enable-msgpack \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS \
     install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package2.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS \
     install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Tools
install -Dpm 644 NTS/tools/yar_debug.inc %{buildroot}%{pear_phpdir}/yar_debug.inc
install -Dpm 755 NTS/tools/yar_debug.php %{buildroot}%{_bindir}/yar_debug

# Documentation
cd NTS
for i in $(grep 'role="doc"' ../package2.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
# Upstream test suite requires a web server
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=json.so \
    --define extension=msgpack.so \
    --define extension=NTS/modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=json.so \
    --define extension=msgpack.so \
    --define extension=ZTS/modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so
%{_bindir}/yar_debug
%{pear_phpdir}/yar_debug.inc

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.2.4-1.1
- Fedora 21 SCL mass rebuild

* Sat Oct 25 2014 Remi Collet <remi@fedoraproject.org> - 1.2.4-1
- Update to 1.2.4
- dont install test suite

* Tue Aug 26 2014 Remi Collet <rcollet@redhat.com> - 1.2.3-3
- improve SCL build

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 1.2.3-2
- add numerical prefix to extension configuration file (php 5.6)

* Thu Jan 02 2014 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3 (stable)
- provides yar_debug command
- fix default options in comments
- adapt for SCL

* Tue Dec 31 2013 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2 (stable)

* Tue Nov 19 2013 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1 (stable)
- install doc in pecl doc_dir
- install tests in pecl test_dir

* Wed Jul 17 2013 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- initial package
