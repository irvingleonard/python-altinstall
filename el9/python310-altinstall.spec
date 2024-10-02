Name:           python310-altinstall
Version:        3.10.15
Release:        1%{?dist}
Summary:        Interpreter of the Python programming language

License:        Python
URL:            https://www.python.org/
Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tgz

BuildRequires:  bzip2-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gdbm-devel
BuildRequires:  libffi-devel
BuildRequires:  libnsl2-devel
BuildRequires:  libuuid-devel
BuildRequires:  openssl-devel
BuildRequires:  readline-devel
BuildRequires:  sqlite-devel
BuildRequires:  tk-devel

## Fixes
# disable shebang mangling of python scripts
%undefine __brp_mangle_shebangs
# disable the creation of debug RPMs
%define debug_package %{nil}

%description
Python is an accessible, high-level, dynamically typed, interpreted programming
language, designed with an emphasis on code readability.
It includes an extensive standard library, and has a vast ecosystem of
third-party libraries.

This uses the upstream method using altinstall which would install in /usr/local

%prep
%setup -q -n Python-%{version}

%build
env CXX=/usr/bin/c++ %{_builddir}/Python-%{version}/configure --enable-optimizations --with-lto --enable-loadable-sqlite-extensions
#make buildbottest

%install
rm -rf %{buildroot}
make altinstall DESTDIR=%{buildroot}
# Compress man page
%{__gzip} --name --best %{buildroot}/usr/local/share/man/man1/python3.10.1

%files
/usr/local/bin/2to3-3.10
/usr/local/bin/idle3.10
/usr/local/bin/pip3.10
/usr/local/bin/pydoc3.10
/usr/local/bin/python3.10
/usr/local/bin/python3.10-config
/usr/local/lib/libpython3.10.a
/usr/local/lib/pkgconfig/python-3.10.pc
/usr/local/lib/pkgconfig/python-3.10-embed.pc
/usr/local/include/python3.10
/usr/local/lib/python3.10
%doc /usr/local/share/man/man1/python3.10.1.gz

%changelog
* Wed Oct 2 2024 Irving Leonard <irvingleonard@github.com> 3.10.15-1
- Upgraded to version 3.10.15
* Wed May 31 2023 Irving Leonard <irvingleonard@github.com> 3.10.11-2
- Fixed the OpenSSL requirement
* Tue May 30 2023 Irving Leonard <irvingleonard@github.com> 3.10.11-1
- Upgraded to version 3.10.11
* Thu Nov 4 2021 Irving Leonard <irvingleonard@github.com> 3.10.0-1
- Upgraded to version 3.10.0
