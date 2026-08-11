from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from models import db, Usuario, Transacao
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from decimal import Decimal
 
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "uma-chave-secreta-aqui"

db.init_app(app)


@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        if not email or not senha:
            flash(
                            "Email e senha são obrigatórios.",
                            "error"
                )
            return redirect(url_for("login"))

        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            flash(
                            "Email ou senha inválidos.",
                            "error"
                )
            return redirect(url_for("login"))

        if not check_password_hash(usuario.senha, senha):
            flash(
                            "Email ou senha inválidos.",
                            "error"
                )
            return redirect(url_for("login"))

        session["usuario_id"] = usuario.id

        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/cadastro", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        confirmsenha = request.form["confirmar_senha"]

        if not nome or not email or not senha:
            flash("Todos os campos são obrigatórios.", "error")
            return redirect(url_for("register"))

        if Usuario.query.filter_by(email=email).first():
            flash("Email já cadastrado.", "error")
            return redirect(url_for("register"))

        if senha != confirmsenha:
            flash("As senhas não coincidem.", "error")
            return redirect(url_for("register"))

        senha_hash = generate_password_hash(senha)

        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha_hash
        )
        db.session.add(novo_usuario)
        db.session.commit()

        session["usuario_id"] = novo_usuario.id
        flash(
                        "Conta criada com sucesso.",
                        "sucesso"
            )

        return redirect(url_for("dashboard"))

    return render_template("cadastro.html")


@app.route("/dashboard")
def dashboard():

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    usuario = db.session.execute(
        db.select(Usuario).where(Usuario.id == session["usuario_id"])
    ).scalars().first()

    if not usuario:
        session.clear()
        return redirect(url_for("login"))

    transacoes = db.session.execute(
        db.select(Transacao).where(
            Transacao.usuario_id == usuario.id
        )
    ).scalars().all()

    total_entradas = sum(
        t.valor
        for t in transacoes
        if t.tipo == "entrada"
    )

    total_saidas = sum(
        t.valor
        for t in transacoes
        if t.tipo == "saida"
    )

    saldo = total_entradas - total_saidas

    return render_template(
        "dashboard.html",
        usuario=usuario,
        transacoes=transacoes,
        total_entradas=total_entradas,
        total_saidas=total_saidas,
        saldo=saldo
    )

@app.route("/transacao/nova", methods=["GET", "POST"])
def nova_transacao():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        descricao = request.form["descricao"]
        valor = request.form["valor"]
        categoria = request.form["categoria"]
        tipo = request.form["tipo"]

        if not descricao or not valor or not categoria or not tipo:
            return flash(
                            "Todos os campos são obrigatórios.",
                            "error"
                )

        try:
            valor = float(valor)
        except ValueError:
            return flash(
                            "Valor inválido.",
                            "error"
                )

        nova_transacao = Transacao(
            descricao=descricao,
            valor=valor,
            categoria=categoria,
            tipo=tipo,
            usuario_id=session["usuario_id"]
        )
        db.session.add(nova_transacao)
        db.session.commit()
        flash(
                        "Transação criada com sucesso.",
                        "sucesso"
            )

    return render_template("nova_transacao.html")

@app.route("/transacao/<int:transacao_id>/deletar", methods=["GET","POST"])
def deletar_transacao(transacao_id):

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    transacao = db.session.get(Transacao, transacao_id)

    if not transacao:
        return "Transação não encontrada", 404

    if transacao.usuario_id != session["usuario_id"]:
        return "Acesso negado", 403

    db.session.delete(transacao)
    db.session.commit()
    
    flash(
                "Transação excluída com sucesso.",
                "sucesso"
    )
    return redirect(url_for("dashboard"))

@app.route("/transacao/<int:id>/editar", methods=["GET", "POST"])
def editar_transacao(id):

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    transacao = db.session.get(Transacao, id)

    if not transacao:
        return "Transação não encontrada", 404

    # Impede um usuário de editar a transação de outro
    if transacao.usuario_id != session["usuario_id"]:
        return "Acesso negado", 403

    if request.method == "POST":

        transacao.descricao = request.form["descricao"]
        transacao.valor = Decimal(request.form["valor"])
        transacao.tipo = request.form["tipo"]
        transacao.categoria = request.form["categoria"]

        transacao.data = datetime.strptime(
            request.form["data"],
            "%Y-%m-%d"
        )

        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template(
        "editar_transacao.html",
        transacao=transacao
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)