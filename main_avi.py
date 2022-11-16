# -*- coding: utf-8 -*- >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""
author: Auri - The AI Training Image Evaluation Simplifier Tool. //////////////
"""
import pygame  # for GUI //////////////////////////////////////////////////////
from pybooru import Danbooru  # ///////////////////////////////////////////////
import wget  # image downloader module/////////////////////////////////////////
import os  # manipulating files ///////////////////////////////////////////////
import time# time (sleep...) //////////////////////////////////////////////////

# Initialize
client = Danbooru('danbooru')  # obj for .self needs
white = (255, 255, 255) # w h i t e
DEFAULT_IMAGE_SIZE = (900, 900)
posts = []

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# define main function
def main():
    # initialize the pygame module
    pygame.init()
    print('Initializing...')
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("AI Trainer Image Evaluator")
    screen = pygame.display.set_mode(DEFAULT_IMAGE_SIZE)

    # define a variable to control the main loop
    running = True

    global posts
    if len(posts) == 0:
        page_num = input('Input desired page number:')
        posts = client.post_list(
            limit=42, page=page_num, tags='tucked_penis', random=False)
        print('Posts found...')

    post = posts[0]
    posts.pop(0)
    print('Continuing with posts...')

    try:
        # download the image
        downloaded_image = wget.download(post["file_url"])
        orig_filename = wget.detect_filename(url=post["file_url"])
        new_filename = f"{round(time.time())}-tucked penis{orig_filename[-4:]}"
        print('Image Successfully Downloaded: ', downloaded_image)
    except:
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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            os.remove(downloaded_image)
            print('Tag not good. Restarting search...')
            main()
        elif keys[pygame.K_RIGHT]:
            os.rename(orig_filename, new_filename)
            finalext = open(new_filename[:-4]+".txt", "wt")
            a = str(post["tag_string_general"])
            b = str(post["tag_string_character"])
            c = str(post["tag_string_artist"])
            d = str(post["tag_string_meta"])
            e = (a+' '+b+' '+c+' '+d+' ').replace(' ',',')
            e = e.replace('_',' ')
            finalext.write(e)
            finalext.close()
            print('Saved Image and Tags!')
            main()
        for event in pygame.event.get():
            #
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
                pygame.quit()
                break;


if __name__ == "__main__":
    # call the main function
    main()