from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import datetime
import os

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


@app.route("/")
def inicio():
  
