import customtkinter as ctk
import pandas as pd
from pandas.errors import EmptyDataError
from selenium.webdriver import Chrome


linkk = "https://64.media.tumblr.com/3b9829cbb2d39d186cd38034fd92a904/tumblr_orj1utQBQp1vt7aw9o1_400.gif"
ctk.set_appearance_mode('dark')

ARQUIVO = "usuarios.csv"

def validar_login():
    usuario = campo_usuario.get().strip()
    senha = campo_senha.get().strip()

    if not usuario or not senha:
        resposta.configure(text='preencha usuario e senha', text_color='red')
        return

    try:
        df = pd.read_csv(ARQUIVO)
    except (FileNotFoundError, EmptyDataError):
        resposta.configure(text='nenhum usuario cadastrado', text_color='red')
        return

    senha_cripto = senha

    valido = df[
        (df["usuario"] == usuario) &
        (df["senha"] == senha_cripto)
    ]

    if not valido.empty:
        resposta.configure(text='login realizado com sucesso', text_color='green')
        browser = Chrome()
        browser.get(linkk)
    else:
        resposta.configure(text='usuario ou senha incorretos', text_color='red')


def registrar_usuario():
    usuario = campo_usuario.get().strip()
    senha = campo_senha.get().strip()
    codigo = campo_codigo.get().strip()

    if not usuario or not senha or not codigo:
        resposta.configure(text='preencha todos os campos', text_color='red')
        return

    if codigo != "123":
        resposta.configure(text='codigo de verificacao invalido', text_color='red')
        return

    try:
        df = pd.read_csv(ARQUIVO)
    except (FileNotFoundError, EmptyDataError):
        df = pd.DataFrame(columns=["usuario", "senha"])

    # verifica se usuário já existe
    if usuario in df["usuario"].values:
        resposta.configure(text='usuario ja existe', text_color='orange')
        return

    senha_cripto = senha

    novo_usuario = pd.DataFrame({
        "usuario": usuario,
        "senha": senha_cripto
    })

    df = pd.concat([df, novo_usuario], ignore_index=True)
    df.to_csv(ARQUIVO, index=False)

    resposta.configure(text='usuario registrado com sucesso', text_color='green')

    campo_usuario.delete(0, 'end')
    campo_senha.delete(0, 'end')
    campo_codigo.delete(0, 'end')


app = ctk.CTk()
app.title('Login / Registro')
app.geometry('320x420')

ctk.CTkLabel(app, text='Usuario').pack(pady=10)
campo_usuario = ctk.CTkEntry(app, placeholder_text='digite o usuario')
campo_usuario.pack(pady=5)

ctk.CTkLabel(app, text='Senha').pack(pady=10)
campo_senha = ctk.CTkEntry(app, placeholder_text='digite a senha', show='*')
campo_senha.pack(pady=5)

ctk.CTkLabel(app, text='Codigo para registro').pack(pady=10)
campo_codigo = ctk.CTkEntry(app, placeholder_text='digite o codigo', show='*')
campo_codigo.pack(pady=5)

ctk.CTkButton(app, text='Login', command=validar_login).pack(pady=15)
ctk.CTkButton(app, text='Registrar', command=registrar_usuario).pack(pady=5)

resposta = ctk.CTkLabel(app, text='')
resposta.pack(pady=15)

app.mainloop()