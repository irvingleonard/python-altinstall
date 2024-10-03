%define dist .sles156
Name:           python39-altinstall
Version:        3.9.20
Release:        1%{?dist}
Summary:        Interpreter of the Python programming language

License:        Python
URL:            https://www.python.org/
Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tgz

BuildRequires:	autoconf-archive
BuildRequires:	automake
BuildRequires:	gcc-c++
BuildRequires:	gdbm-devel
BuildRequires:	libbz2-devel
BuildRequires:	libffi-devel
BuildRequires:	libnsl-devel
BuildRequires:	libopenssl-devel
BuildRequires:	libuuid-devel
BuildRequires:	readline-devel
BuildRequires:	sqlite3-devel
BuildRequires:	tk-devel
BuildRequires:	xz-devel

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
autoreconf -ivf

%build
env CXX=`which g++` %{_builddir}/Python-%{version}/configure --enable-optimizations --with-lto --enable-loadable-sqlite-extensions
make buildbottest

%install
rm -rf %{buildroot}
make altinstall DESTDIR=%{buildroot}
# Compress man page
%{__gzip} --name --best %{buildroot}/usr/local/share/man/man1/python3.9.1
 
%files
/usr/local/bin/2to3-3.9
/usr/local/bin/idle3.9
/usr/local/bin/pip3.9
/usr/local/bin/pydoc3.9
/usr/local/bin/python3.9
/usr/local/bin/python3.9-config
/usr/local/include/python3.9
/usr/local/lib/libpython3.9.a
/usr/local/lib/pkgconfig/python-3.9-embed.pc
/usr/local/lib/pkgconfig/python-3.9.pc
/usr/local/lib/python3.9
%doc /usr/local/share/man/man1/python3.9.1.gz

%changelog
* Wed Oct 2 2024 Irving Leonard <irvingleonard@github.com> 3.9.20-1
- Initial RPM release
