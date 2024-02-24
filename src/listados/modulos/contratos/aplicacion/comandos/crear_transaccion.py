from dataclasses import dataclass, field
from .base import CrearTransaccionBaseHandler
from listados.seedwork.aplicacion.comandos import Comando
from listados.seedwork.aplicacion.comandos import ejecutar_commando as comando
from listados.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from listados.modulos.contratos.aplicacion.dto import TransaccionDTO
from listados.modulos.contratos.dominio.entidades import Transaccion
from listados.modulos.contratos.aplicacion.mapeadores import MapeadorTransaccion
from listados.modulos.contratos.infraestructura.repositorios import RepositorioTransacciones

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

    def handle(self, comando: CrearTransaccion):
        transaccion_dto = TransaccionDTO(
            id = comando.id,
            fecha_creacion = comando.fecha_creacion,
            fecha_actualizacion = comando.fecha_actualizacion,
            valor = comando.valor,
            comprador = comando.comprador,
            vendedor = comando.vendedor,
            inquilino = comando.inquilino,
            arrendatario = comando.arrendatario,
        )
        print('CrearTransaccionHandler')
        print('transaccion_dto: ', transaccion_dto)
        transaccion: Transaccion = self.fabrica_transacciones.crear_objeto(transaccion_dto, MapeadorTransaccion())
        print('transaccion: ', transaccion)
        transaccion.crear_transaccion(transaccion)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioTransacciones.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, transaccion)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

@comando.register(CrearTransaccion)
def ejecutar_comando_crear_transaccion(comando: CrearTransaccion):
    handler = CrearTransaccionHandler()
    handler.handle(comando)
