#!/usr/bin/env python3

import time
import board
import adafruit_dht

# Inicializar el sensor DHT22
dhtDevice = adafruit_dht.DHT22(board.D4)

print("Leyendo datos del sensor DHT22...")
print("Presiona Ctrl+C para salir\n")

try:
    while True:
        try:
            # Leer temperatura y humedad
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            
            if temperature is not None and humidity is not None:
                print(f"Temperatura: {temperature:.1f}°C")
                print(f"Humedad: {humidity:.1f}%")
                print("-" * 30)
            else:
                print("Error: No se pudo leer del sensor")
                
        except RuntimeError as error:
            # Errores comunes de timing del DHT22
            print(f"Error de lectura: {error.args[0]}")
            
        except Exception as error:
            dhtDevice.exit()
            raise error
        
        time.sleep(5)
        
except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario")
    dhtDevice.exit()