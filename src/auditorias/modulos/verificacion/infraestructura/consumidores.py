from auditorias.config.pulsar import Consumidor
from auditorias.modulos.verificacion.aplicacion.comandos.auditar_contrato import ComandoAuditarContrato, ComandoAuditarContratoHandler
""" from auditorias.modulos.verificacion.aplicacion.handlers import (
    ContratoCreadoIntegracionHandler,
) """
""" from auditorias.modulos.verificacion.dominio.eventos import ContratoCreadoIntegracion """


consumidores = [
    # Consumidor(
    #     topico=ContratoCreadoIntegracion().topic_name(),
    #     mensaje=ContratoCreadoIntegracion,
    #     handler=ContratoCreadoIntegracionHandler,
    # ).start,
    Consumidor(
        topico=ComandoAuditarContrato().topic_name(),
        mensaje=ComandoAuditarContrato,
        handler=ComandoAuditarContratoHandler,
    ).start,
    
]
