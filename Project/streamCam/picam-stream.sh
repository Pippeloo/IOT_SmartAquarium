# Source: https://gist.github.com/russfeld/0878b1f8eaf7409136b9125ce5e1458f
# fps -> 30
# max fps (double buffering) -> 60
# Width -> 1920
# Height -> 1080
# Bitrate -> 3500000
echo "Starting stream..."
libcamera-vid -n -t 0 --width 1920 --height 1080 --framerate 30 --bitrate 3500000 -g 60 -o - | ffmpeg -f lavfi -i anullsrc -c:a aac -r 30 -i - -g 60 -strict experimental -threads 4 -vcodec copy -map 0:a --vflip -map 1:v -b:v 3500000 -preset ultrafast -f flv "rtmp://live.twitch.tv/app/live_408109025_naoQdtan54aDKDIYQT0UzCizHtew47"