import requests
import random
import faker
import argparse


parser = argparse.ArgumentParser(description="Helper utility to test the server")

parser.add_argument(
    "--crear-transaccion",
    action="store_true",
)

parser.add_argument(
    "--crear-contrato",
    action="store_true",
)

faker = faker.Faker()


def establecer_transaccion_test():
    url = "http://localhost:5000/contratos/transccion"

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


def establecer_contrato_test():
    response = requests.post("http://localhost:5000/contratos", json={})
    if response.ok:
        print("Contrato establecido")
        print(response.text)
    else:
        print("Error al establecer contrato")
        print(response.text)


args = parser.parse_args()

if args.crear_transaccion:
    establecer_transaccion_test()
elif args.crear_contrato:
    establecer_contrato_test()
else:
    raise ValueError("No se especifico ninguna accion")
