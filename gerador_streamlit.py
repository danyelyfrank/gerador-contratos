import streamlit as st
from fpdf import FPDF
from datetime import datetime
from dateutil.relativedelta import relativedelta
from babel.dates import format_date
import re
import yagmail
from dotenv import load_dotenv
import os
import unicodedata  # ✅ para normalizar os caracteres especiais

# 🔐 Carrega variáveis do .env
load_dotenv()
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
SENHA_EMAIL = os.getenv("SENHA_EMAIL")

# ========= Funções =========
def formatar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return None

def formatar_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) == 14:
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return None

def valor_por_extenso(valor):
    import num2words
    valor_float = float(valor.replace('.', '').replace(',', '.'))
    valor_inteiro = int(valor_float)
    return num2words.num2words(valor_inteiro, lang='pt_BR').upper()

# ✅ nova função para limpar caracteres que causam erro no PDF
def limpar_texto(texto):
    texto = texto.replace("–", "-").replace("“", '"').replace("”", '"')
    return unicodedata.normalize("NFKD", texto).encode("latin1", "ignore").decode("latin1")

def gerar_pdf_com_texto(texto):
    texto_limpo = limpar_texto(texto)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, texto_limpo.strip())
    return pdf.output(dest='S').encode('latin1')

def enviar_email(destinatario, assunto, corpo, anexo_bytes, nome_arquivo):
    yag = yagmail.SMTP(EMAIL_REMETENTE, SENHA_EMAIL)
    yag.send(
        to=destinatario,
        subject=assunto,
        contents=corpo,
        attachments=(nome_arquivo, anexo_bytes)
    )
