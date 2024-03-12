import json
import random
from flask import Flask, request
import requests
import csv
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/check-listados-health')
def check_listados_health():
    url = "http://listados:5000/health"
    response = requests.get(url)

    if response.status_code == 200:
        return "La ruta health del contenedor listados está funcionando correctamente."
    else:
        return "Error al acceder a la ruta health del contenedor listados."
    
@app.route('/crear-propiedad-batch')
def crear_propiedad_batch():
    cantidad = request.args.get('cantidad', default=100, type=int)

    url_crash = "http://listados:5000/listados/crash"

    url_seeder = "http://listados:5000/listados/seeder"
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"cantidad": 1})
    numero_exitosas = 0
    bandera = False
    start_time_total = datetime.now()

    with open('/src/resultados_creacion.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range(cantidad):
            start_time = datetime.now()
            try:
                response = requests.post(url_seeder, headers=headers, data=data)
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()

                if (i == cantidad / 2) and not bandera:
                    response = requests.get(url_crash)
                    bandera = True

                if response.status_code == 202:
                    numero_exitosas += 1
                    writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), i+1, "Éxito", duration])
                else:
                    writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), i+1, "Fallo", duration])
            except requests.exceptions.RequestException as e:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), i+1, "Error de conexión", duration])
                print(f"Error al hacer la solicitud: {e}")

    end_time_total = datetime.now()
    total_duration = (end_time_total - start_time_total).total_seconds()
    return f"Se intentaron crear {cantidad} propiedades. Se crearon exitosamente {numero_exitosas} propiedades durante un tiempo de {total_duration} segundos."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
