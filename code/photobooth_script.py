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
button_delay = 0.2 # seconds bfore the button is ready again
prepare_time = 1    # seconds to prepare before photo is taken
real_path = os.path.dirname(os.path.realpath('__file__')) # path where this file is located

delay_time = 0.5
restart_delay = 5
count_time = 0.4

# image paths
connect_image = 'booth_images/connect_en.png'
start_image = 'booth_images/started_en.png'
instruction_image = 'booth_images/Instructions_en.png'
blank_image  = 'booth_images/blank.png'
count3_image = 'booth_images/count3.png'
count2_image = 'booth_images/count2.png'
count1_image = 'booth_images/count1.png'
smile_image  = 'booth_images/smile_en.png'
done_image   = 'booth_images/done_en.png' 
saving_image = 'booth_images/saving_en.png'
error_image  = 'booth_images/error_en.png'
smiley_image  = 'booth_images/smile.png'


#####################
###   functions   ###
#####################
# setup the wiimote connection
def prepareWiiRemote():
    show_image(connect_image)
    time.sleep(1)
    try:
        print("Connecting!")
        wii = cwiid.Wiimote()
    except:
        show_error_image(error_image)
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

# setup data storage for this eventbased on the date
def setupDataStorage():
    timestr = time.strftime("/%Y%m%d/")
    image_path = real_path + timestr
    if(os.path.isdir(image_path)):
        return image_path
    else:
        os.makedirs(image_path)
        shutil.copy2(smiley_image,image_path)
        return image_path

# init pygame to use the module
def init_pygame():
    pygame.init()
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    pygame.mouse.set_visible(False) #hide the mouse cursor
    return size

# show image that is provided by path
def show_image(image_path):
    screen_size = init_pygame()
    img = pygame.image.load(image_path)
    # following lines moving image to the center of screen
    imgSize = img.get_size()
    offset_x = (screen_size[0] - imgSize[0])/2
    offset_y = (screen_size[1] - imgSize[1])/2
    #screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    screen.blit(img,(offset_x,offset_y))
    pygame.display.flip()

# if an error occured show the error image and then close the image after 30 seconds and quit
def show_error_image(image_path):
    screen_size = init_pygame()
    img = pygame.image.load(image_path)
    # following lines moving image to the center of screen
    imgSize = img.get_size()
    offset_x = (screen_size[0] - imgSize[0])/2
    offset_y = (screen_size[1] - imgSize[1])/2
    #screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    screen.blit(img,(offset_x,offset_y))
    pygame.display.flip()
    time.sleep(10)
    pygame.quit()
    print("The programm was shut down due an error. Nothing went wrong.\n Please try to restart.")
    sys.exit()

# show taken images on start screen
def show_image_start_screen(image_path):
    screen_size = init_pygame()
    random_filename = random.choice([x for x in os.listdir(image_path) if os.path.isfile(os.path.join(image_path,x))])
    img = pygame.image.load(image_path + random_filename)
    imgSize = img.get_size()
    scale_x = int(math.floor(imgSize[0]/3))
    scale_y = int(math.floor(imgSize[1]/3))
    img_scaled = pygame.transform.scale(img,(scale_x,scale_y))
    screen = pygame.display.get_surface()
    screen.blit(img_scaled, (300,500))
    pygame.display.flip()

# check connection to wiimote
def checkConnection(wii):
    if(wii==None):
        image_error_schow(error_image)

##########################################  
# the main photobooth programm.          #
# called when user pushed the "A" button #
##########################################
def start_photobooth_A(image_path):
    # show a blank/instruction image
    show_image(blank_image)
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
        show_error_image(error_image)
        
    show_image(count3_image)
    time.sleep(count_time)
    show_image(count2_image)
    time.sleep(count_time)
    show_image(count1_image)
    time.sleep(count_time)

    # start taking the photo
    show_image(smile_image)
    time.sleep(0.5)
    image_name = time.strftime('%H_%M_%S.jpg')
    storageLocation = image_path + image_name
    
    try:
        camera.capture(storageLocation)

    finally:
        # stop preview and show taken images
        camera.stop_preview()
        time.sleep(delay_time)
        show_image(storageLocation)
        time.sleep(4)
        show_image(done_image)
        time.sleep(delay_time)
        camera.close()

    # finish photo session and show instruction image again
    show_image(saving_image)
    time.sleep(delay_time)
    show_image(instruction_image)


#####################
### main programe ###
#####################

# prepare the wii remote and establish the bt connection
wii = prepareWiiRemote()
# if remote is not useable exit program with error message
if(wii == None):
    show_error_image(error_image)

# set the parameter for data storage
# real_path is were the images are stored
image_path = setupDataStorage()

# show the instroduction image
show_image(start_image)
time.sleep(2)
show_image(instruction_image)

start_time = time.time()

while True:

    # wait for input via the buttons
    buttons = wii.state['buttons']

    # If Plus and Minus buttons pressed together
    if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
        pygame.display.quit()
        stopWiimoteConnection(wii)
        sys.exit();

    # IF "A" button is pressed start the photobooth action
    if(buttons & cwiid.BTN_A):
        start_photobooth_A(image_path)

    # check if wii connection is still running
    checkConnection(wii)

    # place images taken images on screen, change image every 5 seconds
    end_time = time.time()
    if((end_time-start_time) > 5):
        show_image_start_screen(image_path)
        start_time = time.time()
    
  
 
