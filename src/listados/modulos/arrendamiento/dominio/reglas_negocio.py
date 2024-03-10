class ReglaNegocio:
    def __init__(self, valor):
        self.valor = valor
        
  
    def validar_monto_arriendo(self)-> bool:
        case = {
            self.valor > 1: True,
            self.valor == 1: False,
            self.valor == 0: True
        }
        return case.get(True, False)
