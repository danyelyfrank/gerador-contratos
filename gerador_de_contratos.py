from fpdf import FPDF
from datetime import datetime
from num2words import num2words
from dateutil.relativedelta import relativedelta
import unicodedata

# Função para converter valor em extenso
def valor_por_extenso(valor):
    valor_float = float(valor.replace('.', '').replace(',', '.'))
    valor_inteiro = int(valor_float)
    extenso = num2words(valor_inteiro, lang='pt_BR').upper()
    return extenso

# Função para validar entrada de número
def input_numero(mensagem):
    while True:
        valor = input(mensagem)
        try:
            valor_float = float(valor.replace('.', '').replace(',', '.'))
            return valor
        except ValueError:
            print("⚠️ Por favor, digite apenas números. Exemplo: 2.000,00")

# Função para validar entrada de número inteiro
def input_inteiro(mensagem):
    while True:
        valor = input(mensagem)
        if valor.isdigit():
            return valor
        print("⚠️ Por favor, digite apenas números inteiros. Exemplo: 30")

# Função para validar tempo de serviço
def input_tempo_servico(mensagem):
    while True:
        tempo = input(mensagem).strip().lower()
        if tempo.endswith('meses') or tempo.endswith('dias'):
            partes = tempo.split()
            if len(partes) == 2 and partes[0].isdigit():
                return tempo
        print("⚠️ Por favor, informe corretamente o tempo (ex: '6 meses' ou '180 dias').")

# Função para validar entrada de data
def input_data(mensagem):
    while True:
        data = input(mensagem)
        try:
            datetime.strptime(data, "%d/%m/%Y")
            return data
        except ValueError:
            print("⚠️ Por favor, digite a data no formato correto: DD/MM/AAAA (exemplo: 01/05/2025).")

# Função para calcular data de término
def calcular_data_termino(data_inicio, tempo_servico):
    inicio = datetime.strptime(data_inicio, "%d/%m/%Y")
    quantidade, unidade = tempo_servico.split()
    quantidade = int(quantidade)
    if unidade == 'meses':
        termino = inicio + relativedelta(months=quantidade)
    elif unidade == 'dias':
        termino = inicio + relativedelta(days=quantidade)
    else:
        termino = inicio
    return termino.strftime("%d/%m/%Y")

# Função para remover acentos
def remover_acentos(txt):
    return ''.join(c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn')

# Classe para PDF personalizado
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, titulo_capa, ln=True, align='C')
        self.ln(10)

# Escolha do tipo de contrato
print("\n=== Escolha o Modelo de Contrato ===")
print("1. Prestação de Serviços (Agentes de IA e Infoprodutos)")
print("2. Outro tipo de Termo Personalizado")

opcao_modelo = input("Digite 1 ou 2: ")

if opcao_modelo == "1":
    titulo_capa = "TERMO DE PRESTAÇÃO DE SERVIÇOS"
    print("\nDeseja escrever o serviço ou usar o padrão?")
    print("1. Escrever manualmente")
    print("2. Usar descrição padrão")
    escolha_servico = input("Digite 1 ou 2: ")
    if escolha_servico == "1":
        servico = input("Descreva o serviço: ")
    else:
        servico = "Criação de agentes de inteligência artificial personalizados e desenvolvimento de infoprodutos digitais."
else:
    termo_personalizado = input("Digite o nome do tipo de Termo (ex: Parceria, Locação): ")
    titulo_capa = f"TERMO DE {termo_personalizado.upper()}"
    servico = input("Descreva o serviço: ")

# Coleta dos dados
print("\n=== Etapa 1: Dados do(a) CONTRATANTE ===")
nome_contratante = input("Nome completo do(a) contratante: ")
estado_civil_contratante = input("Estado civil do(a) contratante: ")
rg_contratante = input("RG do(a) contratante: ")
cpf_contratante = input("CPF do(a) contratante: ")
endereco_contratante = input("Endereço do(a) contratante: ")

print("\n=== Etapa 2: Dados do(a) CONTRATADO(A) ===")
nome_contratado = input("Nome completo do(a) contratado(a): ")
nacionalidade_contratado = input("Nacionalidade do(a) contratado(a): ")
estado_civil_contratado = input("Estado civil do(a) contratado(a): ")
rg_contratado = input("RG do(a) contratado(a): ")
cpf_contratado = input("CPF do(a) contratado(a): ")
endereco_contratado = input("Endereço do(a) contratado(a): ")

print("\n=== Etapa 3: Dados do CONTRATO ===")
valor = input_numero("Valor do serviço (ex: 2.000,00): ")
forma_pagamento = input("Forma de pagamento (ex: 50% na assinatura, 50% na entrega): ")
tempo_servico = input_tempo_servico("Tempo de serviço contratado (ex: '6 meses' ou '180 dias'): ")
data_inicio = input_data("Data de início (ex: 01/05/2025): ")
data_termino = calcular_data_termino(data_inicio, tempo_servico)
dias_rescisao = input_inteiro("Número de dias para rescisão: ")
cidade = input("Cidade do foro: ")
estado = input("Estado do foro (sigla, ex: RR): ")

print("\n=== Etapa 4: Dados das TESTEMUNHAS ===")
testemunha1_nome = input("Nome da Testemunha 1: ")
testemunha1_cpf = input("CPF da Testemunha 1: ")
testemunha2_nome = input("Nome da Testemunha 2: ")
testemunha2_cpf = input("CPF da Testemunha 2: ")

# Converter valor para extenso
valor_extenso = valor_por_extenso(valor)

# Data completa formatada para rodapé
data_formatada = datetime.strptime(data_inicio, "%d/%m/%Y").strftime("%d de %B de %Y")

# Texto do contrato
contrato = f"""
Pelo presente instrumento particular, de um lado, o(a) CONTRATANTE {nome_contratante}, brasileiro(a), {estado_civil_contratante}, portador(a) da Carteira de Identidade nº {rg_contratante} e inscrito(a) no CPF nº {cpf_contratante}, residente em {endereco_contratante}; e, de outro lado, o(a) CONTRATADO(A) {nome_contratado}, {nacionalidade_contratado}, {estado_civil_contratado}, portador(a) da Carteira de Identidade nº {rg_contratado} e inscrito(a) no CPF nº {cpf_contratado}, residente em {endereco_contratado}.

Têm, entre si, justo e contratado, o presente {titulo_capa}, que se regerá pelas seguintes cláusulas:

CLÁUSULA PRIMEIRA - DO OBJETO:
{servico}

CLÁUSULA SEGUNDA - DO VALOR E FORMA DE PAGAMENTO:
O(a) CONTRATANTE pagará ao(à) CONTRATADO(A) o valor total de R$ {valor} ({valor_extenso} REAIS), a ser pago da seguinte forma: {forma_pagamento}.

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
"""

# Corrigir caracteres especiais para o PDF
contrato = contrato.replace('–', '-').replace('—', '-')

# Criar o PDF
pdf = PDF()
pdf.add_page()
pdf.set_font("Arial", '', 12)

# Escrever o contrato justificado
pdf.multi_cell(0, 8, contrato)

# Espaçamento antes das assinaturas
pdf.ln(15)

# Assinaturas
pdf.cell(0, 10, '_________________________________', ln=True, align='C')
pdf.cell(0, 10, f'CONTRATANTE: {nome_contratante}', ln=True, align='C')
pdf.ln(8)

pdf.cell(0, 10, '_________________________________', ln=True, align='C')
pdf.cell(0, 10, f'CONTRATADO(A): {nome_contratado}', ln=True, align='C')
pdf.ln(8)

pdf.cell(0, 10, '_________________________________', ln=True, align='C')
pdf.cell(0, 10, f'TESTEMUNHA 1: {testemunha1_nome} - CPF: {testemunha1_cpf}', ln=True, align='C')
pdf.ln(8)

pdf.cell(0, 10, '_________________________________', ln=True, align='C')
pdf.cell(0, 10, f'TESTEMUNHA 2: {testemunha2_nome} - CPF: {testemunha2_cpf}', ln=True, align='C')

# Gerar nome do arquivo
agora = datetime.now()
data_hora = agora.strftime("%Y-%m-%d_%H-%M-%S")
nome_arquivo = f"contrato_{remover_acentos(nome_contratante.replace(' ', '_'))}_{data_hora}.pdf"

# Salvar o PDF
pdf.output(nome_arquivo)

print(f"\n✅ Contrato salvo como {nome_arquivo} com sucesso!")

