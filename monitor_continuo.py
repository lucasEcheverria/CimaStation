#!/usr/bin/env python3
"""
Monitor continuo de sensores
Muestra información cada 5 segundos
"""
import time
from sensores_simples import leer_bmp280, leer_sht31, leer_tcs34725, inicializar_tcs34725

# Inicializar TCS34725 una sola vez
print("Inicializando sensores...")
inicializar_tcs34725()
print("✓ Listo\n")

print("="*60)
print("Monitor de Sensores - CimaStation")
print("="*60)
print("Leyendo cada 5 segundos (Ctrl+C para detener)\n")

try:
    while True:
        # Leer BMP280
        bmp_datos = leer_bmp280()
        
        # Leer SHT31
        sht_datos = leer_sht31()
        
        # Leer TCS34725
        tcs_datos = leer_tcs34725()
        
        # Mostrar datos
        print(f"[{time.strftime('%H:%M:%S')}]")
        
        if bmp_datos:
            print(f"  Temperatura: {bmp_datos['temperatura']}°C")
            print(f"  Presión:     {bmp_datos['presion']} hPa")
        
        if sht_datos:
            print(f"  Humedad:     {sht_datos['humedad']}%")
        
        if tcs_datos:
            print(f"  Luz:         {tcs_datos['lux']} lux")
        
        print("-"*60)
        
        # Esperar 5 segundos
        time.sleep(5)
        
except KeyboardInterrupt:
    print("\n\n✓ Monitor detenido")
