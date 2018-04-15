#%{?scl:%scl_package rocksdb}
%global pkg_name rocksdb
%global php_base php72u
%global ini_name  40-%{pkg_name}.ini

Summary: PHP 7 RocksDB bindings
Name: %{php_base}-%{pkg_name}
Version: 0.7
Release: %{?release}%{!?release:1}%{?dist}
License: BSD
Group: Development/Libraries
Source0: http://stash.iloffice.myhrtg.net:7990/plugins/servlet/archive/projects/ROC/repos/php7-rocksdb?at=refs%2Ftags%2Fv%{version}&format=tar.gz#/%{pkg_name}-%{version}.tar.gz
Source1: %{pkg_name}.ini
BuildRequires: %{php_base}-devel,  rocksdb-devel, %{?scl_prefix}gcc >= 4.8.2, %{?scl_prefix}binutils, %{?scl_prefix}gcc-c++ >= 4.8.2
%if 0%{?fedora} < 24
Requires(post): pear1u
Requires(postun): pear1u
%endif
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$

%description
PHP7 RocksDB bindings

%prep
%setup -qc

%build
%{?scl:scl enable %{scl} - << \EOF}
phpize
%{configure} 
%{__make}
%{?scl:EOF}

%install
%{__make} install INSTALL_ROOT=%{buildroot}
# Install config file
%if 0%{?scl:1}
install -Dpm 0644 %{SOURCE1} %{buildroot}/%{_root_sysconfdir}/php.d/%{ini_name}
%else
install -Dpm 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/php.d/%{ini_name}
%endif

rm -rf %{buildroot}%{php_incldir}/ext/%{pkg_name}/

%files
/%{_usr}/%{_lib}/php/modules/%{pkg_name}.so
%config(noreplace) %verify(not md5 mtime size) %{php_inidir}/%{ini_name}

%changelog
