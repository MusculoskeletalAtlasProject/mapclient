#!/bin/sh
version=0.15.0
variant=-mapping-tools

app_name=MAP-Client$variant-$version
dmg_name=$app_name.dmg
test -f $dmg_name && rm $dmg_name
#  --volicon "application_icon.icns" \
create-dmg \
  --volname $app_name \
  --volicon "MAP-Client.icns" \
  --background "map-client-dmg-background.png" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "MAP-Client.app" 200 190 \
  --hide-extension "MAP-Client.app" \
  --app-drop-link 600 185 \
  $dmg_name \
  "../pyinstaller/dist/"

