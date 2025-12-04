import time
import board
import adafruit_dht

#!/usr/bin/env python3

# Inicializar el sensor DHT22
dhtDevice = adafruit_dht.DHT22(board.D4)

while True:
    try:
        humidity = dhtDevice.humidity
        if humidity is not None:
            print(f"Humedad: {humidity:.1f}%")
        else:
            print("Error al leer la humedad")
    except RuntimeError as error:
        print(f"Error de lectura: {error.args[0]}")
    except Exception as error:
        dhtDevice.exit()
        raise error
    
    time.sleep(5)