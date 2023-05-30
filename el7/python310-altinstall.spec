%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%define debug_package %{nil}
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Name:           python310-altinstall
Version:        3.10.11
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
BuildRequires:  libuuid-devel
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  python3
BuildRequires:  readline-devel
BuildRequires:  sqlite-devel
BuildRequires:  tk-devel
BuildRequires:  uuid-devel
BuildRequires:  xz-devel
Provides:       /usr/local/bin/python3.10
# Don't even bother with default python. It's required by this package, that's why is listed here.
Provides:       /usr/local/bin/python

%description
Python is an accessible, high-level, dynamically typed, interpreted programming
language, designed with an emphasis on code readability.
It includes an extensive standard library, and has a vast ecosystem of
third-party libraries.

This uses the upstream method using altinstall which would install in /usr/local

%prep
%setup -q -n Python-%{version}


%build
env CXX=/usr/bin/c++ %{_builddir}/Python-%{version}/configure --enable-optimizations --enable-loadable-sqlite-extensions


%install
rm -rf %{buildroot}
make altinstall DESTDIR=%{buildroot}
# Remove the bytecode generated by the installer. The bytecode is unusable because of mtime not being set correctly.
find %{buildroot} -type f -name '*.pyc' -delete
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
* Tue May 30 2023 Irving Leonard <irvingleonard@github.com> 3.10.11-1
- Upgraded to version 3.10.11
* Thu Nov 4 2021 Irving Leonard <irvingleonard@github.com> 3.10.0-1
- Upgraded to version 3.10.0
