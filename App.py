import os
import tkinter as tk
from tkinter import *
import tkinter.scrolledtext as tkscroll
from tkinter import filedialog
from tkinter import messagebox
from tkinter import TclError


class Application:

	def __init__(self, master=None):
		
		# Variáveis particulares
		self.red 	= "#ff2828"
		self.blue 	= "#0038bb"
		self.green 	= "#17a91c"
		self.orange = "#e86d00"
		self.black 	= "#000000"
		self.filename = ""

		# Blocos de layout
		self.fonteCustom1 = ("Calibri", 10)
		self.fonteCustom2 = ("Calibri", 12, "bold")

		self.primeiroContainer = Frame(master)
		self.primeiroContainer.pack()

		self.segundoContainer = Frame(master)
		self.segundoContainer["pady"] = 10
		self.segundoContainer.pack()

		self.terceiroContainer = Frame(master)
		self.terceiroContainer.pack()

		# Objetos da janela
		self.msg = Label(self.primeiroContainer, text="", font=self.fonteCustom1)
		self.msg.pack(pady=[10,0], side=BOTTOM)

		self.btnAnexo = Button(self.segundoContainer, text="Procurar arquivo", width="20", height="1", font=self.fonteCustom1)
		self.btnAnexo["command"] = self.Open 
		self.btnAnexo["bg"] = "#56c3f9"
		self.btnAnexo.pack(padx=10, side=LEFT)

		self.btnADVPL = Button(self.segundoContainer, text="ADVPL", width="20", height="1", font=self.fonteCustom1)
		self.btnADVPL["bg"] = "#5ae48c"
		self.btnADVPL["command"] = self.transADVPL
		self.btnADVPL.bind('<Control-c>', self.transADVPL)
		self.btnADVPL.pack(padx=10, side=RIGHT)

		self.btnSQL = Button(self.segundoContainer, text="SQL", width="20", height="1", font=self.fonteCustom1)
		self.btnSQL["bg"] = "#ff8e2a"
		self.btnSQL["command"] = self.transSQL
		self.btnSQL.bind('<Control-c>', self.transSQL)
		self.btnSQL.pack(padx=10, side=RIGHT)

		self.textbox = Entry(self.terceiroContainer)
		#self.textbox["width"] = 30
		self.textbox["font"] = self.fonteCustom1
		self.textbox.insert(0, "cQuery")
		self.textbox.pack()

		self.scrollContainer = Frame(master)
		self.scrollContainer.config(width=100, height=10, borderwidth=1)
		self.scrollContainer["padx"] = 20
		self.scrollContainer.pack()

		self.box = tkscroll.ScrolledText(self.scrollContainer, font=self.fonteCustom1)
		self.box.mark_set("insert", "1.0")
		self.box.see("insert")
		self.box.config(borderwidth='1', relief='groove')
		self.box["width"] = 1000
		self.box["height"] = 1000
		self.box["fg"] = self.black
		self.box.pack(fill="both", expand="true", pady=(10,20))


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
				self.msg["fg"] = self.black
				self.msg["font"] = self.fonteCustom1
			else :
				self.msg["text"] = ""
				self.msg["pady"] = 0
				self.msg["padx"] = 0
				self.msg["font"] = self.fonteCustom1
				self.box.delete(1.0, END)
		except Exception :
			messagebox.showerror('Except', 'Não foi possível abrir o arquivo selecionado.\n')


	def transADVPL(self):
		conteudo = self.box.get(1.0, END +'-1c')
		if conteudo != '' :
			try :
				conteudo = self.box.get(1.0, END)
				texto = ''
				for i, linha in enumerate(conteudo.split('\n')) :
					if linha.find('--') != -1 :
						texto += "//"	# se achar '--'					

					if i == 0 :
						texto += self.textbox.get() + ' := \" ' + linha.replace('\n', '').replace('--', '') + ' \"\n'
					else :
						if linha != '' : texto += self.textbox.get() + ' += \" ' + linha.replace('\n', '').replace('--', '') + ' \"\n'
				
				texto = texto.rstrip('\n')
				self.insereTexto(texto)
				self.box["fg"] = self.green

			except Exception :
				messagebox.showerror('Except', "Não foi possível realizar a conversão. Reanalise o código do meu programa!")
		else :
			self.msg["text"] = "Nenhum conteúdo foi selecionado"


	def transSQL(self):
		conteudo = self.box.get(1.0, END +'-1c')
		if conteudo != '' :
			try :
				conteudo = self.box.get(1.0, END)
				texto = ''
				for i, linha in enumerate(conteudo.split('\n')):
					
					pos_aspas_1 = linha.find('"')
					pos_aspas_2 = linha.find("'")

					if linha.find('//') != -1 :
						texto += '--'	
						linha = linha.replace('//', '')				

					if linha.find(':=') != -1 or linha.find('+=') != -1:

						# Verifica o caractere correto que delimita o código SQL
						if pos_aspas_1 != -1 and pos_aspas_2 != -1:			# Se existir os dois tipos de aspas na linha
							
							# Verifica qual vem antes
							if pos_aspas_1 < pos_aspas_2: 	
								ini = pos_aspas_1 + 1
								fim = len(linha) - linha[::-1].find('"') - 1

							if pos_aspas_1 > pos_aspas_2:
								ini = pos_aspas_2 + 1
								fim = len(linha) - linha[::-1].find("'") - 1

						elif pos_aspas_1 != -1:			# Se existir apenas as aspas [""]
							ini = pos_aspas_1 + 1
							fim = len(linha) - linha[::-1].find('"') - 1

						else:							# Se existir apenas as aspas ['']
							ini = pos_aspas_2 + 1
							fim = len(linha) - linha[::-1].find("'") - 1


						linha = linha[ ini : fim ] 
						texto += linha + '\n'

					else :
						if i != len(conteudo.split('\n')):
							texto += linha + '\n'

				texto = texto.rstrip('\n')
				self.insereTexto(texto)
				self.box["fg"] = self.orange
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

		self.msg["text"] = 'Copiado para área de transferência (Ctrl + C)'
		self.msg["fg"] = self.red
		self.msg["font"] = self.fonteCustom2


	def center_window(width, height):
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
