import utime
from machine import Pin, I2C
from usr.LCDPublic import ascii_8x16_dict

# def draw_char_8x16(self, x, y, char, ):
#     # Draw a single character at (x, y) using 8x16 font, 1-bit per pixel.
#     font = usr.LCDPublic.ascii_8x16_dict.get(char)
#     if not font or len(font) != 16:
#          return


class ssd1306:
    def oled_ssd1306():
    # --- Configuration ---
        i2c_obj = I2C(I2C.I2C0, I2C.STANDARD_MODE)
        oled_slave_address = 0x3C  # Standard I2C address for SSD1306

        # --- Command Definitions (0x00 prepended to all) ---
        set_contrast = bytearray([0x00, 0x81, 0xCF])
        set_normal_mode = bytearray([0x00, 0xA6])
        enable_charge_pump = bytearray([0x00, 0x8D, 0x14])
        set_display_mode = bytearray([0x00, 0xAF])  # Display ON
        set_multiplexer_ratio = bytearray([0x00, 0xA8, 0x3F])
        set_dislay_clock = bytearray([0x00, 0xD5, 0x80])
        Set_COM_Pins_Config = bytearray([0x00, 0xDA, 0x12])

        # --- NEW: Addressing Commands ---
        set_memory_addressing = bytearray([0x00, 0x20, 0x00, 0x02])  # Page Addressing Mode
        set_lower_column = bytearray([0x00, 0x00])  # This command picks the starting left-right spot  for drawing on the screen, helping set the "x" position for your letters.
        set_higher_column = bytearray([0x00, 0x10])  # This command sets the second part of the left-right (x-axis) starting column  for drawing on the screen, 
        #working with the lower column command to pinpoint the exact location
        set_start_line = bytearray([0x00, 0x40])  # Start line 0

        # --- Initialization Execution ---
        # --- Setting Mandatory Configuration Commands ---
        i2c_obj.write(oled_slave_address, b'', 0, set_dislay_clock, 3)
        utime.sleep_ms(10)  # Small delay for oscillator to stabilize
        i2c_obj.write(oled_slave_address, b'', 0, set_multiplexer_ratio, 3)
        i2c_obj.write(oled_slave_address, b'', 0, Set_COM_Pins_Config, 3)
        i2c_obj.write(oled_slave_address, b'', 0, enable_charge_pump, 3)  # Power On Booster
        utime.sleep_ms(10)  # Delay after charge pump enable

        # --- Addressing and Display Setup ---
        i2c_obj.write(oled_slave_address, b'', 0, set_memory_addressing, 4)  # Set page addressing mode
        i2c_obj.write(oled_slave_address, b'', 0, set_lower_column, 2)           # Set column start to 0
        i2c_obj.write(oled_slave_address, b'', 0, set_higher_column, 2)          # Set column end
        i2c_obj.write(oled_slave_address, b'', 0, set_start_line, 2)        # Set start row to 0

        # --- Setting Mode and Turning Display ON ---
        i2c_obj.write(oled_slave_address, b'', 0, set_contrast, 3)
        i2c_obj.write(oled_slave_address, b'', 0, set_normal_mode, 2)  # Normal mode
        i2c_obj.write(oled_slave_address, b'', 0, set_display_mode, 2)  # Display ON

        # --- Clear the Screen ---
        for page in range(8):  # 8 pages (0-7)
            set_page = bytearray([0x00, 0xB0 + page])  # Set page (0xB0 to 0xB7)
            i2c_obj.write(oled_slave_address, b'', 0, set_page, 2)
            i2c_obj.write(oled_slave_address, b'', 0, set_lower_column, 2)  # Column 0
            i2c_obj.write(oled_slave_address, b'', 0, set_higher_column, 2)
            clear_data = bytearray([0x40] + [0x00] * 128)  # 0x40 for data, 128 zeros
            i2c_obj.write(oled_slave_address, b'', 0, clear_data, 129)

        # --- Write "helo" on page 0, starting at column 0 ---
        set_page0 = bytearray([0x00, 0xB0])  # Page 0
        i2c_obj.write(oled_slave_address, b'', 0, set_page0, 2)
        i2c_obj.write(oled_slave_address, b'', 0, set_lower_column, 2)  # Column 0
        i2c_obj.write(oled_slave_address, b'', 0, set_higher_column, 2)

        # Simple 5x8 font for "helo" (5 bytes per letter, 1 byte space)
        # font_5x8 = {
        #     'h': [0x7F, 0x08, 0x08, 0x08, 0x70],  # h
        #     'e': [0x3E, 0x41, 0x55, 0x41, 0x22],  # e
        #     'l': [0x7F, 0x40, 0x40, 0x40, 0x40],  # l
        #     'o': [0x3E, 0x41, 0x41, 0x41, 0x3E]   # o
        # }

        # helo_data = []
        # for char in "helo":
        #     helo_data.extend(font_5x8[char])
        #     helo_data.append(0x00)  # Space between letters
        # write_data = bytearray([0x40] + helo_data)  # 0x40 for data mode
        # i2c_obj.write(oled_slave_address, b'', 0, write_data, len(write_data))

        # using in built library

        # msg = "Hello, Quec!"
        # x, y = 0, 0
        # for ch in msg:
        #     oled.draw_char_8x16(x, y, ch, color=1)
        #     x += 8
        #     if x + 8 > oled.width:
        #             x = 0
        #             y += 16
        #             if y + 16 > oled.height:
        #                 break

        print("Full I2C sequence sent. Blue screen should be gone, and 'helo' should appear.")






