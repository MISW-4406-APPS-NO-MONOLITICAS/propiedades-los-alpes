import requests
import random
import faker

faker = faker.Faker()


def establecer_transaccion_test():
    url = "http://localhost:5000/contratos"

    data = {
        "valor": random.randint(1, 1000000),
        "comprador": faker.name(),
        "vendedor": faker.name(),
        "inquilino": faker.name(),
        "arrendatario": faker.name(),
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
