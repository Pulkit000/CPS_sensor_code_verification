from machine import I2C
import utime
from usr.LCDPublic import ascii_8x16_dict

def clear_screen(i2c_obj, oled_address):
    # Clear the entire display (128x64, 8 pages)
    for page in range(8):
        i2c_obj.write(oled_address, b'\x00', 1, bytearray([0xB0 + page, 0x00, 0x10]), 3)  # Set page and column 0
        i2c_obj.write(oled_address, b'\x40', 1, bytearray([0x00] * 128), 128)  # Write 128 zeros
        utime.sleep_ms(20)  # Increased delay for stability

def draw_char(i2c_obj, oled_address, x, page, char):
    font = ascii_8x16_dict.get(char)
    if not font:
        return

    # Set column and page position (simplified for horizontal mode)
    i2c_obj.write(oled_address, b'\x00', 1, bytearray([0xB0 + page, x & 0x0F, 0x10 | (x >> 4)]), 3)
    utime.sleep_ms(20)  # Increased delay

    # Send character pixel data (8x16 font, 16 bytes)
    i2c_obj.write(oled_address, b'\x40', 1, bytearray(font), len(font))
    utime.sleep_ms(20)  # Increased delay

def display_text(i2c_obj, oled_address, text, x=0, page=0):
    for ch in text:
        if x < 128 and page < 8:  # Ensure within screen boundaries
            draw_char(i2c_obj, oled_address, x, page, ch)
            x += 8  # Move right for next character
            if x >= 128:
                x = 0
                page += 2  # Move to next page pair (8x16 font takes 2 pages)
                if page >= 8:
                    break

if __name__ == '__main__':
    i2c = I2C(I2C.I2C0, I2C.STANDARD_MODE)
    oled_address = 0x3c  # Double-check with your OLED (0x3C or 0x3D)

    # OLED initialization for SSD1306
    init_cmds = [
    bytearray([0x00, 0xAE]),        # Display OFF
    bytearray([0x00, 0xA8, 0x3F]),  # Set multiplex ratio (64 lines)
    bytearray([0x00, 0x8D, 0x14]),  # Enable charge pump
    bytearray([0x00, 0xDA, 0x12]),  # Set COM pins
    bytearray([0x00, 0xAF])         # Display ON
]

    for cmd in init_cmds:
        i2c.write(oled_address, b'', 0, cmd, len(cmd))
        utime.sleep_ms(20)  # Increased delay for stability

    # Clear screen before displaying text
    clear_screen(i2c, oled_address)

    # Display text at x=0, page=0
    display_text(i2c, oled_address, "T", 0, 0)  # Uppercase for clarity