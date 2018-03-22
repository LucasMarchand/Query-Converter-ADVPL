import os
import tkinter as tk
import tkinter.scrolledtext as tkscroll
from tkinter import filedialog
from tkinter import messagebox
from tkinter import TclError
from tkinter import *


class Application:

	def __init__(self, master=None):
		# Variáveis particulares
		self.red = "#ff2828"
		self.blue = "#0038bb"
		self.green = "#17a91c"		
		self.filename = ""

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
		self.scrollContainer.config(width=100, height=10, borderwidth=1)
		self.scrollContainer["padx"] = 20
		self.scrollContainer.pack()

		self.msg = Label(self.segundoContainer, text="", font=self.fontePadrao)
		self.msg.pack(side=BOTTOM)

		self.box = tkscroll.ScrolledText(self.scrollContainer, font=self.fontePadrao)
		self.box.mark_set("insert", "1.0")
		self.box.see("insert")
		self.box.config(borderwidth='1', relief='groove')
		self.box["width"] = 1000
		self.box["height"] = 1000
		self.box.pack(fill="both", expand="true", pady=(10,20))

		self.btnAnexo = Button(self.terceiroContainer, text="Procurar arquivo", width="20", height="1", font=self.fontePadrao)
		self.btnAnexo["command"] = self.Open 
		self.btnAnexo["bg"] = "#56c3f9"
		self.btnAnexo.pack(padx=10, side=LEFT)

		self.trans = Button(self.terceiroContainer, text="ADVPL", width="20", height="1", font=self.fontePadrao)
		self.trans["bg"] = "#5ae48c"
		self.trans["command"] = self.Transforma
		self.trans.bind('<Control-c>', self.Transforma)
		self.trans.pack(padx=10, side=RIGHT)

		self.retorna = Button(self.terceiroContainer, text="SQL", width="20", height="1", font=self.fontePadrao)
		self.retorna["bg"] = "#ff2828"
		self.retorna["command"] = self.Retorna
		self.retorna.bind('<Control-c>', self.Retorna)
		self.retorna.pack(padx=10, side=RIGHT)


	def Open(self): 
		try :
			self.filename = filedialog.askopenfilename(filetypes = (("Apenas arquivo SQL", "*.sql"), ("Apenas arquivo texto", "*.txt"), ("Todos arquivos", "*")), title = "Choose a file")

			if self.filename :
				self.box.delete(1.0, END)
				ref_arq = open(self.filename, 'rt')
				self.box.insert(INSERT, ref_arq.read())
				self.box["fg"] = self.blue
				self.msg["text"] = "Arquivo selecionado: " + self.filename.split("/")[-1]
				self.msg["pady"] = 5
				self.msg["padx"] = 20
			else :
				self.msg["text"] = ""
				self.msg["pady"] = 0
				self.msg["padx"] = 0
				self.box.delete(1.0, END)
		except Exception :
			messagebox.showerror('Except', 'Não foi possível abrir o arquivo selecionado.\n')


	def Transforma(self):
		conteudo = self.box.get(1.0, END +'-1c')
		if conteudo != '' :
			try :
				conteudo = self.box.get(1.0, END)
				texto = ''
				for i, linha in enumerate(conteudo.split('\n')) :
					if linha.find('--') != -1 :
						texto += "//"	# se achar '--'					

					if i == 0 :
						texto += 'cQuery := \" ' + linha.replace('\n', '').replace('--', '') + ' \"\n'
					else :
						if linha != '' : texto += 'cQuery += \" ' + linha.replace('\n', '').replace('--', '') + ' \"\n'
				
				texto = texto.rstrip('\n')
				self.insereTexto(texto)
				self.box["fg"] = self.green

			except Exception :
				messagebox.showerror('Except', "Nõa foi possível realizar a conversão. Reanalise o código!")
		else :
			self.msg["text"] = "Nenhum conteúdo foi selecionado"


	def Retorna(self):
		conteudo = self.box.get(1.0, END +'-1c')
		if conteudo != '' :
			try :
				conteudo = self.box.get(1.0, END)
				texto = ''
				for i, linha in enumerate(conteudo.split('\n')):
					if linha.find('//') != -1 :
						texto += '--'	
						linha = linha.replace('//', '')				

					if linha.find(':=') != -1 or linha.find('+=') != -1 :

						ini = linha.find('"') + 1 
						fim = len(linha) - linha[::-1].find('"') - 1
						linha = linha[ ini : fim ] 

						texto += linha + '\n'

					else :
						if i != len(conteudo.split('\n')):
							texto += linha + '\n'

				texto = texto.rstrip('\n')
				self.insereTexto(texto)
				self.box["fg"] = self.red

			except Exception:
				messagebox.showerror('Except', "Não foi possível realizar a conversão. Reanalise o código!")
		else:
			self.msg["text"] = "Nenhum conteúdo foi selecionado"


	def insereTexto(self, texto):

		self.box.delete(1.0, END)
		self.box.insert(INSERT, texto)
		
		# Copiar texto 
		self.box.clipboard_clear()
		self.box.clipboard_append(texto)
		self.box.update()

		self.msg["text"] = 'Copiado para área de transferência'


	def center_window(width=600, height=500):
		# get screen width and height
		screen_width = root.winfo_screenwidth()
		screen_height = root.winfo_screenheight()

		# calculate position x and y coordinates
		x = (screen_width/2) - (width/2)
		y = (screen_height/2) - (height/2)
		root.geometry('%dx%d+%d+%d' % (width, height, x, y))


def quit(event):
	root.quit()


root = Tk()
Application(root)
Application.center_window(1000,800)
root.title("cQuery")
root.mainloop()
