app = Flask(__name__)
app.secret_key = "chave-local-do-projeto-integrador"


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def inicializar_banco():
    with conectar() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                prazo TEXT,
                prioridade TEXT NOT NULL DEFAULT 'Média',
                status TEXT NOT NULL DEFAULT 'Pendente',
                criado_em TEXT NOT NULL
            )
        """)


@app.route("/editar/<int:tarefa_id>", methods=["GET", "POST"])
def editar(tarefa_id):
    ...


@app.route("/excluir/<int:tarefa_id>", methods=["POST"])
def excluir(tarefa_id):
    ...


if __name__ == "__main__":
    inicializar_banco()
    app.run(debug=False, host="127.0.0.1", port=5000)
