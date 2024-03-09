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


class ComandoCancelarContratoAuditado(Comando):
    id_correlacion = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    id_auditoria = schema.String(required=True)

    def topic_name(self) -> str:
        return "auditorias_cancelar_contrato_auditado"
