from auditorias.seedwork.dominio.reglas import ReglaNegocio

class ValorMayorQueCero(ReglaNegocio):
    valor: float

    def __init__(self, valor, mensaje='El valor no es mayor a cero'):
        super().__init__(mensaje)
        self.valor = valor

    def es_valido(self) -> bool:
        return self.valor > 0
