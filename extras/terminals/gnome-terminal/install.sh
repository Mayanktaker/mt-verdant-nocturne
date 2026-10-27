#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Install MT Verdant Nocturne profile into GNOME Terminal via dconf.

set -eu

PROFILE_NAME="MT-Verdant-Nocturne"
PROFILE_ID="$(uuidgen 2>/dev/null || python3 -c 'import uuid; print(uuid.uuid4())')"
DCONF_DIR="/org/gnome/terminal/legacy/profiles:/:${PROFILE_ID}/"

echo "Creating GNOME Terminal profile: ${PROFILE_NAME} (${PROFILE_ID})..."

# Register profile in profile list
CURRENT_LIST="$(dconf read /org/gnome/terminal/legacy/profiles:/list || echo "[]")"
if [ "${CURRENT_LIST}" = "[]" ] || [ -z "${CURRENT_LIST}" ]; then
  NEW_LIST="['${PROFILE_ID}']"
else
  NEW_LIST="$(echo "${CURRENT_LIST}" | sed "s/]/, '${PROFILE_ID}']/")"
fi
dconf write /org/gnome/terminal/legacy/profiles:/list "${NEW_LIST}"

# Write profile settings
dconf write "${DCONF_DIR}visible-name" "'${PROFILE_NAME}'"
dconf write "${DCONF_DIR}use-theme-colors" "false"
dconf write "${DCONF_DIR}background-color" "'rgb(15,20,27)'"
dconf write "${DCONF_DIR}foreground-color" "'rgb(233,241,236)'"
dconf write "${DCONF_DIR}highlight-background-color" "'rgb(143,184,166)'"
dconf write "${DCONF_DIR}highlight-foreground-color" "'rgb(13,19,26)'"
dconf write "${DCONF_DIR}cursor-colors-set" "true"
dconf write "${DCONF_DIR}cursor-background-color" "'rgb(143,184,166)'"
dconf write "${DCONF_DIR}cursor-foreground-color" "'rgb(13,19,26)'"
dconf write "${DCONF_DIR}palette" "['rgb(22,34,42)', 'rgb(229,115,127)', 'rgb(127,200,160)', 'rgb(229,181,128)', 'rgb(82,115,111)', 'rgb(201,163,176)', 'rgb(104,166,158)', 'rgb(167,184,177)', 'rgb(42,65,72)', 'rgb(242,133,145)', 'rgb(61,214,140)', 'rgb(240,195,143)', 'rgb(143,184,166)', 'rgb(220,184,197)', 'rgb(142,197,190)', 'rgb(233,241,236)']"

echo "Profile installed successfully! Select '${PROFILE_NAME}' in GNOME Terminal preferences."
