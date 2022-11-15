# -*- coding: utf-8 -*- >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""
author: Auri - The AI Training Image Evaluation Simplifier Tool. //////////////
"""
import pygame # for GUI ///////////////////////////////////////////////////////
from pygame.locals import * #//////////////////////////////////////////////////
from pybooru import Danbooru #/////////////////////////////////////////////////
import wget # image downloader module//////////////////////////////////////////
import os # manipulating files ////////////////////////////////////////////////
import time # time (sleep...) /////////////////////////////////////////////////

#Initialize 
client = Danbooru('danbooru') #obj for .self needs
input_tag = input("Input desired tag:") 
white = (255,255,255)
DEFAULT_IMAGE_SIZE = (1280,720)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# define main function
def main():
    # initialize the pygame module
    pygame.init()
    print('Initializing...')
    # load and set the logo
    logo = pygame.image.load("logo32x32.png"); pygame.display.set_icon(logo)
    pygame.display.set_caption("AI Trainer Image Evaluator")
    screen = pygame.display.set_mode((1280,720))
    
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
        print('Error: While downloading file;Restarting main()')
        main()
        
    #load image
    loaded_image = pygame.image.load(downloaded_image)
    screen.fill(white)
    resized_image = pygame.transform.scale(loaded_image,DEFAULT_IMAGE_SIZE)
    screen.blit(resized_image,(0,0))
    pygame.display.update()
    print('Displayed Image.')
                
    # main loop
    while running:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            try:
                os.remove(downloaded_image)
                print('Tag not good. Restarting search...')
                time.sleep(0.1)
                main()
            except:
                print('Error: Deleting sequence failed;Retrying...')
                try:
                    os.remove(downloaded_image)
                    print('Tag not good. Restarting search...')
                    time.sleep(0.1)
                    main()
                except:
                    print('Error: Cannot retry; Restarting main()')
        else:
            if keys[pygame.K_RIGHT]:
                try:
                    finalext = open(str(downloaded_image[:-4])+".txt","wt")
                    a = str(post[0]["tag_string_general"])
                    b = str(post[0]["tag_string_character"])
                    c = str(post[0]["tag_string_artist"])
                    d = str(post[0]["tag_string_meta"])
                    e = (a+' '+b+' '+c+' '+d+' ').replace(' ',',')
                    e = e.replace('_',' ')
                    finalext.write(e); finalext.close()
                    print('Saved Image and Tags!')
                    time.sleep(0.1)
                    main()
                except:
                    print('Error: Failed to save tags;Retrying...')
                    try:
                        finalext = open(str(downloaded_image[:-4])+".txt","wt")
                        a = str(post[0]["tag_string_general"])
                        b = str(post[0]["tag_string_character"])
                        c = str(post[0]["tag_string_artist"])
                        d = str(post[0]["tag_string_meta"])
                        e = (a+' '+b+' '+c+' '+d+' ').replace(' ', ',')
                        e = e.replace('_',' ')
                        finalext.write(e); finalext.close()
                        print('Saved Image and Tags!')
                        time.sleep(0.1)
                        main()
                    except:
                        print('Error: Cannot save tags; Restarting main()')
                        main()
        for event in pygame.event.get():
            #
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                pygame.display.quit
                pygame.quit()
                exit()
     
if __name__=="__main__":
#call the main function
    main()