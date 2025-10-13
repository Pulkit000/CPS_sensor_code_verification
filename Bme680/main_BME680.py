from usr.BME680 import BME
# from machine import I2C


# i2c_dev = I2C(I2C.I2C0, I2C.FAST_MODE)
my_sensor=BME()

Temperature,Pressure=my_sensor.read_Temperature_and_Pressure()
Humidity=my_sensor.read_humidity()

# Initialize I2C

print("Temperature",Temperature,"C")
print("Presure",Pressure/100,"hpa")
print("Humidity",Humidity ,"%")

