from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ComponenteModel(Base):
    __tablename__ = "componentes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    categoria: Mapped[str] = mapped_column(String(60))
    quantidade_total: Mapped[int]
    quantidade_disponivel: Mapped[int]


class EmprestimoModel(Base):
    __tablename__ = "emprestimos"

    id: Mapped[int] = mapped_column(primary_key=True)
    componente_id: Mapped[int] = mapped_column(ForeignKey("componentes.id"))
    responsavel: Mapped[str] = mapped_column(String(120), index=True)
    quantidade: Mapped[int]
    data_emprestimo: Mapped[date]
    data_prevista_devolucao: Mapped[date]
    status: Mapped[str] = mapped_column(String(20))
    data_devolucao: Mapped[date | None]
    dias_atraso: Mapped[int] = mapped_column(default=0)