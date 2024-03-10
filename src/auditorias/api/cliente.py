import os
from uuid import uuid4
import requests
import random
import faker

faker = faker.Faker()
test_type = os.environ.get("TEST_TYPE")
url_base = os.environ.get("TEST_URL_BASE")
if not url_base:
    url_base = "http://localhost:5000/auditorias"
id_correlacion = ""
id_transaccion = ""

def solicitar_auditoria_contrato_test():
    url = url_base
    id_correlacion = str(uuid4())
    id_transaccion = str(uuid4())
    data = {
        "id_correlacion": id_correlacion,
        "id_transaccion": id_transaccion,
        "valor": 0 if test_type == "rechazo" else random.randint(1, 1000000),
        "comprador": faker.name(),
        "vendedor": faker.name(),
        "inquilino": faker.name(),
        "arrendatario": faker.name(),
    }

    print("Contrato para auditar:", data)
    response = requests.post(url, json=data)
    if response.ok:
        print("Auditoría de contrato solicitada")   
        if test_type != "rechazo" :
          solicitar_compensacion_auditoria_test(id_correlacion, id_transaccion)

    try:
        import json
        print(json.dumps(response.json(), indent=4))
    except:
        print(response.text)
        

def solicitar_compensacion_auditoria_test(id_correlacion: str, id_transaccion: str):
    url = f"{url_base}/compensacion"
    id_auditoria = str(uuid4())
    data = {
        "id_correlacion": id_correlacion,
        "id_transaccion": id_transaccion,
        "id_auditoria": id_auditoria
    }

    print("Compensación:", data)
    response = requests.post(url, json=data)
    if response.ok:
        print("Compensación solicitada")

    try:
        import json
        print(json.dumps(response.json(), indent=4))
    except:
        print(response.text)


solicitar_auditoria_contrato_test()
