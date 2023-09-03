from pytube import YouTube, extract
from pytube.cli import on_progress
import pandas as pd
import uuid
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os


def DownloadYoutube(link):
    youtubeObject = YouTube(link, on_progress_callback=on_progress)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    name = ''
    
    try:
        name = str(uuid.uuid4()) + '.mp4'
        youtubeObject.download(output_path='videos',filename=name)
        print("Download is completed successfully")
    except:
        name = ''
        print("An error has occurred")

    return name

def convert_to_seconds(time):

    time_div = time.split(':')
    m_arr = [1,60,24]
    seconds = 0

    for count, time in enumerate(reversed(time_div)):
        seconds += int(time)*m_arr[count]    

    return seconds


if __name__ == '__main__':

    df = pd.read_csv('SadEmotions150.csv')
    
    # print(df.head(6))

    link_map = {}

    if not os.path.exists('videos'):
        os.mkdir('videos')

    if not os.path.exists('cropped_videos'):
        os.mkdir('cropped_videos')
    
    for index, row in df.iterrows():
        
        link = row['Url']
        id = extract.video_id(link)

        if id in link_map:
            filename = link_map[id]
        else:
            filename = DownloadYoutube(link)
            link_map[id] = filename

        if len(filename)>0:
            
            timefetch = row['Timestamp']
            timelimits = timefetch.split('-')
            start_time = timelimits[0].strip()
            end_time = timelimits[1].strip()
            
            start_time = convert_to_seconds(start_time)
            end_time = convert_to_seconds(end_time)

            emotion = row['Emotion']
            
            video = VideoFileClip('videos/'+filename).subclip(start_time, end_time)

            if not os.path.exists('cropped_videos/'+emotion):
                os.mkdir('cropped_videos/'+emotion)

            video.write_videofile('cropped_videos/'+emotion+'/'+filename) 
            
            video.close()

            print('Video '+str(index)+' downloaded\n\n')


