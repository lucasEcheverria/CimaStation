# medir_humedad.py
# Lee solo la humedad del sensor BME280 y la muestra por pantalla

import time
import Adafruit_BME280

# Crear objeto del sensor (cambia address si tu BME usa 0x77)
bme = Adafruit_BME280.BME280(address=0x76)

while True:
    humedad = bme.read_humidity()   # %
    print(f"Humedad: {humedad:.2f}%")
    time.sleep(1)



'''Traceback (most recent call last):
  File "/home/pi/Desktop/ClimaStation/Pruebas/pruebaHumedd.py", line 8, in <module>
    bme = Adafruit_BME280.BME280(address=0x76)
  File "/home/pi/Desktop/ClimaStation/venv/lib/python3.13/site-packages/Adafruit_BME280/BME280.py", line 131, in __init__
    self._device = i2c.get_i2c_device(address, **kwargs)
                   ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "/home/pi/Desktop/ClimaStation/venv/lib/python3.13/site-packages/Adafruit_GPIO/I2C.py", line 63, in get_i2c_device
    busnum = get_default_bus()
  File "/home/pi/Desktop/ClimaStation/venv/lib/python3.13/site-packages/Adafruit_GPIO/I2C.py", line 55, in get_default_bus
    raise RuntimeError('Could not determine default I2C bus for platform.')
RuntimeError: Could not determine default I2C bus for platform.
'''
