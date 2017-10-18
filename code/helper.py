##################
# helper scripts #
##################
import os
import pygame.event

# shut down the script without closing the python shell or kill dialog
def script_shutdown():
    os._exit(1)


# comparison if value is outside range -> wrap around
def is_outside_range(a,b=0,c=0):
    if a < b:
        return c
    if a > c:
        return b
    return a


# run by itself
if __name__ == '__main__':
    lower_threshold = 0
    upper_threshold = 2

    print is_outside_range(0,1,3)
    print is_outside_range(1,1,3)
    print is_outside_range(2,1,3)
    print is_outside_range(3,1,3)
    print is_outside_range(4,1,3)

    print get_key()
