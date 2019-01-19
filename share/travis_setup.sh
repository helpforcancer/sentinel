#!/bin/bash
set -evx

mkdir ~/.hfcc

# safety check
if [ ! -f ~/.hfcc/.hfcc.conf ]; then
  cp share/hfcc.conf.example ~/.hfcc/hfcc.conf
fi
