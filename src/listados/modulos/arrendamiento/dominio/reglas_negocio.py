class ReglaNegocio:
    def __init__(self, valor):
        self.valor = valor

    def validar_monto_arriendo(self) -> bool:
        if self.valor > 1:
            return True

        return False
