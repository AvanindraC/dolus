import pyvirtualcam
import numpy as np
import cv2 as cv
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand
import re, requests, urllib.parse, urllib.request
import pafy

@click.group(
    cls=HelpColorsGroup, help_headers_color="yellow", help_options_color="cyan")
@click.version_option('0.1.0')
def main():
    """Dolus - Change your live video from the terminal"""
@main.command('cartoonify', help = 'Gives your face a cartoonish effect')
def cartoonify():
  
  
  with pyvirtualcam.Camera(width=640, height=480, fps=20) as cam:
    print(f'Using virtual camera: {cam.device}')
    b = cv.VideoCapture(0)
    while True:
        isTrue, frame = b.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) 
        gray = cv.medianBlur(gray, 3) 
        edges = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 9, 10)
  # Making a Cartoon of the image
        color = cv.bilateralFilter(frame, 12, 250, 250) 
        cartoon = cv.bitwise_and(color, color, mask=edges)
        cartoon_image = cv.stylization(frame, sigma_s=150, sigma_r=0.25)  
        frame = cartoon_image
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame = cv.resize(frame, (640, 480))
        cam.send(frame)
        cam.sleep_until_next_frame()
def canny_img(photo):
    canny = cv.Canny(photo, 125, 175)
    return canny
@main.command('watercolor', help = 'Gives your face a watercolor effect')
def watercolor():
      
  with pyvirtualcam.Camera(width=640, height=480, fps=20) as cam:
    print(f'Using virtual camera: {cam.device}')
    b = cv.VideoCapture(0)
    while True:
        isTrue, frame = b.read()
        frame = cv.stylization(frame, sigma_s=60, sigma_r=0.6)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame = cv.resize(frame, (640, 480))
        cam.send(frame)
        cam.sleep_until_next_frame()
@main.command('pencil', help = 'Gives your face a pencil sketch effect')        
def pencil():
    with pyvirtualcam.Camera(width=640, height=480, fps=20) as cam:
        print(f'Using virtual camera: {cam.device}')
        b = cv.VideoCapture(0)
        while True:
            isTrue, frame = b.read()
            pencil, color  = cv.pencilSketch(frame, sigma_s=60, sigma_r=0.5, shade_factor=0.010) 
            frame = cv.cvtColor(pencil, cv.COLOR_BGR2RGB)
            frame = cv.resize(frame, (640, 480)) 
            cam.send(frame)
            cam.sleep_until_next_frame()
@main.command('econify', help = 'Gives your face a hacker like theme')
def econify():
  with pyvirtualcam.Camera(width=640, height=480, fps=20) as cam:
    print(f'Using virtual camera: {cam.device}')
    b = cv.VideoCapture(0)
    while True:
        isTrue, frame = b.read()
        canny = canny_img(frame)
        cv.imwrite('canny.jpg', canny)
        img = cv.imread('canny.jpg')
        blue, g, r = cv.split(img) 
        blank = np.zeros(img.shape[:2], dtype='uint8')

        green = cv.merge([blank,g,blank])
        
        frame = green
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame = cv.resize(frame, (640, 480))
        cam.send(frame)
        cam.sleep_until_next_frame()

@main.command('ytvid', help = 'Replace your video with a youtube video')
@click.argument('song', nargs = 1)
def ytvid(song):
    
    music_name = song
    query_string = urllib.parse.urlencode({"search_query": music_name})
    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
    clip = requests.get("https://www.youtube.com/watch?v=" + "{}".format(search_results[0]))
    clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
    video = pafy.new(clip2)
    video = video.getbest(preftype="mp4")
    with pyvirtualcam.Camera(width=640, height=480, fps=20) as cam:
        print(f'Using virtual camera: {cam.device}')
        b = cv.VideoCapture(video.url)
        while True:
            isTrue, frame = b.read()
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            frame = cv.resize(frame, (640, 480))
            cam.send(frame)
            cam.sleep_until_next_frame()
@main.command('negative', help = 'Inverts your face')
def negative():
  
  
  with pyvirtualcam.Camera(width=640, height=480, fps=20) as cam:
    print(f'Using virtual camera: {cam.device}')
    b = cv.VideoCapture(0)
    while True:
        isTrue, frame = b.read()
        frame = cv.bitwise_not(frame)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame = cv.resize(frame, (640, 480))
        cam.send(frame)
        cam.sleep_until_next_frame()
if __name__ == '__main__':
    main()