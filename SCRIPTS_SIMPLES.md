# Scripts Simples - CimaStation

## 📁 Archivos

### `sensores_simples.py`
Funciones exportables para leer los sensores:
- `leer_bmp280()` → temperatura, presión
- `leer_sht31()` → humedad (temperatura del SHT31 no funciona bien en esta placa)
- `leer_tcs34725()` → luz RGB, lux
- `inicializar_tcs34725()` → inicializar sensor de luz (llamar una vez)
- `leer_todos_sensores()` → lee todos y retorna diccionario

**Nota:** En esta placa específica, la temperatura del BMP280 es la que funciona correctamente.

### `monitor_continuo.py`
Script que muestra los datos cada 5 segundos.

---

## 🚀 Uso

### Ejecutar monitor continuo
```bash
python3 monitor_continuo.py
```

**Salida:**
```
[15:30:25]
  Temperatura: 22.45°C
  Humedad:     45.23%
  Presión:     1013.25 hPa
  Luz:         150.3 lux
------------------------------------------------------------
```

### Usar funciones en tu código

```python
from sensores_simples import leer_bmp280, leer_sht31, leer_tcs34725, inicializar_tcs34725

# Inicializar TCS34725 (una sola vez al inicio)
inicializar_tcs34725()

# Leer sensores individuales
bmp_datos = leer_bmp280()
# {'temperatura': 22.5, 'presion': 1013.25}

sht_datos = leer_sht31()
# {'temperatura': 22.45, 'humedad': 45.2}
# Nota: Usar temperatura del BMP280, humedad del SHT31

tcs_datos = leer_tcs34725()
# {'clear': 1234, 'red': 456, 'green': 789, 'blue': 234, 'lux': 150.3}

# O leer todos de una vez
from sensores_simples import leer_todos_sensores

todos = leer_todos_sensores()
# {
#   'bmp280': {...},
#   'sht31': {...},
#   'tcs34725': {...}
# }
```

### Usar en tu API

```python
from flask import Flask, jsonify
from sensores_simples import leer_sht31, leer_bmp280, leer_tcs34725, inicializar_tcs34725

app = Flask(__name__)

# Inicializar al arrancar
inicializar_tcs34725()

@app.route('/api/temperatura')
def temperatura():
    sht = leer_sht31()
    return jsonify({'temperatura': sht['temperatura']})

@app.route('/api/datos')
def datos():
    return jsonify({
        'bmp280': leer_bmp280(),
        'sht31': leer_sht31(),
        'tcs34725': leer_tcs34725()
    })

app.run(host='0.0.0.0', port=5000)
```

---

## 📊 Estructura de datos retornados

### leer_bmp280()
```python
{
    'temperatura': 22.5,  # °C
    'presion': 1013.25    # hPa
}
# Nota: Usamos temperatura del BMP280 porque en esta placa 
# el SHT31 no responde correctamente
```

### leer_sht31()
```python
{
    'temperatura': 22.45,  # °C (puede no funcionar correctamente)
    'humedad': 45.2        # %
}
# Nota: En esta placa, usar temperatura del BMP280
#       y humedad del SHT31
```
```

### leer_tcs34725()
```python
{
    'clear': 1234,   # Luz total (0-65535)
    'red': 456,      # Canal rojo (0-65535)
    'green': 789,    # Canal verde (0-65535)
    'blue': 234,     # Canal azul (0-65535)
    'lux': 150.3     # Iluminancia (lux)
}
```

---

## ⚡ Características

- ✅ **Simple**: Solo funciones, sin clases
- ✅ **Directo**: Hace solo lo necesario
- ✅ **Exportable**: Importa las funciones que necesites
- ✅ **Robusto**: Si un sensor falla, retorna None

---

## 🔧 Ejemplo: Guardar en archivo

```python
import time
from sensores_simples import leer_todos_sensores, inicializar_tcs34725

inicializar_tcs34725()

with open('lecturas.txt', 'a') as f:
    while True:
        datos = leer_todos_sensores()
        
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        temp = datos['bmp280']['temperatura']  # Temperatura del BMP280
        hum = datos['sht31']['humedad']        # Humedad del SHT31
        pres = datos['bmp280']['presion']      # Presión del BMP280
        
        f.write(f"{timestamp},{temp},{hum},{pres}\n")
        f.flush()
        
        time.sleep(300)  # Cada 5 minutos
```

---

**¡Listo para usar! 🚀**