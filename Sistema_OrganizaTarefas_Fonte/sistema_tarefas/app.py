from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "tarefas.db"
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
        #cria o banco e a tabela ao iniciar a aplicação
inicializar_banco =()

@app.route("/")
def inicio():
    filtro = request.args.get("status", "")
    busca = request.args.get("q", "").strip()
    sql = "SELECT * FROM tarefas WHERE 1=1"
    parametros = []
    if filtro in ("Pendente", "Em andamento", "Concluída"):
        sql += " AND status = ?"
        parametros.append(filtro)
    if busca:
        sql += " AND (titulo LIKE ? OR descricao LIKE ?)"
        parametros.extend([f"%{busca}%", f"%{busca}%"])
    sql += """ ORDER BY CASE prioridade
               WHEN 'Alta' THEN 1 WHEN 'Média' THEN 2 ELSE 3 END,
               CASE WHEN prazo IS NULL OR prazo = '' THEN 1 ELSE 0 END,
               prazo, id DESC"""
    with conectar() as conn:
        tarefas = conn.execute(sql, parametros).fetchall()
        totais = conn.execute("""
            SELECT COUNT(*) total,
                   SUM(CASE WHEN status='Pendente' THEN 1 ELSE 0 END) pendentes,
                   SUM(CASE WHEN status='Em andamento' THEN 1 ELSE 0 END) andamento,
                   SUM(CASE WHEN status='Concluída' THEN 1 ELSE 0 END) concluidas
            FROM tarefas
        """).fetchone()
    return render_template("index.html", tarefas=tarefas, totais=totais,
                           filtro=filtro, busca=busca)

@app.route("/nova", methods=["GET", "POST"])
def nova():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        prazo = request.form.get("prazo", "").strip()
        prioridade = request.form.get("prioridade", "Média")
        status = request.form.get("status", "Pendente")
        if not titulo:
            flash("Informe um título para a tarefa.", "erro")
            return render_template("form.html", tarefa=request.form, acao="Nova tarefa")
        if prioridade not in ("Baixa", "Média", "Alta") or status not in ("Pendente", "Em andamento", "Concluída"):
            flash("Selecione uma prioridade e um status válidos.", "erro")
            return render_template("form.html", tarefa=request.form, acao="Nova tarefa")
        with conectar() as conn:
            conn.execute("""INSERT INTO tarefas
                (titulo, descricao, prazo, prioridade, status, criado_em)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (titulo, descricao, prazo, prioridade, status, datetime.now().isoformat(timespec="seconds")))
        flash("Tarefa cadastrada com sucesso.", "sucesso")
        return redirect(url_for("inicio"))
    return render_template("form.html", tarefa={}, acao="Nova tarefa")

@app.route("/editar/<int:tarefa_id>", methods=["GET", "POST"])
def editar(tarefa_id):
    with conectar() as conn:
        tarefa = conn.execute("SELECT * FROM tarefas WHERE id=?", (tarefa_id,)).fetchone()
    if tarefa is None:
        flash("Tarefa não encontrada.", "erro")
        return redirect(url_for("inicio"))
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        prazo = request.form.get("prazo", "").strip()
        prioridade = request.form.get("prioridade", "Média")
        status = request.form.get("status", "Pendente")
        if not titulo:
            flash("Informe um título para a tarefa.", "erro")
            return render_template("form.html", tarefa=request.form, acao="Editar tarefa")
        if prioridade not in ("Baixa", "Média", "Alta") or status not in ("Pendente", "Em andamento", "Concluída"):
            flash("Selecione uma prioridade e um status válidos.", "erro")
            return render_template("form.html", tarefa=request.form, acao="Editar tarefa")
        with conectar() as conn:
            conn.execute("""UPDATE tarefas SET titulo=?, descricao=?, prazo=?,
                prioridade=?, status=? WHERE id=?""",
                (titulo, descricao, prazo, prioridade, status, tarefa_id))
        flash("Tarefa atualizada com sucesso.", "sucesso")
        return redirect(url_for("inicio"))
    return render_template("form.html", tarefa=tarefa, acao="Editar tarefa")

@app.route("/excluir/<int:tarefa_id>", methods=["POST"])
def excluir(tarefa_id):
    with conectar() as conn:
        conn.execute("DELETE FROM tarefas WHERE id=?", (tarefa_id,))
    flash("Tarefa excluída.", "sucesso")
    return redirect(url_for("inicio"))

if __name__ == "__main__":
    inicializar_banco()
    app.run(debug=False, host="127.0.0.1", port=5000)
