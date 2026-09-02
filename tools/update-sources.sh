#!/usr/bin/bash
set -euo pipefail

repo_dir=$(cd "$(dirname "$0")/.." && pwd)
task_tmp=$(mktemp -d)
trap 'rm -rf -- "$task_tmp"' EXIT

git clone --depth 1 https://github.com/MCC45TR/convergence-shell.git "$task_tmp/convergence-shell"
git clone --depth 1 https://github.com/MCC45TR/gnome-extension-touchup.git "$task_tmp/touchup"
git clone --depth 1 https://github.com/MCC45TR/touchshell.git "$task_tmp/touchshell"

(
    cd "$task_tmp/touchup"
    npm ci
    npm run lint:tsc
    npm run build:release
)

package_tree() {
    local tree=$1
    local output=$2
    find "$tree" -exec touch -h -d '@315532800' {} +
    (
        cd "$tree"
        find . -type f -print0 | LC_ALL=C sort -z | xargs -0 zip -Xq "$output"
    )
}

mkdir "$task_tmp/convergence-package" "$task_tmp/touchshell-package"
cp -a \
    "$task_tmp/convergence-shell/extension.js" \
    "$task_tmp/convergence-shell/prefs.js" \
    "$task_tmp/convergence-shell/metadata.json" \
    "$task_tmp/convergence-shell/stylesheet.css" \
    "$task_tmp/convergence-shell/appDrawer.js" \
    "$task_tmp/convergence-shell/widgetSettings.js" \
    "$task_tmp/convergence-shell/src" \
    "$task_tmp/convergence-shell/icons" \
    "$task_tmp/convergence-shell/schemas" \
    "$task_tmp/convergence-shell/LICENSE" \
    "$task_tmp/convergence-package/"
cp -a \
    "$task_tmp/touchshell/extension.js" \
    "$task_tmp/touchshell/prefs.js" \
    "$task_tmp/touchshell/metadata.json" \
    "$task_tmp/touchshell/stylesheet.css" \
    "$task_tmp/touchshell/lib" \
    "$task_tmp/touchshell/schemas" \
    "$task_tmp/touchshell/LICENSE" \
    "$task_tmp/touchshell-package/"

mkdir -p "$repo_dir/sources"
package_tree "$task_tmp/convergence-package" "$repo_dir/sources/convergence-shell.zip"
package_tree "$task_tmp/touchshell-package" "$repo_dir/sources/touchshell.zip"

unzip -q "$task_tmp/touchup/dist/"*.zip -d "$task_tmp/touchup-package"
package_tree "$task_tmp/touchup-package" "$repo_dir/sources/touchup.zip"

for source in "$repo_dir/sources/"*.zip; do
    unzip -t "$source" >/dev/null
    unzip -p "$source" metadata.json | jq -e '."shell-version" | index("51")' >/dev/null
done

{
    printf 'convergence-shell %s\n' "$(git -C "$task_tmp/convergence-shell" rev-parse HEAD)"
    printf 'gnome-extension-touchup %s\n' "$(git -C "$task_tmp/touchup" rev-parse HEAD)"
    printf 'touchshell %s\n' "$(git -C "$task_tmp/touchshell" rev-parse HEAD)"
} > "$repo_dir/sources.lock"
