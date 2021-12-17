#
# This entrypoint is to allow xxh getting current environment variables
# and pass some of them to xxh session to seamless transition to host.
#
# Usage in zsh: source xxh.zsh [ordinary xxh arguments]
#

local_xxh_home=~/.xxh

eargs=""
setopt +o nomatch
for pluginenv_file in "$local_xxh_home"/.xxh/plugins/*-zsh-*/env; do
  if [[ -f $pluginenv_file ]]; then
    plugin_name=$(basename "$(dirname "$pluginenv_file")" | tr "[:lower:]" "[:upper:]" | sed 's/-/_/g')

    if [[ $XXH_VERBOSE == '1' || $XXH_VERBOSE == '2' ]]; then
      echo Load plugin env "$pluginenv_file"
    fi

    for l in $(cat "$pluginenv_file")
    do
      if [[ -v $l ]]; then
        case $(uname -s) in
          Darwin)
          #  bas64 in macos uses -b (break) instead of --wrap, and it's 0 by default
            d=$(declare -p "$l" | base64)
            dd="export $plugin_name"_EXE_"$l=$d"
            ddd=$(echo "$dd" | base64)
          ;;
          *)
            d=$(declare -p "$l" | base64 --wrap=0)
            dd="export $plugin_name"_EXE_"$l=$d"
            ddd=$(echo "$dd" | base64 --wrap=0)
          ;;
        esac
        if [[ $XXH_VERBOSE == '2' ]]; then
          echo Prepare plugin env "$pluginenv_file": name="$l", declare="$d"
          echo Prepare plugin env "$pluginenv_file" bash: "$dd"
        fi
        eargs="$eargs +heb $ddd"
      fi
    done
  fi
done
setopt -o nomatch

CDIR="$(cd "$(dirname "$0")" && pwd)"
[ -f "$CDIR"/xxh ] && xxh="$CDIR"/xxh || xxh='xxh'
# shellcheck disable=SC2296
$xxh +s xxh-shell-zsh "${(z)eargs}" "$@"
