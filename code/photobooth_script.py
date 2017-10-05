#!/usr/bin/env python
# created by kabcode@gmail.com
# information and further details can be found under www.kabelitzens.de

# this is a skript for a interactive photobooth

# imports
from constants import SUCCESS, FAILURE
import time
import picamera
import cwiid
import sys
import os
import pygame
import math
import random
import shutil

#####################
###   variables   ###
#####################
button_delay = 0.2 # seconds before the button is ready again
prepare_time = 1    # seconds to prepare before photo is taken
real_path = os.path.dirname(os.path.realpath('__file__')) # path where this file is located
parent_path = os.path.dirname(real_path)

delay_time = 0.5
restart_delay = 5
count_time = 0.4

# default variables
image_path = parent_path + '/images/'
image_language = 'en'
pygame.surface = None

# images
image_blank = 'blank.png'
image_count1 = 'count1.png'
image_count2 = 'count2.png'
image_count3 = 'count3.png'
image_smiley = 'smiley.png'
image_connect = '_connect.png'
image_started = '_started.png'
image_done = '_done.png'
image_error = '_error.png'
image_instruction = '_instructions.png'
image_saving = '_saving.png'
image_smile = '_smile.png'


############################
###  wiimote functions   ###
############################
# setup the wiimote connection
def prepareWiiRemote():
    show_image(image_connect,1)
    time.sleep(1)
    try:
        print("Connecting...")
        wii = cwiid.Wiimote()
        print("Connected to wiimote.")
    except:
        show_error_image("No wiimote detected.")
        return None

    wii.rumble = 1
    time.sleep(1)
    wii.rumble = 0
    print ('Wii Remote connected...\n')
    # set wiimote in button mode
    wii.rpt_mode = cwiid.RPT_BTN    
    return wii

# stop the wiimote connection and the programm
def stopWiimoteConnection(wii):
    print ('\nClosing connection ...')
    for i in range(2):
        wii.rumble = 1
        time.sleep(0.5)
        wii.rumble = 0
        time.sleep(0.5)
        wii.close()
        sys.exit()

# check connection to wiimote
def checkConnection(wii):
    if(wii==None):
        show_error_image("Lost connection to wiimote.")

#################################
###  data storage functions   ###
#################################
# setup data storage for this eventbased on the date
def setupDataStorage():
    timestr = time.strftime("/%Y%m%d/")
    storage_folder = parent_path + timestr
    if(os.path.isdir(storage_folder)):
        return storage_folder
    else:
        os.makedirs(storage_folder)
        shutil.copy2(image_path + image_smiley,storage_folder)
        print(image_path + image_smiley)
        return storage_folder

##################################
###  visualization functions   ###
##################################
# init pygame to use the module
def init_pygame():
    pygame.init()
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    pygame.mouse.set_visible(False) #hide the mouse cursor
    return size

# show image that is provided by path
def show_image(image_name, language_flag):
    screen_size = init_pygame()
    img = loadImage(image_name,language_flag)
    # following lines moving image to the center of screen
    imgSize = img.get_size()
    offset_x = (screen_size[0] - imgSize[0])/2
    offset_y = (screen_size[1] - imgSize[1])/2
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
    #screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    screen.blit(img,(offset_x,offset_y))
    pygame.display.flip()

# if an error occured show the error image and then close the image after 30 seconds and quit
def show_error_image(msg):
    screen_size = init_pygame()
    img = loadImage(image_error)
    # following lines moving image to the center of screen
    imgSize = img.get_size()
    offset_x = (screen_size[0] - imgSize[0])/2
    offset_y = (screen_size[1] - imgSize[1])/2
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
    #screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    screen.blit(img,(offset_x,offset_y))
    pygame.display.flip()
    time.sleep(10)
    pygame.quit()
    print("The programm was shut down due an error. Possible error:")
    print(msg)
    sys.exit()

# show taken images on start screen
def show_image_start_screen(image_name):
    screen_size = init_pygame()
    random_filename = random.choice([x for x in os.listdir(storage_path) if os.path.isfile(os.path.join(storage_path,x))])
    img = pygame.image.load(storage_path + random_filename)
    imgSize = img.get_size()
    scale_x = int(math.floor(imgSize[0]/3))
    scale_y = int(math.floor(imgSize[1]/3))
    img_scaled = pygame.transform.scale(img,(scale_x,scale_y))
    screen = pygame.display.get_surface()
    screen.blit(img_scaled, (300,500))
    pygame.display.flip()

# load image function for choosen language
def loadImage(image_name, language_flag):
    if(language_flag): # use image with choosen language
        image_full_name = image_path + image_language + image_name
    else:
        image_full_name = image_path + image_name
    image = pygame.image.load(image_full_name)
    return image

##########################################  
# the main photobooth programm.          #
# called when user pushed the "A" button #
##########################################
def start_photobooth_A(storage_path):
    # show a blank/instruction image
    show_image(image_blank,0)
    time.sleep(prepare_time) 
    
    # load camera parameter and present preview
    camera = picamera.PiCamera()
    size = pygame.init()
    # this size is for a 1440x900 px screen
    preview_size = [460,440,520,320]
    print(preview_size)
    try:
        camera.start_preview(fullscreen=False, window=preview_size)
        
    except all:
        print("Problem!")
        show_error_image("Camera error.")
        
    show_image(image_count3,0)
    time.sleep(count_time)
    show_image(image_count2,0)
    time.sleep(count_time)
    show_image(image_count1,0)
    time.sleep(count_time)

    # start taking the photo
    show_image(image_smile,1)
    time.sleep(0.5)
    image_name = time.strftime('%H_%M_%S.jpg')
    storageLocation = storage_path + image_name
    
    try:
        camera.capture(storageLocation)

    finally:
        # stop preview and show taken images
        camera.stop_preview()
        time.sleep(delay_time)
        show_image(image_saving,1)
        time.sleep(4)
        show_image(image_done,1)
        time.sleep(delay_time)
        camera.close()

    # finish photo session and show instruction image again
    show_image(image_instruction,1)


#####################
### main programe ###
#####################
# prepare the wii remote and establish the bt connection
wii = prepareWiiRemote()
# if remote is not useable exit program with error message
if(wii == None):
    show_error_image("No wiimote connection established.")

# set the parameter for data storage
# real_path is were the images are stored
storage_path = setupDataStorage()

# show the instroduction image
show_image(image_started,1)
time.sleep(2)
show_image(image_instruction,1)

start_time = time.time()

while True:

    # wait for input via the buttons
    buttons = wii.state['buttons']

    # if "+" and "-" buttons pressed together, shut down photobooth
    if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
        pygame.display.quit()
        stopWiimoteConnection(wii)
        sys.exit();

    # if "A" button is pressed, start the photobooth action
    if(buttons & cwiid.BTN_A):
        start_photobooth_A(storage_path)

    # if the left or right button are pressed, switch language
    if(buttons - cwiid.BTN_LEFT == 0):
        image_language = 'de'
        show_image(image_instruction,1)
    if(buttons - cwiid.BTN_RIGHT == 0):
        image_language = 'en'
        show_image(image_instruction,1)

    # check if wii connection is still running
    checkConnection(wii)

    # place images taken images on screen, change image every 5 seconds
    end_time = time.time()
    if((end_time-start_time) > 5):
        show_image_start_screen(storage_path)
        start_time = time.time()
    
  
 
