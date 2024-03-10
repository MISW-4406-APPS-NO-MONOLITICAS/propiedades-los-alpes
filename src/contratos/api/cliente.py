import uuid
import requests
import random
import faker
import argparse


parser = argparse.ArgumentParser(description="Helper utility to test the server")

parser.add_argument(
    "--transaccion",
    action="store_true",
    default=False,
)

faker = faker.Faker()


def establecer_transaccion_test():
    url = "http://localhost:5000/contratos"

    data = {
        "id_propiedad": str(uuid.uuid4()),
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


args = parser.parse_args()

if args.transaccion:
    print(args)
    establecer_transaccion_test()
else:
    print("No se especifico ninguna accion correcta")
    parser.print_help()
    exit(1)
