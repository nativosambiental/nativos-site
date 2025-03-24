from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/contato", methods=["POST"])
def contato():
    nome = request.form.get("nome")
    email = request.form.get("email")
    mensagem = request.form.get("mensagem")

    remetente = os.environ.get("EMAIL_USER")
    senha = os.environ.get("EMAIL_PASS")
    destinatario = os.environ.get("EMAIL_DEST") or remetente

    msg = MIMEText(f"Nome: {nome}\nE-mail: {email}\n\nMensagem:\n{mensagem}")
    msg["Subject"] = "Novo Contato do Site"
    msg["From"] = remetente
    msg["To"] = destinatario

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remetente, senha)
            server.sendmail(remetente, destinatario, msg.as_string())
        return "Mensagem enviada com sucesso!"
    except Exception as e:
        return f"Erro ao enviar mensagem: {e}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)