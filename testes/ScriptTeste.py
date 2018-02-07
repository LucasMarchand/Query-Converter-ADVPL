import os

while True :
	try :
		nome_arq = input('Entre com o nome do arquivo que está na sua área de trabalho: ')
		ref_arq = open('C:\\Users\\' + os.getlogin() + '\\Desktop\\' + nome_arq + '.txt', 'r')
	except :
		print('Não existe arquivo chamado \'', nome_arq, '\'. Tente novamente...\n')
	else :
		break

for i, linha in enumerate(ref_arq) :
    if i == 0 : 
        texto = 'cQuery := \" ' + linha.replace('\n', '') + '  \"\n'
    else :
        texto += 'cQuery += \" ' + linha.replace('\n', '') + '  \"\n'
ref_arq.close()
novo_arq = open('C:\\Users\\' + os.getlogin() + '\\Desktop\\Teste_Alterado.txt', 'w')
novo_arq.write(texto)
novo_arq.close()