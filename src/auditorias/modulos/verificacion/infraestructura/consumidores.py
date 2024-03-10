from auditorias.config.pulsar import Consumidor
from auditorias.modulos.verificacion.aplicacion.comandos.auditar_contrato import ComandoAuditarContrato, ComandoAuditarContratoHandler


consumidores = [
    Consumidor(
        mensaje=ComandoAuditarContrato,
        handler=ComandoAuditarContratoHandler().handle,
    ).start,
]
