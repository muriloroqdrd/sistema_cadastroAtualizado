
import sqlite3


def conectar():
    return sqlite3.connect("gestao_pedidos.db")


def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        telefone TEXT,
        numero TEXT,
        cor TEXT,
        tamanho TEXT,
        observacoes TEXT
    )
    """)

    # Mantém os dados existentes e troca o nome da coluna
    cursor.execute("PRAGMA table_info(pedidos)")
    colunas = [coluna[1] for coluna in cursor.fetchall()]

    if "telefone" in colunas and "gravacao" not in colunas:
        cursor.execute("""
        ALTER TABLE pedidos RENAME COLUMN telefone TO gravacao
        """)

    elif "gravacao" not in colunas:
        cursor.execute("""
        ALTER TABLE pedidos ADD COLUMN gravacao TEXT
        """)

    conexao.commit()
    conexao.close()


def adicionar_pedido(
    nome,
    gravacao,
    numero,
    cor,
    tamanho,
    observacoes
):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    INSERT INTO pedidos (
        nome,
        gravacao,
        numero,
        cor,
        tamanho,
        observacoes
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        nome,
        gravacao,
        numero,
        cor,
        tamanho,
        observacoes
    ))

    conexao.commit()
    conexao.close()


def listar_pedidos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT * FROM pedidos
    ORDER BY id DESC
    """)

    pedidos = cursor.fetchall()
    conexao.close()

    return pedidos


def excluir_pedido(id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    DELETE FROM pedidos
    WHERE id = ?
    """, (id,))

    conexao.commit()
    conexao.close()


def buscar_pedido_por_id(id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT * FROM pedidos
    WHERE id = ?
    """, (id,))

    pedido = cursor.fetchone()
    conexao.close()

    return pedido


def atualizar_pedido(
    id,
    nome,
    gravacao,
    numero,
    cor,
    tamanho,
    observacoes
):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    UPDATE pedidos
    SET
        nome = ?,
        gravacao = ?,
        numero = ?,
        cor = ?,
        tamanho = ?,
        observacoes = ?
    WHERE id = ?
    """, (
        nome,
        gravacao,
        numero,
        cor,
        tamanho,
        observacoes,
        id
    ))

    conexao.commit()
    conexao.close()


def buscar_pedidos_por_nome(nome):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT * FROM pedidos
    WHERE nome LIKE ?
    ORDER BY id DESC
    """, (f"%{nome}%",))

    pedidos = cursor.fetchall()
    conexao.close()

    return pedidos
