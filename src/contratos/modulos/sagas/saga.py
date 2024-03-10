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
from contratos.seedwork.dominio.eventos import (
    EventoIntegracion,
    despachar_evento_integracion_localmente,
)
from contratos.seedwork.aplicacion.saga import CoordinadorSaga, Paso
from contratos.config.logger import logger

logger = logger.getChild("saga")


class SagaContratos(CoordinadorSaga):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger.getChild(self.id_correlacion)

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
        self.logger.info(f"Iniciando saga con comando {comando.__class__.__name__}")
        self.agregar_comando(comando)

    @staticmethod
    def eventos_a_escuchar() -> list[type[EventoIntegracion]]:
        eventos = []
        for paso in __class__.pasos():
            eventos.append(paso.evento)
            eventos.append(paso.error)

        return eventos

    def obtener_paso_dado_un_evento(self, evento: EventoIntegracion) -> Paso:
        self.logger.info(f"Obteniendo paso para evento {evento.__class__.__name__}")
        for paso in __class__.pasos():
            if isinstance(evento, paso.evento.__class__) or isinstance(
                evento, paso.error.__class__
            ):
                self.logger.info(
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

    def publicar_comandos(self):
        if len(self.comandos_a_publicar):
            self.logger.info(
                "Publicando comandos %s",
                ", ".join([c.__class__.__name__ for c in self.comandos_a_publicar]),
            )
        else:
            self.logger.info("No hay comandos para publicar")
        super().publicar_comandos()

    def completada(self):
        self.logger.info("Saga completada")
        super().completada()

    def revertida(self):
        self.logger.info("Saga revertida")
        super().revertida()

    def procesar_evento(self, evento: EventoIntegracion) -> None:
        paso = self.get_paso_actual()
        assert (
            evento.id_correlacion == self.id_correlacion
        ), "Id de correlación no coincide"

        self.logger.info(
            "Paso actual: %s, procesando evento %s, evento esperado: %s, evento error: %s",
            paso.index,
            evento.__class__.__name__,
            paso.evento.__name__,
            paso.error.__name__,
        )
        self.last_event_processed = evento.__class__.__name__

        if isinstance(evento, paso.error):
            if paso.dispatch_locally:
                self.logger.info(
                    "Evento de error %s primero se despacha localmente",
                    evento.__class__.__name__,
                )
                despachar_evento_integracion_localmente(evento)

            self.logger.info(
                "Evento de error %s comenza a procesar compensación",
                evento.__class__.__name__,
            )
            while self.index >= 0:
                self.logger.info(f"Procesando compensación para el index: {self.index}")
                paso = self.get_paso_actual()
                if paso.compensacion:
                    comando = paso.compensacion.from_evento(evento)
                    self.logger.info(
                        "Agregando comando de compensación para evento %s -> comando: %s index: %s",
                        evento.__class__.__name__,
                        comando.__class__.__name__,
                        paso.index,
                    )
                    self.agregar_comando(comando)
                else:
                    self.logger.info("No hay compensación para el paso actual")

                if self.index == 0:
                    return self.revertida()

                self.index -= 1

        elif isinstance(evento, paso.evento):
            if paso.dispatch_locally:
                self.logger.info(
                    "Evento de exito %s primero se despacha localmente",
                    evento.__class__.__name__,
                )
                despachar_evento_integracion_localmente(evento)
            self.logger.info(
                "Evento de éxito %s comienza a procesar el siguiente paso",
                evento.__class__.__name__,
            )
            next_paso = self.get_next_paso()
            if isinstance(next_paso, Paso):
                comando = next_paso.comando.from_evento(evento)
                self.logger.info(
                    "Agregando comando %s esperando recibir evento %s index: %s",
                    comando.__class__.__name__,
                    next_paso.evento.__name__,
                    next_paso.index,
                )
                self.agregar_comando(comando)
                self.index += 1
                return
            else:
                self.logger.info(
                    "No hay más pasos, index: %s terminando saga", self.index
                )
                return self.completada()

        self.logger.error(
            "Evento no esperado %s, index actual %s",
            evento.__class__.__name__,
            self.index,
        )
        raise Exception("Evento no hace parte de la transacción")


class ManejadorDeSaga:
    def __init__(self):
        from contratos.modulos.sagas.repository import RepositorioSagaContratosDB

        self.logger = logger.getChild("saga-manager")

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
        self.logger = logger.getChild(evento.id_correlacion)
        self.logger.info(f"Manejando evento {evento.__class__.__name__}")
        saga = self.repositorio.obtener_por_id_or_none(id_correlacion)
        if saga:
            self.logger.info(f"Saga encontrada")
            saga.procesar_evento(evento)
            self.repositorio.persistir(saga)
            saga.publicar_comandos()
            return

        self.logger.info(
            f"Saga no encontrada con id_correlacion {evento.id_correlacion}"
        )

    def iniciar_saga(
        self, id_correlacion: str, comando_inicial: Comando
    ) -> SagaContratos:
        self.logger = logger.getChild(id_correlacion)
        self.logger.info(f"Iniciando nueva saga con id_correlacion {id_correlacion}")
        saga = SagaContratos(
            id_correlacion=id_correlacion,
            index=0,
            last_event_processed=None,
            last_command_dispatched=None,
            fecha_creacion=datetime.datetime.now(),
            fecha_actualizacion=datetime.datetime.now(),
        )
        saga.iniciar(comando=comando_inicial)
        self.repositorio.persistir(saga)
        saga.publicar_comandos()

        return saga


consumidores: list[Consumidor] = ManejadorDeSaga.consumidores()
