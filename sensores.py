#!/usr/bin/env python3
"""
Funciones simples para leer sensores de CimaStation
Exportables para usar en otros scripts
"""
import smbus2
import time

bus = smbus2.SMBus(1)

# =====================================================
# BMP280 - Presión y Temperatura
# =====================================================
def leer_bmp280():
    """
    Lee temperatura y presión del BMP280
    
    Returns:
        dict: {'temperatura': float, 'presion': float} o None si falla
    """
    try:
        address = 0x76
        
        # Leer calibración (solo necesitamos estos)
        cal = bus.read_i2c_block_data(address, 0x88, 24)
        
        # Temperatura
        T1 = cal[0] | (cal[1] << 8)
        T2 = cal[2] | (cal[3] << 8)
        if T2 > 32767: T2 -= 65536
        T3 = cal[4] | (cal[5] << 8)
        if T3 > 32767: T3 -= 65536
        
        # Presión
        P1 = cal[6] | (cal[7] << 8)
        P2 = cal[8] | (cal[9] << 8)
        if P2 > 32767: P2 -= 65536
        P3 = cal[10] | (cal[11] << 8)
        if P3 > 32767: P3 -= 65536
        P4 = cal[12] | (cal[13] << 8)
        if P4 > 32767: P4 -= 65536
        P5 = cal[14] | (cal[15] << 8)
        if P5 > 32767: P5 -= 65536
        P6 = cal[16] | (cal[17] << 8)
        if P6 > 32767: P6 -= 65536
        P7 = cal[18] | (cal[19] << 8)
        if P7 > 32767: P7 -= 65536
        P8 = cal[20] | (cal[21] << 8)
        if P8 > 32767: P8 -= 65536
        P9 = cal[22] | (cal[23] << 8)
        if P9 > 32767: P9 -= 65536
        
        # Configurar sensor (solo si no está configurado)
        bus.write_byte_data(address, 0xF4, 0x27)
        time.sleep(0.01)
        
        # Leer temperatura raw
        datos_temp = bus.read_i2c_block_data(address, 0xFA, 3)
        adc_T = (datos_temp[0] << 12) | (datos_temp[1] << 4) | (datos_temp[2] >> 4)
        
        # Compensar temperatura
        var1 = ((adc_T / 16384.0) - (T1 / 1024.0)) * T2
        var2 = ((adc_T / 131072.0) - (T1 / 8192.0)) ** 2 * T3
        t_fine = var1 + var2
        temperatura = t_fine / 5120.0
        
        # Leer presión raw
        datos_pres = bus.read_i2c_block_data(address, 0xF7, 3)
        adc_P = (datos_pres[0] << 12) | (datos_pres[1] << 4) | (datos_pres[2] >> 4)
        
        # Compensar presión
        var1 = (t_fine / 2.0) - 64000.0
        var2 = var1 * var1 * P6 / 32768.0
        var2 = var2 + var1 * P5 * 2.0
        var2 = (var2 / 4.0) + (P4 * 65536.0)
        var1 = (P3 * var1 * var1 / 524288.0 + P2 * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * P1
        
        if var1 == 0.0:
            presion = 0.0
        else:
            presion = 1048576.0 - adc_P
            presion = (presion - (var2 / 4096.0)) * 6250.0 / var1
            var1 = P9 * presion * presion / 2147483648.0
            var2 = presion * P8 / 32768.0
            presion = presion + (var1 + var2 + P7) / 16.0
            presion = presion / 100.0  # Convertir a hPa
        
        return {
            'temperatura': round(temperatura, 2),
            'presion': round(presion, 2)
        }
        
    except Exception as e:
        print(f"Error leyendo BMP280: {e}")
        return None


# =====================================================
# SHT31 - Temperatura y Humedad
# =====================================================
def leer_sht31():
    """
    Lee temperatura y humedad del SHT31
    
    Returns:
        dict: {'temperatura': float, 'humedad': float} o None si falla
    """
    try:
        address = 0x45
        
        # Enviar comando de medición
        bus.write_i2c_block_data(address, 0x24, [0x00])
        time.sleep(0.02)  # Esperar conversión
        
        # Leer 6 bytes
        datos = bus.read_i2c_block_data(address, 0, 6)
        
        # Extraer valores
        temp_raw = (datos[0] << 8) | datos[1]
        hum_raw = (datos[3] << 8) | datos[4]
        
        # Convertir
        temperatura = -45 + (175 * temp_raw / 65535.0)
        humedad = 100 * hum_raw / 65535.0
        
        return {
            'temperatura': round(temperatura, 2),
            'humedad': round(humedad, 2)
        }
        
    except Exception as e:
        print(f"Error leyendo SHT31: {e}")
        return None


# =====================================================
# TCS34725 - Luz RGB
# =====================================================
def inicializar_tcs34725():
    """
    Inicializa el sensor TCS34725 (llamar una vez al inicio)
    """
    try:
        address = 0x30
        COMMAND_BIT = 0x80
        
        # Enable: Power ON
        bus.write_byte_data(address, COMMAND_BIT | 0x00, 0x01)
        time.sleep(0.003)
        
        # Enable: Power ON + ADC Enable
        bus.write_byte_data(address, COMMAND_BIT | 0x00, 0x03)
        
        # Integration time: 2.4ms
        bus.write_byte_data(address, COMMAND_BIT | 0x01, 0xFF)
        
        # Gain: 1x
        bus.write_byte_data(address, COMMAND_BIT | 0x0F, 0x00)
        
        time.sleep(0.01)
        
    except Exception as e:
        print(f"Error inicializando TCS34725: {e}")


def leer_tcs34725():
    """
    Lee valores RGB y luz del TCS34725
    
    Returns:
        dict: {'clear': int, 'red': int, 'green': int, 'blue': int, 'lux': float} o None si falla
    """
    try:
        address = 0x30
        COMMAND_BIT = 0x80
        
        # Leer 4 canales (2 bytes cada uno)
        clear_data = bus.read_i2c_block_data(address, COMMAND_BIT | 0x14, 2)
        red_data = bus.read_i2c_block_data(address, COMMAND_BIT | 0x16, 2)
        green_data = bus.read_i2c_block_data(address, COMMAND_BIT | 0x18, 2)
        blue_data = bus.read_i2c_block_data(address, COMMAND_BIT | 0x1A, 2)
        
        # Convertir a valores (little-endian)
        clear = (clear_data[1] << 8) | clear_data[0]
        red = (red_data[1] << 8) | red_data[0]
        green = (green_data[1] << 8) | green_data[0]
        blue = (blue_data[1] << 8) | blue_data[0]
        
        # Calcular lux
        lux = (-0.32466 * red) + (1.57837 * clear)
        lux = max(0, lux)
        
        return {
            'clear': clear,
            'red': red,
            'green': green,
            'blue': blue,
            'lux': round(lux, 2)
        }
        
    except Exception as e:
        print(f"Error leyendo TCS34725: {e}")
        return None


# =====================================================
# FUNCIÓN PARA LEER TODOS
# =====================================================
def leer_todos_sensores():
    """
    Lee todos los sensores y retorna diccionario con todos los datos
    
    Returns:
        dict: Datos de todos los sensores
    """
    datos_bmp = leer_bmp280()
    datos_sht = leer_sht31()
    datos_tcs = leer_tcs34725()
    
    return {
        'bmp280': datos_bmp,
        'sht31': datos_sht,
        'tcs34725': datos_tcs
    }
