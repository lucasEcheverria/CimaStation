"""
CimaStation - Monitor ambiental completo
Temperatura, Humedad y Presión cada 10 segundos

Sensores:
- BMP280 (0x76): Temperatura + Presión
- SHT31 (0x45): Temperatura + Humedad
"""
import smbus2
import time

# =====================================================
# CONFIGURACIÓN I2C
# =====================================================
bus = smbus2.SMBus(1)
BMP280_ADDR = 0x76
SHT31_ADDR = 0x45

# =====================================================
# SENSOR SHT31 (Temperatura + Humedad)
# =====================================================
class SHT31:
    def __init__(self, address=0x45):
        self.bus = bus
        self.address = address
        self.CMD_MEASURE_HIGH = [0x24, 0x00]
        
    def leer(self):
        """Retorna: (temperatura_celsius, humedad_porcentaje)"""
        # Enviar comando de medición
        self.bus.write_i2c_block_data(
            self.address,
            self.CMD_MEASURE_HIGH[0],
            [self.CMD_MEASURE_HIGH[1]]
        )
        
        # Esperar medición (alta precisión: ~15ms)
        time.sleep(0.02)
        
        # Leer 6 bytes directamente (sin especificar registro)
        datos = self.bus.read_i2c_block_data(self.address, 0, 6)
        
        # Verificar que tenemos datos válidos
        if len(datos) != 6:
            raise RuntimeError(f"Lectura incompleta: {len(datos)} bytes")
        
        # Extraer valores raw (16 bits cada uno)
        temp_raw = (datos[0] << 8) | datos[1]
        hum_raw = (datos[3] << 8) | datos[4]
        
        # Convertir según datasheet Sensirion
        temperatura = -45 + (175 * temp_raw / 65535.0)
        humedad = 100 * hum_raw / 65535.0
        
        return temperatura, humedad

# =====================================================
# SENSOR BMP280 (Presión + Temperatura)
# =====================================================
class BMP280:
    def __init__(self, address=0x76):
        self.bus = bus
        self.address = address
        
        # Leer parámetros de calibración al inicializar
        self.cal = self._leer_calibracion()
        
        # Configurar modo de medición
        # Control register: osrs_t=1, osrs_p=1, mode=normal (0x27)
        self.bus.write_byte_data(self.address, 0xF4, 0x27)
        
    def _leer_calibracion(self):
        """Lee los 24 bytes de calibración del BMP280"""
        cal = self.bus.read_i2c_block_data(self.address, 0x88, 24)
        
        # Extraer parámetros de temperatura (dig_T1, T2, T3)
        dig_T1 = cal[0] | (cal[1] << 8)
        dig_T2 = self._to_signed_16(cal[2] | (cal[3] << 8))
        dig_T3 = self._to_signed_16(cal[4] | (cal[5] << 8))
        
        # Extraer parámetros de presión (dig_P1 a P9)
        dig_P1 = cal[6] | (cal[7] << 8)
        dig_P2 = self._to_signed_16(cal[8] | (cal[9] << 8))
        dig_P3 = self._to_signed_16(cal[10] | (cal[11] << 8))
        dig_P4 = self._to_signed_16(cal[12] | (cal[13] << 8))
        dig_P5 = self._to_signed_16(cal[14] | (cal[15] << 8))
        dig_P6 = self._to_signed_16(cal[16] | (cal[17] << 8))
        dig_P7 = self._to_signed_16(cal[18] | (cal[19] << 8))
        dig_P8 = self._to_signed_16(cal[20] | (cal[21] << 8))
        dig_P9 = self._to_signed_16(cal[22] | (cal[23] << 8))
        
        return {
            'T1': dig_T1, 'T2': dig_T2, 'T3': dig_T3,
            'P1': dig_P1, 'P2': dig_P2, 'P3': dig_P3,
            'P4': dig_P4, 'P5': dig_P5, 'P6': dig_P6,
            'P7': dig_P7, 'P8': dig_P8, 'P9': dig_P9
        }
    
    def _to_signed_16(self, val):
        """Convierte uint16 a int16 si es negativo"""
        return val - 65536 if val > 32767 else val
    
    def leer(self):
        """Retorna: (temperatura_celsius, presion_hPa)"""
        # Leer temperatura raw (3 bytes desde 0xFA)
        datos_temp = self.bus.read_i2c_block_data(self.address, 0xFA, 3)
        adc_T = (datos_temp[0] << 12) | (datos_temp[1] << 4) | (datos_temp[2] >> 4)
        
        # Compensar temperatura (según datasheet Bosch)
        var1 = ((adc_T / 16384.0) - (self.cal['T1'] / 1024.0)) * self.cal['T2']
        var2 = ((adc_T / 131072.0) - (self.cal['T1'] / 8192.0)) ** 2 * self.cal['T3']
        t_fine = var1 + var2
        temperatura = t_fine / 5120.0
        
        # Leer presión raw (3 bytes desde 0xF7)
        datos_pres = self.bus.read_i2c_block_data(self.address, 0xF7, 3)
        adc_P = (datos_pres[0] << 12) | (datos_pres[1] << 4) | (datos_pres[2] >> 4)
        
        # Compensar presión (algoritmo complejo del datasheet)
        var1 = (t_fine / 2.0) - 64000.0
        var2 = var1 * var1 * self.cal['P6'] / 32768.0
        var2 = var2 + var1 * self.cal['P5'] * 2.0
        var2 = (var2 / 4.0) + (self.cal['P4'] * 65536.0)
        var1 = (self.cal['P3'] * var1 * var1 / 524288.0 + self.cal['P2'] * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * self.cal['P1']
        
        if var1 == 0.0:
            return temperatura, 0.0  # Evitar división por cero
        
        presion = 1048576.0 - adc_P
        presion = (presion - (var2 / 4096.0)) * 6250.0 / var1
        var1 = self.cal['P9'] * presion * presion / 2147483648.0
        var2 = presion * self.cal['P8'] / 32768.0
        presion = presion + (var1 + var2 + self.cal['P7']) / 16.0
        presion = presion / 100.0  # Convertir Pa a hPa
        
        return temperatura, presion

# =====================================================
# PROGRAMA PRINCIPAL
# =====================================================
def main():
    print("=" * 60)
    print("CimaStation - Monitor Ambiental")
    print("=" * 60)
    print("Inicializando sensores...")
    
    # Inicializar sensores
    sht31 = SHT31(SHT31_ADDR)
    bmp280 = BMP280(BMP280_ADDR)
    
    print("✓ Sensores listos")
    print("Leyendo cada 10 segundos (Ctrl+C para detener)...\n")
    
    try:
        while True:
            # Leer SHT31 (temperatura + humedad)
            temp_sht, humedad = sht31.leer()
            
            # Leer BMP280 (temperatura + presión)
            temp_bmp, presion = bmp280.leer()
            
            # Mostrar con formato solicitado
            print(f"Temperatura = {temp_sht:.2f}°C")
            print(f"Humedad     = {humedad:.2f}%")
            print(f"Presión     = {presion:.2f} hPa")
            print("-" * 40)
            
            # Esperar 10 segundos
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n\n✓ Monitorización detenida")
        print("¡Hasta pronto!")

if __name__ == "__main__":
    main()
