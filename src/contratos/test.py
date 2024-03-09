
class ContratoAuditado(EventoIntegracion):
    id_correlacion = schema.String(required=True)

    def topic_name(self) -> str:
        return "contrato_auditado"


class ContratoRechazado(EventoIntegracion):
    id_correlacion = schema.String(required=True)

    def topic_name(self) -> str:
        return "contrato_rechazado"


class ComandoArrendarPropiedad(Comando):
    id_correlacion = schema.String(required=True)

    def topic_name(self) -> str:
        return "arrendar_propiedad"

    @staticmethod
    def from_evento(evento) -> Comando:
        assert isinstance(evento, ContratoAuditado)
        return ComandoArrendarPropiedad(id_correlacion=evento.id_correlacion)


class PropiedadArrendada(EventoIntegracion):
    id_correlacion = schema.String(required=True)

    def topic_name(self) -> str:
        return "propiedad_arrendada"


class ArrendamientoFallido(EventoIntegracion):
    id_correlacion = schema.String(required=True)

    def topic_name(self) -> str:
        return "arrendamiento_fallido"


class ComandoCancelarContratoAuditado(Comando):
    id_correlacion = schema.String(required=True)

    def topic_name(self) -> str:
        return "cancelar_contrato_auditado"

    @staticmethod
    def from_evento(evento) -> Comando:
        assert isinstance(evento, ArrendamientoFallido)
        return ComandoCancelarContratoAuditado(id_correlacion=evento.id_correlacion)
