import pulsar
import pulsar.schema as schema
from pydispatch import dispatcher


class Despachador:
    def _publicar_mensaje(self, topico, evento):
        cliente = pulsar.Client(f"pulsar://pulsar:6650")
        publicador = cliente.create_producer(topico, schema=evento.__class__)
        publicador.send(evento)
        cliente.close()

    def publicar_evento(self, evento):
        self._publicar_mensaje(evento.topico, evento.evento)


despachador = Despachador()

dispatcher.connect(despachador.publicar_evento, signal="Integracion")
