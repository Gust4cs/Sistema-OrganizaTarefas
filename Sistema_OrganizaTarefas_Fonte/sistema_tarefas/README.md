# OrganizaTarefas — Projeto Integrador

Aplicação web para cadastro, edição, exclusão, consulta e acompanhamento de tarefas.

## Requisitos
- Python 3.10 ou superior
- pip

## Como executar
1. Abra o terminal na pasta `sistema_tarefas`.
2. (Opcional, recomendado) Crie um ambiente virtual:
   - Windows: `py -m venv .venv` e `.venv\\Scripts\\activate`
   - Linux/macOS: `python3 -m venv .venv` e `source .venv/bin/activate`
3. Instale as dependências: `pip install -r requirements.txt`
4. Execute: `python app.py`
5. Acesse no navegador: http://127.0.0.1:5000

O banco SQLite `tarefas.db` é criado automaticamente na primeira execução.

## Funcionalidades
- Criar tarefas com título, descrição, prazo, prioridade e status.
- Editar os dados de uma tarefa.
- Excluir tarefas com confirmação.
- Pesquisar por título ou descrição.
- Filtrar por status.
- Visualizar indicadores de tarefas totais, pendentes, em andamento e concluídas.

## Observações
Projeto acadêmico demonstrativo. Para publicação em produção, recomenda-se configurar autenticação,
proteção CSRF, variáveis de ambiente, testes automatizados e servidor WSGI apropriado.
