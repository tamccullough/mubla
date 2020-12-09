# Todd McCullough

from datetime import date, datetime, timedelta
from flask import Flask
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, send_file
from PIL import Image as ipl
from random import randrange
from werkzeug.security import check_password_hash, generate_password_hash

import mubla as mub

#import db
import functools
import numpy as np
import os
from os import listdir
from os.path import isfile, join
import pandas as pd
import re

root_folder = '/your/photos/path/'
directory = root_folder

def clean_thumbs():
    thumbdir = 'static/images/thumbs/'
    thumblist = [ f for f in os.listdir(thumbdir) if f.endswith('.jpg') | f.endswith('.JPG') ]
    for f in thumblist:
        os.remove(os.path.join(thumbdir, f))

def clean_served():
    stored = 'static/images/served/'
    onlyfiles = [f for f in listdir(stored) if isfile(join(stored, f))]
    print('\n',onlyfiles,'\n')
    for f in onlyfiles:
        os.remove(os.path.join(stored, f))

all_files = mub.get_all_files(directory)
directories = pd.DataFrame(all_files,columns=['root','year','month','day','file'])
years = directories.year.unique()

mubla = Flask(__name__, instance_relative_config=True)
mubla.config.from_mapping(
        SECRET_KEY='dev', # change to a random value later when deploying
        DATABASE=os.path.join(mubla.instance_path, 'main.sqlite'),
    )

theme, tfont, bfont = 'mono', ['Pacifico','sans-serif'], ['Open Sans','sans-serif']

@mubla.route('/')
def index():
    clean_thumbs()
    clean_served()
    years = [x for x in directories['year'].unique() if x[0:4].isdigit()]
    years = sorted(years)
    if len(years) <= 2:
        placement = 'squeeze'
    elif len(years) <= 4:
        placement = 'tight'
    else:
        placement = ''
    return render_template('index.html', placement = placement,
    link = 'months', location = 'mubla',
    home = 'mubla', image = 'static/images/folder.svg', folder = years,
    theme = theme,  tfont = tfont, bfont = bfont)

@mubla.route('/months', methods=['POST'])
def month():
    global year
    year = request.form['months']+'/'
    directory = root_folder+year
    months = [x for x in directories[directories['year'] == year]['month'].unique() if x[0] != '.']
    months = [x for x in months if (x[0] != '.') | (x[:1] != 'mt')]
    months = sorted(months)
    if len(months) <= 2:
        placement = 'squeeze'
    elif len(months) <= 4:
        placement = 'tight'
    else:
        placement = ''
    return render_template('index.html', placement = placement,
    link = 'days', location = year[:-1],
    home = 'mubla', image = 'static/images/folderm.svg', folder = months,
    theme = theme,  tfont = tfont, bfont = bfont)

@mubla.route('/days', methods=['POST'])
def day():
    global month
    month = request.form['days']+'/'
    days = directories[(directories['year'] == year) & (directories['month'] == month)]['day'].unique()
    days = [x for x in days if (x[0] != '.') | (x[:1] != 'mt')]
    days = sorted(days)
    if len(days) <= 2:
        placement = 'squeeze'
    elif len(days) <= 4:
        placement = 'tight'
    else:
        placement = ''
    return render_template('index.html', placement = placement,
    link = 'files', location = month[:-1]+'-'+year[:-1],
    home = 'mubla', image = 'static/images/folderd.svg', folder = days,
    theme = theme,  tfont = tfont, bfont = bfont)

@mubla.route('/files', methods=['POST'])
def file():
    global day
    day = request.form['files']+'/'
    directory = root_folder+year+month+day
    files = directories[(directories['year'] == year) & (directories['month'] == month) & (directories['day'] == day)]['file'].values
    files = [x for x in files if (x[0] != '.') | (x[:1] != 'mt')]
    files = sorted(files)
    files = [x for x in files if x != '.comments']
    print('\n',files,'\n')
    if len(files) <= 2:
        placement = 'squeeze'
    elif len(files) <= 4:
        placement = 'tight'
    else:
        placement = ''
    for x in files:
        if (x[-4:] == '.jpg') or (x[-4:] == '.JPG'):
            mub.image_thumb(directory+x)
        else:
            if x == '.comments':
                pass
            else:
                mub.video_thumb(directory,x)
    return render_template('index.html', placement = placement,
    link = 'view', location = month[:-1]+'-'+day[:-1]+'-'+year[:-1],
    home = 'mubla', image = '', folder = files, path = directory,
    theme = theme,  tfont = tfont, bfont = bfont)

@mubla.route('/view', methods=['POST'])
def view():
    filename = request.form['file']
    directory = root_folder+year+month+day
    gen = randrange(1000)
    clean_served()
    if (filename[-3:].lower() == 'jpg') | (filename[-3:].lower() == 'jpeg'):
        img = mub.image_open(directory+filename)
        if img.size[0] > img.size[1]:
            size = 'wide'
        else:
            size = 'tall'
        print('\n',gen,'\n',size,'\n')
        image_scaled = mub.image_resize(img,value=3,scale=0)
        image_scaled.save(f'static/images/served/out{gen}.jpg',quality=100)
        return render_template('file.html', scale = 'l',
        link = 'months', location = month[:-1]+'-'+day[:-1]+'-'+year[:-1], check = 'img', query = gen,
        home = 'mubla', ext = '.jpg', folder = years, size = size,
        theme = theme,  tfont = tfont, bfont = bfont)
        ## testing above
        #return send_file('static/images/served/out.jpg', cache_timeout=0)
    else:
        mub.video_copy(directory+filename,gen)
        if int(year[:-1]) < 2010:
            scale = 's'
        else:
            scale = 'l'
        print('\n',scale,'\n')
        return render_template('file.html', scale = scale,
        link = 'months', location = month[:-1]+'-'+day[:-1]+'-'+year[:-1], check = 'video', query = gen,
        home = 'mubla', ext = '.jpg', folder = years, size = 'wide',
        theme = theme,  tfont = tfont, bfont = bfont)
        ## testing above
        #return send_file(directory+filename, cache_timeout=0)

#db.init_app(mubla)

if __name__ == "__main__":
    mubla.run()
