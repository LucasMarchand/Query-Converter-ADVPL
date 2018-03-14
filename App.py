import os
import tkinter as tk
import subprocess
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import TclError
import tkinter.scrolledtext as tks

class Application:

	def Open(self): 
		self.filename = filedialog.askopenfilename(filetypes = (("Apenas arquivo SQL", "*.sql"), ("Apenas arquivo texto", "*.txt"), ("Todos arquivos", "*")), title = "Choose a file")	#
		try :
			if self.filename :
				self.box.delete(1.0, END)
				ref_arq = open(self.filename, 'rt')
				self.box.insert(INSERT, ref_arq.read())
				self.box["fg"] = "#0096e0"
				self.msg["text"] = "Arquivo selecionado: " + self.filename.split("/")[-1]
				self.msg["pady"] = 5
				self.msg["padx"] = 20
			else :
				self.msg["text"] = ""
				self.msg["pady"] = 0
				self.msg["padx"] = 0
				self.box.delete(1.0, END)
		except :
			messagebox.showerror(self.filename, "ERRO!")

	def Transforma(self):
		conteudo = self.box.get(1.0, END +'-1c')
		if conteudo != '' :
			try :
				conteudo = self.box.get(1.0, END)
				for i, linha in enumerate(conteudo.split('\n')) :
					if i == 0 : 
						texto = 'cQuery := \" ' + linha.replace('\n', '').strip(" ") + ' \"\n'
					elif i == len(conteudo.split('\n')) - 1 :
						texto
					else :
						if linha != '' :
							texto += 'cQuery += \" ' + linha.replace('\n', '').strip(" ") + '\"\n'
				self.box.delete(1.0, END)
				self.box.insert(INSERT, texto)

				# Copiar texto 
				self.box.clipboard_clear()
				self.box.clipboard_append(texto)
				self.box.update()
				self.box["fg"] = "#43ad69"
				messagebox.showinfo(self.filename, "Copiado para área de transferência")
			except Exception :
				self.msg["text"] = 'Não existe arquivo chamado \'' + filename.split("/")[-1] + '\'. Tente novamente...\n'
		else :
			messagebox.showerror(self.filename, "Nenhum conteúdo foi selecionado")
			self.msg["text"] = ''

	def Retorna(self):
		conteudo = self.box.get(1.0, END +'-1c')
		if conteudo != '' :
			try :
				conteudo = self.box.get(1.0, END)
				texto = ''
				for i, linha in enumerate(conteudo.split('\n')) :

					#if linha.find('//') != -1 :
						#linha.replace('//', '--')
						#texto += linha.replace('//', '--') 

					# elif linha.find('/*') != -1 :
					# 	if linha.find('*/') != -1 :
					# 		linha.replace('//', '--')

					if linha.find(':=') != -1 or linha.find('+=') != -1 :
						linha = linha.replace('//', '--')
						linha = linha[linha.find('"') + 1 : linha.find('"', -1)]
						texto += linha + '\n'

						print(linha.replace('"', '', -1))
					else :
						if i != len(conteudo.split('\n')):
							texto += linha + '\n'

					# if i == 0 :
					# 	texto = linha.strip("cQuery := \"").strip(linha[-1]) + '\n' if linha[-1] == '"' else linha.strip("cQuery := \"") + '\n'
					# else :
					# 	if linha != '' :
							
					# 		texto += linha.strip("cQuery += \"").strip(linha[-1]) + '\n' if linha[-1].rstrip() == '"' else linha.strip("cQuery += \"") + '\n'
							
							
					# 		if linha.find('=') != -1:
					# 			print(linha[linha.find('=') + 1:]) 
					# 		else: 
					# 			print('nope')
					# 	else :
					# 		print('útlima linha')

				#texto = texto.strip(texto.split('\n')[-1])
				self.box.delete(1.0, END)
				self.box.insert(INSERT, texto)
				#print(texto)
			except Exception :
				self.msg["text"] = 'Não existe arquivo chamado \'' + filename.split("/")[-1] + '\'. Tente novamente...\n'
		else:
			messagebox.showerror(self.filename, "Nenhum conteúdo foi selecionado")
			self.msg["text"] = ''

	def __init__(self, master=None):
		# Variáveis particulares
		filename = ""
		self.filename = filename

		# Blocos de layout
		self.fontePadrao = ("Calibri", 10)
		self.primeiroContainer = Frame(master)
		self.primeiroContainer["pady"] = 10
		self.primeiroContainer["padx"] = 20
		self.primeiroContainer.pack()

		self.segundoContainer = Frame(master)
		self.segundoContainer["padx"] = 20
		self.segundoContainer.pack()

		self.terceiroContainer = Frame(master)
		self.terceiroContainer["pady"] = 10
		self.terceiroContainer.pack()

		self.scrollContainer = Frame(master)
		self.scrollContainer.config(width=800, height=150, borderwidth=1)
		self.scrollContainer["pady"] = 10
		self.scrollContainer["padx"] = 20
		self.scrollContainer.pack()

		self.box = tks.ScrolledText(self.scrollContainer, font=self.fontePadrao)
		self.box.mark_set("insert", "1.0")
		self.box.see("insert")
		self.box.config(borderwidth='4', relief='groove')
		self.box.pack(fill="both", expand="true")

		self.btnAnexo = Button(self.terceiroContainer, text="Procurar arquivo", )
		self.btnAnexo["command"] = self.Open 
		self.btnAnexo["font"] = ("Calibri", "10")
		self.btnAnexo["bg"] = "#56c3f9"
		self.btnAnexo["width"] = 20
		self.btnAnexo.pack(padx=5, side=LEFT)

		self.msg = Label(self.segundoContainer, text="", font=self.fontePadrao)
		self.msg.pack(side=BOTTOM)

		self.trans = Button(self.terceiroContainer)
		self.trans["text"] = "Transformar"
		self.trans["font"] = ("Calibri", "10")
		self.trans["bg"] = "#5ae48c"
		self.trans["width"] = 20
		self.trans["command"] = self.Transforma
		self.trans.bind('<Control-c>', self.Transforma)
		self.trans.pack(padx=5, side=RIGHT)

		self.retorna = Button(self.terceiroContainer)
		self.retorna["text"] = "Retornar"
		self.retorna["font"] = ("Calibri", "10")
		#self.retorna["bg"] = "#5ae48c"
		self.retorna["width"] = 20
		self.retorna["command"] = self.Retorna
		#self.retorna.bind('<Control-c>', self.Retorna)
		self.retorna.pack(padx=5, side=RIGHT)

	def center_window(width=300, height=200):
		# get screen width and height
		screen_width = root.winfo_screenwidth()
		screen_height = root.winfo_screenheight()

		# calculate position x and y coordinates
		x = (screen_width/2) - (width/2)
		y = (screen_height/2) - (height/2)
		root.geometry('%dx%d+%d+%d' % (width, height, x, y))

def quit(event) :
	root.quit()

root = Tk()
Application(root)
Application.center_window(600,500)
root.title("cQuery")
root.mainloop()
