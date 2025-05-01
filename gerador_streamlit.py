import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta
from babel.dates import format_date
import re
import os
import smtplib
import unicodedata
from email.message import EmailMessage
from dotenv import load_dotenv
import num2words
from fpdf import FPDF

# 🔐 Carrega variáveis de ambiente
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
    valor_float = float(valor.replace('.', '').replace(',', '.'))
    valor_inteiro = int(valor_float)
    return num2words.num2words(valor_inteiro, lang='pt_BR').upper()

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
    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = destinatario
    msg.set_content(corpo)
    msg.add_attachment(anexo_bytes, maintype='application', subtype='pdf', filename=nome_arquivo)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_REMETENTE, SENHA_EMAIL)
        smtp.send_message(msg)

# ========= Streamlit App =========
st.set_page_config(page_title="Gerador de Contratos", page_icon="📋")
pagina = st.sidebar.radio("Navegação", ["Preencher Contrato", "Revisar e Gerar PDF"])

# ===== Página 1: Preenchimento =====
if pagina == "Preencher Contrato":
    st.title("📝 Gerador de Contrato")
    tipo_termo = st.selectbox("📄 Tipo de contrato:", ["Prestação de Serviço", "Outro"])
    titulo_capa = "TERMO DE PRESTAÇÃO DE SERVIÇOS" if tipo_termo == "Prestação de Serviço" else st.text_input("Digite o nome do termo:").upper()

    st.subheader("🡩‍💼 Dados do Contratante")
    nome_contratante = st.text_input("Nome completo:")
    estado_civil_contratante = st.text_input("Estado civil:")
    rg_contratante = st.text_input("RG:")
    tipo_doc_contratante = st.selectbox("Documento:", ["CPF", "CNPJ"])
    doc_contratante = st.text_input("Número do documento:")
    if tipo_doc_contratante == "CPF" and doc_contratante:
        doc_contratante = formatar_cpf(doc_contratante)
    if tipo_doc_contratante == "CNPJ" and doc_contratante:
        doc_contratante = formatar_cnpj(doc_contratante)
    endereco_contratante = st.text_input("Endereço:")

    st.subheader("🡩‍🎓 Dados do Contratado")
    nome_contratado = st.text_input("Nome completo contratado:")
    nacionalidade_contratado = st.text_input("Nacionalidade:")
    estado_civil_contratado = st.text_input("Estado civil contratado:")
    rg_contratado = st.text_input("RG contratado:")
    tipo_doc_contratado = st.selectbox("Documento contratado:", ["CPF", "CNPJ"])
    doc_contratado = st.text_input("Número do documento contratado:")
    if tipo_doc_contratado == "CPF" and doc_contratado:
        doc_contratado = formatar_cpf(doc_contratado)
    if tipo_doc_contratado == "CNPJ" and doc_contratado:
        doc_contratado = formatar_cnpj(doc_contratado)
    endereco_contratado = st.text_input("Endereço contratado:")

    st.subheader("📄 Informações do Contrato")
    servico = st.text_area("Serviço contratado:")
    valor = st.text_input("Valor do serviço (ex: 2.000,00):")
    forma_pagamento = st.text_input("Forma de pagamento:")
    tempo_servico = st.text_input("Tempo de serviço (ex: '6 meses'):")
    data_inicio = st.text_input("Data de início (ex: 01/05/2025):")
    cidade = st.text_input("Cidade:")
    estado = st.text_input("Estado (sigla):")
    dias_rescisao = st.text_input("Dias de aviso prévio:")
    testemunha1_nome = st.text_input("Nome da testemunha 1:")
    testemunha1_cpf = st.text_input("CPF da testemunha 1:")
    testemunha2_nome = st.text_input("Nome da testemunha 2:")
    testemunha2_cpf = st.text_input("CPF da testemunha 2:")

    if st.button("➡️ Avançar para Revisão"):
        try:
            inicio = datetime.strptime(data_inicio, "%d/%m/%Y")
            quantidade, unidade = tempo_servico.split()
            quantidade = int(quantidade)
            termino = inicio + relativedelta(months=quantidade if "mes" in unidade else 0,
                                             days=quantidade if "dia" in unidade else 0)
            data_termino = termino.strftime("%d/%m/%Y")
            data_formatada = format_date(inicio, format='d "de" MMMM "de" y', locale='pt_BR')
        except:
            data_termino = ""
            data_formatada = ""

        contrato_texto = f"""
{titulo_capa}

Pelo presente instrumento particular, de um lado, o(a) CONTRATANTE {nome_contratante}, brasileiro(a), {estado_civil_contratante}, portador(a) da Carteira de Identidade nº {rg_contratante} e inscrito(a) no {tipo_doc_contratante} nº {doc_contratante}, residente a {endereco_contratante}; e, de outro lado, o(a) CONTRATADO(A) {nome_contratado}, {nacionalidade_contratado}, {estado_civil_contratado}, portador(a) da Carteira de Identidade nº {rg_contratado} e inscrito(a) no {tipo_doc_contratado} nº {doc_contratado}, residente a {endereco_contratado}.

Têm, entre si, justo e contratado, o presente {titulo_capa}, que se regerá pelas seguintes cláusulas:

CLÁUSULA PRIMEIRA - DO OBJETO:
{servico}

CLÁUSULA SEGUNDA - DO VALOR E FORMA DE PAGAMENTO:
O(a) CONTRATANTE pagará ao(à) CONTRATADO(A) o valor total de R$ {valor} ({valor_por_extenso(valor)} REAIS), a ser pago da seguinte forma: {forma_pagamento}.

CLÁUSULA TERCEIRA - DO TEMPO DE SERVIÇO:
O serviço terá duração de {tempo_servico}, com início em {data_inicio} e término previsto para {data_termino}.

CLÁUSULA QUARTA - DAS OBRIGAÇÕES DO(A) CONTRATANTE:
Fornecer todas as informações necessárias para a execução dos serviços, efetuar os pagamentos pontualmente e cumprir as demais obrigações previstas neste contrato.

CLÁUSULA QUINTA - DAS OBRIGAÇÕES DO(A) CONTRATADO(A):
Prestar os serviços com diligência, qualidade e dentro dos prazos estabelecidos.

CLÁUSULA SEXTA - DA RESCISÃO:
O presente contrato poderá ser rescindido mediante comunicação prévia, por escrito, com antecedência mínima de {dias_rescisao} dias.

CLÁUSULA SÉTIMA - DO FORO:
Para dirimir quaisquer dúvidas oriundas deste contrato, fica eleito o foro da Comarca de {cidade} - {estado}.

{cidade}, {data_formatada}.

______________________________________
{nome_contratante}

______________________________________
{nome_contratado}

______________________________________
Testemunha 1 – Nome: {testemunha1_nome}  CPF: {testemunha1_cpf}

______________________________________
Testemunha 2 – Nome: {testemunha2_nome}  CPF: {testemunha2_cpf}
        """

        st.session_state.contrato_texto = contrato_texto
        st.success("Minuta pronta! Vá para a aba 'Revisar e Gerar PDF'.")

# ===== Página 2: Revisão e Envio =====
if pagina == "Revisar e Gerar PDF":
    st.title("📄 Revisar e Gerar Contrato")
    contrato_texto = st.session_state.get("contrato_texto", "")

    if not contrato_texto:
        st.warning("Preencha os dados na aba anterior primeiro.")
    else:
        contrato_editado = st.text_area("✍️ Edite o contrato abaixo:", contrato_texto, height=600)

        if st.button("📄 Gerar PDF"):
            st.session_state.pdf_bytes = gerar_pdf_com_texto(contrato_editado)
            st.success("✅ PDF gerado com sucesso!")

        if st.session_state.get("pdf_bytes"):
            st.download_button(
                label="📅 Baixar Contrato em PDF",
                data=st.session_state.pdf_bytes,
                file_name="contrato_gerado.pdf",
                mime="application/pdf"
            )

        email_destinatario = st.text_input("📧 Digite o e-mail do cliente para envio do contrato:")

        if st.button("📬 Enviar por e-mail"):
            if email_destinatario:
                try:
                    enviar_email(
                        destinatario=email_destinatario,
                        assunto="📄 Seu contrato está pronto!",
                        corpo="Olá! Segue em anexo o contrato gerado pela plataforma.",
                        anexo_bytes=st.session_state.pdf_bytes,
                        nome_arquivo="contrato_gerado.pdf"
                    )
                    st.success("📧 E-mail enviado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao enviar: {e}")
            else:
                st.warning("Digite um e-mail válido para envio.")
