import pygame
from os import walk

def blit_center(display, surf, position):
    x = int((surf.get_width)/2)
    y = int((surf.get_height)/2)
    display.blit(surf, (position[0] - x, position[1] - y))

def read_animation_file(path):
    action_durations = {}
    f = open(path + 'animation', 'r')
    data = f.read()
    f.close()
    for i in data.split('\n'):
        sections = i.split(' ')
        type = sections[0]
        action = sections[1]
        timings = sections[2].split(';')
        int_timings = []
        for timing in timings:
            int_timings.append(int(timing))
        action_durations[action] = int_timings
    return [type, action_durations]


def load_animations(path):
    anim_info = read_animation_file(path)
    full_path = path + anim_info[0]
    duration = anim_info[1]
    animation_database = {}
    animation_frame_data = {}
    for _, action, ___ in walk(full_path):
        if action != []:
            anim_name = action

    for animation_name in anim_name:
        anim_data = []
        n = 0
        for frames in duration[animation_name]:
            animation_ID = animation_name + '_' + str(n)
            animation_path = full_path + '/' + animation_name + '/' + animation_ID + '.png'
            animation = pygame.image.load(animation_path).convert_alpha()
            animation.set_colorkey((255, 255, 255))
            animation_database[animation_ID] = animation.copy()
            for frame in range(frames):
                anim_data.append(animation_ID)
            n += 1
            animation_frame_data[animation_name] = anim_data
    return [animation_frame_data, animation_database]



