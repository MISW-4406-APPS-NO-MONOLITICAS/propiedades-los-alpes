from dataclasses import dataclass, field
from .base import CrearTransaccionBaseHandler
from listados.seedwork.aplicacion.comandos import Comando
from listados.seedwork.aplicacion.comandos import ejecutar_commando as comando

@dataclass
class CrearTransaccion(Comando):
    id: str
    fecha_creacion: str
    fecha_actualizacion: str
    valor: float
    comprador: str
    vendedor: str
    inquilino: str
    arrendatario: str

class CrearTransaccionHandler(CrearTransaccionBaseHandler):
    ...

@comando.register(CrearTransaccion)
def ejecutar_comando_crear_transaccion(comando: CrearTransaccion):
    handler = CrearTransaccionHandler()
    handler.handle(comando)
