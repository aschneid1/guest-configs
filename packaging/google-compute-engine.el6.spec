# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

Name: google-compute-engine
Epoch: 1
Version: %{_version}
Release: g1.el6
Summary: Google Compute Engine guest environment.
License: ASL 2.0
Url: https://github.com/GoogleCloudPlatform/compute-image-packages
Source0: %{name}_%{version}.orig.tar.gz
Requires: curl
Requires: google-compute-engine-oslogin
Requires: google-guest-agent
Requires: rsyslog
# Old packages.
Obsoletes: google-compute-engine-init
Obsoletes: google-config
Obsoletes: google-startup-scripts

BuildArch: noarch

# Allow other files in the source that don't end up in the package.
%define _unpackaged_files_terminate_build 0

%description
This package contains scripts, configuration, and init files for features
specific to the Google Compute Engine cloud environment.

%prep
%autosetup

%install
cp -a src/{etc,usr,sbin} %{buildroot}
install -d %{buildroot}/lib/
cp -a src/lib/udev %{buildroot}/lib
mkdir -p %{buildroot}/etc/dhcp
ln -sf /usr/bin/google_set_hostname %{buildroot}/etc/dhcp/dhclient-exit-hooks

%files
%defattr(0644,root,root,0755)
%attr(0755,-,-) %{_bindir}/*
%attr(0755,-,-) /sbin/google-dhclient-script
/lib/udev/rules.d/*
/etc/dhcp/dhclient-exit-hooks
%config /etc/modprobe.d/*
%config /etc/rsyslog.d/*
%config /etc/sysctl.d/*

%pre
if [ $1 -gt 1 ] ; then
  # This is an upgrade. Stop services previously owned by this package, if any.
  for svc in google-ip-forwarding-daemon google-network-setup \
    google-network-daemon google-accounts-daemon google-clock-skew-daemon; do
      if initctl status $svc >/dev/null 2>&1; then
        initctl stop ${svc} || :
      fi
  done
fi
