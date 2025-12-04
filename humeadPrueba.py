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
