#!/bin/sh
version=$1
variant=$2

src_dir="../pyinstaller/dist/"

app_name=MAP-Client$variant
app_name_with_version=MAP-Client$variant-$version
dmg_name=$app_name_with_version.dmg
test -d $src_dir/$app_name && rm -rf $src_dir/$app_name
test -f $dmg_name && rm $dmg_name
#  --volicon "application_icon.icns" \
create-dmg \
  --volname "$app_name_with_version" \
  --volicon "MAP-Client.icns" \
  --background "map-client-dmg-background.png" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "$app_name.app" 200 190 \
  --hide-extension "$app_name.app" \
  --app-drop-link 600 185 \
  "$dmg_name" \
  "$src_dir"

