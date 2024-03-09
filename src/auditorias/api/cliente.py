import os
import requests
import random
import faker

faker = faker.Faker()
test_type = os.environ.get("TEST_TYPE")


def establecer_transaccion_test():
    url = "http://localhost:5002/auditorias"
    #url = "http://localhost:5000/contratos"

    data = {
        "valor": 0 if test_type == "rechazo" else random.randint(1, 1000000),
        "comprador": faker.name(),
        "vendedor": faker.name(),
        "inquilino": faker.name(),
    }

    print("About to send the following data to the server:", data)
    response = requests.post(url, json=data)
    if response.ok:
        print("Transaccion establecida")

    # Pretty print the response
    try:
        import json

        print(json.dumps(response.json(), indent=4))
    except:
        print(response.text)


establecer_transaccion_test()
