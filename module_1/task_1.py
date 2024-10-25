import time
import math
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

'''
Task 1.1
Implement a program that uses the two development board buttons to control a “UFO”. The UFO is
shown at the bottom of the screen with characters “<=>”. SW0 and SW2 are used to move the UFO left
and right. The program must stop the UFO at the edges of the screen so that it is completely visible.
When UFO is at left edge it must only be possible to move the UFO right and vice versa.

The font size is 8x8 pixels.
- SW0 pressed:
   UFO moves right
- SW2 pressed:
   UFO moves left
'''
class UFO:    
    def __init__(self, characters, font_width, font_height):
        self.characters = characters
        self.font_width = font_width
        self.font_height = font_height
        self.lenght = len(characters)
        self.coordinates = [0, 0]

class Game:
    def __init__(self, ufo, btn_right, btn_left, scl, sda, screen_size):
        self.ufo = ufo
        self.btn_right = Pin(btn_right, Pin.IN, Pin.PULL_UP)
        self.btn_left = Pin(btn_left, Pin.IN, Pin.PULL_UP)
        self.screen_size = screen_size
        self.oled = SSD1306_I2C(screen_size[0], screen_size[1],
                                I2C(1, scl=Pin(scl), sda=Pin(sda), freq=400_000))
        
        self.ufo.coordinates = self.initial_ufo_coordinates()
        self.update_ufo_location()
        
    def initial_ufo_coordinates(self):
        x_coordinate =  math.floor((self.screen_size[0] - self.ufo.lenght * self.ufo.font_width) / 2)
        y_coordinate = 	self.screen_size[1] - self.ufo.font_height
        
        return [x_coordinate, y_coordinate]
    
    def update_ufo_location(self):
        self.oled.fill(0)
        self.oled.text(self.ufo.characters, self.ufo.coordinates[0], self.ufo.coordinates[1], 1)
        self.oled.show()
        
    def move_right(self):
        new_x_coordinate = self.ufo.coordinates[0] + 1
        if not (new_x_coordinate + self.ufo.lenght * self.ufo.font_width) > self.screen_size[0]:
            self.ufo.coordinates[0] = new_x_coordinate
            
        self.update_ufo_location()
    
    def move_left(self):
        new_x_coordinate = self.ufo.coordinates[0] - 1
        if not new_x_coordinate < 0:
            self.ufo.coordinates[0] = new_x_coordinate
        
        self.update_ufo_location()
        
    
def main():
    ufo = UFO("<=>", 8, 8)
    game = Game(ufo, 9, 7, 15, 14, (128, 64))
    
    while True:
        if not game.btn_right.value():
            game.move_right()
        if not game.btn_left.value():
            game.move_left()

if __name__ == "__main__":
    main()