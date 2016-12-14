#!/bin/zsh
SEC=`date +"%s"`
`cp "$1" favicon"$SEC".png`
`convert favicon"$SEC".png -resize 256x256 -bordercolor transparent -border 128x128 -gravity center -crop 256x256+0+0 +repage favicon-256"$SEC".png`
`convert favicon-256"$SEC".png -resize 128x128 favicon-128"$SEC".png`
`convert favicon-256"$SEC".png -resize 64x64 favicon-64"$SEC".png`
`convert favicon-256"$SEC".png -resize 32x32 favicon-32"$SEC".png`
`convert favicon-256"$SEC".png -resize 16x16 favicon-16"$SEC".png`
`convert favicon-16"$SEC".png favicon-32"$SEC".png favicon-64"$SEC".png favicon-128"$SEC".png favicon-256"$SEC".png favicon.ico`
`rm favicon"$SEC".png favicon-16"$SEC".png favicon-32"$SEC".png favicon-64"$SEC".png favicon-128"$SEC".png favicon-256"$SEC".png`
