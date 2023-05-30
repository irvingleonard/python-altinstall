
Name:           python310-altinstall
Version:        3.10.11
Release:        1%{?dist}
Summary:        Interpreter of the Python programming language

License:        Python
URL:            https://www.python.org/
Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tgz

BuildRequires:	autoconf-archive
BuildRequires:	automake
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	gdbm-devel
BuildRequires:	gzip
BuildRequires:	libbz2-devel
BuildRequires:	libffi-devel
BuildRequires:	libopenssl-devel
BuildRequires:	libuuid-devel
BuildRequires:	make
#BuildRequires:	python3
BuildRequires:	readline-devel
BuildRequires:	sqlite3-devel
BuildRequires:	tk-devel
BuildRequires:	ncurses-devel
BuildRequires:	uuid-devel
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
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
autoreconf -ivf


%build
env CXX=`which g++` %{_builddir}/Python-%{version}/configure --enable-optimizations --enable-loadable-sqlite-extensions


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
/usr/local/include/python3.10
/usr/local/lib/pkgconfig
/usr/local/lib/python3.10
/usr/local/lib/libpython3.10.a
%doc /usr/local/share/man

%changelog
* Tue May 30 2023 Irving Leonard <irvingleonard@github.com> 3.10.11-1
- Upgraded to version 3.10.11
* Wed Oct 13 2021 Irving Leonard <irvingleonard@github.com> 3.10.0-1
- Initial RPM release
