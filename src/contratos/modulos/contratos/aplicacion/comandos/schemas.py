import uuid
import pulsar.schema as schema

from contratos.seedwork.aplicacion.comandos import Comando


class ComandoCrearContrato(Comando):
    id_correlacion = schema.String(required=True)
    id_propiedad = schema.String(required=True)
    valor = schema.Float(required=True)
    comprador = schema.String()
    vendedor = schema.String()
    inquilino = schema.String()
    arrendatario = schema.String()

    def as_dict(self):
        return {
            "id_correlacion": self.id_correlacion,
            "id_propiedad": self.id_propiedad,
            "valor": self.valor,
            "comprador": self.comprador,
            "vendedor": self.vendedor,
            "inquilino": self.inquilino,
            "arrendatario": self.arrendatario,
        }

    def topic_name(self) -> str:
        return "contratos_crear"


class ComandoAuditarContrato(Comando):
    id_correlacion = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    valor = schema.Float(required=True)
    comprador = schema.String()
    vendedor = schema.String()
    inquilino = schema.String()
    arrendatario = schema.String()
    fecha_evento = schema.String(required=True)

    def topic_name(self) -> str:
        return "auditorias_auditar_contrato"


class ComandoArrendarPropiedad(Comando):
    id_correlacion = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    id_propiedad = schema.String(required=True)
    valor = schema.Float(required=True)
    comprador = schema.String()
    vendedor = schema.String()
    inquilino = schema.String()
    arrendatario = schema.String()

    def topic_name(self) -> str:
        return "listados_arrendar_propiedad"

    @staticmethod
    def from_evento(evento):
        from contratos.modulos.contratos.aplicacion.eventos.schemas import (
            ContratoAuditado,
        )
        from contratos.modulos.contratos.infraestructura.repositorios import (
            RepositorioTrasaccionesDB,
        )

        assert isinstance(
            evento, ContratoAuditado
        ), "Evento no es de tipo ContratoAuditado"
        transaccion = RepositorioTrasaccionesDB().obtener_por_id(
            uuid.UUID(str(evento.id_transaccion))
        )
        assert transaccion, "Transaccion no encontrada"

        return ComandoArrendarPropiedad(
            id_correlacion=evento.id_correlacion,
            id_transaccion=evento.id_transaccion,
            id_propiedad=transaccion.id_propiedad,
            valor=transaccion.valor.valor,
            comprador=transaccion.comprador,
            vendedor=transaccion.vendedor,
            inquilino=transaccion.inquilino,
            arrendatario=transaccion.arrendatario,
        )


class ComandoCancelarContratoAuditado(Comando):
    id_correlacion = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    id_auditoria = schema.String(required=True)

    def topic_name(self) -> str:
        return "auditorias_cancelar_contrato_auditado"

    @staticmethod
    def from_evento(evento):
        from contratos.modulos.contratos.aplicacion.eventos.schemas import (
            PropiedadArrendamientoRechazado,
        )

        assert isinstance(
            evento, PropiedadArrendamientoRechazado
        ), "Evento no es de tipo PropiedadArrendamientoRechazado"

        from contratos.modulos.contratos.infraestructura.repositorios import (
            RepositorioTrasaccionesDB,
        )

        transaccion = RepositorioTrasaccionesDB().obtener_por_id(
            uuid.UUID(str(evento.id_transaccion))
        )
        assert transaccion, "Transaccion no encontrada"

        return ComandoCancelarContratoAuditado(
            id_correlacion=evento.id_correlacion,
            id_transaccion=evento.id_transaccion,
            id_auditoria=transaccion.id_auditoria,
        )
