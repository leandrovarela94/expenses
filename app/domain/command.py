from datetime import datetime

from pydantic import BaseModel


class Command(BaseModel):
    pass


class DespesasCommand(Command):
    nome: str
    valor: float
    data_vencimento: datetime
    prioridade: str

    def get_command(self):
        return DespesasCommand(nome=self.nome, valor=self.valor, data_vencimento=self.data_vencimento, prioridade=self.prioridade)
