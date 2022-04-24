from cmu_cs3_graphics import *
from cmu_graphics.utils import *
from tqdm import tqdm
import time

# Music - Carefree Kevin MacLeod (incompetech.com)
# Licensed under Creative Commons: By Attribution 4.0 License
# http://creativecommons.org/licenses/by/4.0/
# Music promoted on https://www.chosic.com/free-music/all/ 

# Sound Effect from https://sc.chinaz.com/

def loadMedia(app):
    print('')
    print('Loading Sounds...Please Wait!')

    #Use tqdm to see progress of sound loading. Tqdm learned in course
    app.soundInfo = {
    'bgm' : 'https://media.chosic.com/wp-content/uploads/2020/07/Carefree.mp3',
    'ding' : 'https://vod.ruotongmusic.com/sv/4a19706b-179cd1d9417/4a19706b-179cd1d9417.wav',
    'turn': 'https://downsc.chinaz.net/Files/DownLoad/sound1/201212/2504.mp3',
    'unlock': 'https://downsc.chinaz.net/Files/DownLoad/sound1/202104/14150.mp3',
    'countdown': 'https://downsc.chinaz.net/Files/DownLoad/sound/huang/cd9/mp3/111.mp3',
    'explode': 'https://vod.ruotongmusic.com/sv/352655e5-179ccfb54dd/352655e5-179ccfb54dd.wav',
    }
    
    app.sound = {}
    for key in tqdm((app.soundInfo)):
        app.sound[key] = Sound(app.soundInfo[key])

    print('Sounds loaded successfully!')
    print('')
    
    app.sound['bgm'].play(loop = True)
    app.turnPlay = 0