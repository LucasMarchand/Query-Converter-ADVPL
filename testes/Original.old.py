import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import filedialog

class Application:
	def __init__(self, master=None):
		self.fontePadrao = ("Calibri", "10")
		self.primeiroContainer = Frame(master)
		self.primeiroContainer["pady"] = 10

		self.primeiroContainer.pack()

		self.segundoContainer = Frame(master)
		self.segundoContainer["padx"] = 20
		self.segundoContainer.pack()

		self.terceiroContainer = Frame(master)
		self.terceiroContainer["pady"] = 20
		self.terceiroContainer.pack()

		self.titulo = Label(self.primeiroContainer, text="Coverte para ADVPL")
		self.titulo["font"] = ("Calibri", "11", "bold")
		self.titulo.pack()

		self.nomeLabel = Label(self.segundoContainer, text="Nome do arquivo  ", font=self.fontePadrao, justify=RIGHT)
		self.nomeLabel.pack(side=LEFT)

		self.nome = Entry(self.segundoContainer, cursor="ARROW")
		self.nome["width"] = 30
		self.nome["font"] = self.fontePadrao
		self.nome.pack(side=RIGHT)

		self.trans = Button(self.terceiroContainer)
		self.trans["text"] = "Transformar"
		self.trans["font"] = ("Calibri", "8")
		self.trans["width"] = 12
		self.trans["command"] = self.Transformar
		self.trans.pack()

		self.msg = Label(self.terceiroContainer, text="", font=self.fontePadrao)
		self.msg.pack()
   
	def Transformar(self):
		#nome_arq = self.nome.get()
		Tk().withdraw()
		Tk().filename = filedialog.askopenfilename(filetypes = (("Apenas arquivo texto", "*.txt"), ("Todos arquivos", "*")))
		file = Tk().filename
		try :
			#ref_arq = open('C:\\Users\\' + os.getlogin() + '\\Desktop\\' + nome_arq + '.txt', 'r')
			ref_arq = open(file, 'r')
			if True :
				for i, linha in enumerate(ref_arq) :
				    if i == 0 : 
				        texto = 'cQuery := \" ' + linha.replace('\n', '') + '  \"\n'
				    else :
				        texto += 'cQuery += \" ' + linha.replace('\n', '') + '  \"\n'
				ref_arq.close()
				novo_arq = open('C:\\Users\\' + os.getlogin() + '\\Desktop\\Query_Alterada.txt', 'w')
				novo_arq.write(texto)
				novo_arq.close()	
			self.msg["text"] = 'Feito! Olhar o arquivo \'Query_Alterada\'.'
		except :
			self.msg["text"] = 'Não existe arquivo chamado \'' + nome_arq + '\'. Tente novamente...\n'
			

root = Tk()
style = ttk.Style(root)
style.theme_use("clam")
Application(root)
root.mainloop()