import streamlit as st
from fpdf import FPDF
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Função para gerar o PDF
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, dados['titulo_capa'], ln=True, align="C")
    pdf.ln(10)

    contrato = f"""
Pelo presente instrumento particular, de um lado, o(a) CONTRATANTE {dados['nome_contratante']}, brasileiro(a), {dados['estado_civil_contratante']}, portador(a) da Carteira de Identidade nº {dados['rg_contratante']} e inscrito(a) no {dados['tipo_doc_contratante']} nº {dados['doc_contratante']}, residente a {dados['endereco_contratante']}; e, de outro lado, o(a) CONTRATADO(A) {dados['nome_contratado']}, {dados['nacionalidade_contratado']}, {dados['estado_civil_contratado']}, portador(a) da Carteira de Identidade nº {dados['rg_contratado']} e inscrito(a) no {dados['tipo_doc_contratado']} nº {dados['doc_contratado']}, residente a {dados['endereco_contratado']}.

Têm, entre si, justo e contratado, o presente {dados['titulo_capa']}, que se regerá pelas seguintes cláusulas:

CLÁUSULA PRIMEIRA - DO OBJETO:
{dados['servico']}

CLÁUSULA SEGUNDA - DO VALOR E FORMA DE PAGAMENTO:
O(a) CONTRATANTE pagará ao(à) CONTRATADO(A) o valor total de R$ {dados['valor']} ({dados['valor_extenso']} REAIS), a ser pago da seguinte forma: {dados['forma_pagamento']}.

CLÁUSULA TERCEIRA - DO TEMPO DE SERVIÇO:
O serviço terá duração de {dados['tempo_servico']}, com início em {dados['data_inicio']} e término previsto para {dados['data_termino']}.

CLÁUSULA QUARTA - DAS OBRIGAÇÕES DO(A) CONTRATANTE:
Fornecer todas as informações necessárias para a execução dos serviços, efetuar os pagamentos pontualmente e cumprir as demais obrigações previstas neste contrato.

CLÁUSULA QUINTA - DAS OBRIGAÇÕES DO(A) CONTRATADO(A):
Prestar os serviços com diligência, qualidade e dentro dos prazos estabelecidos.

CLÁUSULA SEXTA - DA RESCISÃO:
O presente contrato poderá ser rescindido mediante comunicação prévia, por escrito, com antecedência mínima de {dados['dias_rescisao']} dias.

CLÁUSULA SÉTIMA - DO FORO:
Para dirimir quaisquer dúvidas oriundas deste contrato, fica eleito o foro da Comarca de {dados['cidade']} - {dados['estado']}.

{dados['cidade']}, {dados['data_formatada']}.
    """

    pdf.multi_cell(0, 8, contrato.strip())
    return pdf.output(dest='S').encode('latin1')

# Função para converter valor para extenso
def valor_por_extenso(valor):
    import num2words
    valor_float = float(valor.replace('.', '').replace(',', '.'))
    valor_inteiro = int(valor_float)
    return num2words.num2words(valor_inteiro, lang='pt_BR').upper()

# Streamlit App
st.title("📝 Gerador de Contratos")

# Escolha do tipo de contrato
st.subheader("Tipo de Termo")
tipo_termo = st.selectbox("Escolha o tipo de contrato:", ["Prestacão de Serviço", "Outro"])

if tipo_termo == "Outro":
    titulo_capa = st.text_input("Digite o nome do termo:").upper()
else:
    titulo_capa = "TERMO DE PRESTAÇÃO DE SERVIÇOS"

st.subheader("Dados do Contratante")
nome_contratante = st.text_input("Nome completo do(a) contratante:")
estado_civil_contratante = st.text_input("Estado civil do(a) contratante:")
rg_contratante = st.text_input("RG do(a) contratante:")
tipo_doc_contratante = st.selectbox("Documento do Contratante:", ["CPF", "CNPJ"])
doc_contratante = st.text_input(f"Número do {tipo_doc_contratante} do contratante:")
endereco_contratante = st.text_input("Endereço do(a) contratante:")

st.subheader("Dados do Contratado")
nome_contratado = st.text_input("Nome completo do(a) contratado(a):")
nacionalidade_contratado = st.text_input("Nacionalidade do(a) contratado(a):")
estado_civil_contratado = st.text_input("Estado civil do(a) contratado(a):")
rg_contratado = st.text_input("RG do(a) contratado(a):")
tipo_doc_contratado = st.selectbox("Documento do Contratado:", ["CPF", "CNPJ"])
doc_contratado = st.text_input(f"Número do {tipo_doc_contratado} do contratado:")
endereco_contratado = st.text_input("Endereço do(a) contratado(a):")

st.subheader("Dados do Contrato")
servico = st.text_area("Serviço contratado:")
valor = st.text_input("Valor do serviço (ex: 2.000,00):")
forma_pagamento = st.text_input("Forma de pagamento:")
tempo_servico = st.text_input("Tempo de serviço (ex: '6 meses' ou '180 dias'):")
data_inicio = st.text_input("Data de início (ex: 01/05/2025):")
data_termino = ""
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
    except:
        pass
cidade = st.text_input("Cidade do foro:")
estado = st.text_input("Estado (sigla, ex: RR):")
dias_rescisao = st.text_input("Dias de aviso prévio para rescisão:")

# Botão para gerar contrato
if st.button("📄 Gerar Contrato"):
    if all([nome_contratante, rg_contratante, doc_contratante, endereco_contratante, nome_contratado, nacionalidade_contratado, estado_civil_contratado, rg_contratado, doc_contratado, endereco_contratado, servico, valor, forma_pagamento, tempo_servico, data_inicio, cidade, estado, dias_rescisao]):

        dados = {
            'titulo_capa': titulo_capa,
            'nome_contratante': nome_contratante,
            'estado_civil_contratante': estado_civil_contratante,
            'rg_contratante': rg_contratante,
            'tipo_doc_contratante': tipo_doc_contratante,
            'doc_contratante': doc_contratante,
            'endereco_contratante': endereco_contratante,
            'nome_contratado': nome_contratado,
            'nacionalidade_contratado': nacionalidade_contratado,
            'estado_civil_contratado': estado_civil_contratado,
            'rg_contratado': rg_contratado,
            'tipo_doc_contratado': tipo_doc_contratado,
            'doc_contratado': doc_contratado,
            'endereco_contratado': endereco_contratado,
            'servico': servico,
            'valor': valor,
            'valor_extenso': valor_por_extenso(valor),
            'forma_pagamento': forma_pagamento,
            'tempo_servico': tempo_servico,
            'data_inicio': data_inicio,
            'data_termino': data_termino,
            'dias_rescisao': dias_rescisao,
            'cidade': cidade,
            'estado': estado,
            'data_formatada': datetime.strptime(data_inicio, "%d/%m/%Y").strftime("%d de %B de %Y")
        }

        pdf_bytes = gerar_pdf(dados)

        st.success("✅ Contrato gerado com sucesso!")

        st.download_button(
            label="📥 Baixar Contrato em PDF",
            data=pdf_bytes,
            file_name=f"contrato_{nome_contratante.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
    else:
        st.error("⚠️ Por favor, preencha todos os campos corretamente!")
