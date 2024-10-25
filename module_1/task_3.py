import math
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

'''
Implement a program that uses the three development board buttons to control line drawing. When the
program starts, it starts to draw pixels from the left side of the screen halfway between top and bottom
of the screen and constantly moves towards the right edge of the screen. When the drawing reaches the
right edge of the screen, the drawing is wrapped back to the left side. Buttons SW0 and SW2 are used to
move the pixels towards the top or bottom of the screen, so that by pressing buttons you can draw lines
at different heights. Pressing SW1 clears the screen and continues drawing from middle left side.
'''

class Screen:
    def __init__(self, btn_reset, btn_up, btn_down, scl, sda,
                 screen_size, font_width = 8, font_height = 8):
        self.btn_reset = Pin(btn_reset, Pin.IN, Pin.PULL_UP)
        self.btn_up = Pin(btn_up, Pin.IN, Pin.PULL_UP)
        self.btn_down = Pin(btn_down, Pin.IN, Pin.PULL_UP)
        self.screen_size = screen_size
        self.oled = SSD1306_I2C(screen_size[0], screen_size[1],
                                I2C(1, scl=Pin(scl), sda=Pin(sda), freq=400_000))
        self.font_width = font_width
        self.font_height = font_height
        self.next_position = [0, 0]
        
    def update(self):
        self.oled.show()
     
    def restart(self):
        middle_y_coordinate = math.floor(self.screen_size[1] / 2) # Calculate middle Y coordinate 
        self.oled.fill(0)
        
        self.next_position = [0, middle_y_coordinate]
        
    def move(self):
        if self.next_position[0] >= self.screen_size[0]:
            self.next_position[0] = 0
            
        self.oled.pixel(self.next_position[0], self.next_position[1], 1)

    def next_position_up(self):
        if self.next_position[1] - 1 >= 0:
            self.next_position[1] -= 1
    
    def next_position_down(self):
        if self.next_position[1] + 1 < self.screen_size[1]:
            self.next_position[1] += 1

def main():
    screen = Screen(
        btn_reset = 8,
        btn_up = 7,
        btn_down = 9,
        scl = 15,
        sda = 14,
        screen_size = (128, 64))
    
    screen.restart()
    
    while True:
        screen.move()
        screen.update()
        
        screen.next_position[0] += 1
        
        if not screen.btn_reset.value():
            screen.restart()
            
        elif not screen.btn_up.value():
            screen.next_position_up()
            
        elif not screen.btn_down.value():
            screen.next_position_down()        


if __name__ == "__main__":
    main()
    
