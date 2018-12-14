#!/bin/bash
echo "Press CTRL-C in 5 seconds to stop executing script"
sleep 5

amixer sset PCM 100%
while [ 1 ]; do
  sudo ip addr l
  mpg123 --loop -1 fan.mp3
done
