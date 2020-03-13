#
# This entrypoint is to allow xxh getting current environment variables
# and pass some of them to xxh session to seamless transition to host.
#
# Usage in zsh: source xxh.zsh [ordinary xxh arguments]
#
d=`declare -p 2>/dev/null`
if [ ! $d ]; then
  echo  "\nThis entrypoint is to allow xxh getting current environment variables"
  echo  "and pass some of them to xxh session to seamless transition to host.\n"
  echo  "Usage in zsh: source xxh.zsh [ordinary xxh arguments]\n"
else
  XXH_SH_ENV=$d xxh +E +s xxh-shell-zsh "$@"
fi