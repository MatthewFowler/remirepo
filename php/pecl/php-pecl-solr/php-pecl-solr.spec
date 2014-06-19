# spec file for php-pecl-solr
#
# Copyright (c) 2011-2014 Remi Collet
# Copyright (c) 2010 Johan Cwiklinski
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package         php-pecl-solr}
%{!?php_inidir:  %global php_inidir   %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl       %{_bindir}/pecl}
%{!?__php:       %global __php        %{_bindir}/php}

%global pecl_name solr
%global with_zts  0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
# After curl, json
%global ini_name  %{pecl_name}.ini
%else
# After 20-curl, 40-json
%global ini_name  50-%{pecl_name}.ini
%endif

Summary:        Object oriented API to Apache Solr
Summary(fr):    API orientée objet pour Apache Solr
Name:           %{?scl_prefix}php-pecl-solr
Version:        1.1.0
Release:        1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/solr

Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# http://git.php.net/?p=pecl/search_engine/solr.git;a=blob_plain;f=tests/bootstrap.inc;hb=333d932e89f7032260be8069dbf3c26a2fd34a9c
Source1:        bootstrap.inc
# http://git.php.net/?p=pecl/search_engine/solr.git;a=blob_plain;f=tests/test.config.inc;hb=333d932e89f7032260be8069dbf3c26a2fd34a9c
Source2:        test.config.inc
# http://git.php.net/?p=pecl/search_engine/solr.git;a=blob_plain;f=tests/skip.if.server_not_configured.inc;hb=333d932e89f7032260be8069dbf3c26a2fd34a9c
Source3:        skip.if.server_not_configured.inc
# http://git.php.net/?p=pecl/search_engine/solr.git;a=blob_plain;f=tests/files/response_xml.1.xml;hb=333d932e89f7032260be8069dbf3c26a2fd34a9c
Source4:        response_xml.1.xml

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-curl
BuildRequires:  %{?scl_prefix}php-json
BuildRequires:  curl-devel
BuildRequires:  libxml2-devel

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

Provides:       %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}

# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
%if "%{php_version}" > "5.4"
Obsoletes:     php54-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name}
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Feature-rich library that allows PHP developers to communicate easily and
efficiently with Apache Solr server instances using an object-oriented API.

It effectively simplifies the process of interacting with Apache Solr using
PHP5 and it already comes with built-in readiness for the latest features
added in Solr 3.1. The extension has features such as built-in,
serializable query string builder objects which effectively simplifies the
manipulation of name-value pair request parameters across repeated requests.
The response from the Solr server is also automatically parsed into native php
objects whose properties can be accessed as array keys or object properties
without any additional configuration on the client-side. Its advanced HTTP
client reuses the same connection across multiple requests and provides
built-in support for connecting to Solr servers secured behind HTTP
Authentication or HTTP proxy servers. It is also able to connect to
SSL-enabled containers.

More info on PHP-Solr can be found at:
http://www.php.net/manual/en/book.solr.php

Warning: PECL Solr 1 is not compatible with Solr Server >= 4.0.
PECL Solr 2 is available in php-pecl-solr2 package.


%description -l fr
Bibliothèque riche en fonctionnalités qui permet aux développeurs PHP
de communiquer facilement et efficacement avec des instances du serveur
Apache Solr en utilisant une API orientée objet.

Cela simplifie réellement le processus d'interaction avec Apache Solr en
utilisant PHP5 et fournit dores et déjà des facilités pour les dernières
fonctionnalités ajoutées dans Solr 3.1. L'extension possède des
fonctionnalités telles qu'un constructeur de requêtes embarqué et sérialisable
qui simplifie réellement la manipulation des couples de paramètres  nom-valeur
entre différentes requêtes. La réponse de Solr est également analysée
automatiquement en objets php natifs dont les propriétés sont accessibles
en tant que clés de tableaux ou en tant que propriétés d'objets sans la moindre
configuration supplémentaire sur le client. Son client HTTP avancé utilise 
la même connexion entre différentes requêtes et fournit un support embarqué
pour la connexion aux serveurs Solr protégés par authentification HTTP ou
par un serveur mandataire. Il est également possible de se connecter à des 
serveurs via SSL.

Plus d'informations sur PHP-Solr sur:
http://www.php.net/manual/fr/book.solr.php

Attention: PECL Solr 1 n'est pas compatible avec un serveur Solr >= 4.0.
PECL Solr 2 est disponible dans le paquet php-pecl-solr2.


%prep
%setup -c -q

mv %{pecl_name}-%{version}%{?prever} NTS
cd NTS

# Restore missing file in archive
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} tests/
mkdir tests/files
cp %{SOURCE4} tests/files/

# Check version
extver=$(sed -n '/#define PHP_SOLR_VERSION /{s/.* "//;s/".*$//;p}' php_solr_version.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

# Fix rights
chmod -x README.* \
         CREDITS \
         LICENSE \
         TODO \
         docs/documentation.php \
         *.c \
         *.h
cd ..

# Create configuration file
cat > %{ini_name} << 'EOF'
; Enable Solr extension module
extension=%{pecl_name}.so
EOF

%if %{with_zts}
cp -r NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}


# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Test & Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in LICENSE $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
DEP="-d extension=curl.so -d extension=json.so"
cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    $DEP \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

TEST_PHP_ARGS="-n $DEP -d extension=$PWD/modules/%{pecl_name}.so" \
   REPORT_EXIT_STATUS=1 \
   NO_INTERACTION=1 \
   TEST_PHP_EXECUTABLE=%{__php} \
   %{__php} \
   run-tests.php

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    $DEP \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

TEST_PHP_ARGS="-n $DEP -d extension=$PWD/modules/%{pecl_name}.so" \
   REPORT_EXIT_STATUS=1 \
   NO_INTERACTION=1 \
   TEST_PHP_EXECUTABLE=%{__ztsphp} \
   %{__ztsphp} \
   run-tests.php
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, -)
%doc %{pecl_docdir}/%{pecl_name}
%doc %{pecl_testdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Thu Jun 19 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0 (stable)

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-9
- add numerical prefix to extension configuration file (php 5.6)

* Tue Mar 25 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-8
- allow SCL build

* Sun Mar  9 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-7
- cleanups
- install doc in pecl_docdir
- install tests in pecl_testdir

* Sun Oct 21 2012 Remi Collet <remi@fedoraproject.org> - 1.0.2-4
- rebuild

* Tue Nov 29 2011 Remi Collet <remi@fedoraproject.org> - 1.0.2-2
- php 5.4 build

* Tue Nov 29 2011 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2

* Mon Nov 28 2011 Remi Collet <remi@fedoraproject.org> - 1.0.1-4.svn320130
- svn snapshot (test suite is now ok)

* Wed Nov 16 2011 Remi Collet <remi@fedoraproject.org> - 1.0.1-3
- build against php 5.4
- ignore test result because of https://bugs.php.net/60313

* Thu Oct 06 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.1-2
- ZTS extension
- spec cleanups

* Fri Jun 10 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.1-1
- Version 1.0.1 (stable) - API 1.0.1 (stable)
- run test suite after build

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 23 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.11-1
- update to latest release

* Thu May 13 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.10-2
- consitent use of pecl_name macro
- add %%check
- fixes some typos
- thanks Remi :)

* Thu May 13 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.10-1
- update to latest release

* Tue Apr 27 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.9-2
- Add missing Requires
- Remove conditionnal 'php_zend_api' 'pecl_install' no longer required
- %%define no longer must be used
- Thanks to Remi :)

* Mon Apr 26 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.9-1
- Initial packaging
