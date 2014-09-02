# -*- coding: utf-8 -*- 

import platform
import wx
import wx.html
import os
import logging
from PhanterDefs import Tradutor, configuracoes, imagens_jogos, lista_de_jogos, convert_tamanho, verifica_jogo

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

corrente = os.getcwd()
conf_prog = configuracoes()

dicionario = conf_prog.leitor_configuracao('dicionario')

class meu_splash(wx.App): 
	def OnInit(self):
		
		bmp = wx.Image (os.path.join(corrente,'imagens','conexao.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		
		wx.SplashScreen ( bmp, wx.CENTER_ON_SCREEN | wx.SPLASH_TIMEOUT, 1200, None, style = wx.NO_BORDER | wx.SIMPLE_BORDER | wx.STAY_ON_TOP ) 
		wx.Yield() 
		return True


class meu_programa(wx.App):
	def OnInit(self):

		favicon = wx.Icon(os.path.join(corrente,'imagens','favicon.png'), wx.BITMAP_TYPE_ANY)
		self.title = "PhanterPS2"
		self.frame = meu_frame(self.title, (-1,-1), (800,600))
		self.frame.SetIcon(favicon) 
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True

class meu_frame(wx.Frame):
	def __init__ (self, title, pos, size):
		wx.Frame.__init__(self, None, wx.ID_ANY, title, pos, size)
		self.pastadefault = conf_prog.pasta_padrao_jogos

		x = lista_de_jogos(self.pastadefault)
		self.jogos_e_info = x.jogos_e_info
		self.listjogos = self.jogos_e_info[0]

		imagem1 = wx.Image(os.path.join(corrente,'imagens','isops2.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		imagem2 = wx.Image(os.path.join(corrente,'imagens','salvar.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imagem3 = wx.Image(os.path.join(corrente,'imagens','config.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imagem4 = wx.Image(os.path.join(corrente,'imagens','sobre.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()

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

		#self.painel_principal.Destroy()
		self.painel_principal = wx.Panel(self, wx.ID_ANY) #Painel Pinricpal

		sizer_panel_titulo = wx.GridBagSizer(0, 0) #sizers
		sizer_panel = wx.GridBagSizer(0, 100)
		sizer_panel_rodape = wx.GridBagSizer(0, 0)

		#self.SendSizeEvent() #uncomente no atualizar

		self.painel_cabecalho = wx.Panel(self.painel_principal, wx.ID_ANY, (0,0),(-1,25), style = wx.ALIGN_CENTER|wx.ALL|wx.EXPAND)
		text0 = wx.StaticText(self.painel_cabecalho, wx.ID_ANY, Tradutor(u"Lista de Jogos - Playstation 2", dicionario), (0, 0), style = wx.TE_RICH)
		font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
		text0.SetFont(font)
		sizer_panel_titulo.Add(text0, (0,0), (1,1), wx.ALIGN_CENTER, 5)
		sizer_panel_titulo.AddGrowableCol(0)
		self.painel_cabecalho.SetSizerAndFit(sizer_panel_titulo)


		self.painel_scroll = wx.ScrolledWindow(self.painel_principal, wx.ID_ANY, (0,0),(-1,525), style = wx.ALIGN_CENTER|wx.ALL|wx.EXPAND|wx.BORDER_DOUBLE)		
		sizer_jogos = wx.GridSizer(cols=2, hgap=0, vgap=0)
		self.imagens_jogos = imagens_jogos(os.path.join(self.pastadefault,'ART'))
		logger.debug(self.imagens_jogos)
		for x in self.listjogos:
			logger.debug('Construindo lista de jogos: retorno da função lista de jogos %s' %x)
			sizer_jogos.Add(painel_de_jogos(self.painel_scroll, wx.ID_NEW, (0,0),(-1,110),
				arquivo_do_jogo = x[0], codigo_do_jogo = x[1], nome_do_jogo = x[2], tamanho_do_jogo = x[3], lista_cover_art = self.imagens_jogos), 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND,5)
			#self.SendSizeEvent()
		self.painel_scroll.SetSizer(sizer_jogos)
		self.painel_scroll.SetScrollbars(1, 1, -1, -1)

		self.painel_info_e_acao = wx.Panel(self.painel_principal, wx.ID_ANY, (0,0),(-1,50), style = wx.ALIGN_CENTER|wx.ALL|wx.EXPAND)
		text1 = wx.StaticText(self.painel_info_e_acao, wx.ID_ANY, Tradutor(u"Total de jogos", dicionario), (0,0), style = wx.TE_RICH)
		form1 = wx.TextCtrl(self.painel_info_e_acao, wx.ID_ANY, str(self.jogos_e_info[1]), (0,0), style = wx.TE_RICH)
		form1.Enabled = False
		text2 = wx.StaticText(self.painel_info_e_acao, wx.ID_ANY, Tradutor(u"Tamanho total", dicionario), (0,0), style = wx.TE_RICH)
		form2 = wx.TextCtrl(self.painel_info_e_acao, wx.ID_ANY, convert_tamanho(self.jogos_e_info[2]), (0,0), style = wx.TE_RICH)
		form2.Enabled = False
		sizer_panel_rodape.Add(text1, (0,0), (1,1), wx.ALL | wx.EXPAND, 5)
		sizer_panel_rodape.Add(form1, (0,1), (1,3), wx.ALL | wx.EXPAND, 5)
		sizer_panel_rodape.Add(text2, (1,0), (1,1), wx.ALL | wx.EXPAND, 5)
		sizer_panel_rodape.Add(form2, (1,1), (1,3), wx.ALL | wx.EXPAND, 5)
		sizer_panel_rodape.AddGrowableCol(3)
		self.painel_info_e_acao.SetSizerAndFit(sizer_panel_rodape)


		sizer_panel.Add(self.painel_cabecalho, (0,0),(1,1), wx.ALL|wx.EXPAND, 5)
		sizer_panel.Add(self.painel_scroll, (1,0),(3,1), wx.ALL|wx.EXPAND, 5)
		sizer_panel.Add(self.painel_info_e_acao, (4,0),(1,1), wx.ALL|wx.EXPAND, 5)
		sizer_panel.AddGrowableCol(0)
		sizer_panel.AddGrowableRow(1)
		self.painel_principal.SetSizerAndFit(sizer_panel)


		self.Bind(wx.EVT_BUTTON, self.dofilho) #No atualizer deve ser comentado
		self.Layout()
		self.CenterOnScreen()
		self.SendSizeEvent()

	def atualizar(self):
		logger.debug('Executando função atualizar()')

		self.painel_principal.Destroy()
		self.painel_principal = wx.Panel(self, wx.ID_NEW) #Painel Pinricpal

		sizer_panel_titulo = wx.GridBagSizer(0, 0) #sizers
		sizer_panel = wx.GridBagSizer(0, 100)
		sizer_panel_rodape = wx.GridBagSizer(0, 0)

		self.SendSizeEvent() #uncomente no atualizar

		self.painel_cabecalho = wx.Panel(self.painel_principal, wx.ID_NEW, (0,0),(-1,25), style = wx.ALIGN_CENTER|wx.ALL|wx.EXPAND)
		text0 = wx.StaticText(self.painel_cabecalho, wx.ID_NEW, Tradutor(u"Lista de Jogos - Playstation 2", dicionario), (0, 0), style = wx.TE_RICH)
		font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
		text0.SetFont(font)
		sizer_panel_titulo.Add(text0, (0,0), (1,1), wx.ALIGN_CENTER, 5)
		sizer_panel_titulo.AddGrowableCol(0)
		self.painel_cabecalho.SetSizerAndFit(sizer_panel_titulo)


		self.painel_scroll = wx.ScrolledWindow(self.painel_principal, wx.ID_NEW, (0,0),(-1,525), style = wx.ALIGN_CENTER|wx.ALL|wx.EXPAND|wx.BORDER_DOUBLE)		
		sizer_jogos = wx.GridSizer(cols=2, hgap=0, vgap=0)
		self.imagens_jogos = imagens_jogos(os.path.join(self.pastadefault, 'ART'))
		logger.debug(self.imagens_jogos)
		for x in self.listjogos:
			sizer_jogos.Add(painel_de_jogos(self.painel_scroll, wx.ID_NEW, (0,0),(-1,110),
				arquivo_do_jogo = x[0], codigo_do_jogo = x[1], nome_do_jogo = x[2], tamanho_do_jogo = x[3], lista_cover_art = self.imagens_jogos), 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND,5)
			self.SendSizeEvent()
		self.painel_scroll.SetSizer(sizer_jogos)
		self.painel_scroll.SetScrollbars(1, 1, -1, -1)

		self.painel_info_e_acao = wx.Panel(self.painel_principal, wx.ID_NEW, (0,0),(-1,50), style = wx.ALIGN_CENTER|wx.ALL|wx.EXPAND)
		text1 = wx.StaticText(self.painel_info_e_acao, wx.ID_NEW, Tradutor(u"Total de jogos", dicionario), (0,0), style = wx.TE_RICH)
		form1 = wx.TextCtrl(self.painel_info_e_acao, wx.ID_NEW, str(self.jogos_e_info[1]), (0,0), style = wx.TE_RICH)
		form1.Enabled = False
		text2 = wx.StaticText(self.painel_info_e_acao, wx.ID_NEW, Tradutor(u"Tamanho total", dicionario), (0,0), style = wx.TE_RICH)
		form2 = wx.TextCtrl(self.painel_info_e_acao, wx.ID_NEW, convert_tamanho(self.jogos_e_info[2]), (0,0), style = wx.TE_RICH)
		form2.Enabled = False
		sizer_panel_rodape.Add(text1, (0,0), (1,1), wx.ALL | wx.EXPAND, 5)
		sizer_panel_rodape.Add(form1, (0,1), (1,3), wx.ALL | wx.EXPAND, 5)
		sizer_panel_rodape.Add(text2, (1,0), (1,1), wx.ALL | wx.EXPAND, 5)
		sizer_panel_rodape.Add(form2, (1,1), (1,3), wx.ALL | wx.EXPAND, 5)
		sizer_panel_rodape.AddGrowableCol(3)
		self.painel_info_e_acao.SetSizerAndFit(sizer_panel_rodape)


		sizer_panel.Add(self.painel_cabecalho, (0,0),(1,1), wx.ALL|wx.EXPAND, 5)
		sizer_panel.Add(self.painel_scroll, (1,0),(3,1), wx.ALL|wx.EXPAND, 5)
		sizer_panel.Add(self.painel_info_e_acao, (4,0),(1,1), wx.ALL|wx.EXPAND, 5)
		sizer_panel.AddGrowableCol(0)
		sizer_panel.AddGrowableRow(1)
		self.painel_principal.SetSizerAndFit(sizer_panel)


		#self.Bind(wx.EVT_BUTTON, self.dofilho) #No atualizer deve ser comentado
		self.Layout()
		self.CenterOnScreen()
		self.SendSizeEvent()

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


	def Sobre (self, event):
		x = sobre()
		x.Show()

	def Config(self, event):
		frame = painel_configuracao(self, -1, Tradutor(u"Configurações",dicionario))
		frame.Show(True)


	def dofilho(self, event):
		logger.debug('Capturando evento filho')

		conf_prog = configuracoes()
		self.pastadefault = conf_prog.pasta_padrao_jogos
		logger.debug('Pasta default mudada para %s' %self.pastadefault)

		x = lista_de_jogos(self.pastadefault)
		self.jogos_e_info = x.jogos_e_info
		self.listjogos = self.jogos_e_info[0]
		self.atualizar()



class painel_de_jogos(wx.Panel):
	def __init__ (self, parent, ID, pos, size, arquivo_do_jogo, codigo_do_jogo, nome_do_jogo, tamanho_do_jogo, lista_cover_art):
		wx.Panel.__init__(self, parent, wx.ID_ANY, pos, size, wx.EXPAND)
		pastadefault = conf_prog.pasta_padrao_jogos

		self.cover_art=lista_cover_art.localiza_cover_art(codigo_do_jogo)
		logger.debug('convertando imagem: %s' %(os.path.join(self.cover_art[0], self.cover_art[1])))
		imagem5 = wx.Image(os.path.join(self.cover_art[0], self.cover_art[1]), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		new_imagem5 = wx.ImageFromBitmap(imagem5).Scale(70, 100, wx.IMAGE_QUALITY_NORMAL).ConvertToBitmap()
		botao_imagem = wx.BitmapButton(self, wx.ID_ANY, new_imagem5, (0, 0),(80, 110))
		botao_imagem.SetToolTipString(Tradutor(u"Clique na imagem para mudá-la", dicionario))
		self.Bind(wx.EVT_BUTTON , self.Mudar_imagem, botao_imagem)
		text0 = wx.StaticText(self, wx.ID_ANY, Tradutor(u"Código:", dicionario), (0, 0), style = wx.TE_RICH)
		form0 = wx.TextCtrl( self, wx.ID_ANY, codigo_do_jogo,(0,0), style = wx.TE_RICH)
		form0.Enabled = False
		text1 = wx.StaticText(self, wx.ID_ANY, Tradutor(u"Nome:", dicionario), (0, 0), style = wx.TE_RICH)
		form1 = wx.TextCtrl( self, wx.ID_ANY, nome_do_jogo,(0,0), style = wx.TE_RICH)
		form1.Enabled = False
		text2 = wx.StaticText(self, wx.ID_ANY, Tradutor("Arquivo:", dicionario), (0, 0), style = wx.TE_RICH)
		form2 = wx.TextCtrl( self, wx.ID_ANY, arquivo_do_jogo,(0,0),  style = wx.TE_RICH)
		if arquivo_do_jogo[-6:] =='ul.cfg':
			text2.SetForegroundColour(wx.RED)
			form2.SetForegroundColour(wx.RED)
		form2.Enabled = False
		text3 = wx.StaticText(self, wx.ID_ANY, Tradutor("Tamanho:", dicionario), (0, 0), style = wx.TE_RICH)
		form3 = wx.TextCtrl( self, wx.ID_ANY, convert_tamanho(tamanho_do_jogo),(0,0), style = wx.TE_RICH)
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
		self.Layout()
	def Mudar_imagem(self, event):
		print self.cover_art


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
	def __init__ (self, parent, ID, title):
		wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
		self.parent=parent
		painel = wx.Panel(self, wx.ID_ANY, (0,0), (400,300))
		pastadefault = conf_prog.pasta_padrao_jogos
		config_pasta_jogos = conf_prog.leitor_configuracao('pasta_destino_jogos')



		text0 = wx.StaticText(painel, wx.ID_ANY, Tradutor(u"Pasta de jogos", dicionario), (0, 0))

		self.form0 = wx.TextCtrl( painel, wx.ID_ANY, config_pasta_jogos,(0,0), (250,-1))
		self.form0.Enabled = False
		botao0 = wx.Button(painel, wx.ID_ANY, '...', (0,0), (20,20))
		self.Bind(wx.EVT_BUTTON, self.Pega_pasta_jogo, botao0)
		text1 = wx.StaticText(painel, wx.ID_ANY, Tradutor(u"Arquivos de Tradução",dicionario), (0, 0))
		self.form1 = wx.TextCtrl(painel, wx.ID_ANY, "",(0,0), (250,-1))
		self.form0.Enabled = False
		linha_horizontal = wx.StaticLine(painel, id=wx.ID_ANY, pos=(0,0), size=(-1,-1),
										style=wx.LI_HORIZONTAL| wx.BORDER_DOUBLE , name='wx.StaticLineNameStr')
		text2 = wx.StaticText(painel, wx.ID_ANY, Tradutor(u"Pasta de DVD",dicionario), (0, 0))
		
		self.form2 = wx.TextCtrl(painel, wx.ID_ANY, os.path.join(config_pasta_jogos, 'DVD'),(0,0), (250,-1))
		self.form2.Enabled = False
		text3 = wx.StaticText(painel, wx.ID_ANY, Tradutor(u"Pasta de CD",dicionario), (0, 0))
		self.form3 = wx.TextCtrl(painel, wx.ID_ANY, os.path.join(config_pasta_jogos, 'CD'),(0,0), (250,-1))
		self.form3.Enabled = False
		text4 = wx.StaticText(painel, wx.ID_ANY, Tradutor(u"Pasta de capas",dicionario), (0, 0))
		self.form4 = wx.TextCtrl(painel, wx.ID_ANY, os.path.join(config_pasta_jogos, 'ART'),(0,0), (250,-1))
		self.form4.Enabled = False
		text5 = wx.StaticText(painel, wx.ID_ANY, Tradutor(u"Pasta de configurações",dicionario), (0, 0))
		self.form5 = wx.TextCtrl(painel, wx.ID_ANY, os.path.join(config_pasta_jogos, 'CFG'),(0,0), (250,-1))
		self.form5.Enabled = False

		self.form1.Enabled = False
		botao1 = wx.Button(painel, wx.ID_ANY, '...', (0,0), (20,20))
		botaook = wx.Button(painel, wx.ID_OK, 'OK', (0,0))
		self.Bind(wx.EVT_BUTTON, self.Confirmar, botaook)

		sizer = wx.GridBagSizer(0, 10)
		sizer2 = wx.GridBagSizer(0, 0)

		sizer.Add(text0, (1, 1), (1,1), wx.ALIGN_RIGHT, 2)
		sizer.Add(self.form0, (1, 2), (1,2), wx.ALL|wx.EXPAND, 2)
		sizer.Add(botao0, (1, 4), (1,4), wx.ALL, 2)
		sizer.Add(text1, (2, 1), (1,1), wx.ALIGN_RIGHT, 2)
		sizer.Add(self.form1, (2, 2), (1,2), wx.ALL|wx.EXPAND, 2)
		sizer.Add(botao1, (2, 4), (1,4), wx.ALL, 2)
		sizer.Add(linha_horizontal, (3, 1), (1,5), wx.ALL|wx.EXPAND|wx.ALIGN_CENTER, 4)
		sizer.Add(text2, (4, 1), (1,1), wx.ALIGN_RIGHT, 2)
		sizer.Add(self.form2, (4, 2), (1,2), wx.ALL|wx.EXPAND, 2)
		sizer.Add(text3, (5, 1), (1,1), wx.ALIGN_RIGHT, 2)
		sizer.Add(self.form3, (5, 2), (1,2), wx.ALL|wx.EXPAND, 2)
		sizer.Add(text4, (6, 1), (1,1), wx.ALIGN_RIGHT, 2)
		sizer.Add(self.form4, (6, 2), (1,2), wx.ALL|wx.EXPAND, 2)
		sizer.Add(text5, (7, 1), (1,1), wx.ALIGN_RIGHT, 2)
		sizer.Add(self.form5, (7, 2), (1,2), wx.ALL|wx.EXPAND, 2)
		sizer.Add(botaook, (9,0), (2,7), wx.ALL|wx.ALIGN_CENTER, 10)	

		painel.SetSizerAndFit(sizer)
		sizer2.Add(painel, (0,0), (1,1), wx.ALL|wx.EXPAND|wx.ALIGN_CENTER)
		sizer2.AddGrowableCol(0)
		sizer2.AddGrowableRow(0)
		self.SetSizerAndFit(sizer2)
		self.Centre()

	def Pega_pasta_jogo (self, event):
		dlg = wx.DirDialog(self, Tradutor(u"Selecionando pasta de jogos...", dicionario), corrente, style=wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			valor_dialog = dlg.GetPath()
			self.form0.SetValue(valor_dialog)
			self.form2.SetValue(os.path.join(valor_dialog, 'DVD'))
			self.form3.SetValue(os.path.join(valor_dialog, 'CD'))
			self.form4.SetValue(os.path.join(valor_dialog, 'ART'))
			self.form5.SetValue(os.path.join(valor_dialog, 'CFG'))
			dlg.Destroy()


	def Confirmar (self, event):
		confg1 = self.form0.GetValue()
		confg2 = self.form1.GetValue()
		conf_prog.mudar_configuracao('pasta_destino_jogos', confg1)
		conf_prog.mudar_configuracao('dicionario', confg2)

		self.Destroy()
		wx.PostEvent(self.parent, event)

if __name__ == '__main__':

	x = meu_splash()
	x.MainLoop()
	y = meu_programa()
	y.MainLoop()
