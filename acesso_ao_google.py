import customtkinter as ctk
import pandas as pd
from pandas.errors import EmptyDataError
from selenium.webdriver import Chrome


linkk = "https://www.google.com/"
ctk.set_appearance_mode('dark')

ARQUIVO = "usuarios.csv"

#login
def validar_login():
    usuario = campo_usuario.get().strip()
    senha = campo_senha.get().strip()

    try:
        df = pd.read_csv(ARQUIVO)
    except (FileNotFoundError, EmptyDataError):
        resposta.configure(text='erro no arquivo de usuarios', text_color='red')
        return

    valido = df[
        (df["usuario"] == usuario) &
        (df["senha"] == senha)
    ]

    if not valido.empty:
        resposta.configure(text='login realizado com sucesso', text_color='green')
        browser = Chrome()
        browser.get(linkk)
    else:
        resposta.configure(text='usuario ou senha incorretos', text_color='red')


#Registro
def registrar_usuario():
    usuario = campo_usuario.get().strip()
    senha = campo_senha.get().strip()

    if not usuario or not senha:
        resposta.configure(text='preencha todos os campos', text_color='red')
        return

    try:
        df = pd.read_csv(ARQUIVO)
    except (FileNotFoundError, EmptyDataError):

        df = pd.DataFrame(columns=["usuario", "senha"])

    # verifica se usuário já existe
    if usuario in df["usuario"].values:
        resposta.configure(text='usuario ja existe', text_color='orange')
        return

    # adiciona novo usuário
    novo_usuario = pd.DataFrame(
        [{"usuario": usuario, "senha": senha}]
    )

    df = pd.concat([df, novo_usuario], ignore_index=True)

    # salva no CSV
    df.to_csv(ARQUIVO, index=False)

    resposta.configure(text='usuario registrado com sucesso', text_color='green')

    campo_usuario.delete(0, 'end')
    campo_senha.delete(0, 'end')


app = ctk.CTk()
app.title('Login / Registro')
app.geometry('320x420')

ctk.CTkLabel(app, text='Usuario').pack(pady=10)
campo_usuario = ctk.CTkEntry(app, placeholder_text='digite o usuario')
campo_usuario.pack(pady=5)

ctk.CTkLabel(app, text='Senha').pack(pady=10)
campo_senha = ctk.CTkEntry(app, placeholder_text='digite a senha', show='*')
campo_senha.pack(pady=5)

ctk.CTkButton(app, text='Login', command=validar_login).pack(pady=15)
ctk.CTkButton(app, text='Registrar', command=registrar_usuario).pack(pady=5)

resposta = ctk.CTkLabel(app, text='')
resposta.pack(pady=15)

app.mainloop()
