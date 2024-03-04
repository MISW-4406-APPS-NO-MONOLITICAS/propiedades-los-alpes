import requests
import random
import faker

faker = faker.Faker()


def establecer_transaccion_test():
    url = "http://localhost:5000/listados"

    data = {
        "tipo_construccion": faker.word(),
        "estado": faker.boolean(),
        "area": faker.pyfloat(),
        "direccion": faker.address(),
        "lote": faker.random_int(min=1, max=100),
        "compania": faker.company(),
        "fecha_registro": faker.date_this_year(),
        "fecha_actualizacion": faker.date_this_year(),
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
