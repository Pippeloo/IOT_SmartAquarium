#!/bin/bash

# Import the configuration file
. ./setup.config

# Command
echo "Starting stream..."
libcamera-vid -n -t 0 --width $WIDTH --height $HEIGHT --framerate $FRAMERATE --bitrate $BITRATE -g $KEYFRAME -o - | ffmpeg -f lavfi -i anullsrc -c:a aac -r $FRAMERATE -i - -g $KEYFRAME -strict experimental -threads 4 -vcodec copy -map 0:a -map 1:v -b:v $BITRATE -preset ultrafast -f flv "${TWITCH_STREAM_URL}/${TWITCH_STREAM_KEY}"