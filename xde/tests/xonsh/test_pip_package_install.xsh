#!/usr/bin/env xonsh

pip install @('--verbose' if $XXH_VERBOSE == 2 else '--quiet') --upgrade pandas
