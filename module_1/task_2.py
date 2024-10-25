import time
import math
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

'''
Task 1.2
Implement a program that reads user input from the keyboard in an infinite loop. The input is typed in
Thonny Shell window while the program is running. The user input is drawn to the OLED screen starting
from the top of the screen. Each input is drawn below the previous one. When the screen is full the
display is scrolled up by one line and then new text is drawn at the bottom of the screen.
'''

def main():
    screen_size = (128, 64)
    font_width = 8
    font_height = 8
    max_rows = math.floor(screen_size[1] / font_height)
    
    i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400_000)
    oled = SSD1306_I2C(screen_size[0], screen_size[1], i2c)
    oled.fill(0)
    
    y_position = 0 # Track the next line Y position
    
    while True:
        new_text = input("Give input: ")
        
        if y_position >= screen_size[1]:
            oled.scroll(0, -font_height)
            used_y_position = y_position - font_height
            
            oled.fill_rect(0, used_y_position, screen_size[0], screen_size[1], 0)
            oled.text(new_text, 0, used_y_position, 1)
        else:
            oled.text(new_text, 0, y_position, 1)
            y_position += font_height
            
        oled.show()
        
        
if __name__ == "__main__":
    main()