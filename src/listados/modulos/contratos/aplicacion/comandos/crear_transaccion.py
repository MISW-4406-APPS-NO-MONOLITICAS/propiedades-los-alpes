from dataclasses import dataclass, field
from .base import BaseHandler
from listados.seedwork.aplicacion.comandos import Comando
from listados.seedwork.aplicacion.comandos import ejecutar_commando as comando
from listados.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from listados.modulos.contratos.aplicacion.dto import TransaccionDTO, Valor


@dataclass
class CrearTransaccion(Comando):
    valor: Valor
    comprador: str
    vendedor: str
    inquilino: str
    arrendatario: str


class CrearTransaccionHandler(BaseHandler):
    def handle(self, comando: CrearTransaccion):
        transaccion_dto = TransaccionDTO(
            valor=comando.valor,
            comprador=comando.comprador,
            vendedor=comando.vendedor,
            inquilino=comando.inquilino,
            arrendatario=comando.arrendatario,
        )
        transaccion = self.fabrica_transacciones.crear_objeto(transaccion_dto)
        transaccion.crear_transaccion()  # Genera los eventos

        # Se programa en el uow
        UnidadTrabajoPuerto.registrar_batch(
            self.repositorio_transaciones.agregar, transaccion
        )
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CrearTransaccion)
def ejecutar_comando_crear_transaccion(comando: CrearTransaccion):
    handler = CrearTransaccionHandler()
    handler.handle(comando)
