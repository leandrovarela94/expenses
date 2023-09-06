import re
from datetime import datetime

from pydantic import BaseModel, Field, validator


class Despesas(BaseModel):
    nome: str
    valor: float
    data_vencimento: datetime
    prioridade: str

    @validator('data_vencimento', always=True)
    def validation_date(cls, value):

        regex = '^\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}:\d{2}(?:\.\d*)?(?:[-+]\d{2}:\d{2})?)?(?:Z)?$'

        if re.match(regex, value):
            print(f' O value é {value} e está correto')

        return value
