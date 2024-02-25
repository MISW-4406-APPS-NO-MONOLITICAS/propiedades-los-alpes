import requests
import random


def establecer_transaccion_test():
    url = "http://localhost:5000/contratos"

    data = {
        "id": random.randint(1, 1000000),
        "fecha_creacion": "2021-01-01 12:00:00",
        "fecha_actualizacion": "2021-01-01 12:00:00",
        "valor": random.randint(1, 1000000),
        "comprador": "comprador",
        "vendedor": "vendedor",
        "inquilino": "inquilino",
        "arrendatario": "arrendatario",
    }
    
    response = requests.post(url, json=data)
    if response.ok:
        print('Transaccion establecida')

    # Pretty print the response
    try:
        import json
        print(json.dumps(response.json(), indent=4))
    except:
        print(response.text)

establecer_transaccion_test()
