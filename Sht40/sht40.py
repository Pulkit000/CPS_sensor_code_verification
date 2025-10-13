import log
from machine import I2C
import utime
from machine import Pin


if __name__ == '__main__':
          
    i2c_obj = I2C(I2C.I2C0, I2C.STANDARD_MODE) # Setting up i2c communication

    I2C_sht40_ADDR = 0x44 # I2C device address

    command = 0xFD     #command for temperature and humidity measurement

    data = bytearray([command]) # register address for Temperature and humidity measurement
    # print(data)
    #write_function 
    i2c_obj.write(I2C_sht40_ADDR, b'' , 0, data , 1) # write command for Temperature and humidity measurent from specific register
    utime.sleep(0.2)
    #read_function  
    buf =  bytearray(6) # variable of type bytearray to hold raw Temperature and humidity values
    # print(buf)
    i2c_obj.read(I2C_sht40_ADDR, b'', 0, buf , 6 , 0) # read command to extract temperture and humidity measurement from specific registers
    my_data = buf
    # for i in range(5):
    #     print(my_data)
    temperature_raw = (my_data[0] << 8) | my_data[1] # bit shifting on raw temperature data
    hum_raw = (my_data[3] << 8) | my_data[4]    # bit shifting on raw humidity data
    # print("Raw sensor data:", temperature_raw)
    # print("Raw sensor data:", hum_raw)
    temperature = -45.0 + 175.0 * temperature_raw / 65535.0 # calibration for temperature
    hum = -6.0 + 125.0 * hum_raw / 65535.0 # calibration for humidity
    print("Current temp", temperature) # printing callibrated temperature data
    print("Current Hum", hum)          # printing callibrated humidity data