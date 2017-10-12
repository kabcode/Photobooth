#!/usr/bin/env python
# created by kabcode@gmail.com
# information and further details can be found under www.kabelitzens.de

# this is a skript for a interactive photobooth

# import lib
import time
import picamera
import cwiid
import sys
import os
import pygame
import math
import random
import shutil

# import own files
import wifi_detection

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
font_path = parent_path + '/font/'
image_language = 'en'
pygame.surface = None
advanced_setup = 1

# advanced setup variables
wlan_connection = None

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
image_german = 'de_flag.png'
image_english = 'en_flag.png'
image_selected = 'image_selected_language.png'
image_plusbutton = 'image_left_right.png'

# font
font_board = 'erasdust.ttf'

########################
###  advaned setup   ###
########################
# try to establish an wifi detection
def run_advanced_setup():
    pygame.init()
    screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
    cells = wifi_detection.searchWifi()
    show_wifi_networks(cells)
    i=0
    for cell in cells:
        print '['+str(i)+']:' + cell.ssid
        i=i+1

    # get number from user and try to connect to selected wifi
    user_input = raw_input("Please type password:")
    print 'Try to connect to: '+ cells[int(user_input)].ssid
    print wifi_detection.connectToWifi(cells[int(user_input)].ssid)


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
    img = loadImage(image_error,1)
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
    img_scaled = scaleImage(img,1/3.0)
    screen = pygame.display.get_surface()
    screen.blit(img_scaled, (400,500))
    pygame.display.flip()

# load image function for choosen language
def loadImage(image_name, language_flag):
    if(language_flag): # use image with choosen language
        image_full_name = image_path + image_language + image_name
    else:
        image_full_name = image_path + image_name
    image = pygame.image.load(image_full_name)
    return image

# display options for language (currently germand and english)
def display_language_options():
    flag_german = loadImage(image_german,0)
    flag_english = loadImage(image_english,0)
    selected = loadImage(image_selected,0)
    wiiplus = loadImage(image_plusbutton,0)
    scaledFlag_german = scaleTo(flag_german, 100, 0)
    scaledFlag_english = scaleTo(flag_english, 100, 0)
    scaledSelected = scaleTo(selected, 110, 0)
    scaledWiiplus = scaleTo(wiiplus, 0, 62)
    screen = pygame.display.get_surface()
    if(image_language == 'de'):
        screen.blit(scaledSelected,(45,745))
    else:
        screen.blit(scaledSelected,(227,745))
    screen.blit(scaledFlag_german,(50,750))
    screen.blit(scaledWiiplus,(160,750))
    screen.blit(scaledFlag_english,(232,750))
    pygame.display.flip()

# show wifi options on screen
def show_wifi_networks(cells):
    numberOfWifi = len(cells)
    
    heigth = pygame.display.Info().current_h
    font_padding = 50
    font_size = (heigth-numberOfWifi*3)/(numberOfWifi + 2)
    
    font = pygame.font.Font(font_path + font_board, font_size)
    print 'Loaded font:' + font_path + font_board
    
    # update screen with all available networks
    screen = pygame.display.get_surface()
    background = loadImage(image_blank,0)
    screen.blit(background,(0,0))
    fg = 255,255,255

    surf = font.render("Choose a wifi:", True, fg)
    screen.blit(surf,(font_padding/5,0))
    for i in range(0,numberOfWifi):
        text = "["+str(i)+u"]:    " +cells[i].ssid
        if i==1:
            text = "["+str(i)+u"]:     " +cells[i].ssid
        surf = font.render(text, True, fg)
        screen.blit(surf,(font_padding,(i+1)*font_size))
    surf = font.render("Cancel", True, fg)
    screen.blit(surf,(font_padding/5,(numberOfWifi+1)*font_size))
    pygame.display.flip()
    time.sleep(2)
    

# helper funtion for scaling images (scaling factor needs to be float value)
def scaleImage(image, scale):
    imgSize = image.get_size()
    width  = int(math.floor(imgSize[0]*scale))
    heigth = int(math.floor(imgSize[1]*scale))
    image_scaled = pygame.transform.scale(image,(width,heigth))
    return image_scaled

# helper function for scaling to a certain width or heigth
# the wanted width or heigth need to be non zero otherwise the smaller scale is choosen
def scaleTo(image, width = 0, heigth = 0):
    imgSize = image.get_size()
    scale = 1
    if(width != 0):
        scale = float(width)/imgSize[0]
    if(heigth != 0):
        scale = float(heigth)/imgSize[1]
    if(width != 0 & heigth != 0):
        scaleWidth = float(width)/imgSize[0]
        scaleHeigth = float(heigth)/imgSize[1]
        scale = scaleWidth if scaleWidth < scaleHeigth else scaleHeigth
    print("Scale: " + str(scale))
    image_scaled = scaleImage(image,scale)
    return image_scaled

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
    display_language_options()


#####################
### main programe ###
#####################
# if advanced setup variable is set run the setup first
if(advanced_setup):
    run_advanced_setup()
exit()
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
display_language_options()

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
        display_language_options()
    if(buttons - cwiid.BTN_RIGHT == 0):
        image_language = 'en'
        show_image(image_instruction,1)
        display_language_options()

    # check if wii connection is still running
    checkConnection(wii)

    # place images taken images on screen, change image every 5 seconds
    end_time = time.time()
    if((end_time-start_time) > 5):
        show_image_start_screen(storage_path)
        start_time = time.time()
    
  
 
