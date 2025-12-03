import bme680
import time

# Inicializar sensor en dirección 0x76
sensor = bme680.BME680(0x76)

# Configuración básica (opcional pero mejora precisión)
sensor.set_temperature_oversample(bme680.OS_8X)

print("🌡️  Monitor de Temperatura")
print("Presiona Ctrl+C para detener\n")

try:
    while True:
        # Obtener datos del sensor
        if sensor.get_sensor_data():
            temp = sensor.data.temperature
            print(f"Temperatura: {temp:.2f} °C")
        
        # Esperar 3 segundos
        time.sleep(3)
        
except KeyboardInterrupt:
    print("\n\n✅ Monitor detenido")