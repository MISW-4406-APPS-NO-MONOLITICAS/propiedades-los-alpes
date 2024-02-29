from pydispatch import dispatcher
from .handlers import HandlerTransaccionDominio

dispatcher.connect(HandlerTransaccionDominio.handle_transaccion_creada, signal='TransaccionCreadaDominio')
