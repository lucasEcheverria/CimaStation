#!/usr/bin/env python3
# test_humidity.py
# Script simple para probar el sensor de humedad del BME280

import time
import Adafruit_BME280
import Adafruit_GPIO.I2C as I2C

# Inicializar el sensor BME280
# Especificamos el bus I2C manualmente (busnum=1 para Raspberry Pi)
# Cambia a address=0x77 si tu sensor usa esa dirección
try:
    bme = Adafruit_BME280.BME280(address=0x76, busnum=1)
    print("✓ Sensor BME280 inicializado correctamente")
    print("✓ Bus I2C: 1")
    print("✓ Dirección I2C: 0x76")
    print("-" * 50)
except Exception as e:
    print(f"❌ Error al inicializar el sensor: {e}")
    print("\n🔧 Soluciones:")
    print("1. Verifica las conexiones físicas del sensor")
    print("2. Habilita I2C: sudo raspi-config → Interface → I2C")
    print("3. Verifica dispositivos I2C: sudo i2cdetect -y 1")
    print("4. Si ves 0x77 en lugar de 0x76, cambia 'address=0x77'")
    exit(1)

# Función para leer solo la humedad
def leer_humedad():
    try:
        humedad = bme.read_humidity()
        return round(humedad, 2)
    except Exception as e:
        print(f"Error al leer humedad: {e}")
        return None

# Loop principal
if __name__ == '__main__':
    print("\n📊 Iniciando lectura de humedad...")
    print("Presiona Ctrl+C para detener\n")
    
    try:
        while True:
            humedad = leer_humedad()
            
            if humedad is not None:
                # Mostrar resultado con indicador visual
                print(f"💧 Humedad: {humedad}% ", end="")
                
                # Barra visual simple
                barras = int(humedad / 5)  # 20 barras para 100%
                print("█" * barras)
                
                # Interpretación del nivel de humedad
                if humedad < 30:
                    print("   → Ambiente muy seco")
                elif humedad < 40:
                    print("   → Ambiente seco")
                elif humedad <= 60:
                    print("   → Humedad confortable")
                elif humedad <= 70:
                    print("   → Ambiente húmedo")
                else:
                    print("   → Muy húmedo")
                
                print()
            
            time.sleep(2)  # Lectura cada 2 segundos
            
    except KeyboardInterrupt:
        print("\n\n✓ Prueba finalizada")
        print("Sensor desconectado correctamente")
