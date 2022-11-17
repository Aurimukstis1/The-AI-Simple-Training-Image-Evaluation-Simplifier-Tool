# -*- coding: utf-8 -*- >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""
author: Auri - The AI Training Image Evaluation Simplifier Tool. //////////////
"""
import pygame # for GUI ///////////////////////////////////////////////////////
from pybooru import Danbooru #/////////////////////////////////////////////////
import wget # image downloader module//////////////////////////////////////////
import os # manipulating files ////////////////////////////////////////////////
import time # time (sleep...) /////////////////////////////////////////////////
import keyboard #//////////////////////////////////////////////////////////////

#Initialize 
client = Danbooru('danbooru') #obj for .self needs
input_tag = input("Input desired tag:")
white = (255,255,255)
DEFAULT_IMAGE_SIZE = (1280,720)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# define main function
def main():
    with open("tempcounter.json", "r") as file:
        count = int(file.read())

    with open("tempcounter.json", "wt") as file:
        file.write(str(count + 1))
    
    # initialize the pygame module
    pygame.init()
    print('Initializing...')
    # load and set the logo
    logo = pygame.image.load("logo32x32.png"); pygame.display.set_icon(logo)
    pygame.display.set_caption("1.1 - TASTIEST")
    screen = pygame.display.set_mode((DEFAULT_IMAGE_SIZE))
    
    # define a variable to control the main loop
    running = True
    
    #find random post
    post = client.post_list(limit=1,page=1,tags=input_tag,random=True)
    print('Post found...')
    
    #save image
    try:
        #download the image
        downloaded_image = wget.download(post[0]["file_url"])
        print('Image Successfully Downloaded: ', downloaded_image)
    except:
        #epic fail
        print('Error: While downloading file;Restarting main()')
        main()
        
    # load image
    loaded_image = pygame.image.load(downloaded_image)

    # Resize the image to fit nicely
    size_x = loaded_image.get_rect()[2]
    size_y = loaded_image.get_rect()[3]

    if size_x > size_y:
        rescale = DEFAULT_IMAGE_SIZE[0]/size_x
    else:
        rescale = DEFAULT_IMAGE_SIZE[1]/size_y

    screen.fill(white)
    resized_image = pygame.transform.scale(
        loaded_image, (rescale*size_x, rescale*size_y))
    #resized_image = pygame.transform.scale(loaded_image, DEFAULT_IMAGE_SIZE)
    screen.blit(resized_image, (0, 0))
    pygame.display.update()
    print('Displayed Image.')
                
    # main loop
    while running:

        if keyboard.is_pressed('left'):
            os.remove(downloaded_image)
            print('Tag not good;Restarting main()')
            time.sleep(0.1)
            main()
            
        if keyboard.is_pressed('right'):
            try:
                #first rename the image to a singular name.
                old_name = str(downloaded_image)
                new_name = 'TrainingImage_' + str(count)
                os.rename(old_name, new_name + ".jpg")
                #then save the tags
                finalext = open(new_name+".txt","wt")
                a = str(post[0]["tag_string_general"])
                b = str(post[0]["tag_string_character"])
                c = str(post[0]["tag_string_artist"])
                d = str(post[0]["tag_string_meta"])
                e = (a+' '+b+' '+c+' '+d+' ').replace(' ',',')
                e = e.replace('_',' ')
                finalext.write(e)
                finalext.close()
                print('Saved Image and Tags!')
                time.sleep(0.1)
                main()
            except:
                print('Error: Failed to save tags')
                print(str(count))

        for event in pygame.event.get():
            #
            if event.type == pygame.QUIT:
                #clear out the temporary image file to not clot folder
                os.remove(downloaded_image)
                #exiting the loop and exiting the window
                running = False
                pygame.display.quit
                pygame.quit()
                break;
     
if __name__=="__main__":
#call the main function
    main()