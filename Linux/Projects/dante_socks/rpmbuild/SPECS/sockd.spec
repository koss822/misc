Name:           sockd
Version:        1.4.2
Release:        0
Summary:        Dante Socks Proxy with basic config and SystemD daemon
BuildArch:	x86_64

Group:          TecAdmin
BuildArch:      noarch
License:        GPL
URL:            https://www.enigma14.eu/martin/blog/2018/02/01/dante-socks-proxy-how-to-install-and-manage-on-rhel-or-other-distros/
Source0:        sockd-1.4.2.tar.gz

%description
Dante Socks Proxy with basic config and SystemD daemon

%prep
%setup -q
%build
%install
install -m 0755 -d $RPM_BUILD_ROOT/usr/local/bin
install -m 0755 -d $RPM_BUILD_ROOT/usr/lib/systemd/system
install -m 0755 -d $RPM_BUILD_ROOT/etc
install -m 0755 sockd $RPM_BUILD_ROOT/usr/local/bin/sockd
install -m 0644 sockd.service $RPM_BUILD_ROOT/usr/lib/systemd/system/sockd.service
install -m 0644 sockd.conf $RPM_BUILD_ROOT/etc/sockd.conf

%files
/usr/local/bin/sockd
/usr/lib/systemd/system/sockd.service
/etc/sockd.conf

%changelog
* Thu Aug 01 2019 Martin Konicek  1.4.2
  - Initial rpm release
