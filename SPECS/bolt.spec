Name:          bolt
Version:       0.9.1
Release:       1%{?dist}
Summary:       Thunderbolt device manager
License:       LGPLv2+
URL:           https://gitlab.freedesktop.org/bolt/bolt
Source0:       %{url}/-/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: asciidoc
BuildRequires: meson
BuildRequires: libudev-devel
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(libudev)
BuildRequires: polkit-devel
BuildRequires: systemd
%{?systemd_requires}

%description
bolt is a system daemon to manage Thunderbolt devices via a D-BUS
API. Thunderbolt 3 introduced different security modes that require
devices to be authorized before they can be used. The D-Bus API can be
used to list devices, enroll them (authorize and store them in the
local database) and forget them again (remove previously enrolled
devices). It also emits signals if new devices are connected (or
removed). During enrollment devices can be set to be automatically
authorized as soon as they are connected.  A command line tool, called
boltctl, can be used to control the daemon and perform all the above
mentioned tasks.

%prep
%autosetup -p1

%build
%meson -Ddb-name=boltd
%meson_build

%check
%meson_test

%install
%meson_install
install -m0755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/boltd

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license COPYING
%doc README.md CHANGELOG.md
%{_bindir}/boltctl
%{_libexecdir}/boltd
%{_unitdir}/%{name}.service
%{_udevrulesdir}/*-%{name}.rules
%{_datadir}/dbus-1/system.d/org.freedesktop.bolt.conf
%{_datadir}/dbus-1/interfaces/org.freedesktop.bolt.xml
%{_datadir}/polkit-1/actions/org.freedesktop.bolt.policy
%{_datadir}/polkit-1/rules.d/org.freedesktop.bolt.rules
%{_datadir}/dbus-1/system-services/org.freedesktop.bolt.service
%{_mandir}/man1/boltctl.1*
%{_mandir}/man8/boltd.8*
%ghost %dir %{_localstatedir}/lib/boltd

%changelog
* Wed Jan 13 2021 Christian Kellner <ckellner@redhat.com> - 0.9.1-1
- bolt 0.9 upstream release
- Update description with less emphasis on Thunderbolt version

* Mon Jun 15 2020 Christian Kellner <ckellner@redhat.com> - 0.9-1
- bolt 0.9 upstream release

* Fri Jun 14 2019 Christian Kellner <ckellner@redhat.com> - 0.8-2
- Rebuilt for fixed gating.yaml (remove missing tier1 gate)

* Thu Jun 13 2019 Christian Kellner <ckellner@redhat.com> - 0.8-1
- bolt 0.8 upstream release with pre-boot ACL and IOMMU support
  D-Bus Configuration moved from sysconfdir to datadir
  Resolves: #1629715

* Wed Jul 18 2018 Christian Kellner <ckellner@redhat.com> - 0.4-1
- bolt 0.4 upstream release
- Remove optional test dependencies

* Tue Apr 10 2018 Christian Kellner <ckellner@redhat.com> - 0.3-1
- bolt 0.3 upstream release
- Update BuildRequires to include gcc
- Use forge macros

* Tue Mar  6 2018 Christian Kellner <ckellner@redhat.com> - 0.2-1
- bolt 0.2 upstream release
- Update BuildRequires dependencies.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 17 2017 Christian Kellner <ckellner@redhat.com> - 0.1-2
- Set database path to /var/lib/boltd, create it during
  installation, which is needed for the service file to work.

* Thu Dec 14 2017 Christian Kellner <ckellner@redhat.com> - 0.1-1
- Initial upstream release
