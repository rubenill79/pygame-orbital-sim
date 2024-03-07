import pygame

def load_img(path):
    img = pygame.image.load('resources/images/' + path + '.png').convert()
    img.set_colorkey((0,0,0))
    return img

def swap_color(img, old_c, new_c):
    # Create a copy of the image
    surf = img.copy()
    
    # Set the color key to old_c
    surf.set_colorkey(old_c)
    
    # Loop through each pixel in the image
    for x in range(surf.get_width()):
        for y in range(surf.get_height()):
            # If the pixel matches old_c, change it to new_c
            if surf.get_at((x, y)) == old_c:
                surf.set_at((x, y), new_c)
    
    # Set the color key to None
    surf.set_colorkey(None)
    
    return surf