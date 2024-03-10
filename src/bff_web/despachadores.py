import pulsar
from pulsar.schema import *
import pulsar.schema as schemaAvr

from . import utils

class Despachador:
    def __init__(self):
        ...

    def publicar_mensaje(self, mensaje:schemaAvr.Record, topico:str):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=schemaAvr.AvroSchema(mensaje.__class__))
        publicador.send(mensaje)
        cliente.close()
        
    def publicar_comando(self, comando: utils.Comando):
        self.publicar_mensaje(topico=comando.topic_name(), mensaje=comando)