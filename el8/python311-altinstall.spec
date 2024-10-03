Name:           python311-altinstall
Version:        3.11.10
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
make buildbottest

%install
rm -rf %{buildroot}
make altinstall DESTDIR=%{buildroot}
# Compress man page
%{__gzip} --name --best %{buildroot}/usr/local/share/man/man1/python3.11.1

%files
/usr/local/bin/2to3-3.11
/usr/local/bin/idle3.11
/usr/local/bin/pip3.11
/usr/local/bin/pydoc3.11
/usr/local/bin/python3.11
/usr/local/bin/python3.11-config
/usr/local/lib/libpython3.11.a
/usr/local/lib/pkgconfig/python-3.11.pc
/usr/local/lib/pkgconfig/python-3.11-embed.pc
/usr/local/include/python3.11
/usr/local/lib/python3.11
%doc /usr/local/share/man/man1/python3.11.1.gz

%changelog
* Thu Oct 3 2024 Irving Leonard <irvingleonard@github.com> 3.11.10-1
- Initial RPM release
