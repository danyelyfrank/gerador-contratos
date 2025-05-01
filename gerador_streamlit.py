import streamlit as st
from fpdf import FPDF
from datetime import datetime
from dateutil.relativedelta import relativedelta
from babel.dates import format_date
import re

# Função para formatar CPF

def formatar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return None

# Função para formatar CNPJ

def formatar_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) == 14:
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return None

# Função para converter valor para extenso

def valor_por_extenso(valor):
    import num2words
    valor_float = float(valor.replace('.', '').replace(',', '.'))
    valor_inteiro = int(valor_float)
    return num2words.num2words(valor_inteiro, lang='pt_BR').upper()

# Função para gerar o PDF

def gerar_pdf_com_texto(texto, nome_contratante):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, texto.strip())
    return pdf.output(dest='S').encode('latin1')

# ========== Streamlit App ==========
st.set_page_config(page_title="Gerador de Contratos", page_icon="📝")
st.title("📝 Gerador de Contratos Automático")
st.markdown("---")

st.subheader("📜 Tipo de Termo")
tipo_termo = st.selectbox("Escolha o tipo de contrato:", ["Prestação de Serviço", "Outro"])

titulo_capa = "TERMO DE PRESTAÇÃO DE SERVIÇOS" if tipo_termo == "Prestação de Serviço" else st.text_input("Digite o nome do termo:").upper()

# Dados do Contratante
with st.container():
    st.subheader("🧐 Dados do Contratante")
    nome_contratante = st.text_input("Nome completo do(a) contratante:")
    estado_civil_contratante = st.text_input("Estado civil do(a) contratante:")
    rg_contratante = st.text_input("RG do(a) contratante:")
    tipo_doc_contratante = st.selectbox("Documento do Contratante:", ["CPF", "CNPJ"])
    doc_contratante = st.text_input(f"Número do {tipo_doc_contratante} do contratante:")
    if tipo_doc_contratante == "CPF" and doc_contratante:
        doc_contratante = formatar_cpf(doc_contratante) or doc_contratante
    if tipo_doc_contratante == "CNPJ" and doc_contratante:
        doc_contratante = formatar_cnpj(doc_contratante) or doc_contratante
    endereco_contratante = st.text_input("Endereço do(a) contratante:")

# Dados do Contratado
with st.container():
    st.subheader("🧑‍🏫 Dados do Contratado")
    nome_contratado = st.text_input("Nome completo do(a) contratado(a):")
    nacionalidade_contratado = st.text_input("Nacionalidade do(a) contratado(a):")
    estado_civil_contratado = st.text_input("Estado civil do(a) contratado(a):")
    rg_contratado = st.text_input("RG do(a) contratado(a):")
    tipo_doc_contratado = st.selectbox("Documento do Contratado:", ["CPF", "CNPJ"])
    doc_contratado = st.text_input(f"Número do {tipo_doc_contratado} do contratado:")
    if tipo_doc_contratado == "CPF" and doc_contratado:
        doc_contratado = formatar_cpf(doc_contratado) or doc_contratado
    if tipo_doc_contratado == "CNPJ" and doc_contratado:
        doc_contratado = formatar_cnpj(doc_contratado) or doc_contratado
    endereco_contratado = st.text_input("Endereço do(a) contratado(a):")

# Dados do Contrato
with st.container():
    st.subheader("📄 Informações do Contrato")
    servico = st.text_area("Serviço contratado:")
    valor = st.text_input("Valor do serviço (ex: 2.000,00):")
    forma_pagamento = st.text_input("Forma de pagamento:")
    tempo_servico = st.text_input("Tempo de serviço (ex: '6 meses' ou '180 dias'):")
    data_inicio = st.text_input("Data de início (ex: 01/05/2025):")

    data_termino = ""
    data_formatada = ""
    if data_inicio and tempo_servico:
        try:
            inicio = datetime.strptime(data_inicio, "%d/%m/%Y")
            quantidade, unidade = tempo_servico.split()
            quantidade = int(quantidade)
            if "mes" in unidade:
                termino = inicio + relativedelta(months=quantidade)
            else:
                termino = inicio + relativedelta(days=quantidade)
            data_termino = termino.strftime("%d/%m/%Y")
            data_formatada = format_date(inicio, format='d "de" MMMM "de" y', locale='pt_BR')
        except:
            pass

    cidade = st.text_input("Cidade do foro:")
    estado = st.text_input("Estado (sigla, ex: RR):")
    dias_rescisao = st.text_input("Dias de aviso prévio para rescisão:")

    testemunha1_nome = st.text_input("Nome da testemunha 1:")
    testemunha1_cpf = st.text_input("CPF da testemunha 1:")
    testemunha2_nome = st.text_input("Nome da testemunha 2:")
    testemunha2_cpf = st.text_input("CPF da testemunha 2:")

st.markdown("---")

if st.button("🚀 Gerar Minuta para Revisão"):
    if all([nome_contratante, estado_civil_contratante, rg_contratante, doc_contratante,
            endereco_contratante, nome_contratado, nacionalidade_contratado, estado_civil_contratado,
            rg_contratado, doc_contratado, endereco_contratado, servico, valor, forma_pagamento,
            tempo_servico, data_inicio, cidade, estado, dias_rescisao]):

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

        contrato_editado = st.text_area("✍️ Revise ou edite o contrato abaixo antes de gerar o PDF:", contrato_texto.strip(), height=600)

        if st.button("📄 Gerar PDF com texto editado"):
            pdf_bytes = gerar_pdf_com_texto(contrato_editado, nome_contratante)
            st.success("✅ Contrato gerado com sucesso!")
            st.download_button(
                label="📅 Baixar Contrato em PDF",
                data=pdf_bytes,
                file_name=f"contrato_{nome_contratante.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
    else:
        st.error("⚠️ Por favor, preencha todos os campos corretamente antes de gerar o contrato.")