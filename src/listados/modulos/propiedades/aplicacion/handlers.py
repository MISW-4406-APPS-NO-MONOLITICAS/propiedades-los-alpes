from listados.modulos.contratos.dominio.eventos import TransaccionCreada
from listados.seedwork.aplicacion.handlers import Handler

class HandlerTransaccionDominio(Handler):

    @staticmethod
    def handle_transaccion_creada(evento):
        print('================ EVENTO DE DOMINIO TRANSACCION CREADA ================')