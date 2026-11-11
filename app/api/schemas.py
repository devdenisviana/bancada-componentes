from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.domain.emprestimo import StatusEmprestimo


class ComponenteCriar(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    categoria: str = Field(min_length=1, max_length=60)
    quantidade_total: int = Field(ge=0)


class ComponenteSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    categoria: str
    quantidade_total: int
    quantidade_disponivel: int


class EmprestimoCriar(BaseModel):
    componente_id: int
    responsavel: str = Field(min_length=1, max_length=120)
    quantidade: int


class EmprestimoSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    componente_id: int
    responsavel: str
    quantidade: int
    data_emprestimo: date
    data_prevista_devolucao: date
    status: StatusEmprestimo
    data_devolucao: date | None
    dias_atraso: int