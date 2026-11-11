from fastapi import APIRouter, Depends

from app.api.dependencias import obter_servico
from app.api.schemas import (
    ComponenteCriar,
    ComponenteSaida,
    EmprestimoCriar,
    EmprestimoSaida,
)
from app.services.bancada import BancadaService

router = APIRouter()


@router.post("/componentes", response_model=ComponenteSaida, status_code=201)
def criar_componente(
    dados: ComponenteCriar, servico: BancadaService = Depends(obter_servico)
):
    return servico.cadastrar_componente(
        dados.nome, dados.categoria, dados.quantidade_total
    )


@router.get("/componentes", response_model=list[ComponenteSaida])
def listar_componentes(servico: BancadaService = Depends(obter_servico)):
    return servico.listar_componentes()


@router.post("/emprestimos", response_model=EmprestimoSaida, status_code=201)
def criar_emprestimo(
    dados: EmprestimoCriar, servico: BancadaService = Depends(obter_servico)
):
    return servico.emprestar(dados.componente_id, dados.responsavel, dados.quantidade)


@router.post("/emprestimos/{emprestimo_id}/devolucao", response_model=EmprestimoSaida)
def devolver_emprestimo(
    emprestimo_id: int, servico: BancadaService = Depends(obter_servico)
):
    return servico.devolver(emprestimo_id)


@router.get("/emprestimos", response_model=list[EmprestimoSaida])
def listar_emprestimos(
    responsavel: str | None = None, servico: BancadaService = Depends(obter_servico)
):
    return servico.listar_emprestimos(responsavel)