Name:           gnome-extension-group
Version:        1.0.0
Release:        2%{?dist}
Summary:        Independently installable GNOME touch extensions
License:        GPL-2.0-only AND GPL-3.0-only AND GPL-3.0-or-later
URL:            https://github.com/MCC45TR/gnome-extension-group
Source0:        convergence-shell.zip
Source1:        touchup.zip
Source2:        touchshell.zip
Source3:        README.packaging.md

BuildArch:      noarch
BuildRequires:  glib2-devel
BuildRequires:  jq
BuildRequires:  nodejs
BuildRequires:  unzip

%description
This source package is a catalog for GNOME touch extensions. The extension
binary RPMs are intentionally independent: install only the ones you want.

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
License:        GPL-2.0-only
Requires:       gnome-shell >= 49
Requires:       gnome-extensions-app

%description -n gnome-shell-extension-touchshell
Touch gestures, fullscreen behavior, text actions, tiling gestures, and other
tablet-oriented GNOME Shell helpers.

%prep
%setup -q -c -T
mkdir convergence touchup touchshell
unzip -q %{SOURCE0} -d convergence
unzip -q %{SOURCE1} -d touchup
unzip -q %{SOURCE2} -d touchshell

%build
for extension in convergence touchup touchshell; do
    glib-compile-schemas --strict "$extension/schemas"
done

%install
install -d %{buildroot}%{_datadir}/gnome-shell/extensions
cp -a convergence %{buildroot}%{_datadir}/gnome-shell/extensions/convergence@daniel-blandford.github.io
cp -a touchup %{buildroot}%{_datadir}/gnome-shell/extensions/touchup@mityax
cp -a touchshell %{buildroot}%{_datadir}/gnome-shell/extensions/touchshell@touchshell.com
install -Dpm0644 %{SOURCE3} \
    %{buildroot}%{_docdir}/%{name}/README.md

%check
for pair in \
    'convergence:convergence@daniel-blandford.github.io' \
    'touchup:touchup@mityax' \
    'touchshell:touchshell@touchshell.com'; do
    extension=${pair%%:*}
    uuid=${pair#*:}
    test "$(jq -r .uuid "$extension/metadata.json")" = "$uuid"
    jq -e '."shell-version" | index("51")' "$extension/metadata.json" >/dev/null
    test -s "$extension/extension.js"
    test -s "$extension/schemas/gschemas.compiled"
    find "$extension" -type f -name '*.js' -print0 | xargs -0 -n1 node --check
done

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

%changelog
* Wed Sep 02 2026 mcc45tr <mcc45tr@gmail.com> - 1.0.0-2
- Accept GNOME 51 prereleases used by current Fedora Rawhide

* Wed Sep 02 2026 mcc45tr <mcc45tr@gmail.com> - 1.0.0-1
- Initial unified source package with three independent GNOME extensions
- Port the packaged sources to GNOME Shell 51 APIs
