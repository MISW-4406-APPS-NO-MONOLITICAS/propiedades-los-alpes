import os
from uuid import uuid4
import requests
import random
import faker

faker = faker.Faker()
test_type = os.environ.get("TEST_TYPE")
uuid = ""

def solicitar_auditoria_contrato_test():
    url = "http://localhost:5002/auditorias"
    uuid = str(uuid4())
    data = {
        "id_transaccion": uuid,
        "valor": 0 if test_type == "rechazo" else random.randint(1, 1000000),
        "comprador": faker.name(),
        "vendedor": faker.name(),
        "inquilino": faker.name(),
    }

    print("Contrato para auditar:", data)
    response = requests.post(url, json=data)
    if response.ok:
        print("Auditoría de contrato solicitada")   
        if test_type != "rechazo" :
          solicitar_compensacion_auditoria_test(uuid)

    # Pretty print the response
    try:
        import json

        print(json.dumps(response.json(), indent=4))
    except:
        print(response.text)
        

def solicitar_compensacion_auditoria_test(uuid: str):
    url = "http://localhost:5002/auditorias/compensacion"

    data = {
        "id_transaccion": uuid
    }

    print("Compensación:", data)
    response = requests.post(url, json=data)
    if response.ok:
        print("Compensación solicitada")

    # Pretty print the response
    try:
        import json

        print(json.dumps(response.json(), indent=4))
    except:
        print(response.text)


solicitar_auditoria_contrato_test()
