
from flask import Flask, render_template, request, redirect

from database import (
    criar_tabela,
    adicionar_pedido,
    listar_pedidos,
    buscar_pedido_por_id,
    atualizar_pedido,
    excluir_pedido,
    buscar_pedidos_por_nome
)

app = Flask(__name__)

criar_tabela()


@app.route("/")
def home():
    pesquisa = request.args.get("pesquisa", "")

    if pesquisa:
        lista_pedidos = buscar_pedidos_por_nome(pesquisa)
    else:
        lista_pedidos = listar_pedidos()

    return render_template(
        "index.html",
        pedidos=lista_pedidos,
        pesquisa=pesquisa
    )


@app.route("/pedidos")
def pedidos():
    lista_pedidos = listar_pedidos()

    return render_template(
        "pedidos.html",
        pedidos=lista_pedidos
    )


@app.route("/excluir/<int:id>")
def excluir(id):
    excluir_pedido(id)
    return redirect("/")


@app.route("/novo-pedido", methods=["GET", "POST"])
def novo_pedido():
    if request.method == "POST":
        nome = request.form["nome"]
        gravacao = request.form.get("gravacao", "")
        numero = request.form.get("numero", "")
        cor = request.form.get("cor", "")
        tamanho = request.form.get("tamanho", "")
        observacoes = request.form.get("observacoes", "")

        adicionar_pedido(
            nome,
            gravacao,
            numero,
            cor,
            tamanho,
            observacoes
        )

        return redirect("/")

    return render_template("novo_pedido.html")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    pedido = buscar_pedido_por_id(id)

    if pedido is None:
        return redirect("/")

    if request.method == "POST":
        nome = request.form["nome"]
        gravacao = request.form.get("gravacao", "")
        numero = request.form.get("numero", "")
        cor = request.form.get("cor", "")
        tamanho = request.form.get("tamanho", "")
        observacoes = request.form.get("observacoes", "")

        atualizar_pedido(
            id,
            nome,
            gravacao,
            numero,
            cor,
            tamanho,
            observacoes
        )

        return redirect("/")

    return render_template(
        "editar_pedido.html",
        pedido=pedido
    )


if __name__ == "__main__":
    app.run(debug=True)
