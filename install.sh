#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Root convenience entrypoint forwarding to tools/install.sh

exec "$(dirname "$0")/tools/install.sh" "$@"
