import pulsar
import pulsar.schema as schema
from pydispatch import dispatcher


def get_pulsar_client():
    return pulsar.Client(f"pulsar://pulsar:6650")


class Despachador:
    def _publicar_mensaje(self, topico: str, evento: schema.Record):
        cliente = get_pulsar_client()
        print(f"Publicando evento {type(evento).__name__} en el topico {topico}")
        publicador = cliente.create_producer(
            topico, schema=schema.AvroSchema(evento.__class__)
        )
        publicador.send(evento)
        cliente.close()

    def publicar_evento(self, evento):
        self._publicar_mensaje(evento.topico, evento.evento)


despachador = Despachador()

dispatcher.connect(despachador.publicar_evento, signal="Integracion")
