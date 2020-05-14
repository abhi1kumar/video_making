

"""
    Sample Run:
    python suppress_noise_in_video.py --input cvpr.mp4
    python suppress_noise_in_video.py --input cvpr.mp4 --noise None

    Cleans the video and audio.

    Version 1 2020-05-13 Abhinav Kumar

    Taken from 
    http://tejeshraut.blogspot.com/2016/06/record-noise-free-audio-in-ubuntu-or.html

    time = 1
    ffmpeg -i original.mp4 -qscale 0 -an tmpvid.mp4
    ffmpeg -i original.mp4 -qscale 0     tmpaud.wav
    sox tmpaud.wav noise.wav trim 0 0.5
    sox tmpaud.wav cleaned.wav noisered noise.prof 0.2
    ffmpeg -i cleaned.wav -i tmpvid.mp4 -qscale 0 -strict -2 cleanedvid.mp4

"""

import os, sys
import argparse
import warnings

def execute(command, print_flag= True):
    if print_flag:
        print(command)
    os.system(command)

parser = argparse.ArgumentParser(description = 'Cleans the video of the noise')
parser.add_argument('--input'   ,        type = str,            default = 'cvpr.mp4' , help = 'input video to use')
parser.add_argument('--noise'   ,        type = str,            default = 'noise.wav', help = 'noise profile')
parser.add_argument('--time'    ,        type = float,          default = 10,          help = 'end time for noise profiling')
args = parser.parse_args()
warnings.filterwarnings("ignore")

# Split the video into audio and visual streams
base_wo_ext = ".".join(os.path.basename(args.input).split(".")[:-1])
split_vis   = "tmp_" + base_wo_ext + ".mp4"
split_aud   = "tmp_" + base_wo_ext + ".wav"
cleaned_aud = "cleaned_" + base_wo_ext + ".wav"

if args.noise == "None":
    noise_aud  = "noisy_" + base_wo_ext + ".wav"
    noise_prof = "prof_"  + base_wo_ext + ".prof"
else:
    noise_prof = args.noise


command = "ffmpeg -i " + args.input + " -qscale 0 -an " + split_vis
execute(command)

command = "ffmpeg -i " + args.input + " -qscale 0     " + split_aud
execute(command)

# Clean the audio
if args.noise == "None":
    # Create the noise sample and profile
    command = "sox " + split_aud + " " + noise_aud + " trim 0 " + str(args.time)
    execute(command)
    
    command = "sox " + noise_aud + " -n noiseprof " + noise_prof
    execute(command)    

command = "sox " + split_aud +" " + cleaned_aud + " noisered " + noise_prof + " 0.3"
execute(command)

# Combine with video
cleaned_vid = base_wo_ext + "_cleaned.mp4"
command = "ffmpeg -i " + cleaned_aud + " -i " + split_vis + " -qscale 0 -strict -2 " + cleaned_vid
execute(command)

# Remove the temp files
command = "rm " + split_vis + " " + split_aud + " " + cleaned_aud
execute(command)

if args.noise == "None":
    command = "rm " + noise_aud + " " + noise_prof
    execute(command)
