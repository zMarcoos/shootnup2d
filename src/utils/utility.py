from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy

def load_texture(filename):
    image = Image.open(filename)
    transposed_image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image_data = transposed_image.convert("RGBA").tobytes()
    
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,  image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glBindTexture(GL_TEXTURE_2D, 0)

    return texture_id

def load_texture_with_sprites(filename, sprite_size):
    image = Image.open(filename).convert("RGBA")
    transposed_image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image_data = numpy.array(transposed_image, dtype=numpy.uint8)

    width, height = image.size
    sprite_count_x = width // sprite_size[0]
    sprite_count_y = height // sprite_size[1]

    textures = glGenTextures(sprite_count_x * sprite_count_y)
    texture_ids = []

    for index in range(sprite_count_y):
        for jndex in range(sprite_count_x):
            glBindTexture(GL_TEXTURE_2D, textures[index * sprite_count_x + jndex])
            sprite_data = image_data[index * sprite_size[1]:(index + 1) * sprite_size[1], jndex * sprite_size[0]:(jndex + 1) * sprite_size[0], :].copy()
            sprite_data = numpy.flip(sprite_data, axis=0)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, sprite_size[0], sprite_size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, sprite_data)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            texture_ids.append(textures[index * sprite_count_x + jndex])

    glBindTexture(GL_TEXTURE_2D, 0)
    return texture_ids
