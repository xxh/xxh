#!/usr/bin/env xonsh

xpip install xontrib-autojump > /dev/null 2> /dev/null
xpip install xontrib-schedule > /dev/null 2> /dev/null

xontrib load autojump > /dev/null 2> /dev/null
xontrib load schedule > /dev/null 2> /dev/null

xontrib list autojump schedule 2>&1
