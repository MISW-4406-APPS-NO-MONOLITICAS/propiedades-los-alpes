import pulsar.schema as schema

class EventoIntegracion(schema.Record):
    fecha_evento =  schema.String(required=True)
    def topic_name(self) -> str:
        raise ValueError("La subclase debe implementar el método topic_name")