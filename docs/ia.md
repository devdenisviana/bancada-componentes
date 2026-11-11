# Uso de IA

Usei o **Claude** (Anthropic) como assistente durante todo o projeto. Este
documento resume os prompts que mais pesaram e o que decidi eu mesmo.

## Prompts que importaram (resumidos)

1. **Entender o trabalho:** pedi que o Claude lesse os slides do Encontro 24 e
   resumisse as instruções do projeto final em um documento.
2. **Escolher a ideia:** pedi um passo a passo completo, a partir da ideia
   inicial, com sugestões para eu escolher. O Claude propôs cinco ideias de API
   de domínio único (reservas de salas, encurtador de URLs, empréstimo de
   componentes de bancada, carteira digital e pedidos de lanchonete).
3. **Modelar o domínio:** o Claude propôs as entidades, as seis regras de negócio
   e o uso do padrão Strategy; eu li e confirmei.
4. **Condução passo a passo:** combinei que só avançaríamos quando eu
   confirmasse cada passo, com um comando por vez, para corrigir erros sem
   confusão.
5. **Correções durante o caminho:** colei no chat os erros que apareceram (por
   exemplo, o aviso do lint sobre `Depends` e o problema do Docker Desktop
   fechado) e pedi a correção.

## Decisões que foram minhas

- Fazer o projeto no **nível B** e **individual**.
- Escolher a ideia do **inventário e empréstimo de componentes de bancada**
  (a opção 3 entre as sugeridas).
- Usar **Python + FastAPI** e **SQLite** como banco de dados.
- Aceitar as regras de negócio propostas (limite de 10 unidades por pessoa,
  prazo de 7 dias, controle de atraso) e a cobertura mínima de testes de 80%.
- Registrar no ADR o padrão Strategy, com as alternativas descartadas.

## Onde a IA errou ou precisou de ajuste

- Os primeiros comandos vieram para o terminal Linux, e eu uso o PowerShell no
  Windows; foram reescritos.
- Um endereço enviado no chat terminou com um ponto e foi copiado junto,
  resultando em "Not Found"; identifiquei pelo log do servidor.
- O lint acusou um falso alarme (`B008`) com o `Depends` do FastAPI, resolvido
  com uma configuração no `pyproject.toml`.

## Como verifiquei o que a IA sugeriu

- Executei os testes (unitários e de integração) e conferi a cobertura mínima.
- Testei a API manualmente pela documentação interativa (`/docs`), inclusive os
  casos de erro (limite excedido, por exemplo).
- Conferi o CI verde no GitHub e a persistência dos dados após recriar o container.
- Medi o desempenho com o k6, e os números do `docs/desempenho.md` vêm da saída
  real do teste.

## Sobre o código

O código foi escrito pelo Claude e aplicado por mim, arquivo por arquivo, com a
explicação de cada trecho. Reviso e consigo explicar o que entrego; as decisões
de projeto e de arquitetura estão registradas em `docs/adr/`.