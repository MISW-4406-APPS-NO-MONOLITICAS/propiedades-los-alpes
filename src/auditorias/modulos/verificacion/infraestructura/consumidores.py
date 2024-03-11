from auditorias.config.pulsar import Consumidor
from auditorias.modulos.verificacion.aplicacion.comandos.auditar_contrato import ComandoAuditarContrato, ComandoAuditarContratoHandler
from auditorias.modulos.verificacion.aplicacion.comandos.cancelar_contrato_auditado import ComandoCancelarContratoAuditado, ComandoCancelarContratoAuditadoHandler


consumidores = [
    Consumidor(
        topico=ComandoAuditarContrato().topic_name(),
        mensaje=ComandoAuditarContrato,
        handler=ComandoAuditarContratoHandler().handle,
    ).start,
    Consumidor(
        topico=ComandoCancelarContratoAuditado().topic_name(),
        mensaje=ComandoCancelarContratoAuditado,
        handler=ComandoCancelarContratoAuditadoHandler().handle,
    ).start,
]
