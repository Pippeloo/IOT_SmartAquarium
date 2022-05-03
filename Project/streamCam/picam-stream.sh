#!/bin/bash
# -=====- BASIC SETUP -=====-
# Twitch Stream setup
TWITCH_STREAM_URL=rtmp://live.twitch.tv/app/
TWITCH_STREAM_KEY=live_408109025_naoQdtan54aDKDIYQT0UzCizHtew47

# -=====- ADVANCED SETUP -=====-
# Set width and height of output video
WIDTH=1920
HEIGHT=1080

# Set output framerate
FRAMERATE=30

# Set keyframe spacing (must be double the framerate)
KEYFRAME=60

# Set bitrate (Twitch recommends 3500000)
BITRATE=3500000

# Command
echo "Starting stream..."
echo 'libcamera-vid -n -t 0 --width $WIDTH --height $HEIGHT --framerate $FRAMERATE --bitrate $BITRATE -g $KEYFRAME -o - | ffmpeg -f lavfi -i anullsrc -c:a aac -r $FRAMERATE -i - -g $KEYFRAME -strict experimental -threads 4 -vcodec copy -map 0:a -map 1:v -b:v $BITRATE -preset ultrafast -f flv "${TWITCH_STREAM_URL}/${TWITCH_STREAM_KEY}"'
libcamera-vid -n -t 0 --width $WIDTH --height $HEIGHT --framerate $FRAMERATE --bitrate $BITRATE -g $KEYFRAME -o - | ffmpeg -f lavfi -i anullsrc -c:a aac -r $FRAMERATE -i - -g $KEYFRAME -strict experimental -threads 4 -vcodec copy -map 0:a -map 1:v -b:v $BITRATE -preset ultrafast -f flv "${TWITCH_STREAM_URL}/${TWITCH_STREAM_KEY}"
