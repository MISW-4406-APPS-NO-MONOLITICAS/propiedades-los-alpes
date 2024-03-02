from dataclasses import dataclass, field
from contratos.config.logger import logger
from .base import BaseHandler
from contratos.seedwork.aplicacion.comandos import Comando
from contratos.seedwork.aplicacion.comandos import ejecutar_commando as comando
from contratos.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from contratos.modulos.contratos.aplicacion.dto import TransaccionDTO, Valor
import pulsar.schema as schema


class ComandoCrearTransaccion(Comando):
    valor = schema.Float()
    comprador = schema.String()
    vendedor = schema.String()
    inquilino = schema.String()
    arrendatario = schema.String()

    def topic_name(self):
        return "crear_transaccion"

    def as_dict(self):
        return {
            "valor": self.valor,
            "comprador": self.comprador,
            "vendedor": self.vendedor,
            "inquilino": self.inquilino,
            "arrendatario": self.arrendatario,
        }


class ComandoCrearTransaccionHandler(BaseHandler):
    def handle(self, comando: ComandoCrearTransaccion):
        logger.info(f"Manejando comando {comando.__class__.__name__}")
        transaccion_dto = TransaccionDTO(
            valor=Valor(comando.valor),
            comprador=comando.comprador,
            vendedor=comando.vendedor,
            inquilino=comando.inquilino,
            arrendatario=comando.arrendatario,
        )
        transaccion = self.fabrica_transacciones.crear_objeto(transaccion_dto)
        transaccion.crear_transaccion()  # Genera los eventos

        # Se programa en el uow
        logger.info(f"Inscribiendo en unidad de trabajo del comando {comando.__class__.__name__}")
        UnidadTrabajoPuerto.registrar_batch(
            self.repositorio_transaciones.agregar, transaccion
        )
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(ComandoCrearTransaccion)
def ejecutar_comando_crear_transaccion(comando: ComandoCrearTransaccion):
    handler = ComandoCrearTransaccionHandler()
    handler.handle(comando)
