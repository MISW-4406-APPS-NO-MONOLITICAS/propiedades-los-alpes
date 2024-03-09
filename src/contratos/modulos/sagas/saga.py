import datetime
from contratos.config.pulsar import Consumidor
from contratos.modulos.contratos.aplicacion.comandos.schemas import (
    ComandoArrendarPropiedad,
    ComandoAuditarContrato,
    ComandoCancelarContratoAuditado,
)
from contratos.modulos.contratos.aplicacion.eventos.schemas import (
    ContratoAuditado,
    ContratoAuditoriaRechazada,
    PropiedadArrendada,
    PropiedadArrendamientoRechazado,
)
from contratos.seedwork.aplicacion.comandos import Comando
from contratos.seedwork.dominio.eventos import EventoIntegracion
from contratos.seedwork.aplicacion.saga import CoordinadorSaga, Paso
from contratos.config.logger import logger

logger = logger.getChild("saga-contratos")


class SagaContratos(CoordinadorSaga):
    @staticmethod
    def pasos() -> list[Paso]:
        return [
            Paso(
                index=0,
                comando=ComandoAuditarContrato,
                evento=ContratoAuditado,
                error=ContratoAuditoriaRechazada,
                compensacion=None,
            ),
            Paso(
                index=1,
                comando=ComandoArrendarPropiedad,
                evento=PropiedadArrendada,
                error=PropiedadArrendamientoRechazado,
                compensacion=ComandoCancelarContratoAuditado,
            ),
        ]

    def iniciar(self, comando: Comando):
        logger.info(f"Iniciando saga con comando {comando.__class__.__name__}")
        self.publicar_comando(comando)

    @staticmethod
    def eventos_a_escuchar() -> list[type[EventoIntegracion]]:
        eventos = []
        for paso in __class__.pasos():
            eventos.append(paso.evento)
            eventos.append(paso.error)

        return eventos

    def obtener_paso_dado_un_evento(self, evento: EventoIntegracion) -> Paso:
        logger.info(f"Obteniendo paso para evento {evento.__class__.__name__}")
        for paso in __class__.pasos():
            if isinstance(evento, paso.evento.__class__) or isinstance(
                evento, paso.error.__class__
            ):
                logger.info(
                    f"Paso encontrado para evento {evento.__class__.__name__}, paso: {paso.index}"
                )
                return paso

        raise Exception("Evento no hace parte de la transacción")

    def get_next_paso(self) -> Paso | None:
        if self.index == self.length() - 1:
            return None
        return self.pasos()[self.index + 1]

    def get_paso_actual(self) -> Paso:
        return self.pasos()[self.index]

    def completada(self):
        logger.info("Saga con id_correlacion %s completada", self.id_correlacion)
        super().completada()

    def revertida(self):
        logger.info("Saga con id_correlacion %s revertida", self.id_correlacion)
        super().revertida()

    def procesar_evento(self, evento: EventoIntegracion) -> None:
        paso = self.get_paso_actual()
        logger.info(
            "Paso actual: %s, procesando evento %s, evento esperado: %s, evento error: %s",
            paso.index,
            evento.__class__.__name__,
            paso.evento.__name__,
            paso.error.__name__,
        )
        self.last_event_processed = evento.__class__.__name__

        if isinstance(evento, paso.error):
            logger.info(
                "Evento de error %s comenza a procesar compensación",
                evento.__class__.__name__,
            )
            while self.index >= 0:
                logger.info(f"Procesando compensación para el index: {self.index}")
                paso = self.get_paso_actual()
                if paso.compensacion:
                    comando = paso.compensacion.from_evento(evento)
                    logger.info(
                        "Publicando comando de compensación para evento %s -> comando: %s index: %s",
                        evento.__class__.__name__,
                        comando.__class__.__name__,
                        paso.index,
                    )
                    self.publicar_comando(comando)
                else:
                    logger.info("No hay compensación para el paso actual")

                if self.index == 0:
                    return self.revertida()

                self.index -= 1

        elif isinstance(evento, paso.evento):
            logger.info(
                "Evento de éxito %s comienza a procesar el siguiente paso",
                evento.__class__.__name__,
            )
            next_paso = self.get_next_paso()
            if isinstance(next_paso, Paso):
                comando = next_paso.comando.from_evento(evento)
                logger.info(
                    "Publicando comando %s esperando recibir evento %s index: %s",
                    comando.__class__.__name__,
                    next_paso.evento.__class__.__name__,
                    next_paso.index,
                )
                self.publicar_comando(comando)
                self.index += 1
                return
            else:
                logger.info("No hay más pasos, index: %s terminando saga", self.index)
                return self.completada()

        logger.error(
            "Evento no esperado %s, id_correlacion evento %s, id_correlacion saga %s, index actual %s",
            evento.__class__.__name__,
            evento.id_correlacion,
            self.id_correlacion,
            self.index,
        )
        raise Exception("Evento no hace parte de la transacción")


log_manejador = logger.getChild("manejador-saga-contratos")


class ManejadorDeSaga:
    def __init__(self):
        from contratos.modulos.sagas.repository import RepositorioSagaContratosDB

        self.repositorio = RepositorioSagaContratosDB()

    @staticmethod
    def consumidores() -> list[Consumidor]:
        eventos = SagaContratos.eventos_a_escuchar()
        consumidores: list[Consumidor] = []
        for evento in eventos:
            consumidores.append(
                Consumidor(
                    mensaje=evento,
                    handler=lambda evento: ManejadorDeSaga().handler(evento),
                )
            )

        return consumidores

    def handler(self, evento: EventoIntegracion):
        id_correlacion = str(evento.id_correlacion)
        log_manejador.info(
            f"Manejando evento {evento.__class__.__name__} con id_correlacion {id_correlacion}"
        )
        saga = self.repositorio.obtener_por_id_or_none(id_correlacion)
        if saga:
            log_manejador.info(f"Saga encontrada con id_correlacion {id_correlacion}")
            saga.procesar_evento(evento)
            self.repositorio.persistir(saga)
            return

        log_manejador.info(
            f"Saga no encontrada con id_correlacion {evento.id_correlacion}"
        )

    def iniciar_saga(
        self, id_correlacion: str, comando_inicial: Comando
    ) -> SagaContratos:
        log_manejador.info(f"Creando nueva saga con id_correlacion {id_correlacion}")
        saga = SagaContratos(
            id_correlacion=id_correlacion,
            index=0,
            last_event_processed=None,
            last_command_dispatched=None,
            fecha_creacion=datetime.datetime.now(),
            fecha_actualizacion=datetime.datetime.now(),
        )
        self.repositorio.persistir(saga)
        saga.iniciar(comando=comando_inicial)
        self.repositorio.persistir(saga)
        return saga


consumidores: list[Consumidor] = ManejadorDeSaga.consumidores()
