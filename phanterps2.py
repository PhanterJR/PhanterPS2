# -*- coding: utf-8 -*- 
import wx
import wx.html
import os
import iso9660
import re

corrente = os.getcwd()

#Interface

class meu_splash(wx.App): 
	def OnInit(self):
		
		bmp = wx.Image ( corrente +'\imagens\conexao.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		
		wx.SplashScreen ( bmp, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT, 1200, None, style = wx.NO_BORDER | wx.SIMPLE_BORDER | wx.STAY_ON_TOP ) 
		wx.Yield() 
		return True


class meu_programa(wx.App):
	def OnInit(self):

		favicon = wx.Icon(corrente +'\imagens\\favicon.png', wx.BITMAP_TYPE_ANY)
		self.title = "PhanterPS2"
		frame = meu_frame(self.title, (-1,-1), (450,340))
		frame.SetIcon(favicon) 
		frame.Show()
		self.SetTopWindow(frame)
		return True

class meu_frame(wx.Frame):
	def __init__ (self, title, pos, size):

		self.text = '''
		<html>
		<body bgcolor="#ACAA60">
		<center><table bgcolor="#455481" width="100%" cellspacing="0"
		cellpadding="0" border="1">
		<tr>
		<td align="center"><h1>Sketch!</h1></td>
		</tr>
		</table>
		</center>
		<p><b>Sketch</b> is a demonstration program for
		<b>wxPython In Action</b>
		Chapter 6. It is based on the SuperDoodle demo included
		with wxPython, available at http://www.wxpython.org/
		</p>
		<p><b>SuperDoodle</b> and <b>wxPython</b> are brought to you by
		<b>Robin Dunn</b> and <b>Total Control Software</b>, Copyright
		&copy; 1997-2006.</p>
		</body>
		</html>'''
		self.title = "PhanterPS2"
		imagem1 = wx.Image ( corrente+'\imagens\isops2.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imagem2 = wx.Image ( corrente+'\imagens\salvar.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imagem3 = wx.Image ( corrente+'\imagens\sobre.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()

		wx.Frame.__init__(self, None, -1, title, pos, size)
		painel = wx.Panel(self)
		barra_de_status = self.CreateStatusBar()
		self.SetStatusText("Bem vindo ao PhanterPS2")
		barra_de_ferramentas = self.CreateToolBar()
		tool1 = barra_de_ferramentas.AddSimpleTool(wx.NewId(), imagem1 , "Novo Iso", u"Selecionar imagens iso dos jogos")
		barra_de_ferramentas.AddSimpleTool(wx.NewId(), imagem2 , "Salvar", u"Salvar as configurações")
		barra_de_ferramentas.AddSimpleTool(wx.NewId(), imagem3 , "Sobre", u"Sobre o programa e autor")
		barra_de_ferramentas.Realize()
		Barra_de_menu = wx.MenuBar()
		menu1 = wx.Menu()
		Item_submenu1 = menu1.Append(-1, "A&dicionar novo(s) iso(s)", u"Selecionar imagens iso dos jogos")
		Item_submenu2 = menu1.Append(-1, "Salvar", u"Salvar configurações")
		Barra_de_menu.Append(menu1, "&Arquivo")

		self.Bind(wx.EVT_MENU, self.AbrirIso, Item_submenu1)
		self.Bind(wx.EVT_TOOL, self.AbrirIso, tool1)
		self.SetMenuBar(Barra_de_menu)

		html = wx.html.HtmlWindow(self)
		html.SetPage(self.text)
		button = wx.Button(self, wx.ID_OK, "Okay")
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(html, 1, wx.EXPAND|wx.ALL, 5)
		sizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		self.SetSizer(sizer)
		self.Layout()


#ações

	wildcard = "Imagem iso (*.iso)|*.iso|All files (*.*)|*.*"
	def AbrirIso (self, event):
		dlg = wx.FileDialog(self, u"Selecionando Imagem...", corrente, style=wx.MULTIPLE, wildcard=self.wildcard)
		if dlg.ShowModal() == wx.ID_OK:
			self.arquivoiso = dlg.GetPaths()
			self.nomeiso = dlg.GetFilenames()

			self.ReadFile(self.arquivoiso)
			nomes=''
			for nome in self.nomeiso:
				nomes += nome+', '
			nomes = nomes[0:-2] + '.'
			if len(nomes) > 100:
				nomes = nomes[0:100] +'...'

			self.SetTitle(self.title + ' - Adicionando:  ' + nomes)
			dlg.Destroy()
	
	def ReadFile(self, arquivosiso):
		resultados =[]
		for arquivoiso in arquivosiso:
			#print "verificando: " + arquivoiso
			result = verifica_jogo(arquivoiso)
			#print "resultado: %s" %(result)
			#print "==============================="
			resultados.append(result)
		self.resultados = resultados

		pass
	def SalveConf(self, event):
		pass
	def PastaDoJogo (self, event):
		dlg = wx.DirDialog(self, u"Abrindo arquivo de configuração...", corrente, style=wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.dir = dlg.GetPath()
			self.SetTitle(self.title + ' -- ' + self.filename)
			dlg.Destroy()

# Logica

procura_cod_e_nome = re.compile(r'([a-zA-Z]{4}_[0-9]{3}\.[0-9]{2}\..*\.[iI][sS][oO])')
procura_nome_e_cod_no_ul = re.compile(r'([ a-zA-Z0-9]*.*ul\.[ a-zA-Z0-9]{4}_[0-9]{3}\.[0-9]{2})')
procura_apenas_cod = re.compile(r'^/([a-zA-Z]{4}_[0-9]{3}\.[0-9]{2})')

def procura_cod_in_iso(endereco):
	x = iso9660.ISO9660(endereco)
	for y in x.tree():

		if procura_apenas_cod.match(y):

			p = procura_apenas_cod.findall(y)
			return p[0]
		else:
			pass
	return False

def verifica_jogo(endereco_do_jogo):
	"""verifica se o arquivo existe. 
	Verifica se o jogo já se encontra com a nomeclatura do OPL (XXX_999.99.NOME_DO_JOGO.iso)
	Abre o arquivo iso para verificar a existência do arquivo launch do jogo (XXX_999.99)
	Se os 3 testes passarem será criado uma lista com tuplas com endereço, código e nome do jogo seguido dos respectivos estados.
	Ex.: [('C:\XXX_999.99.NOME_DO_JOGO.iso', True), ('XXX_999.99',True), ('NOME_DO_JOGO', True)]
	Se não passar a lista será como o exemplo seguinte.
	Ex.: [('C:\COD_INVALIDO.NOME_QUALQUER_DE_JOGO.iso', True), ('', False), ('NOME_DO_JOGO', False)]
	"""
	resultado_final = False
	nome_do_arquivo=''
	#print "Existe? %s" %(os.path.exists(endereco_do_jogo))
	if os.path.exists(endereco_do_jogo):
		nome_do_arquivo=[]
		nome_do_arquivo = procura_cod_e_nome.findall(endereco_do_jogo)
		end_jogo = endereco_do_jogo, True
		codigo_do_jogo2 = []
		codigo_do_jogo1=''
		nome_do_jogo1=''


		if nome_do_arquivo:
			codigo_do_jogo1 = nome_do_arquivo[0][:11]
			nome_do_jogo1 = nome_do_arquivo[0][12:-4]

		codigo_do_jogo2 = procura_cod_in_iso(endereco_do_jogo)

		nome_do_jogo2 = "NOME_DO_JOGO"

		if codigo_do_jogo2 == False and nome_do_arquivo == []:
			codigo_do_jogo = '', False
			nome_do_jogo = '', False
		elif codigo_do_jogo2 == False and not nome_do_arquivo ==[]:
			codigo_do_jogo = codigo_do_jogo1, False
			nome_do_jogo = nome_do_jogo1, True
		else:
			codigo_do_jogo = codigo_do_jogo2 or codigo_do_jogo1, True
			nome_do_jogo = nome_do_jogo1 or nome_do_jogo2, True

		resultado_final = [end_jogo, codigo_do_jogo, nome_do_jogo]
	else:
		pass

	return resultado_final

if __name__ == '__main__':
	x = meu_splash()
	x.MainLoop()
	y = meu_programa()
	y.MainLoop()
