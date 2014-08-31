# -*- coding: utf-8 -*- 

import wx
import wx.html
import os

from PhanterDefs import Tradutor, leitor_configuracao, localiza_cover_art, lista_de_jogos, convert_tamanho

corrente = os.getcwd()
dicionario = leitor_configuracao('dicionario')
#Interface

class meu_splash(wx.App): 
	def OnInit(self):
		
		bmp = wx.Image ( corrente +'\imagens\conexao.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		
		wx.SplashScreen ( bmp, wx.CENTER_ON_SCREEN | wx.SPLASH_TIMEOUT, 1200, None, style = wx.NO_BORDER | wx.SIMPLE_BORDER | wx.STAY_ON_TOP ) 
		wx.Yield() 
		return True


class meu_programa(wx.App):
	def OnInit(self):

		favicon = wx.Icon(corrente +'\imagens\\favicon.png', wx.BITMAP_TYPE_ANY)
		self.title = "PhanterPS2"
		frame = meu_frame(self.title, (-1,-1), (800,600))
		frame.SetIcon(favicon) 
		frame.Show()

		self.SetTopWindow(frame)
		return True

class meu_frame(wx.Frame):
	def __init__ (self, title, pos, size):
		wx.Frame.__init__(self, None, wx.ID_ANY, title, pos, size)

		pastadefault = 'D:\PS2'
		listjogos = lista_de_jogos(pastadefault) 

		imagem1 = wx.Image(corrente+'\imagens\isops2.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		imagem2 = wx.Image(corrente+'\imagens\salvar.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imagem3 = wx.Image(corrente+'\imagens\config.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imagem4 = wx.Image(corrente+'\imagens\sobre.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()

		new_imagem1 = wx.ImageFromBitmap(imagem1).Scale(16, 16, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap() #diminui a imagem para 16x16#
		new_imagem2 = wx.ImageFromBitmap(imagem2).Scale(16, 16, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap() #diminui a imagem para 16x16#
		new_imagem3 = wx.ImageFromBitmap(imagem4).Scale(16, 16, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap() #diminui a imagem para 16x16#
		new_imagem4 = wx.ImageFromBitmap(imagem3).Scale(16, 16, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap() #diminui a imagem para 16x16#

		self.title = title

		barra_de_status = self.CreateStatusBar()
		self.SetStatusText(Tradutor("Bem vindo ao PhanterPS2", dicionario))
		barra_de_ferramentas = self.CreateToolBar()
		barra_de_ferramentas.SetBackgroundColour('#BEBEBE')

		tool1 = barra_de_ferramentas.AddSimpleTool(wx.NewId(), imagem1 , Tradutor("Adicionar novos jogos iso", dicionario), Tradutor(u"Selecionar imagens iso dos jogos", dicionario))
		tool2 = barra_de_ferramentas.AddSimpleTool(wx.NewId(), imagem2 , Tradutor("Salvar", dicionario), Tradutor(u"Salvar as configurações", dicionario))
		tool3 = barra_de_ferramentas.AddSimpleTool(wx.NewId(), imagem3, Tradutor(u"Configurações", dicionario), Tradutor("Configurar o PhanterPS2", dicionario))
		tool4 = barra_de_ferramentas.AddSimpleTool(wx.NewId(), imagem4 , Tradutor("Sobre", dicionario), Tradutor(u"Sobre o programa e autor", dicionario))

		barra_de_ferramentas.Realize()

		Barra_de_menu = wx.MenuBar()
		menu_arquivo = wx.Menu()
		item1_menu_arquivo = wx.MenuItem(menu_arquivo, wx.ID_ANY, Tradutor("A&dicionar novo(s) iso(s)\tCtrl+A", dicionario), Tradutor(u"Selecionar imagens iso dos jogos", dicionario))

		item1_menu_arquivo.SetBitmap(new_imagem1)
		menu_arquivo.AppendItem(item1_menu_arquivo)

		item2_menu_arquivo = menu_arquivo.Append(wx.ID_ANY, Tradutor("Salvar", dicionario), Tradutor(u"Salvar configurações", dicionario))
		Barra_de_menu.Append(menu_arquivo, Tradutor("&Arquivo", dicionario))

		menu_sobre = wx.Menu()

		item1_menu_sobre = wx.MenuItem(menu_sobre, wx.ID_ANY, Tradutor(u"&Sobre\tF1", dicionario), Tradutor("Sobre o PhanterPS2", dicionario))
		item1_menu_sobre.SetBitmap(new_imagem3)
		menu_sobre.AppendItem(item1_menu_sobre)
		Barra_de_menu.Append(menu_sobre, Tradutor("Ajuda", dicionario))



		self.Bind(wx.EVT_MENU, self.AbrirIso, item1_menu_arquivo)
		self.Bind(wx.EVT_MENU, self.Sobre, item1_menu_sobre)

		self.Bind(wx.EVT_TOOL, self.AbrirIso, tool1)
		self.Bind(wx.EVT_TOOL, self.Config, tool3)
		self.Bind(wx.EVT_TOOL, self.Sobre, tool4)

		self.SetMenuBar(Barra_de_menu)

		sizer_panel = wx.GridBagSizer(0, 100)
		self.painel_principal = wx.Panel(self, wx.ID_ANY)

		self.painel_cabecalho = wx.Panel(self.painel_principal, wx.ID_ANY, (0,0),(-1,25), style = wx.ALIGN_CENTER|wx.ALL|wx.EXPAND)
		self.painel_scroll = wx.ScrolledWindow(self.painel_principal, wx.ID_ANY, (0,0),(-1,525), style = wx.ALIGN_CENTER|wx.ALL|wx.EXPAND|wx.BORDER_DOUBLE)
		self.painel_info_e_acao = wx.Panel(self.painel_principal, wx.ID_ANY, (0,0),(-1,50), style = wx.ALIGN_CENTER|wx.ALL|wx.EXPAND)

		sizer_jogos = wx.GridSizer(cols=2, hgap=0, vgap=0)

		for x in listjogos:

			sizer_jogos.Add(painel_de_jogos(self.painel_scroll,(0,0),(-1,110),
				arquivo_do_jogo = x[0], codigo_do_jogo = x[1], nome_do_jogo = x[2], tamanho_do_jogo = x[3]), 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND,5)
		
		self.painel_scroll.SetSizer(sizer_jogos)
		self.painel_scroll.SetScrollbars(1, 1, -1, -1)

		sizer_panel.Add(self.painel_cabecalho, (0,0),(1,1), wx.ALL|wx.EXPAND, 5)
		sizer_panel.Add(self.painel_scroll, (1,0),(3,1), wx.ALL|wx.EXPAND, 5)
		sizer_panel.Add(self.painel_info_e_acao, (4,0),(1,1), wx.ALL|wx.EXPAND, 5)
		sizer_panel.AddGrowableCol(0)
		sizer_panel.AddGrowableRow(1)

		self.painel_principal.SetSizerAndFit(sizer_panel)		
		self.CenterOnScreen()


	#ações

	wildcard = "Imagem iso (*.iso)|*.iso|All files (*.*)|*.*"
	def AbrirIso (self, event):
		dlg = wx.FileDialog(self, Tradutor(u"Selecionando Imagem...", dicionario), corrente, style=wx.MULTIPLE, wildcard=self.wildcard)
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
			result = verifica_jogo(arquivoiso)
			resultados.append(result)
		self.resultados = resultados
		pass

	def SalveConf(self, event):
		pass

	def PastaDoJogo (self, event):
		dlg = wx.DirDialog(self, Tradutor(u"Selecionando pasta de jogos...", dicionario), corrente, style=wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.dir = dlg.GetPath()
			self.SetTitle(self.title + ' -- ' + self.filename)
			dlg.Destroy()

	def Sobre (self, event):
		x = sobre()
		x.Show()
	def Config(self, event):
		x = painel_configuracao()
		x.Show()

class painel_de_jogos(wx.Panel):
	def __init__ (self, parent, pos, size, arquivo_do_jogo, codigo_do_jogo, nome_do_jogo, tamanho_do_jogo='4 GB'):
		wx.Panel.__init__(self, parent, -1, pos, size, wx.EXPAND)
		pastadefault = 'D:\PS2'
		cover_art = localiza_cover_art(pastadefault, codigo_do_jogo)
		imagem5 = wx.Image(cover_art[0]+'\\'+cover_art[1], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		new_imagem5 = wx.ImageFromBitmap(imagem5).Scale(70, 100, wx.IMAGE_QUALITY_NORMAL).ConvertToBitmap()
		botao_imagem = wx.BitmapButton(self, wx.ID_ANY, new_imagem5, (0, 0),(80, 110))
		botao_imagem.SetToolTipString(Tradutor(u"Clique na imagem para mudá-la", dicionario))
		text0 = wx.StaticText(self, wx.ID_ANY, Tradutor(u"Código:", dicionario), (0, 0))
		form0 = wx.TextCtrl( self, wx.ID_ANY, codigo_do_jogo,(0,0))
		form0.Enabled = False
		text1 = wx.StaticText(self, wx.ID_ANY, Tradutor(u"Nome:", dicionario), (0, 0))
		form1 = wx.TextCtrl( self, wx.ID_ANY, nome_do_jogo,(0,0))
		form1.Enabled = False
		text2 = wx.StaticText(self, wx.ID_ANY, Tradutor("Arquivo:", dicionario), (0, 0), style = wx.TE_RICH)
		form2 = wx.TextCtrl( self, wx.ID_ANY, arquivo_do_jogo,(0,0),  style = wx.TE_RICH)
		if arquivo_do_jogo[-6:] =='ul.cfg':
			text2.SetForegroundColour(wx.RED)
			form2.SetForegroundColour(wx.RED)
		form2.Enabled = False
		text3 = wx.StaticText(self, wx.ID_ANY, Tradutor("Tamanho:", dicionario), (0, 0))
		form3 = wx.TextCtrl( self, wx.ID_ANY, convert_tamanho(tamanho_do_jogo),(0,0))
		form3.Enabled = False
		radio = wx.CheckBox(self, wx.ID_ANY, Tradutor("Selecionar", dicionario))

		sizer = wx.GridBagSizer(0, 10)

		sizer.Add(botao_imagem, (0,0),(6,2),  wx.ALL|wx.EXPAND, 2)
		sizer.Add(text0, (0, 2), (1,1), wx.ALIGN_RIGHT, 2)
		sizer.Add(form0, (0, 3), (1,1), wx.ALL|wx.EXPAND, 2)
		sizer.Add(text1, (1, 2), (1,1), wx.ALIGN_RIGHT, 2)
		sizer.Add(form1, (1, 3), (1,1), wx.ALL|wx.EXPAND, 2)
		sizer.Add(text2, (2, 2), (1,1), wx.ALIGN_RIGHT, 2)
		sizer.Add(form2, (2, 3), (1,1), wx.ALL|wx.EXPAND, 2)
		sizer.Add(text3, (3, 2), (1,1), wx.ALIGN_RIGHT, 2)
		sizer.Add(form3, (3, 3), (1,1), wx.ALL|wx.EXPAND, 2)
		sizer.Add(radio, (4, 2),(1,3), wx.ALIGN_CENTER, 2)
		sizer.AddGrowableCol(3)
		self.SetSizerAndFit(sizer)
		self.Centre()

class sobre(wx.Frame):
	def __init__ (self):
		wx.Frame.__init__(self, None, wx.ID_ANY, Tradutor('Sobre',dicionario), (-1,-1), (400,400),style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX )
		self.codigo_html = u'''
		<html>
		<body bgcolor="#FFFFFF">
		<center><table bgcolor="#AAAAAA"  width="100%" cellspacing="0"
		cellpadding="0" border="1">
		<tr>
		<td align="center"><h2>PhanterPS2</h2></br><h5>versão 1.0</h5></td>

		</tr>
		</table>
		</center>
		<p>O <b>PhanterPS2</b> foi desenvolvido por <b>PhanterJR</b>, sócio-proprietário da Conexão Didata.
		</p>
		<p>PhanterPS2: Copyright &copy; 2014 PhanterJR - Licença GPL2</p>
		<p align="center"><b>CONTRIBUIÇÃO</b></p>
		<p><b>Junior Polegato</b><br>
		Módulo pycrc32<br>
		Copyright &copy; 2014 Junior Polegato<br>
		Licença LGPL<br>
		https://github.com/JuniorPolegato</p>
		<p><b>Barnaby Gale</b><br>
		Módulo iso9660<br>
		Copyright &copy; 2013-2014 Barnaby Gale<br>
		Licença BSD<br>
		https://github.com/barneygale
		</p>
		<p>
		<b>Python Software Foundation; All Rights Reserved</b><br>
		Linguagem Python2.7<br>
		Copyright &copy; 2001-2014 Python Software Foundation<br>
		Licença OSI<br>
		http://www.python.org
		</p>
		<p>
		<b>wxPython</b><br>
		wxWindows Library Licence, Versão 3.1<br>
		Copyright &copy; 1998-2005 Julian Smart, Robert Roebling et al<br>
		Licença LGPL<br>
		http://www.wxpython.org/
		</p>		

		</body>
		</html>'''

		html = wx.html.HtmlWindow(self)
		html.SetPage(self.codigo_html)
		button1 = wx.Button(self, wx.ID_OK, "OK")
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(html, 1, wx.EXPAND|wx.ALL, 5)
		sizer.Add(button1, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		self.SetSizer(sizer)
		self.Layout()
		self.Bind(wx.EVT_BUTTON, self.destruir, button1)
		self.CenterOnScreen() # coloca no centro da tela

	def destruir(self, event):
		self.Destroy()

class painel_configuracao (wx.Frame):
	def __init__ (self):
		wx.Frame.__init__(self, None, wx.ID_ANY, Tradutor(u'Configuração do PhanterPS2', dicionario), (-1,-1), (400,400), style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
		self.text1 = wx.StaticText(self, wx.ID_ANY, Tradutor(u"Nome:", dicionario), (0, 0))
		button1 = wx.Button(self, wx.ID_OK, "OK")
		self.Layout()
		self.CenterOnScreen()


if __name__ == '__main__':

	x = meu_splash()
	x.MainLoop()
	y = meu_programa()
	y.MainLoop()
