#!/bin/bash

wget --load-cookies cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1OvswVCGkPEY632eWUOfrpaEZ2aceEu9Q' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1OvswVCGkPEY632eWUOfrpaEZ2aceEu9Q" -O admorph.zip && rm -rf cookies.txt
unzip -q admorph.zip
rm admorph.zip
