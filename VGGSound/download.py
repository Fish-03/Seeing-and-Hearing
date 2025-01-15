import yt_dlp
import ffmpeg
import pandas as pd
import os
from tqdm import tqdm
from moviepy import *
def read_csv(file_path):
    return pd.read_csv(file_path, header=None)

dataset = read_csv('vggsound.csv')

url_head = "https://www.youtube.com/watch?v="
dataset_ = dataset.values.tolist()
dataset_ = dataset_[4:5]
# URLS = [url_head + str(dataset_[0][i]) for i in range(len(dataset_))]
datapath = 'vggsound'
if not os.path.exists(datapath):
    os.makedirs(datapath)
import yt_dlp


# ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
ydl_opts = {}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for data in tqdm(dataset_):
        url = url_head + str(data[0])
        time = data[1]
        try:   
            info = ydl.extract_info(url, download=False)
            name = info["display_id"]
            
            # ℹ️ ydl.sanitize_info makes the info json-serializable
            # print(json.dumps(ydl.sanitize_info(info)))
            infos = ydl.sanitize_info(info)
            # print(infos['requested_formats'])
            if "requested_formats" not in infos:
                raise Exception("No requested formats")
            requested_formats = infos['requested_formats']
            # print(requested_formats)
            download_url = {"audio" if "audio only" in requested_formats[i]['format'] else "video"
                             :requested_formats[i]['url'] for i in range(len(requested_formats))}
            # if len(download_url) != 2:
            #     if len(download_url) > 2:
            #         print(f"【Warning】More than 2 audio streams: {name}")
            #     raise Exception("Not 2 audio streams")
            if not os.path.exists(os.path.join(datapath, name)):
                os.makedirs(os.path.join(datapath, name))
            if os.listdir(os.path.join(datapath, name)):
                print(f"Already downloaded {name}")
                continue
            for k,v in download_url.items():
                if k == "audio":
                    ffmpeg.input(v,
                                 ).output(os.path.join(datapath, name, name + ".mp3")).run()
                    clip = AudioFileClip(os.path.join(datapath, name, name + ".mp3"))
                    start = float(time)
                    end = clip.duration
                    clip = clip.subclipped(start, end)
                    clip.write_audiofile(os.path.join(datapath, name, name + "_clip.mp3"))
                    clip.close()
                    os.remove(os.path.join(datapath, name, name + ".mp3"))
                    os.rename(os.path.join(datapath, name, name + "_clip.mp3"), os.path.join(datapath, name, name + ".mp3"))
                    
                else:
                    ffmpeg.input(v,
                                 ).output(os.path.join(datapath, name, name + ".mp4")).run()
                    clip = VideoFileClip(os.path.join(datapath, name, name + ".mp4"))
                    
                    start = float(time)
                    end = clip.duration
                    clip = clip.subclipped(start, end)
                    clip.write_videofile(os.path.join(datapath, name, name+"_clip.mp4"))
                    clip.close()
                    os.remove(os.path.join(datapath, name, name + ".mp4"))
                    os.rename(os.path.join(datapath, name, name + "_clip.mp4"), os.path.join(datapath, name, name + ".mp4"))
                    
            
        except Exception as e:
            print(e)
            continue
    