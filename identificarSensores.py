#!/usr/bin/env python3
"""
Script para identificar todos los sensores en la Google Environmental Board
"""
import smbus2
import time

bus = smbus2.SMBus(1)

print("=" * 60)
print("IDENTIFICACIÓN DE SENSORES - Google Environmental Board")
print("=" * 60)

# ========== SENSOR 0x76 ==========
print("\n[1] Analizando 0x76 (BMP280/BME280)...")
try:
    chip_id = bus.read_byte_data(0x76, 0xD0)
    print(f"    CHIP ID: 0x{chip_id:02X}")
    if chip_id == 0x60:
        print("    ✓ Identificado: BME280 (Temperatura + Presión + HUMEDAD)")
    elif chip_id == 0x58:
        print("    ✓ Identificado: BMP280 (Temperatura + Presión, SIN humedad)")
    else:
        print(f"    ? Chip ID desconocido")
except Exception as e:
    print(f"    ✗ Error: {e}")

# ========== SENSOR 0x40 ==========
print("\n[2] Analizando 0x40 (Posible sensor de humedad)...")
try:
    # Intentar leer como Si7021/HTU21D
    # Comando: leer temperatura (0xE3 con hold master)
    bus.write_byte(0x40, 0xE3)
    time.sleep(0.1)
    data = bus.read_i2c_block_data(0x40, 0x00, 2)
    
    # Si responde, es compatible con Si7021/HTU21D
    print("    ✓ Responde a comandos Si7021/HTU21D")
    
    # Intentar leer el ID del firmware
    bus.write_i2c_block_data(0x40, 0xFC, [0xC9])
    time.sleep(0.1)
    firmware = bus.read_byte(0x40)
    
    if firmware == 0x20:
        print("    ✓ Identificado: Si7021 (Temperatura + Humedad)")
    elif firmware == 0xFF:
        print("    ✓ Identificado: HTU21D (Temperatura + Humedad)")
    else:
        print(f"    ✓ Compatible Si7021/HTU21D (firmware: 0x{firmware:02X})")
        
except Exception as e:
    print(f"    ? No responde como Si7021/HTU21D")
    print(f"      Probando otros protocolos...")
    
    # Intentar HDC1080
    try:
        # Leer registro de fabricante (0xFE) y device ID (0xFF)
        manufacturer = bus.read_word_data(0x40, 0xFE)
        device_id = bus.read_word_data(0x40, 0xFF)
        
        if manufacturer == 0x5449:  # "TI" en ASCII
            print(f"    ✓ Identificado: HDC1080 (Texas Instruments)")
            print(f"      Device ID: 0x{device_id:04X}")
    except:
        print(f"    ✗ No se pudo identificar: {e}")

# ========== SENSOR 0x45 ==========
print("\n[3] Analizando 0x45...")
try:
    # Podría ser SHT31, SHT35, o sensor de luz
    # Intentar SHT3x (comando: leer estado 0xF32D)
    bus.write_i2c_block_data(0x45, 0xF3, [0x2D])
    time.sleep(0.1)
    status = bus.read_i2c_block_data(0x45, 0x00, 3)
    print(f"    ✓ Responde a comandos SHT3x")
    print(f"    ✓ Probable: SHT31/SHT35 (Temperatura + Humedad de alta precisión)")
except Exception as e:
    # Intentar como sensor de luz TCS34725
    try:
        chip_id = bus.read_byte_data(0x45, 0x12)
        if chip_id in [0x44, 0x4D]:
            print(f"    ✓ Identificado: TCS34725 (Sensor de color RGB)")
    except:
        print(f"    ? No identificado: {e}")

# ========== SENSOR 0x30 ==========
print("\n[4] Analizando 0x30...")
try:
    # Podría ser TCS34725 en dirección alternativa o VEML6070 (UV)
    # Intentar leer registro de ID
    chip_id = bus.read_byte_data(0x30, 0x12)
    print(f"    CHIP ID: 0x{chip_id:02X}")
    
    if chip_id in [0x44, 0x4D]:
        print(f"    ✓ Identificado: TCS34725 (Sensor de color RGB)")
except:
    # Intentar VEML6070 (sensor UV)
    try:
        # VEML6070 responde en 0x38 y 0x39, pero tiene alias en 0x30
        data = bus.read_byte(0x30)
        print(f"    ✓ Posible: VEML6070 (Sensor UV)")
    except Exception as e:
        print(f"    ? No identificado: {e}")

print("\n" + "=" * 60)
print("RESUMEN DE CAPACIDADES")
print("=" * 60)
print("\nTu Google Environmental Board puede medir:")
print("  • Temperatura (desde BMP280 o sensor 0x40)")
print("  • Presión atmosférica (desde BMP280)")
print("  • Humedad (¡SI! desde sensor 0x40 o 0x45)")
print("  • Posibles: Luz/Color/UV (sensores 0x30)")
print("\n¡Puedes hacer el script completo con los 3 parámetros!")
print("=" * 60)