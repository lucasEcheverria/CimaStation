# CimaStation

============================================================
IDENTIFICACIÓN DE SENSORES - Google Environmental Board
============================================================

[1] Analizando 0x76 (BMP280/BME280)...
    CHIP ID: 0x58
    ✓ Identificado: BMP280 (Temperatura + Presión, SIN humedad)

[2] Analizando 0x40 (Posible sensor de humedad)...
    ? No responde como Si7021/HTU21D
      Probando otros protocolos...

[3] Analizando 0x45...
    ✓ Responde a comandos SHT3x
    ✓ Probable: SHT31/SHT35 (Temperatura + Humedad de alta precisión)

[4] Analizando 0x30...
    CHIP ID: 0x04

============================================================
RESUMEN DE CAPACIDADES
============================================================

Tu Google Environmental Board puede medir:
  • Temperatura (desde BMP280 o sensor 0x40)
  • Presión atmosférica (desde BMP280)
  • Humedad (¡SI! desde sensor 0x40 o 0x45)
  • Posibles: Luz/Color/UV (sensores 0x30)

¡Puedes hacer el script completo con los 3 parámetros!
