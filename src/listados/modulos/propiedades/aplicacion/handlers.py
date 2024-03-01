from pydispatch import dispatcher
from listados.modulos.contratos.dominio.eventos import TransaccionCreada
from listados.seedwork.aplicacion.handlers import Handler


class HandlerTransaccionDominio(Handler):
    @staticmethod
    def handle_transaccion_creada(evento):
        print("================ EVENTO DE DOMINIO TRANSACCION CREADA ================")


def registrar():
    dispatcher.connect(
        HandlerTransaccionDominio.handle_transaccion_creada,
        signal="TransaccionCreadaDominio",
    )
