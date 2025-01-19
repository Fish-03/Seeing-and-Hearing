import yt_dlp
import ffmpeg
import pandas as pd
import os
from tqdm import tqdm
from moviepy import *
import numpy as np
from threading import Thread
import json
def read_csv(file_path):
    return pd.read_csv(file_path, header=None)
totaldownload = 300
if os.path.exists('vggsound_modified.csv'):
    dataset = read_csv('vggsound_modified.csv')
    dataset_ = dataset.values.tolist()
    dataset_ = np.array(dataset_)
else:
    dataset = read_csv('vggsound.csv')
    dataset_ = dataset.values.tolist()
    dataset_ = np.array(dataset_)
    dataset_ = np.random.permutation(dataset_)
    pd.DataFrame(dataset_).to_csv('vggsound_modified.csv', header=None, index=None)

url_head = "https://www.youtube.com/watch?v="

# URLS = [url_head + str(dataset_[0][i]) for i in range(len(dataset_))]
datapath = 'vggsound'
if not os.path.exists(datapath):
    os.makedirs(datapath)
import yt_dlp
format_note = "360p"
successdownload = len(os.listdir(datapath))-1
# ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
ydl_opts = {
    "format_note": "360p",
}

def download(dataset_, successdownload, totaldownload):
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        
        for i in range(successdownload, len(dataset_)):
            data = dataset_[i]
            if successdownload == totaldownload:
                return
            url = url_head + str(data[0])
            time = data[1]
            try:   
                info = ydl.extract_info(url, download=False)
                name = info["display_id"]
                
                # ℹ️ ydl.sanitize_info makes the info json-serializable
                # print(json.dumps(ydl.sanitize_info(info)))
                infos = ydl.sanitize_info(info)
                # print(infos['requested_formats'])
                if "formats" not in infos:
                    raise Exception("No formats")
                requested_formats = infos['formats']
                # print(requested_formats)
                
                # with open('vggsound.txt', 'a') as f:
                #     f.write(f"{requested_formats}\n")
                # break
                # download_url = {"audio" if "audio" in requested_formats[i]['format'] else "video"
                #                 :requested_formats[i]['url'] for i in range(len(requested_formats))}
                download_url = {}
                audio = False
                for i in range(len(requested_formats)):
                    if "format_note" in requested_formats[i]:
                        if requested_formats[i]['format_note'] == format_note:
                            download_url["video"] = requested_formats[i]['url']
                    if not audio:
                        if "audio" in requested_formats[i]['format']:
                            download_url["audio"] = requested_formats[i]['url']
                            audio = True
                        
                if len(download_url) != 2:
                    continue
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
                successdownload += 1
                
            except Exception as e:
                print(f"【Error】{e}")
                continue
print(f"Success download: {successdownload}")
download(dataset_, successdownload, totaldownload)

    
    