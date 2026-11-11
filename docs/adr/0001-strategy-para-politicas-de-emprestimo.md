# ADR 0001: Strategy para as políticas de empréstimo

- **Status:** Aceita
- **Data:** 11/11/2026

## Contexto

Todo empréstimo de componente segue duas regras que podem variar: o **limite de
unidades em aberto por pessoa** (hoje, 10) e o **prazo de devolução** (hoje,
7 dias). É razoável imaginar que essas regras mudem, por exemplo com um limite
maior ou um prazo mais longo para professores ou para o uso em laboratório.

Precisamos decidir onde essas regras ficam no código, de forma que mudá-las não
exija alterar a lógica do empréstimo.

## Decisão

Usar o padrão de projeto **Strategy**:

- `PoliticaEmprestimo` é o contrato (uma classe abstrata) com dois métodos:
  `limite_por_pessoa()` e `prazo_em_dias()`.
- `PoliticaPadrao` é a implementação atual (10 unidades e 7 dias).
- `Emprestimo.abrir(...)` e `BancadaService` recebem a política como parâmetro,
  sem conhecer os valores concretos.

## Alternativas consideradas

**Alternativa descartada: constantes fixas dentro do código do empréstimo**
(por exemplo `LIMITE = 10` e `PRAZO = 7` em `emprestimo.py`).
Seria a opção mais curta, mas qualquer mudança de regra exigiria editar a
lógica central, e os testes não conseguiriam exercitar valores diferentes sem
alterar o código de produção.

**Alternativa descartada: ler limite e prazo de variáveis de ambiente.**
Permitiria ajustar os valores sem mexer no código, mas só troca *números*, não
*regras*. Uma política que dependa de quem pede (por exemplo, perfil de
professor) não cabe em uma variável de ambiente.

## Consequências

- **Positivas:** novas políticas entram criando uma classe nova, sem alterar o
  código existente; os testes usam uma política própria para provar isso (veja
  `test_politica_customizada_altera_limite_e_prazo`); o domínio continua sem
  depender de configuração externa.
- **Negativas:** há uma classe e uma abstração a mais para um sistema que hoje
  tem uma única política; a política ainda não é escolhida por configuração ou
  por requisição, apenas injetada no serviço.