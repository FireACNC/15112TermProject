from cmu_cs3_graphics import *
from cmu_graphics.utils import *
from pygame import mixer
from PIL import Image

#load music & images.

# Music - Carefree Kevin MacLeod (incompetech.com)
# Licensed under Creative Commons: By Attribution 4.0 License
# http://creativecommons.org/licenses/by/4.0/
# Music promoted on https://www.chosic.com/free-music/all/ 

# Sound Effect from https://sc.chinaz.com/
#     'bgm' : 'https://media.chosic.com/wp-content/uploads/2020/07/Carefree.mp3',
#     'ding' : 'https://vod.ruotongmusic.com/sv/4a19706b-179cd1d9417/4a19706b-179cd1d9417.wav',
#     'turn': 'https://downsc.chinaz.net/Files/DownLoad/sound1/201212/2504.mp3',
#     'unlock': 'https://downsc.chinaz.net/Files/DownLoad/sound1/202104/14150.mp3',
#     'countdown': 'https://downsc.chinaz.net/Files/DownLoad/sound/huang/cd9/mp3/111.mp3',
#     'explode': 'https://vod.ruotongmusic.com/sv/352655e5-179ccfb54dd/352655e5-179ccfb54dd.wav',

# pygame is used only for sounds
# PIL is used for images.
# I drew the images by myself.



def loadMedia(app):
    #sounds
    mixer.init()
    app.sound = {}
    for soundName in ['bgm','ding','turn','unlock','countdown','explode']:
        app.sound[soundName] = mixer.Sound(f'sounds/{soundName}.mp3')

    app.sound['bgm'].play(loops = -1)
    app.turnPlay = 0

    #images
    app.images = {}
    for imageName in ['bg','spider_0','spider_1','wall','key','lock','bomb_0','bomb_1','cover','grid']:
        app.images[imageName] = CMUImage(Image.open(f'images/{imageName}.png'))

    app.images['spider'] = app.images['spider_0']