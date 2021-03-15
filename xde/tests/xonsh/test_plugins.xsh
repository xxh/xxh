#!/usr/bin/env xonsh

# xxh-plugin-xonsh-autojump
cd / 2>&1
cd /tmp 2>&1

# xxh-plugin-xonsh-pipe-liner
echo "4321\n8765" | pl "line[::-1]"

# xxh-plugin-xonsh-theme-bar
echo $PROMPT