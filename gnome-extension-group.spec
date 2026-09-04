Name:           gnome-extension-group
Version:        1.0.0
Release:        9%{?dist}
Summary:        Independently installable GNOME touch extensions
License:        GPL-2.0-or-later AND GPL-3.0-or-later
URL:            https://github.com/MCC45TR/gnome-extension-group
Source0:        convergence-shell.zip
Source1:        touchup.zip
Source2:        touchshell.zip
Source3:        nabu-tablet-controls.zip
Source4:        README.packaging.md

BuildArch:      noarch
BuildRequires:  glib2-devel
BuildRequires:  gettext
BuildRequires:  jq
BuildRequires:  nodejs
BuildRequires:  unzip

%description
This source package is a catalog for GNOME touch extensions. The extension
binary RPMs are intentionally independent: install only the ones you want.

%package -n gnome-shell-extension-nabu-tablet-controls
Summary:        Native Xiaomi Pad 5 hardware controls for GNOME Shell
License:        GPL-3.0-or-later
Requires:       gnome-shell >= 51~alpha
Requires:       gnome-extensions-app
Requires:       nabu-core-meta >= 3.0.0-35
Obsoletes:      nabu-flashlight-integration-gnome < 1.0.0-16
Provides:       nabu-flashlight-integration-gnome = 1.0.0-16

%description -n gnome-shell-extension-nabu-tablet-controls
Native GNOME Quick Settings controls for Xiaomi Pad 5 flashlight, ambient
brightness, USB roles, accessories and grip-aware sleep. Every control can be
configured from the stock GNOME Extensions preferences application.

%package -n gnome-shell-extension-convergence
Summary:        Convergence Shell for GNOME 51
License:        GPL-3.0-or-later
Requires:       gnome-shell >= 51~alpha
Requires:       gnome-extensions-app

%description -n gnome-shell-extension-convergence
A touch-first convergent shell layer with a mobile app drawer, home screen,
gesture navigation, notification panel, and device-aware helpers.

%package -n gnome-shell-extension-touchup
Summary:        TouchUp tablet interaction enhancements for GNOME Shell
License:        GPL-3.0-or-later
Requires:       gnome-shell >= 49
Requires:       gnome-extensions-app

%description -n gnome-shell-extension-touchup
Touch navigation, notification, on-screen keyboard, rotation, and overview
enhancements. Features can be enabled independently in its preferences.

%package -n gnome-shell-extension-touchshell
Summary:        Touchshell touchscreen helpers for GNOME Shell
License:        GPL-2.0-or-later
Requires:       gnome-shell >= 49
Requires:       gnome-extensions-app

%description -n gnome-shell-extension-touchshell
Touch gestures, fullscreen behavior, text actions, tiling gestures, and other
tablet-oriented GNOME Shell helpers.

%prep
%setup -q -c -T
mkdir convergence touchup touchshell nabu
unzip -q %{SOURCE0} -d convergence
unzip -q %{SOURCE1} -d touchup
unzip -q %{SOURCE2} -d touchshell
unzip -q %{SOURCE3} -d nabu

%build
for extension in convergence touchup touchshell nabu; do
    glib-compile-schemas --strict "$extension/schemas"
done
for po in nabu/translations/*.po; do
    lang="$(basename "$po" .po)"
    mkdir -p "nabu/locale/$lang/LC_MESSAGES"
    msgfmt --check --check-format -o \
        "nabu/locale/$lang/LC_MESSAGES/nabu_tablet_control.mo" "$po"
done

%install
install -d %{buildroot}%{_datadir}/gnome-shell/extensions
cp -a convergence %{buildroot}%{_datadir}/gnome-shell/extensions/convergence@daniel-blandford.github.io
cp -a touchup %{buildroot}%{_datadir}/gnome-shell/extensions/touchup@mityax
cp -a touchshell %{buildroot}%{_datadir}/gnome-shell/extensions/touchshell@touchshell.com
install -d %{buildroot}%{_datadir}/gnome-shell/extensions/nabulinuxproject@mcc45tr
install -Dm0644 nabu/extension.js nabu/metadata.json nabu/prefs.js \
    %{buildroot}%{_datadir}/gnome-shell/extensions/nabulinuxproject@mcc45tr/
cp -a nabu/schemas nabu/locale \
    %{buildroot}%{_datadir}/gnome-shell/extensions/nabulinuxproject@mcc45tr/
install -Dm0755 nabu/integration/nabu-gnome-extension-enable \
    %{buildroot}%{_libexecdir}/nabu-gnome-extension-enable
install -Dm0644 nabu/integration/nabu-gnome-extension-enable.service \
    %{buildroot}%{_userunitdir}/nabu-gnome-extension-enable.service
install -d %{buildroot}%{_userunitdir}/graphical-session.target.wants
ln -s ../nabu-gnome-extension-enable.service \
    %{buildroot}%{_userunitdir}/graphical-session.target.wants/nabu-gnome-extension-enable.service
install -Dpm0644 %{SOURCE4} \
    %{buildroot}%{_docdir}/%{name}/README.md

%check
for pair in \
    'convergence:convergence@daniel-blandford.github.io' \
    'touchup:touchup@mityax' \
    'touchshell:touchshell@touchshell.com' \
    'nabu:nabulinuxproject@mcc45tr'; do
    extension=${pair%%:*}
    uuid=${pair#*:}
    test "$(jq -r .uuid "$extension/metadata.json")" = "$uuid"
    jq -e '."shell-version" | index("51")' "$extension/metadata.json" >/dev/null
    test -s "$extension/extension.js"
    test -s "$extension/schemas/gschemas.compiled"
    find "$extension" -type f -name '*.js' -print0 | xargs -0 -n1 node --check
done
sh -n nabu/integration/nabu-gnome-extension-enable
test "$(find nabu/translations -name '*.po' | wc -l)" = 27

%files
%doc %{_docdir}/%{name}/README.md

%files -n gnome-shell-extension-convergence
%license %{_datadir}/gnome-shell/extensions/convergence@daniel-blandford.github.io/LICENSE
%{_datadir}/gnome-shell/extensions/convergence@daniel-blandford.github.io

%files -n gnome-shell-extension-touchup
%license %{_datadir}/gnome-shell/extensions/touchup@mityax/LICENSE.md
%{_datadir}/gnome-shell/extensions/touchup@mityax

%files -n gnome-shell-extension-touchshell
%license %{_datadir}/gnome-shell/extensions/touchshell@touchshell.com/LICENSE
%{_datadir}/gnome-shell/extensions/touchshell@touchshell.com

%files -n gnome-shell-extension-nabu-tablet-controls
%license nabu/LICENSE
%{_datadir}/gnome-shell/extensions/nabulinuxproject@mcc45tr
%{_libexecdir}/nabu-gnome-extension-enable
%{_userunitdir}/nabu-gnome-extension-enable.service
%{_userunitdir}/graphical-session.target.wants/nabu-gnome-extension-enable.service

%changelog
* Fri Sep 04 2026 mcc45tr <mcc45tr@gmail.com> - 1.0.0-9
- Rebuild synchronized extension payloads

* Thu Sep 03 2026 mcc45tr <mcc45tr@gmail.com> - 1.0.0-8
- Add Nabu Tablet Controls as a fourth independently installable extension.
- Migrate its extension identity to nabulinuxproject@mcc45tr.

* Thu Sep 03 2026 mcc45tr <mcc45tr@gmail.com> - 1.0.0-7
- Align package SPDX expressions with the upstream license declarations

* Thu Sep 03 2026 mcc45tr <mcc45tr@gmail.com> - 1.0.0-6
- Document and serialize the fail-closed autobuild pipeline
- Include the final synchronized GNOME 51 TouchUp payload

* Thu Sep 03 2026 mcc45tr <mcc45tr@gmail.com> - 1.0.0-3
- Rebuild synchronized fork payloads and version automated source updates

* Wed Sep 02 2026 mcc45tr <mcc45tr@gmail.com> - 1.0.0-2
- Accept GNOME 51 prereleases used by current Fedora Rawhide

* Wed Sep 02 2026 mcc45tr <mcc45tr@gmail.com> - 1.0.0-1
- Initial unified source package with three independent GNOME extensions
- Port the packaged sources to GNOME Shell 51 APIs
