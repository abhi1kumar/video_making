
# Remember to put ss after i otherwise video will not be cropped exactly
ffmpeg -i cvpr5_cleaned.mp4 -ss 00:00:18 -t 00:01:00 -c copy cvpr5_cleaned_f.mp4

# See the length of video
ffmpeg -i cvpr5_cleaned_f.mp4 2>&1 | grep Duration | cut -d ' ' -f 4 | sed s/,//
