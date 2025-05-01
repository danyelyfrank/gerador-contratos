#variaveis é um nome e não pode nome de comando do python 
#o código executa de cima para baixo. Definir as variaveis primeiro e depois faz o comando, se não vai aparecer o erro.
# "="- recebe
#int= numeros inteiros, float= numeros com casas decimais; strings = textos; booleen = booleanos(true or false)

faturamento = 1100
custo = 600
novas_vendas = 150000
faturamento = novas_vendas + faturamento
lucro = faturamento - custo

mensagem = print ("O faturamento da loja é de"), faturamento

print("O faturamento =", faturamento)
print("O custo =", custo)
print("O Lucro =", faturamento - custo)

#operadores especiais
#mod -> % - percentual - resto da divisão de um numero pelo outro 
#10 % 3 - qual é o resto da divisão? 
print(10 % 3)