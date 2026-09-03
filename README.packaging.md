# GNOME Extension Group

One Fedora source package produces a small catalog package and four fully
independent extension RPMs:

- `gnome-shell-extension-nabu-tablet-controls`
- `gnome-shell-extension-convergence`
- `gnome-shell-extension-touchup`
- `gnome-shell-extension-touchshell`

The packages do not depend on one another. Installing `gnome-extension-group`
only installs this catalog document; it deliberately does not select all three
extensions. Use DNF to install any desired extension package by name.

The extension files are installed system-wide. Enable each extension from the
GNOME Extensions application after logging into a compatible GNOME session.

The packaged downstream source forks are:

- https://github.com/MCC45TR/convergence-shell
- https://github.com/MCC45TR/gnome-extension-touchup
- https://github.com/MCC45TR/touchshell
- https://github.com/MCC45TR/nabu-tablet-controls

## Automated updates

Each fork attempts an hourly, fail-closed merge from its original upstream and
runs its GNOME 51 validation before pushing. This repository then rebuilds the
three deterministic payload archives hourly, increments the RPM release only
when a payload changes, validates the source RPM, and pushes the result. A
GitHub push webhook submits that revision to the `mcc45tr/nabu-linux` COPR.

Merge conflicts, TypeScript errors, JavaScript syntax failures, missing GNOME
51 metadata, or RPM source validation failures stop publication.
