#!/usr/bin/bash
set -euo pipefail

repo_dir=$(cd "$(dirname "$0")" && pwd)
rpmbuild -bs "$repo_dir/gnome-extension-group.spec" \
    --define "_sourcedir $repo_dir/sources" \
    --define "_srcrpmdir ${outdir:-$repo_dir}"
