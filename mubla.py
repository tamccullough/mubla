# canpl statistics
# Todd McCullough 2020
from datetime import date, datetime, timedelta
#from IPython import get_ipython
from pathlib import Path

from PIL import Image as ipl
from PIL import ImageFile, ImageFilter, ImageEnhance, ImageChops, ImageOps, ImageMath
from shutil import copyfile

#import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import subprocess
#import requests

root_folder = '/your/photos/path/'
directory = root_folder

def get_all_files(directory):
    file_list = []
    with os.scandir(directory) as years:
        for year in years:
            if (year.name == 'lost+found') | (year.name[0] == '.'):
                pass
            else:
                try:
                    months = os.listdir(directory+year.name)
                    for month in months:
                        try:
                            days = os.listdir(directory+year.name+'/'+month)
                            for day in days:
                                files = os.listdir(directory+year.name+'/'+month+'/'+day)
                                for file in files:
                                    try:
                                        file_list.append([root_folder,year.name+'/',month+'/',day+'/',file])
                                    except:
                                        file_list.append([root_folder,year.name+'/',month+'/',day+'/','mt'])
                        except:
                            file_list.append([root_folder,year.name+'/',month+'/','mt','mt'])
                except:
                    file_list.append([root_folder,year.name+'/','mt','mt','mt'])
    return file_list

all_files = get_all_files(directory)
directories = pd.DataFrame(all_files,columns=['root','year','month','day','files'])

today = date.today().strftime('%Y-%m-%d')

def get_weekday():
    weekDays = ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')
    current_year = date.today().strftime('%Y')
    month = datetime.today().strftime('%B')
    today = datetime.today()
    day = datetime.today().strftime('%d')

    weekday_num = today.weekday()
    weekday = weekDays[weekday_num]
    return month, day, weekday

def utc_convert(string):
    day = int(string[8:10])
    month = int(string[5:7])
    year = int(string[:4])
    offset = 693594
    itime = datetime(year,month,day)
    n = itime.toordinal()
    m = (n - offset)
    return m

def image_bands(img):
    bands = img.split()
    return bands[0].point(lambda x: 255 if x < 20 else 0) # alter what x is greater than

def image_blur(img):
    return img.filter(ImageFilter.GaussianBlur)# better than BLUR

def image_crop(img):
    # figure out how to make this square and others
    width, height = img.size
    return img.crop((width/5, height/8, width-(width/7), height-(height/5)))

def image_data(img):
    return np.array(img)

def image_channel(img,chk='r'):
    img_data = image_data(img)
    img_chn = np.zeros(img_data.shape, dtype='uint8')
    if chk == 'b':
        img_chn[:,:,2] = img_data[:,:,2]
    elif chk == 'g':
        img_chn[:,:,1] = img_data[:,:,1]
    else:
        img_chn[:,:,0] = img_data[:,:,0]
    return ipl.fromarray(img_chn)

def image_combine(img,img2):
    return ImageMath.eval("convert(min(a, b), 'L')", a=img, b=img2)

def image_edges(img):
    return img.filter(ImageFilter.FIND_EDGES)

def image_flip(img):
    img_data = image_data(img)
    img_flipped_data = np.flip(img_data, axis=1)
    return ipl.fromarray(img_flipped_data)

def image_negative(img):
    img_data = image_data(img)
    img_reversed_data = 255 - img_data
    return ipl.fromarray(img_reversed_data)
def image_open(filename):
    return ipl.open(filename)

def image_overlay_color(main,colour,alpha):
    overlay = Image.new(main.mode, main.size, colour)
    bw_img = ImageEnhance.Color(main).enhance(0.0)
    return ipl.blend(bw_img, overlay, alpha)

def image_overlay_blend(main,overlay,alpha):
    #main = ImageEnhance.Color(main).enhance(0.0)
    overlay = overlay.resize((main.size[0], main.size[1]),Image.ANTIALIAS)
    return ipl.blend(main, overlay, alpha)

def image_overlay_add(main,overlay):
    overlay = overlay.resize((main.size[0], main.size[1]),Image.ANTIALIAS)
    return ImageChops.add(main,overlay,1,0)

def image_recolorize(main, black="#000099", white="#99CCFF"):
    return ImageOps.colorize(ImageOps.grayscale(main), black, white)

def image_resize(img,value=2,scale=0):
    if (img.size[0] < 800) | (img.size[1] < 800):
        return img
    else:
        if scale == 0:
            return img.resize((int(img.size[0] / value), int(img.size[1] / value)),ipl.ANTIALIAS)
        else:
            return img.resize((int(img.size[0] * value), int(img.size[1] * value)))

def image_thumb(img):
    img_new = image_open(img)
    filename = img_new.filename.split('/')[-1]
    out = img_new.resize((int(img_new.size[0] / 15), int(img_new.size[1] / 15)),ipl.ANTIALIAS)
    out.save(f'static/images/thumbs/thumb-{filename[:-3]}jpg',quality=100)

def image_save(image,contrast_factor,color_factor,filename):
    # give each enhance object a separate name
    contrast = ImageEnhance.Contrast(im)
    # load each consecutive enhance object into the next object
    color = ImageEnhance.Color(contrast.enhance(contrast_factor))
    color.enhance(color_factor).save(filename, quality=100)

def video_thumb(directory,filename):
    print('\n',filename,'\n')
    img_output_path = f'static/images/thumbs/thumb-{filename[:-3]}jpg'
    subprocess.call(['ffmpeg', '-i', directory+filename, '-ss', '00:00:00.000', '-vframes', '1', img_output_path])

def video_copy(filename,gen):
    copyfile(filename, os.path.join(f'/home/todd/Documents/git/mubla/static/images/served/out{gen}.mp4'))
