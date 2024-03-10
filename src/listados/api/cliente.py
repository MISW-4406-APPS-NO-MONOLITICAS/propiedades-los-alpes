import requests
import random
import faker

faker = faker.Faker()


def establecer_transaccion_test():
    import uuid

    url = "http://localhost:5000/listados"

    data = {
        "id_correlacion": str(uuid.uuid4()),
        "id_propiedad": str(uuid.uuid4()),
        "id_transaccion": str(uuid.uuid4()),
        "fecha_evento": faker.date_time_this_month().isoformat(),
        "valor": 2,
        "inquilino": faker.name(),
        "arrendatario": faker.name()
    }

    print("About to send the following data to the server:", data)
    response = requests.post(url, json=data)
    if response.ok:
        print("Actualizacion exitosa")

    # Pretty print the response
    try:
        import json

        print(json.dumps(response.json(), indent=4))
    except:
        print(response.text)


establecer_transaccion_test()
