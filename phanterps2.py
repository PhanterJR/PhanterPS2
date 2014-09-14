# -*- coding: utf-8 -*- 

import platform 
import wx
import wx.html
import os
import logging 
from phanterdefs import Tradutor, configuracoes, imagens_jogos, lista_de_jogos, convert_tamanho, verifica_jogo, manipula_ul, retirar_exitf_imagem, muda_nome_jogo  #meu módulo
import glob
from contrib import pycrc32
import time


logging.basicConfig(level=logging.ERROR) 
logger = logging.getLogger(__name__) 

corrente = os.getcwd() 
conf_prog = configuracoes() 
imagem_check = configuracoes('imagem_check.cfg')
memoria = {}
memoria['tamanho_total_dos_jogos'] = 0
memoria['jogos_selecionados'] = 0
memoria['progresso'] = 0
dicionario = conf_prog.leitor_configuracao('dicionario')

class meu_programa(wx.App):
	def OnInit(self):
		bmp = wx.Image (os.path.join(corrente,'imagens','splash.jpg'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		wx.SplashScreen ( bmp, wx.CENTER_ON_SCREEN | wx.SPLASH_TIMEOUT, 3000, None, style = wx.NO_BORDER | wx.SIMPLE_BORDER | wx.STAY_ON_TOP ) 
		wx.Yield()
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
		self.lista_de_selecionados=[]
		self.pastadefault = conf_prog.pasta_padrao_jogos
		self.tamanho_vindo_do_filho = 0
		zz = lista_de_jogos(self.pastadefault)
		self.jogos_e_info = zz.jogos_e_info
		self.listjogos = self.jogos_e_info[0]

		imagem1 = wx.Image(os.path.join(corrente,'imagens','isops2.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		imagem2 = wx.Image(os.path.join(corrente,'imagens','multips2.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		imagem3 = wx.Image(os.path.join(corrente,'imagens','atualizar.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imagem4 = wx.Image(os.path.join(corrente,'imagens','config.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		self.imagem5 = wx.Image(os.path.join(corrente,'imagens','sobre.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()

		new_imagem1 = wx.ImageFromBitmap(imagem1).Scale(16, 16, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap() #diminui a imagem para 16x16#
		new_imagem2 = wx.ImageFromBitmap(imagem2).Scale(16, 16, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap() #diminui a imagem para 16x16#
		new_imagem3 = wx.ImageFromBitmap(imagem3).Scale(16, 16, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap() #diminui a imagem para 16x16#
		new_imagem4 = wx.ImageFromBitmap(imagem4).Scale(16, 16, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap() #diminui a imagem para 16x16#
		new_imagem5 = wx.ImageFromBitmap(self.imagem5).Scale(16, 16, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap() #diminui a imagem para 16x16#

		self.title = title

		barra_de_status = self.CreateStatusBar()
		self.SetStatusText(Tradutor("Bem vindo ao PhanterPS2", dicionario))
		barra_de_ferramentas = self.CreateToolBar()
		barra_de_ferramentas.SetBackgroundColour('#BEBEBE')

		tool1 = barra_de_ferramentas.AddSimpleTool(wx.NewId(), imagem1 , Tradutor("Adicionar novo jogo ISO", dicionario), Tradutor(u"Selecionar imagens ISO para adicionar a lista de jogos", dicionario))
		tool2 = barra_de_ferramentas.AddSimpleTool(wx.NewId(), imagem2, Tradutor(u'Adicionar múltiplos jogos ISO', dicionario), Tradutor(u'Selecionar vários ISOs para adicionar a lista de jogos', dicionario))
		tool3 = barra_de_ferramentas.AddSimpleTool(wx.NewId(), imagem3 , Tradutor("Atualizar", dicionario), Tradutor(u"Atualizar lista de jogos", dicionario))
		tool4 = barra_de_ferramentas.AddSimpleTool(wx.NewId(), imagem4, Tradutor(u"Configurações", dicionario), Tradutor("Configurar o PhanterPS2", dicionario))
		tool5 = barra_de_ferramentas.AddSimpleTool(wx.NewId(), self.imagem5 , Tradutor("Sobre", dicionario), Tradutor(u"Sobre o programa e autor", dicionario))

		barra_de_ferramentas.Realize()

		Barra_de_menu = wx.MenuBar()
		menu_arquivo = wx.Menu()

		item1_menu_arquivo = wx.MenuItem(menu_arquivo, wx.ID_ANY, Tradutor("A&dicionar novo ISO\tCtrl+A", dicionario), Tradutor(u"Selecionar imagens ISO para adicionar a lista de jogos", dicionario))
		item1_menu_arquivo.SetBitmap(new_imagem1)
		item2_menu_arquivo = wx.MenuItem(menu_arquivo, wx.ID_ANY, Tradutor(u'A&dicionar múltiplos jogos ISO\tCtrl+M', dicionario), Tradutor(u'Selecionar vários ISOs para adicionar a lista de jogos', dicionario))
		item2_menu_arquivo.SetBitmap(new_imagem2)
		item3_menu_arquivo = wx.MenuItem(menu_arquivo,wx.ID_ANY, Tradutor("A&tualizar", dicionario), Tradutor(u"Atualizar lista de jogos", dicionario))
		item3_menu_arquivo.SetBitmap(new_imagem3)
		item4_menu_arquivo = wx.MenuItem(menu_arquivo, wx.ID_ANY, Tradutor(u"Configurações", dicionario), Tradutor(u"Configurar o PhanterPS2", dicionario))
		item4_menu_arquivo.SetBitmap(new_imagem4)

		menu_arquivo.AppendItem(item1_menu_arquivo)
		menu_arquivo.AppendItem(item2_menu_arquivo)
		menu_arquivo.AppendItem(item3_menu_arquivo)
		menu_arquivo.AppendItem(item4_menu_arquivo)


		Barra_de_menu.Append(menu_arquivo, Tradutor("&Arquivo", dicionario))

		menu_sobre = wx.Menu()

		item1_menu_sobre = wx.MenuItem(menu_sobre, wx.ID_ANY, Tradutor(u"&Sobre\tF1", dicionario), Tradutor("Sobre o PhanterPS2", dicionario))
		item1_menu_sobre.SetBitmap(new_imagem5)
		menu_sobre.AppendItem(item1_menu_sobre)
		Barra_de_menu.Append(menu_sobre, Tradutor("Ajuda", dicionario))
		self.Bind(wx.EVT_MENU, self.AbrirIso, item1_menu_arquivo)
		self.Bind(wx.EVT_MENU, self.MultiIso, item2_menu_arquivo)
		self.Bind(wx.EVT_MENU, self.Atualizar, item3_menu_arquivo)
		self.Bind(wx.EVT_MENU, self.Config, item4_menu_arquivo)
		self.Bind(wx.EVT_MENU, self.Sobre, item1_menu_sobre)
		self.Bind(wx.EVT_TOOL, self.AbrirIso, tool1)
		self.Bind(wx.EVT_TOOL, self.MultiIso, tool2)
		self.Bind(wx.EVT_TOOL, self.Atualizar, tool3)
		self.Bind(wx.EVT_TOOL, self.Config, tool4)
		self.Bind(wx.EVT_TOOL, self.Sobre, tool5)
		self.SetMenuBar(Barra_de_menu)

		#self.painel_principal.Destroy()
		self.painel_principal = wx.Panel(self, wx.ID_ANY) #Painel Pinricpal


		sizer_panel_titulo = wx.GridBagSizer(0, 0) #sizers
		sizer_panel = wx.GridBagSizer(0, 100)

		sizer_panel_rodape = wx.GridSizer(cols=2, hgap=0, vgap=0)

		#self.SendSizeEvent() #uncomente no atualizar

		self.painel_cabecalho = wx.Panel(self.painel_principal, wx.ID_ANY, (0,0),(-1,25), style = wx.ALIGN_CENTER|wx.ALL|wx.EXPAND)
		text0 = wx.StaticText(self.painel_cabecalho, wx.ID_ANY, Tradutor(u"Lista de Jogos - Playstation 2", dicionario), (0, 0), style = wx.TE_RICH)
		font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
		text0.SetFont(font)
		sizer_panel_titulo.Add(text0, (0,0), (1,1), wx.ALIGN_CENTER, 5)
		sizer_panel_titulo.AddGrowableCol(0)
		self.painel_cabecalho.SetSizerAndFit(sizer_panel_titulo)


		self.painel_scroll = wx.ScrolledWindow(self.painel_principal, wx.ID_ANY, (0,0),(-1,525))		
		sizer_jogos = wx.GridSizer(cols=2, hgap=0, vgap=0)
		self.imagens_jogos = imagens_jogos(os.path.join(self.pastadefault,'ART'))
		logger.debug(self.imagens_jogos)
		wx.Yield()

		for x in self.listjogos:
			logger.debug('Construindo lista de jogos: retorno da função lista de jogos %s' %x)
			sizer_jogos.Add(painel_de_jogos(self.painel_scroll, wx.ID_NEW, (0,0),(-1,110),
				arquivo_do_jogo = x[0], codigo_do_jogo = x[1], nome_do_jogo = x[2], tamanho_do_jogo = x[3], lista_cover_art = self.imagens_jogos), 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND,5)
			#self.SendSizeEvent()
		self.painel_principal.Show()
		self.painel_scroll.SetWindowStyleFlag(wx.ALIGN_CENTER|wx.ALL|wx.EXPAND|wx.BORDER_DOUBLE)
		self.painel_scroll.SetSizer(sizer_jogos)
		self.painel_scroll.SetScrollbars(1, 1, -1, -1)

		#rodapé
		self.painel_info_e_acao = wx.Panel(self.painel_principal, wx.ID_ANY, (0,0),(-1,-1), style = wx.ALIGN_CENTER|wx.ALL|wx.EXPAND)
	############ caixa info da esquerda
		self.painel_info = wx.Panel(self.painel_info_e_acao, wx.ID_ANY,(0,0), (-1,-1), style = wx.ALIGN_CENTER| wx.ALL | wx.EXPAND)
		sizer_painel_info = wx.GridBagSizer(0,0)
		textTilulo1 = wx.StaticText(self.painel_info, wx.ID_ANY, Tradutor(u'INFORMAÇÕES GERAIS', dicionario), (0,0), style = wx.ALIGN_CENTER|wx.TE_RICH)
		text1 = wx.StaticText(self.painel_info, wx.ID_ANY, Tradutor(u"Total de jogos", dicionario), (0,0), style = wx.TE_RICH)
		form1 = wx.TextCtrl(self.painel_info, wx.ID_ANY, str(self.jogos_e_info[1]), (0,0), style = wx.TE_RICH)
		form1.Enabled = False
		text2 = wx.StaticText(self.painel_info, wx.ID_ANY, Tradutor(u"Tamanho total", dicionario), (0,0), style = wx.TE_RICH)
		form2 = wx.TextCtrl(self.painel_info, wx.ID_ANY, convert_tamanho(self.jogos_e_info[2]), (0,0), style = wx.TE_RICH)
		form2.Enabled = False
		sizer_painel_info.Add(textTilulo1, (0,0), (1,3), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
		sizer_painel_info.Add(text1, (1,0), (1,1), wx.ALL |wx.ALIGN_CENTER_VERTICAL, 5)
		sizer_painel_info.Add(form1, (1,1), (1,2), wx.ALL | wx.EXPAND, 5)
		sizer_painel_info.Add(text2, (2,0), (1,1), wx.ALL |wx.ALIGN_CENTER_VERTICAL, 5)
		sizer_painel_info.Add(form2, (2,1), (1,2), wx.ALL | wx.EXPAND, 5)
		self.painel_info.SetSizerAndFit(sizer_painel_info)
		sizer_painel_info.AddGrowableCol(2)

	  ##########Caixa de ações
		painel_acao = wx.Panel(self.painel_info_e_acao, wx.ID_ANY,(0,0), (-1,-1), style = wx.ALIGN_CENTER| wx.ALL | wx.EXPAND)
		sizer_painel_acao = wx.GridBagSizer(0,0)
		textTilulo2 = wx.StaticText(painel_acao, wx.ID_ANY, Tradutor(u'INFORMAÇÕES E AÇÕES DOS SELECIONADOS', dicionario), (0,0), style = wx.ALIGN_CENTER|wx.TE_RICH)
		text3 = wx.StaticText(painel_acao, wx.ID_ANY, Tradutor(u"Total de jogos", dicionario), (0,0), style = wx.TE_RICH)
		self.form3 = wx.TextCtrl(painel_acao, wx.ID_ANY, '0', (0,0), style = wx.TE_RICH)
		self.form3.Enabled = False
		text4 = wx.StaticText(painel_acao, wx.ID_ANY, Tradutor(u"Tamanho Total", dicionario), (0,0), style = wx.TE_RICH)
		self.form4 = wx.TextCtrl(painel_acao, wx.ID_ANY, convert_tamanho(memoria['tamanho_total_dos_jogos']), (0,0), style = wx.TE_RICH)
		self.form4.Enabled = False
		sizer_painel_acao.Add(textTilulo2, (0,0), (1,3), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
		sizer_painel_acao.Add(text3, (1,0), (1,1), wx.ALL |wx.ALIGN_CENTER_VERTICAL, 5)
		sizer_painel_acao.Add(self.form3, (1,1), (1,2), wx.ALL | wx.EXPAND, 5)
		sizer_painel_acao.Add(text4, (2,0), (1,1), wx.ALL |wx.ALIGN_CENTER_VERTICAL, 5)
		sizer_painel_acao.Add(self.form4, (2,1), (1,2), wx.ALL | wx.EXPAND, 5)

		painel_acao.SetSizerAndFit(sizer_painel_acao)
		sizer_painel_acao.AddGrowableCol(2)
	  #FIM Caixa de ações

		sizer_panel_rodape.Add(self.painel_info , 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND,5)
		sizer_panel_rodape.Add(painel_acao, 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND,5)

		self.painel_info_e_acao.SetSizerAndFit(sizer_panel_rodape)

		self.Bind(wx.EVT_CHECKBOX, self.dofilho2) #No atualizar deve ser comentado

		sizer_panel.Add(self.painel_cabecalho, (0,0),(1,1), wx.ALL|wx.EXPAND, 5)
		sizer_panel.Add(self.painel_scroll, (1,0),(3,1), wx.ALL|wx.EXPAND, 5)
		sizer_panel.Add(self.painel_info_e_acao, (4,0),(1,1), wx.ALL|wx.EXPAND, 5)
		sizer_panel.AddGrowableCol(0)
		sizer_panel.AddGrowableRow(1)
		self.painel_principal.SetSizerAndFit(sizer_panel)


		self.Bind(wx.EVT_BUTTON, self.dofilho) #No atualizar deve ser comentado
		self.Layout()
		self.CenterOnScreen()
		self.SendSizeEvent()

	def atualizar(self):

		logger.debug('Executando função atualizar()')

		self.painel_principal.Destroy()
		self.painel_principal = wx.Panel(self, wx.ID_NEW) #Painel Pinricpal
		self.painel_principal.Hide()

		sizer_panel_titulo = wx.GridBagSizer(0, 0) #sizers
		sizer_panel = wx.GridBagSizer(0, 100)

		sizer_panel_rodape = wx.GridSizer(cols=2, hgap=0, vgap=0)

		self.SendSizeEvent() #uncomente no atualizar

		self.painel_cabecalho = wx.Panel(self.painel_principal, wx.ID_NEW, (0,0),(-1,25), style = wx.ALIGN_CENTER|wx.ALL|wx.EXPAND)
		text0 = wx.StaticText(self.painel_cabecalho, wx.ID_NEW, Tradutor(u"Lista de Jogos - Playstation 2", dicionario), (0, 0), style = wx.TE_RICH)
		font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
		text0.SetFont(font)
		sizer_panel_titulo.Add(text0, (0,0), (1,1), wx.ALIGN_CENTER, 5)
		sizer_panel_titulo.AddGrowableCol(0)
		self.painel_cabecalho.SetSizerAndFit(sizer_panel_titulo)


		self.painel_scroll = wx.ScrolledWindow(self.painel_principal, wx.ID_NEW, (0,0),(-1,525))		
		sizer_jogos = wx.GridSizer(cols=2, hgap=0, vgap=0)
		self.imagens_jogos = imagens_jogos(os.path.join(self.pastadefault,'ART'))
		logger.debug(self.imagens_jogos)
		wx.Yield()

		for x in self.listjogos:
			logger.debug('Construindo lista de jogos: retorno da função lista de jogos %s' %x)
			sizer_jogos.Add(painel_de_jogos(self.painel_scroll, wx.ID_NEW, (0,0),(-1,110),
				arquivo_do_jogo = x[0], codigo_do_jogo = x[1], nome_do_jogo = x[2], tamanho_do_jogo = x[3], lista_cover_art = self.imagens_jogos), 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND,5)
			self.SendSizeEvent()
		self.painel_principal.Show()
		self.painel_scroll.SetWindowStyleFlag(wx.ALIGN_CENTER|wx.ALL|wx.EXPAND|wx.BORDER_DOUBLE)
		self.painel_scroll.SetSizer(sizer_jogos)
		self.painel_scroll.SetScrollbars(1, 1, -1, -1)

		#rodapé
		self.painel_info_e_acao = wx.Panel(self.painel_principal, wx.ID_NEW, (0,0),(-1,-1), style = wx.ALIGN_CENTER|wx.ALL|wx.EXPAND)
	############ caixa info da esquerda
		self.painel_info = wx.Panel(self.painel_info_e_acao, wx.ID_NEW,(0,0), (-1,-1), style = wx.ALIGN_CENTER| wx.ALL | wx.EXPAND)
		sizer_painel_info = wx.GridBagSizer(0,0)
		textTilulo1 = wx.StaticText(self.painel_info, wx.ID_NEW, Tradutor(u'INFORMAÇÕES GERAIS', dicionario), (0,0), style = wx.ALIGN_CENTER|wx.TE_RICH)
		text1 = wx.StaticText(self.painel_info, wx.ID_NEW, Tradutor(u"Total de jogos", dicionario), (0,0), style = wx.TE_RICH)
		form1 = wx.TextCtrl(self.painel_info, wx.ID_NEW, str(self.jogos_e_info[1]), (0,0), style = wx.TE_RICH)
		form1.Enabled = False
		text2 = wx.StaticText(self.painel_info, wx.ID_NEW, Tradutor(u"Tamanho total", dicionario), (0,0), style = wx.TE_RICH)
		form2 = wx.TextCtrl(self.painel_info, wx.ID_NEW, convert_tamanho(self.jogos_e_info[2]), (0,0), style = wx.TE_RICH)
		form2.Enabled = False
		sizer_painel_info.Add(textTilulo1, (0,0), (1,3), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
		sizer_painel_info.Add(text1, (1,0), (1,1), wx.ALL | wx.EXPAND, 5)
		sizer_painel_info.Add(form1, (1,1), (1,2), wx.ALL | wx.EXPAND, 5)
		sizer_painel_info.Add(text2, (2,0), (1,1), wx.ALL | wx.EXPAND, 5)
		sizer_painel_info.Add(form2, (2,1), (1,2), wx.ALL | wx.EXPAND, 5)
		self.painel_info.SetSizerAndFit(sizer_painel_info)
		sizer_painel_info.AddGrowableCol(2)
	  ##########Caixa de ações
		painel_acao = wx.Panel(self.painel_info_e_acao, wx.ID_NEW,(0,0), (-1,-1), style = wx.ALIGN_CENTER| wx.ALL | wx.EXPAND)
		sizer_painel_acao = wx.GridBagSizer(0,0)
		textTilulo2 = wx.StaticText(painel_acao, wx.ID_NEW, Tradutor(u'INFORMAÇÕES E AÇÕES DOS SELECIONADOS', dicionario), (0,0), style = wx.ALIGN_CENTER|wx.TE_RICH)
		text3 = wx.StaticText(painel_acao, wx.ID_NEW, Tradutor(u"Total de jogos", dicionario), (0,0), style = wx.TE_RICH)
		self.form3 = wx.TextCtrl(painel_acao, wx.ID_NEW, '0', (0,0), style = wx.TE_RICH)
		self.form3.Enabled = False
		text4 = wx.StaticText(painel_acao, wx.ID_NEW, Tradutor(u"Tamanho Total", dicionario), (0,0), style = wx.TE_RICH)
		self.form4 = wx.TextCtrl(painel_acao, wx.ID_NEW, convert_tamanho(memoria['tamanho_total_dos_jogos']), (0,0), style = wx.TE_RICH)
		self.form4.Enabled = False
		sizer_painel_acao.Add(textTilulo2, (0,0), (1,3), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
		sizer_painel_acao.Add(text3, (1,0), (1,1), wx.ALL | wx.EXPAND, 5)
		sizer_painel_acao.Add(self.form3, (1,1), (1,2), wx.ALL | wx.EXPAND, 5)
		sizer_painel_acao.Add(text4, (2,0), (1,1), wx.ALL | wx.EXPAND, 5)
		sizer_painel_acao.Add(self.form4, (2,1), (1,2), wx.ALL | wx.EXPAND, 5)

		painel_acao.SetSizerAndFit(sizer_painel_acao)
		sizer_painel_acao.AddGrowableCol(2)
	  #FIM Caixa de ações

		sizer_panel_rodape.Add(self.painel_info , 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND,5)
		sizer_panel_rodape.Add(painel_acao, 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND,5)

		self.painel_info_e_acao.SetSizerAndFit(sizer_panel_rodape)

		#self.Bind(wx.EVT_CHECKBOX, self.dofilho2) #No atualizar deve ser comentado

		sizer_panel.Add(self.painel_cabecalho, (0,0),(1,1), wx.ALL|wx.EXPAND, 5)
		sizer_panel.Add(self.painel_scroll, (1,0),(3,1), wx.ALL|wx.EXPAND, 5)
		sizer_panel.Add(self.painel_info_e_acao, (4,0),(1,1), wx.ALL|wx.EXPAND, 5)
		sizer_panel.AddGrowableCol(0)
		sizer_panel.AddGrowableRow(1)
		self.painel_principal.SetSizerAndFit(sizer_panel)


		#self.Bind(wx.EVT_BUTTON, self.dofilho) #No atualizar deve ser comentado
		self.Layout()
		self.CenterOnScreen()
		self.SendSizeEvent()

	#ações

	wildcard = "%s (*.iso)|*.iso" %(Tradutor('Imagem ISO',dicionario))
	def AbrirIso (self, event):
		self.janeladlg = wx.FileDialog(self, Tradutor(u"Selecionando Imagem...", dicionario), corrente, style=wx.OPEN, wildcard=self.wildcard)
		if self.janeladlg.ShowModal() == wx.ID_OK:
			self.arquivoiso = self.janeladlg.GetPaths()
			self.janeladlg.Destroy()
			self.ReadFile(self.arquivoiso[0])
			logger.debug(u'%s, %s, %s' %(self.resultados[0][0], self.resultados[1][0], self.resultados[2][0]))
			self.frame = janela_adicionar_iso(self, wx.ID_ANY, Tradutor(u"Adicione o nome e código do jogo", dicionario), self.resultados[0], self.resultados[1], self.resultados[2], self.resultados[3],self.listjogos )
			self.frame.Show(True)
	def MultiIso(self, event):
		self.janeladlg = wx.FileDialog(self, Tradutor(u"Selecionando Imagens...", dicionario), corrente, style=wx.MULTIPLE, wildcard=self.wildcard)
		if self.janeladlg.ShowModal() == wx.ID_OK:
			self.arquivoiso = self.janeladlg.GetPaths()
			lis = []
			tam_tot = 0
			for d in self.arquivoiso:
				ver = verifica_jogo(d)
				res = ver.resultado_final
				tam_tot+= res[3]
				uno=[res[0], res[1], res[2], res[3]]
				lis.append(uno)
			lista_de_jogoss = [lis, tam_tot]
			print lista_de_jogoss

			self.janeladlg.Destroy()
			self.frame = frame_adicionar_multiplos(self.title, lista_de_jogoss[0],  lista_de_jogoss[1],(-1,-1), (500,600))
			self.frame.Show(True)

	def  Atualizar(self, event):
		conf_prog = configuracoes()
		self.pastadefault = conf_prog.pasta_padrao_jogos
		logger.debug('Pasta default mudada para %s' %self.pastadefault)

		x = lista_de_jogos(self.pastadefault)
		self.jogos_e_info = x.jogos_e_info
		self.listjogos = self.jogos_e_info[0]
		event.Skip()
		bmp = wx.Image (os.path.join(corrente,'imagens','processando.jpg'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		busy = wx.SplashScreen ( bmp, wx.CENTER_ON_SCREEN | wx.SPLASH_TIMEOUT, 1200, None, style = wx.NO_BORDER | wx.SIMPLE_BORDER | wx.STAY_ON_TOP )
		wx.Yield()
		self.atualizar()
		del busy

	
	def ReadFile(self, arquivosiso):
		logger.debug(u'Na funcao ReadFile os arquivos que serão lidos serão: %s' %(arquivosiso))
		result = verifica_jogo(arquivosiso)
		resultados=result.resultado_final
		self.resultados = resultados


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
		event.Skip()
		bmp = wx.Image (os.path.join(corrente,'imagens','processando.jpg'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		busy = wx.SplashScreen ( bmp, wx.CENTER_ON_SCREEN | wx.SPLASH_TIMEOUT, 1200, None, style = wx.NO_BORDER | wx.SIMPLE_BORDER | wx.STAY_ON_TOP )
		wx.Yield()
		self.atualizar()
		del busy

	def dofilho2(self, event):
		self.form3.SetValue(str(memoria['jogos_selecionados']))
		self.form4.SetValue(convert_tamanho(memoria['tamanho_total_dos_jogos']))

class painel_de_jogos(wx.Panel):
	def __init__ (self, parent, ID, pos, size, arquivo_do_jogo, codigo_do_jogo, nome_do_jogo, tamanho_do_jogo, lista_cover_art):
		wx.Panel.__init__(self, parent, wx.ID_ANY, pos, size, wx.EXPAND)
		self.arquivo_do_jogo = arquivo_do_jogo
		self.condigo_do_jogo = codigo_do_jogo
		self.parent = parent
		self.tamanho_total=0
		pastadefault = conf_prog.pasta_padrao_jogos
		self.tamanho_do_jogo = tamanho_do_jogo
		self.cover_art=lista_cover_art.localiza_cover_art(codigo_do_jogo)
		self.endereco_da_imagem = os.path.join(self.cover_art[0], self.cover_art[1])
		#try:
		if imagem_check.leitor_configuracao(self.endereco_da_imagem) == 'OK':
			pass
		else:
			retirar_exitf_imagem(self.endereco_da_imagem)
			imagem_check.mudar_configuracao(self.endereco_da_imagem, 'OK')
		imagem5 = wx.Image(self.endereco_da_imagem, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		#except:
		#	imagem_check.mudar_configuracao(self.endereco_da_imagem, 'Falhou')
		#	imagem5 = wx.Image(os.path.join(corrente, 'imagens', 'erro.jpg'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()

		new_imagem5 = wx.ImageFromBitmap(imagem5).Scale(70, 100, wx.IMAGE_QUALITY_NORMAL).ConvertToBitmap()
		mask = wx.Mask(new_imagem5, wx.BLUE)
		new_imagem5.SetMask(mask)
		self.botao_imagem = wx.BitmapButton(self, wx.ID_ANY, new_imagem5, (0, 0),(80, 110))
		self.botao_imagem.SetToolTipString(Tradutor(u"Clique na imagem para mudá-la", dicionario))
		self.Bind(wx.EVT_BUTTON , self.MudarImagem, self.botao_imagem)
		text0 = wx.StaticText(self, wx.ID_ANY, Tradutor(u"Código:", dicionario), (0, 0), style = wx.TE_RICH)
		self.form0 = wx.TextCtrl( self, wx.ID_ANY, codigo_do_jogo,(0,0), style = wx.TE_RICH)
		self.form0.Enabled = False
		text1 = wx.StaticText(self, wx.ID_ANY, Tradutor(u"Nome:", dicionario), (0, 0), style = wx.TE_RICH)
		self.form1 = wx.TextCtrl( self, wx.ID_ANY, nome_do_jogo,(0,0), style = wx.TE_RICH)
		self.form1.Enabled = False
		text2 = wx.StaticText(self, wx.ID_ANY, Tradutor("Arquivo:", dicionario), (0, 0), style = wx.TE_RICH)
		self.form2 = wx.TextCtrl( self, wx.ID_ANY, self.arquivo_do_jogo,(0,0),  style = wx.TE_RICH)
		if self.arquivo_do_jogo[-6:] =='ul.cfg':
			text2.SetForegroundColour(wx.RED)
			self.form2.SetForegroundColour(wx.RED)
		self.form2.Enabled = False
		text3 = wx.StaticText(self, wx.ID_ANY, Tradutor("Tamanho:", dicionario), (0, 0), style = wx.TE_RICH)
		self.form3 = wx.TextCtrl( self, wx.ID_ANY, convert_tamanho(self.tamanho_do_jogo),(0,0), style = wx.TE_RICH)
		self.form3.Enabled = False
		self.radio = wx.CheckBox(self, wx.ID_ANY, Tradutor("Selecionar", dicionario))
		self.Bind(wx.EVT_CHECKBOX, self.Selecionado, self.radio)
		self.botao_renomear = wx.Button(self, wx.ID_ANY, Tradutor('Renomear', dicionario), (0, 0))
		self.Bind(wx.EVT_BUTTON, self.Renomear, self.botao_renomear)
		self.botao_deletar = wx.Button(self, wx.ID_ANY, Tradutor('Deletar', dicionario), (0, 0))
		self.Bind(wx.EVT_BUTTON, self.Deletar, self.botao_deletar)
		self.botao_copiar_para = wx.Button(self, wx.ID_ANY, Tradutor('Copiar para...', dicionario), (0, 0))
		self.Bind(wx.EVT_BUTTON, self.CopiarPara, self.botao_copiar_para)

		self.MeuGridsizer = wx.GridBagSizer(3, 5)

		self.MeuGridsizer.Add(self.botao_imagem, (0,0),(4,2),  wx.ALL|wx.EXPAND, 2)
		self.MeuGridsizer.Add(text0, (0, 2), (1,1), wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
		self.MeuGridsizer.Add(self.form0, (0, 3), (1,4), wx.ALL|wx.EXPAND, 2)
		self.MeuGridsizer.Add(text1, (1, 2), (1,1), wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
		self.MeuGridsizer.Add(self.form1, (1, 3), (1,4), wx.ALL|wx.EXPAND, 2)
		self.MeuGridsizer.Add(text2, (2, 2), (1,1), wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
		self.MeuGridsizer.Add(self.form2, (2, 3), (1,4), wx.ALL|wx.EXPAND, 2)
		self.MeuGridsizer.Add(text3, (3, 2), (1,1), wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
		self.MeuGridsizer.Add(self.form3, (3, 3), (1,4), wx.ALL|wx.EXPAND, 2)
		self.MeuGridsizer.Add(self.radio, (4, 0),(3,2), wx.ALIGN_CENTER, 0)
		self.MeuGridsizer.Add(self.botao_renomear, (4,2), (2,1), wx.ALIGN_CENTER, 0)
		self.MeuGridsizer.Add(self.botao_deletar, (4,3), (2,1), wx.ALIGN_CENTER, 0)
		self.MeuGridsizer.Add(self.botao_copiar_para, (4,4), (2,1), wx.ALIGN_CENTER, 0)
		self.MeuGridsizer.AddGrowableCol(6)
		self.SetSizerAndFit(self.MeuGridsizer)
		self.Centre()
		self.Layout()

	def Renomear(self, event):
		
		if self.form1.Enabled == False:
			self.form1.Enabled = True
			self.botao_renomear.SetLabel("OK")
			self.acao_enderecodojogo = self.form2.GetValue()
			self.acao_codigo = self.form0.GetValue()
			self.acao_nomedojogoatual = self.form1.GetValue()
			
		elif self.form1.Enabled == True:
			if self.acao_nomedojogoatual == self.form1.GetValue():
				print 'Não mudou'
			elif self.arquivo_do_jogo[-6:] == 'ul.cfg':
				end_base = os.path.dirname(self.acao_enderecodojogo)
				muda_ul = manipula_ul()
				novo_nome_zx = self.form1.GetValue()
				retoronoul = muda_ul.renomear_jogo_ul(end_base, self.acao_nomedojogoatual, novo_nome_zx)
				self.form1.Enabled = False
				self.form1.SetValue(retoronoul)
				if retoronoul == novo_nome_zx:
					msgbox = wx.MessageDialog(self, Tradutor(u'O nome do arquivo foi alterado com sucesso!', dicionario), Tradutor('Sucesso!', dicionario), wx.OK | wx.ICON_INFORMATION)
					msgbox .ShowModal()
					msgbox .Destroy()
				else: 
					msg01 = Tradutor(u'O nome do arquivo foi alterado, mas como já havia um outro jogo com o mesmo nome, o programa renomeou para', dicionario)
					msg02 = u" %s" %retoronoul
					msg = msg01 + msg02
					msgbox = wx.MessageDialog(self, msg , Tradutor('Sucesso!', dicionario), wx.OK | wx.ICON_INFORMATION)
					msgbox .ShowModal()
					msgbox .Destroy()


			else:
				novo_nome_zx = self.form1.GetValue()
				resultafinal = muda_nome_jogo(self.acao_enderecodojogo, novo_nome_zx)
				self.form2.SetValue(resultafinal[0])
				self.form1.SetValue(resultafinal[2])
				self.form1.Enabled = False
				if resultafinal[2] == novo_nome_zx:
					msgbox = wx.MessageDialog(self, Tradutor(u'O nome do arquivo foi alterado com sucesso!', dicionario), Tradutor('Sucesso!', dicionario), wx.OK | wx.ICON_INFORMATION)
					msgbox .ShowModal()
					msgbox .Destroy()
				else: 
					msg01 = Tradutor(u'O nome do arquivo foi alterado, mas como já havia um outro jogo com o mesmo nome, o programa renomeou para', dicionario)
					msg02 = u" %s" %retoronoul
					msg = msg01 + msg02
					msgbox = wx.MessageDialog(self, msg , Tradutor('Sucesso!', dicionario), wx.OK | wx.ICON_INFORMATION)
					msgbox .ShowModal()
					msgbox .Destroy()
				self.form2.SetValue(resultafinal[0])
				self.form1.SetValue(resultafinal[2])
				self.form1.Enabled = False

			self.form1.Enabled = False
			self.botao_renomear.SetLabel("Renomear")

	def Deletar(self, event):
		msgbox = wx.MessageDialog(self, 'Deletando' , Tradutor('Deletando jogo', dicionario), wx.YES_NO | wx.ICON_INFORMATION)
		resultado = msgbox.ShowModal()
		self.acao_enderecodojogo = self.form2.GetValue()
		if resultado == wx.ID_YES:
			if self.arquivo_do_jogo[-6:] == 'ul.cfg':
				end_base = os.path.dirname(self.acao_enderecodojogo)
				deleta_ul = manipula_ul()
				novo_nome_zx = self.form1.GetValue()
				deleta_ul.deletar_jogo_ul(end_base, novo_nome_zx)
			else:
				os.remove(self.acao_enderecodojogo)
			self.form0.SetValue('')
			self.form1.SetValue('')
			self.form2.SetValue('')
			self.form3.SetValue('')

			self.botao_renomear.Enabled=False
			self.botao_deletar.Enabled=False
			self.botao_copiar_para.Enabled=False
			
			self.radio.Enabled=False

			self.SetBackgroundColour(wx.RED)
			
			self.form1.SetBackgroundColour(wx.RED)
			self.form2.SetBackgroundColour(wx.RED)
			self.form3.SetBackgroundColour(wx.RED)

			i = wx.Image(os.path.join(corrente, 'imagens', 'deletado.jpg'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
			isv = wx.ImageFromBitmap(i).Scale(70, 100, wx.IMAGE_QUALITY_NORMAL).ConvertToBitmap()
			self.botao_imagem.SetBitmapDisabled(isv)
			self.botao_imagem.Enabled=False
			self.Refresh()


		elif resultado == wx.ID_NO:
			pass
			msgbox.Destroy()


	def CopiarPara(self, event):
		nome_do_jogo=self.form1.GetValue()
		comparador = os.path.basename(self.form2.GetValue())
		if comparador == 'ul.cfg':
			tipo = 'ul.cfg'
		else:
			tipo = ''

		self.objcopiar = Copiar_para(self, wx.ID_ANY, Tradutor('Copiar para...', dicionario), self.form2.GetValue(), self.form0.GetValue(), nome_do_jogo, tamanho_do_jogo = self.tamanho_do_jogo, destino='',  tipo_origem = tipo, tipo_destino='')
		self.objcopiar.Show()


	
	def MudarImagem(self, event):
		wildcardx = "%s (*.jpg)|*.jpg|%s (*.png)|*.png" %(Tradutor('Imagem jpg', dicionario),Tradutor('Imagem png',dicionario))
		dlg = wx.FileDialog(self, Tradutor(u"Selecionando Imagem...", dicionario), os.path.dirname(self.endereco_da_imagem), style=wx.OPEN , wildcard=wildcardx)
		if dlg.ShowModal() == wx.ID_OK:
			self.arquivoimg = dlg.GetPath()
			logger.info('%s' %self.arquivoimg)
			dlg.Destroy()
			if not self.endereco_da_imagem == self.arquivoimg[0]:
				retirar_exitf_imagem(self.arquivoimg)
				extencao = self.arquivoimg.split('.')[-1]
				pasta_art = conf_prog.leitor_configuracao(chave='pasta_ART')
				nome_da_imagem = "%s_COV.%s" %(self.condigo_do_jogo, extencao)
				with open(self.arquivoimg, 'rb') as imgdfg:
					conteudo = imgdfg.read()

					destinodfg = os.path.join(pasta_art, nome_da_imagem)
					print destinodfg
					with open(destinodfg, 'wb') as binaimagem:
						binaimagem.write(conteudo)

				imagem_check.mudar_configuracao(destinodfg, 'OK')
				i = wx.Image(os.path.join(pasta_art, nome_da_imagem), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
				isv = wx.ImageFromBitmap(i).Scale(70, 100, wx.IMAGE_QUALITY_NORMAL).ConvertToBitmap()
				self.botao_imagem.SetBitmapDisabled(isv)
			dlg.Destroy()				


	def Selecionado(self, event):
		valor_do_radio = self.radio.GetValue()
		atual = memoria['tamanho_total_dos_jogos']
		selecionados = memoria['jogos_selecionados']
		if valor_do_radio == True:
			atual += self.tamanho_do_jogo
			selecionados+= 1
		elif valor_do_radio == False:
			atual -= self.tamanho_do_jogo
			selecionados-=1
		memoria['tamanho_total_dos_jogos'] = atual
		memoria['jogos_selecionados'] = selecionados
		
		wx.PostEvent(self.parent, event)

class frame_adicionar_multiplos(wx.Frame):
	def __init__ (self, title, lista_de_jogos, total_geral, pos, size):
		wx.Frame.__init__(self, None, wx.ID_ANY, title, pos, size)
		self.listjogos=lista_de_jogos
		self.lista_de_selecionados=[]
		self.pastadefault = conf_prog.pasta_padrao_jogos
		self.tamanho_vindo_do_filho = 0

		#self.painel_principal.Destroy()
		self.painel_principal = wx.Panel(self, wx.ID_ANY) #Painel Pinricpal

		sizer_panel_titulo = wx.GridBagSizer(0, 0) #sizers
		sizer_panel = wx.GridBagSizer(0, 100)

		sizer_panel_rodape = wx.GridSizer(cols=1, hgap=0, vgap=0)

		#self.SendSizeEvent() #uncomente no atualizar

		self.painel_cabecalho = wx.Panel(self.painel_principal, wx.ID_ANY, (0,0),(-1,25), style = wx.ALIGN_CENTER|wx.ALL|wx.EXPAND)
		text0 = wx.StaticText(self.painel_cabecalho, wx.ID_ANY, Tradutor(u"Copiando multiplos jogos", dicionario), (0, 0), style = wx.TE_RICH)
		font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
		text0.SetFont(font)
		sizer_panel_titulo.Add(text0, (0,0), (1,1), wx.ALIGN_CENTER, 5)
		sizer_panel_titulo.AddGrowableCol(0)
		self.painel_cabecalho.SetSizerAndFit(sizer_panel_titulo)

		self.painel_scroll = wx.ScrolledWindow(self.painel_principal, wx.ID_ANY, (0,0),(-1,200))		
		sizer_jogos = wx.BoxSizer(wx.VERTICAL)
		self.imagens_jogos = imagens_jogos(os.path.join(self.pastadefault,'ART'))
		logger.debug(self.imagens_jogos)
		wx.Yield()
		linha_horizontal = wx.StaticLine(self.painel_scroll, id=wx.ID_ANY, pos=(0,0), size=(-1,-1),
								style=wx.LI_HORIZONTAL| wx.BORDER_DOUBLE)
		sizer_jogos.Add(linha_horizontal, 0, wx.ALIGN_CENTER, 5)
		self.tamanho_selecionado = 0
		tot_selecionado = 0
		id_jogos = 0

		for x in self.listjogos:
			id_jogos +=1
			ppp = painel_lista_de_jogos(self.painel_scroll, wx.ID_NEW, (0,0),(-1,-1),
				arquivo_do_jogo = x[0], codigo_do_jogo = x[1], nome_do_jogo = x[2], tamanho_do_jogo = x[3], id_jogo = id_jogos, lista_cover_art = self.imagens_jogos)
			sizer_jogos.Add(ppp, 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND,0)
			self.SendSizeEvent()
			if not ppp.tamanho_computado==0:
				tot_selecionado+=1


			self.tamanho_selecionado +=ppp.tamanho_computado
		memoria['multiplos_selecionados'] = [tot_selecionado, self.tamanho_selecionado]

			
		self.painel_scroll.SetWindowStyleFlag(wx.ALIGN_CENTER|wx.ALL|wx.EXPAND|wx.BORDER_DOUBLE)
		self.painel_scroll.SetSizer(sizer_jogos)
		self.painel_scroll.SetScrollbars(1, 1, -1, -1)

		#rodapé
		self.painel_botao_confirmar = wx.Panel(self.painel_principal, wx.ID_ANY, (0,0),(-1,-1), style = wx.ALIGN_CENTER|wx.ALL|wx.EXPAND)

		self.botao_confirmar = wx.Button(self.painel_botao_confirmar, wx.ID_ANY, 'OK')
		self.Bind(wx.EVT_BUTTON, self.Confirmar, self.botao_confirmar)
		sizer_panel_rodape.Add(self.botao_confirmar , 0, wx.ALIGN_CENTER|wx.ALL, 5)


		self.painel_botao_confirmar.SetSizerAndFit(sizer_panel_rodape)



		sizer_panel.Add(self.painel_cabecalho, (0,0),(1,1), wx.ALL|wx.EXPAND, 5)
		sizer_panel.Add(self.painel_scroll, (1,0),(3,1), wx.ALL|wx.EXPAND, 5)
		sizer_panel.Add(self.painel_botao_confirmar, (4,0),(1,1), wx.ALL|wx.EXPAND, 5)
		sizer_panel.AddGrowableCol(0)
		sizer_panel.AddGrowableRow(1)
		self.painel_principal.SetSizerAndFit(sizer_panel)


		# self.Bind(wx.EVT_BUTTON, self.dofilho) #No atualizar deve ser comentado
		self.Layout()
		self.CenterOnScreen()
		self.SendSizeEvent()
		self.Bind(wx.EVT_CHECKBOX, self.DoFilho)
	def DoFilho (self, event):
		print 'do filho'


	def Confirmar(self, event):
		pass

class painel_lista_de_jogos(wx.Panel):
	def __init__ (self, parent, ID, pos, size, arquivo_do_jogo, codigo_do_jogo, nome_do_jogo, tamanho_do_jogo, id_jogo, lista_cover_art):
		wx.Panel.__init__(self, parent, wx.ID_ANY, pos, size, wx.EXPAND)
		self.arquivo_do_jogo = arquivo_do_jogo
		self.condigo_do_jogo = codigo_do_jogo[0]
		self.parent = parent
		self.tamanho_total=0
		pastadefault = conf_prog.pasta_padrao_jogos
		self.tamanho_do_jogo = tamanho_do_jogo
		self.tamanho_computado = tamanho_do_jogo
		print codigo_do_jogo
		if codigo_do_jogo[0] == False or codigo_do_jogo[1] == False:
			self.status = u'ERRO'
			self.condigo_do_jogo = 'XXXX_000.00'
			self.tamanho_computado=0
		else:
			self.status = 'OK'

		text0 = wx.StaticText(self, wx.ID_ANY, Tradutor(u"Código:", dicionario), (0, 0), style = wx.TE_RICH|  wx.ALIGN_CENTER_VERTICAL )
		self.form0 = wx.TextCtrl( self, wx.ID_ANY, u'%s' %self.condigo_do_jogo,(0,0), (85, -1), style = wx.TE_RICH)
		self.form0.Enabled = False if self.status == "OK" else True
		text1 = wx.StaticText(self, wx.ID_ANY, Tradutor(u"Nome:", dicionario), (0, 0), style = wx.TE_RICH)
		self.form1 = wx.TextCtrl( self, wx.ID_ANY, nome_do_jogo[0],(0,0), (200,-1), style = wx.TE_RICH)
		self.form1.Enabled = False if not nome_do_jogo[0] == 'NOME_DO_JOGO' else True
		text2 = wx.StaticText(self, wx.ID_ANY, Tradutor("Arquivo:", dicionario), (0, 0), style = wx.TE_RICH)
		self.form2 = wx.TextCtrl( self, wx.ID_ANY, self.arquivo_do_jogo[0],(0,0),  style = wx.TE_RICH)
		self.form2.Enabled = False
		text3 = wx.StaticText(self, wx.ID_ANY, Tradutor("Tamanho:", dicionario), (0, 0), style = wx.TE_RICH)
		self.form3 = wx.TextCtrl( self, wx.ID_ANY, convert_tamanho(self.tamanho_do_jogo),(0,0), style = wx.TE_RICH)
		self.form3.Enabled = False
		self.radio = wx.CheckBox(self, wx.ID_ANY, Tradutor("Selecionar", dicionario))

		self.radio.SetValue(True if self.status == "OK" else False)
		self.Bind(wx.EVT_CHECKBOX, self.Selecionado, self.radio)
		text4 = wx.StaticText(self, wx.ID_ANY, Tradutor("Status:", dicionario), (0, 0), style = wx.TE_RICH)
		self.form4 = wx.TextCtrl( self, wx.ID_ANY, self.status,(0,0), (50,-1), style = wx.TE_RICH)
		self.form4.Enabled = False
		linha = wx.StaticLine(self, id=wx.ID_ANY, pos=(0,0), size=(-1,-1),
									style=wx.LI_HORIZONTAL| wx.BORDER_DOUBLE)

		self.MeuGridsizer = wx.GridBagSizer(0, 5)

		self.MeuGridsizer.Add(text0, (0, 1), (1,1), wx.ALIGN_RIGHT| wx.ALIGN_CENTER_VERTICAL, 0)
		self.MeuGridsizer.Add(self.form0, (0, 2), (1,1), wx.ALL|wx.EXPAND, 0)
		self.MeuGridsizer.Add(text1, (0, 3), (1,1), wx.ALIGN_RIGHT| wx.ALIGN_CENTER_VERTICAL, 0)
		self.MeuGridsizer.Add(self.form1, (0, 4), (1,1), wx.ALL|wx.EXPAND, 0)
		self.MeuGridsizer.Add(text2, (0, 5), (1,1), wx.ALIGN_RIGHT| wx.ALIGN_CENTER_VERTICAL, 0)
		self.MeuGridsizer.Add(self.form2, (0, 6), (1,1), wx.ALL|wx.EXPAND, 0)
		self.MeuGridsizer.Add(text3, (0, 7), (1,1), wx.ALIGN_RIGHT| wx.ALIGN_CENTER_VERTICAL, 0)
		self.MeuGridsizer.Add(self.form3, (0, 8), (1,2), wx.ALL|wx.EXPAND, 0)
		self.MeuGridsizer.Add(text4, (0, 10), (1,1), wx.ALIGN_RIGHT| wx.ALIGN_CENTER_VERTICAL, 0)
		self.MeuGridsizer.Add(self.form4, (0, 11), (1,1), wx.ALL|wx.EXPAND, 0)
		self.MeuGridsizer.Add(self.radio, (0, 12),(1,1), wx.ALL|wx.EXPAND, 0)
		self.MeuGridsizer.Add(linha, (1,0),(1,13), wx.ALL|wx.EXPAND, 5)
		self.MeuGridsizer.AddGrowableCol(6)

		self.SetSizerAndFit(self.MeuGridsizer)
		self.Centre()
		self.Layout()
	def Selecionado (self, event):
		memoria['multiplos_jogoselecionado_%s' %id_jogo] = self.radio.GetValue()
		wx.PostEvent(self.parent, event)

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
		self.estado = config_pasta_jogos


		text0 = wx.StaticText(painel, wx.ID_ANY, Tradutor(u"Pasta de jogos", dicionario), (0, 0))

		self.form0 = wx.TextCtrl( painel, wx.ID_ANY, config_pasta_jogos,(0,0), (250,-1))
		self.form0.Enabled = False
		botao0 = wx.Button(painel, wx.ID_ANY, '...', (0,0), (20,20))
		self.Bind(wx.EVT_BUTTON, self.PegaPastaJogo, botao0)
		text1 = wx.StaticText(painel, wx.ID_ANY, Tradutor(u"Arquivos de Tradução",dicionario), (0, 0))
		self.form1 = wx.TextCtrl(painel, wx.ID_ANY, "",(0,0), (250,-1))
		self.form1.Enabled = False
		botao1 = wx.Button(painel, wx.ID_ANY, '...', (0,0), (20,20))
		self.Bind(wx.EVT_BUTTON, self.PegaArquivoTradu, botao1)
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

		botaook = wx.Button(painel, wx.ID_OK, 'OK', (0,0))
		self.Bind(wx.EVT_BUTTON, self.Confirmar, botaook)

		sizer = wx.GridBagSizer(0, 10)
		sizer2 = wx.GridBagSizer(0, 0)

		sizer.Add(text0, (1, 1), (1,1), wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
		sizer.Add(self.form0, (1, 2), (1,2), wx.ALL|wx.EXPAND, 2)
		sizer.Add(botao0, (1, 4), (1,4), wx.ALL, 2)
		sizer.Add(text1, (2, 1), (1,1), wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
		sizer.Add(self.form1, (2, 2), (1,2), wx.ALL|wx.EXPAND, 2)
		sizer.Add(botao1, (2, 4), (1,4), wx.ALL, 2)
		sizer.Add(linha_horizontal, (3, 1), (1,5), wx.ALL|wx.EXPAND|wx.ALIGN_CENTER, 4)
		sizer.Add(text2, (4, 1), (1,1), wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
		sizer.Add(self.form2, (4, 2), (1,2), wx.ALL|wx.EXPAND, 2)
		sizer.Add(text3, (5, 1), (1,1), wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
		sizer.Add(self.form3, (5, 2), (1,2), wx.ALL|wx.EXPAND, 2)
		sizer.Add(text4, (6, 1), (1,1), wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
		sizer.Add(self.form4, (6, 2), (1,2), wx.ALL|wx.EXPAND, 2)
		sizer.Add(text5, (7, 1), (1,1), wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
		sizer.Add(self.form5, (7, 2), (1,2), wx.ALL|wx.EXPAND, 2)
		sizer.Add(botaook, (9,0), (2,7), wx.ALL|wx.ALIGN_CENTER, 10)	

		painel.SetSizerAndFit(sizer)
		sizer2.Add(painel, (0,0), (1,1), wx.ALL|wx.EXPAND|wx.ALIGN_CENTER)
		sizer2.AddGrowableCol(0)
		sizer2.AddGrowableRow(0)
		self.SetSizerAndFit(sizer2)
		self.Centre()

	def PegaPastaJogo (self, event):
		dlg = wx.DirDialog(self, Tradutor(u"Selecionando pasta de jogos...", dicionario), corrente, style=wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			valor_dialog = dlg.GetPath()
			self.form0.SetValue(valor_dialog)
			self.DVD = os.path.join(valor_dialog, 'DVD')
			self.CD = os.path.join(valor_dialog, 'CD')
			self.ART = os.path.join(valor_dialog, 'ART')
			self.CFG = os.path.join(valor_dialog, 'CFG')

			self.form2.SetValue(self.DVD)
			self.form3.SetValue(self.CD)
			self.form4.SetValue(self.ART)
			self.form5.SetValue(self.CFG)
			dlg.Destroy()
	
	def PegaArquivoTradu (self,event):
		self.wildcard2 = u"%s (*.lng)|*.lng" %(Tradutor(u'Arquivo de Tradução', dicionario))
		dlg2 = wx.FileDialog(self, Tradutor(u'Selecionando arquivo de tradução', dicionario), corrente, style=wx.OPEN, wildcard=self.wildcard2)
		if dlg2.ShowModal() == wx.ID_OK:
			valor_dialog = dlg2.GetPath()
			self.form1.SetValue(self.valor_dialog)

	def Confirmar (self, event):
		confg1 = self.form0.GetValue()
		confg2 = self.form1.GetValue()
		conf_prog.mudar_configuracao('pasta_destino_jogos', confg1)
		conf_prog.mudar_configuracao('dicionario', confg2)

		lista_de_diretorios = [['pasta_DVD',self.DVD],['pasta_CD', self.CD],['pasta_ART', self.ART],['pasta_CFG', self.CFG]]
		for dirs in lista_de_diretorios:
			try:
				os.makedirs(dirs[1])
				conf_prog.mudar_configuracao(dirs[0], dirs[1])
			except:
				if os.path.exists(dirs[1]):
					conf_prog.mudar_configuracao(dirs[0], dirs[1])
				
		self.Destroy()
		if not confg1 == self.estado:
			wx.PostEvent(self.parent, event)

class janela_adicionar_iso(wx.Frame):
	def __init__ (self, parent, ID, title, endereco = ('',False), codigo_do_jogo=(False,False), nome_do_jogo=('NOVO_JOGO', True), tamanho_do_jogo=0, lista_de_jogos=[]):
		wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
		texto_adicional ='\n\n%s' %Tradutor(u'OBSERVAÇÃO: Caso coloque um nome já usado o programa se encarregará de por um nome válido, Ex.:XXX_000.00.NOME_DO_ARQUIVO - 01', dicionario)
		for procus in lista_de_jogos:
			if procus[1] == codigo_do_jogo[0]:
				T1 = Tradutor(u'OBSERVAÇÃO: Já existe uma jogo com esse mesmo código localizado em', dicionario)
				T2 = Tradutor(u'de nome', dicionario)
				T3 =  Tradutor(u'e tamanho', dicionario)
				texto_adicional = u'\n\n%s "%s" %s "%s" %s "%s". O programa se encarregará de colocar um nome válido. Ex.: XXX_000.00.NOME_DO_ARQUIVO - 01' %(T1, procus[0], T2, procus[2], T3, convert_tamanho(procus[3]))

		self.parent=parent
		self.endereco_do_jogo=endereco[0]
		self.codigo_do_jogo=codigo_do_jogo
		self.nome_do_jogo=nome_do_jogo[0]
		self.tamanho_do_jogo = convert_tamanho(tamanho_do_jogo)
		pastadefault = conf_prog.pasta_padrao_jogos
		self.config_pasta_jogos = conf_prog.leitor_configuracao('pasta_destino_jogos')
		self.midia = ['CD', 'DVD', 'ul.cfg']

		print self.codigo_do_jogo
		if self.codigo_do_jogo[0]==False and self.codigo_do_jogo[1]==False:
			texto_info = Tradutor(u"ATENÇÃO: O arquivo ISO selecionado não passou na checagem. Ao abrir o arquivo não foi encontrado o arquivo código característicos dos jogos de PS2. Isso pode ocorrer em jogos que possui alguma proteção.", dicionario)
		elif not self.codigo_do_jogo[0]==False and self.codigo_do_jogo[1]==False:
			texto_info = Tradutor(u"O arquivo ISO selecionado não passou no teste, ", dicionario)+" "+Tradutor(u"Ao abrir o arquivo não foi encontrado o arquivo código característicos dos jogos de PS2. Porém no nome do ISO selecionado apresenta um código válido.", dicionario)
		elif self.codigo_do_jogo[0]==False and self.codigo_do_jogo[1]==True:
			texto_info = Tradutor(u"O arquivo ISO passou no teste. O código sugerido acima foi encontrado em seu interior.", dicionario)
		else:
			texto_info = Tradutor(u"A checagem do arquivo ISO ocorreu sem problemas. O código sugerido acima foi encontrado em seu interior.", dicionario)
		texto_info += texto_adicional

		painel = wx.Panel(self, wx.ID_ANY, (0,0), (400,300))
		text0 = wx.StaticText(painel, wx.ID_ANY, Tradutor(u"Código do jogo", dicionario), (0, 0))
		self.form0 = wx.TextCtrl( painel, wx.ID_ANY, self.codigo_do_jogo[0] if not self.codigo_do_jogo[0]==False else '' ,(0,0), (250,-1))
		text1 = wx.StaticText(painel, wx.ID_ANY, Tradutor(u"Nome do jogo",dicionario), (0, 0))
		self.form1 = wx.TextCtrl(painel, wx.ID_ANY, self.nome_do_jogo,(0,0), (250,-1))
		text2 = wx.StaticText(painel, wx.ID_ANY, Tradutor(u"Tamanho do jogo",dicionario), (0, 0))
		self.form2 = wx.TextCtrl(painel, wx.ID_ANY, self.tamanho_do_jogo,(0,0), (250,-1))
		self.radius1 = wx.RadioBox(painel, wx.ID_ANY, Tradutor(u"Mídia", dicionario), wx.DefaultPosition, wx.DefaultSize,
                self.midia, 3, wx.RA_SPECIFY_ROWS)

		if tamanho_do_jogo > 1024*1024*750:
			self.radius1.SetSelection(1)
		elif tamanho_do_jogo > 1024*1024*1024*1024:
			self.radius1.SetSelection(2)
		else:
			self.radius1.SetSelection(0)
                
		linha_horizontal = wx.StaticLine(painel, id=wx.ID_ANY, pos=(0,0), size=(-1,-1),
										style=wx.LI_HORIZONTAL| wx.BORDER_DOUBLE)

		text3 = wx.StaticText(painel, wx.ID_ANY, texto_info, (0, 0), style = wx.ALIGN_CENTER| wx.TE_MULTILINE)
		text3.Wrap(400)
		
		botaook = wx.Button(painel, wx.ID_OK, 'OK', (0,0))
		botaocancelar = wx.Button(painel, wx.ID_CANCEL, Tradutor('CANCELAR',dicionario), (0,0))
		self.Bind(wx.EVT_BUTTON, self.Confirmar, botaook)

		self.Bind(wx.EVT_BUTTON, self.Cancelar, botaocancelar)

		sizer_botoes = wx.GridSizer(cols=2, hgap=30, vgap=0)
		sizer_botoes.Add(botaook, 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND,5)
		sizer_botoes.Add(botaocancelar, 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND,5)

		sizer = wx.GridBagSizer(10, 10)
		sizer.Add(text0, (1, 1), (1,1), wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
		sizer.Add(self.form0, (1, 2), (1,1), wx.ALL|wx.EXPAND, 2)
		sizer.Add(text1, (2, 1), (1,1), wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
		sizer.Add(self.form1, (2, 2), (1,1), wx.ALL|wx.EXPAND, 2)
		sizer.Add(text2, (3, 1), (1,1), wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
		sizer.Add(self.form2, (3, 2), (1,1), wx.ALL|wx.EXPAND, 2)
		sizer.Add (self.radius1, (1,3),(3,2), wx.ALL|wx.EXPAND, 2)
		sizer.Add(linha_horizontal, (4, 0), (1,7), wx.ALL|wx.EXPAND|wx.ALIGN_CENTER, 4)
		sizer.Add(text3, (5, 0), (2,7), wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL, 2)
		sizer.Add(sizer_botoes, (7,0), (2,7), wx.ALL|wx.ALIGN_CENTER|wx.EXPAND, 10)

		sizer.AddGrowableRow(5)
		painel.SetSizerAndFit(sizer)

		sizer2 = wx.GridBagSizer(0, 0)
		sizer2.Add(painel, (0,0), (1,1), wx.ALL|wx.EXPAND|wx.ALIGN_CENTER)
		sizer2.AddGrowableCol(0)
		sizer2.AddGrowableRow(0)
		self.SetSizerAndFit(sizer2)
		self.Centre()

	def Pega_pasta_jogo (self, event):
		pass

	def Confirmar (self, event):
		self.yy = ProgressDialog(self, '%s %s' %(Tradutor(u'Adicionando ', dicionario) , self.nome_do_jogo))
		self.yy.Show()
		valor_tipo = self.radius1.GetSelection()

		tradu = self.midia[self.radius1.GetSelection()]
		print tradu
		if valor_tipo == 2:
			self.yy.CopiarParaUl(self.endereco_do_jogo, self.codigo_do_jogo[0], self.nome_do_jogo, self.config_pasta_jogos)
		else:
			self.yy.CopiarParaIso(self.endereco_do_jogo, self.codigo_do_jogo[0], self.nome_do_jogo, self.tamanho_do_jogo, self.config_pasta_jogos, tipo_destino = self.midia[self.radius1.GetSelection()])
		self.Destroy()

	def Cancelar(self, event):
		self.Destroy()

class Copiar_para(wx.Frame):
	def __init__ (self, parent, ID, title, endereco_do_jogo, codigo_do_jogo, nome_do_jogo, tamanho_do_jogo=0, destino = '', tipo_origem = '', tipo_destino=''):
		wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

		self.endereco_do_jogo=endereco_do_jogo
		self.codigo_do_jogo=codigo_do_jogo
		self.nome_do_jogo=nome_do_jogo
		self.tamanho_do_jogo = tamanho_do_jogo
		self.destino = destino
		self.tipo_origem = tipo_origem
		self.tipo_destino = tipo_destino

		painel = wx.Panel(self, wx.ID_ANY, (0,0), (400,300))

		text0 = wx.StaticText(painel, wx.ID_ANY, Tradutor(u"Destino", dicionario), (0, 0))
		self.form0 = wx.TextCtrl( painel, wx.ID_ANY, destino,(0,0), (250,-1))
		self.form0.Enabled = False
		botao0 = wx.Button(painel, wx.ID_ANY, '...', (0,0), (20,20))
		self.Bind(wx.EVT_BUTTON, self.PegaPastaDestino, botao0)
		if tipo_origem == 'ul.cfg':
			texto1 = Tradutor(u'Copiar no padrão ul.cfg', dicionario)
			texto2 = Tradutor(u'Converter ao padrão ISO', dicionario)
		else:
			texto1 = Tradutor(u'Converter ao padrão ul.cfg', dicionario)
			texto2 = Tradutor(u'Copiar no padrão ISO', dicionario)
		self.midia=[texto1, texto2]

		self.radius1 = wx.RadioBox(painel, wx.ID_ANY, Tradutor(u"Escolha qual método de cópia.", dicionario), wx.DefaultPosition, wx.DefaultSize,
                self.midia, 2, wx.RA_SPECIFY_COLS| wx.ALIGN_CENTER)

		botaook = wx.Button(painel, wx.ID_OK, 'OK', (0,0))
		self.Bind(wx.EVT_BUTTON, self.Confirmar, botaook)

		sizer = wx.GridBagSizer(0, 10)
		sizer2 = wx.GridBagSizer(0, 0)

		sizer.Add(text0, (1, 1), (1,1), wx.ALIGN_RIGHT, 2)
		sizer.Add(self.form0, (1, 2), (1,2), wx.ALL|wx.EXPAND, 2)
		sizer.Add(botao0, (1, 4), (1,4), wx.ALL, 2)
		sizer.Add(self.radius1, (2, 1), (2,3), wx.ALL|wx.EXPAND|wx.ALIGN_CENTER, 2)
		sizer.Add(botaook, (5,1), (2,5), wx.ALL|wx.ALIGN_CENTER, 10)	

		painel.SetSizerAndFit(sizer)
		sizer2.Add(painel, (0,0), (1,1), wx.ALL|wx.EXPAND|wx.ALIGN_CENTER)
		sizer2.AddGrowableCol(0)
		sizer2.AddGrowableRow(0)
		self.SetSizerAndFit(sizer2)
		self.Centre()

	def PegaPastaDestino(self, event):
		dlg = wx.DirDialog(self, Tradutor(u"Selecionando pasta destino...", dicionario), corrente, style=wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.valor_dialog = dlg.GetPath()
			self.form0.SetValue(self.valor_dialog)

	def Confirmar (self, event):
			if self.form0.GetValue() == '':
				msgbox = wx.MessageDialog(self, Tradutor(u'Escolhar um dispositivo ou pasta como destino da cópia.', dicionario), Tradutor(u'Atenção!', dicionario), wx.OK | wx.ICON_INFORMATION)
				resultado = msgbox.ShowModal()
			else:
				if self.radius1.GetSelection() == 0:

					self.zzxxdd = ProgressDialog(self, '%s %s' %(Tradutor(u'Copiando', dicionario) , self.nome_do_jogo))
					self.zzxxdd.Show()
					self.zzxxdd.CopiarParaUl(self.endereco_do_jogo, self.codigo_do_jogo, self.nome_do_jogo, destino=self.valor_dialog , tipo_origem=self.tipo_origem, BUFFER = 1024, tamanho_maximo_fatia = 1073741824)
					self.Destroy()
				else:
					self.zzxxdd = ProgressDialog(self, '%s %s' %(Tradutor(u'Copiando', dicionario) , self.nome_do_jogo))
					self.zzxxdd.Show()

					self.zzxxdd.CopiarParaIso(self.endereco_do_jogo, self.codigo_do_jogo, self.nome_do_jogo, self.tamanho_do_jogo, pasta_destino=self.valor_dialog)
					self.Destroy()				
	
class ProgressDialog(wx.Dialog):

	def __init__(self, parent, title, cancelar_ativo=True):
		wx.Dialog.__init__(self, parent, title=title, style=wx.CAPTION)
		self.count = 0
		self.progresso=0
		self.acabouse = False

		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
		self.gauge = wx.Gauge(self, range=100, size=(180, 30))
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.gauge, 0, wx.ALL, 10)

		if cancelar_ativo:
			self.cancel = wx.Button(self, wx.ID_CANCEL, "&Cancel")
			self.cancel.SetDefault()
			self.cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
			btnSizer = wx.StdDialogButtonSizer()
			btnSizer.AddButton(self.cancel)
			btnSizer.Realize()
			sizer.Add(btnSizer, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
			self.SetSizer(sizer)
			sizer.Fit(self)
			self.SetFocus()
			self.timer.Start(5)


	def CopiarParaIso(self, endereco_do_jogo, codigo_do_jogo, nome_do_jogo, tamanho_total, pasta_destino, tipo_origem = '',tipo_destino = ''):

		self.tipo = tipo_destino if not tipo_destino == 'ul.cfg' else ''
		self.endereco_do_jogo = endereco_do_jogo
		self.codigo_do_jogox = codigo_do_jogo
		self.nome_do_jogo = nome_do_jogo
		self.pasta_destino_jogos = pasta_destino
		self.tamanho_do_jogo=tamanho_total
		self.progresso=0
		if type(self.nome_do_jogo) == list():
			arquivos = self.endereco_do_jogo
		else:
			arquivos = [self.endereco_do_jogo]
		if os.path.basename(self.endereco_do_jogo) == 'ul.cfg' or tipo_origem == 'ul.cfg':
			basedirhjk = os.path.dirname(self.endereco_do_jogo)
			nomeulsdf = "ul.%08X.%s.*" %(pycrc32.crc32(nome_do_jogo), codigo_do_jogo)
			arqudf = glob.glob(os.path.join(basedirhjk, nomeulsdf))
			arquivos=arqudf



		self.destinov = os.path.join(self.pasta_destino_jogos, self.tipo)
		nome='%s.%s.iso'%(self.codigo_do_jogox, self.nome_do_jogo)

		gravados = 0
		BUFFER = 1024
		self.arquivo_em_uso = os.path.join(self.destinov, nome)
		automatico = 0
		while os.path.exists(self.arquivo_em_uso):
			automatico+=1
			novo_nome = "%s.%s - %02d.iso" %(self.codigo_do_jogox, self.nome_do_jogo, automatico)
			self.arquivo_em_uso = os.path.join(self.destinov, novo_nome)
		try:
			os.makedirs(self.destinov)
		except:
			print 'Pasta já existe ou não pode ser criada'
		with open(self.arquivo_em_uso, "wb") as self.arquivo_alvo:
			tamanho_total=0
			for f in arquivos:
				vv = os.stat(f)

				tamanho_parcial = vv.st_size
				tamanho_total += tamanho_parcial
			for f in arquivos:
				with open(f, "rb") as self.arquivo_in:
					x = os.stat(f)
					self.tam = x.st_size

					while True:
						y = self.arquivo_in.read(BUFFER)
						self.tam-=BUFFER
						gravados +=BUFFER

						self.progresso = int((float(gravados)/float(tamanho_total))*100)
						self.gauge.SetValue(self.progresso)
						wx.Yield()
						try:
							self.arquivo_alvo.write(y)
						except ValueError:
							break
						if not self.tam > 0:
							self.acabouse = True
							break

	def CopiarParaUl(self, endereco_do_jogo, codigo_do_jogo, nome_do_jogo, destino='', tipo_origem='', BUFFER = 1024, tamanho_maximo_fatia = 1073741824):
		self.copiar_ul = manipula_ul()
		self.jogosul=''
		self.jogosul_hex=''
		if os.path.exists(os.path.join(destino,'ul.cfg')):
			with open(os.path.join(destino,'ul.cfg'), 'r') as jklq:
				conteudo_ulcfg=jklq.read()
			self.jogosul_hex = conteudo_ulcfg.encode('hex')

		if tipo_origem=="ul.cfg":
			crcorigem = pycrc32.crc32(nome_do_jogo)
			dfg=os.path.join(os.path.dirname(endereco_do_jogo),'ul.%08X.*'%crcorigem)
			partes = glob.glob(dfg)
			quant_de_partes = len(partes)
		else:
			starsfileklk = os.stat(endereco_do_jogo)
			tmldkopo = starsfileklk.st_size
			quant_de_partes = int(tmldkopo/tamanho_maximo_fatia+1)


		hex_jogo = self.copiar_ul.criar_nome_ul(codigo_do_jogo, nome_do_jogo, 'DVD', quant_de_partes).encode('hex')
		novo_hex = hex_jogo
		cont = 0
		novo_nome = nome_do_jogo

		hex_jogos_fatiados = []
		ini_co = 0
		for x in range(len(self.jogosul_hex)/128):
			hex_jogos_fatiados.append(self.jogosul_hex[ini_co:ini_co+128])
			ini_co+=128
		while hex_jogo in hex_jogos_fatiados:
			cont+=1
			str_cont = '%02d' %cont
			novo_nome = '%s %s' %(nome_do_jogo, str_cont)
			hex_jogo = self.copiar_ul.criar_nome_ul(codigo_do_jogo, nome_do_jogo, 'DVD', quant_de_partes).encode('hex')

		self.jogosul_hex = '%s%s'%(self.jogosul_hex, hex_jogo)

		if tipo_origem == 'ul.cfg':
			crcorigem = pycrc32.crc32(nome_do_jogo)

			dfg=os.path.join(os.path.dirname(endereco_do_jogo),'ul.%08X.*'%crcorigem)

			partes = glob.glob(dfg)
			nonono = self.copiar_ul.criar_nome_base_arquivo(codigo_do_jogo, novo_nome)
			cont2 = 0
			tamanho_total_local = 0
			gravados=0
			for parte in partes:
				starsfile = os.stat(parte)
				tamanhosss = starsfile.st_size
				tamanho_total_local +=tamanhosss
			for parte in partes:
				nonono2 = "%s.%02d" %(nonono, cont2)
				cont2+=1
				self.arquivo_em_uso = os.path.join(destino, nonono2)
				with open(self.arquivo_em_uso, "wb") as self.arquivo_alvo:
					with open(parte, "rb") as self.arquivo_in:
						zumba = os.stat(parte)
						self.tam = zumba.st_size
						while True:
							superbytes = self.arquivo_in.read(BUFFER)
							self.tam-=BUFFER
							gravados +=BUFFER

							self.progresso = int((float(gravados)/float(tamanho_total_local))*100)
							self.gauge.SetValue(self.progresso)
							wx.Yield()
							try:
								self.arquivo_alvo.write(superbytes)
							except ValueError:
								break
							if not self.tam > 0:
								break
							logger.debug('----------\nTotal: %s\nGravados: %s\nFaltando: %s\nProgresso: %s\n' %(tamanho_total_local, gravados, self.tam, self.progresso))
		else:
			gravados=0
			grav_xuxu = 0
			tamanho_total_local = 0
			starsfile = os.stat(endereco_do_jogo)
			tamanhosss = starsfile.st_size
			tamanho_total_local =tamanhosss
			self.tam = tamanho_total_local			
			
			self.tamanho_maximo_fatia  = tamanho_maximo_fatia 
			fatias = 0

			basename = self.copiar_ul.criar_nome_base_arquivo(codigo_do_jogo, novo_nome)

			ARQUIVO = endereco_do_jogo
			contador_de_bytes_gravados=0
			fim=False
			with open(ARQUIVO, 'rb') as arquivo_in:
				while True:
					self.arquivo_em_uso = os.path.join(destino,'%s.%02d' %(basename, fatias))
					self.arquivo_alvo = open(self.arquivo_em_uso, 'wb')
					gravados = 0
					while gravados < self.tamanho_maximo_fatia:

						datax = arquivo_in.read(BUFFER)
						if datax:
							self.arquivo_alvo.write(datax)
							self.tam -=BUFFER
							gravados += BUFFER
							grav_xuxu+= BUFFER
							self.progresso = int((float(grav_xuxu)/float(tamanho_total_local))*100)
							self.gauge.SetValue(self.progresso)
							wx.Yield()
						else:
							fim = True
							break
						logger.debug('----------\nTotal: %s\nGravados: %s\nFaltando: %s\nProgresso: %s\n' %(tamanho_total_local, gravados, self.tam, self.progresso))	
					fatias+=1
					if datax:
						pass
					else:
						logger.info('copia concluida')
						break
							
		with open(os.path.join(destino, 'ul.cfg'), 'w') as ulaberto:
			dadoshjxks = self.jogosul_hex.decode('hex')
			ulaberto.write(dadoshjxks)
		self.acabouse = True

	def on_timer(self, event):
	  	if self.acabouse == True:
	  		self.timer.Stop()
	  		self.Destroy()

	def on_cancel(self, event):
		if self.gauge.GetValue() == 100:
			self.Destroy()
		else:
			self.tam = -1
			time.sleep(2)
			self.arquivo_alvo.close()
			time.sleep(2)
			os.remove(self.arquivo_em_uso)
			self.Destroy()

if __name__ == '__main__':

	class meu_programa2(wx.App):
		def OnInit(self):
			self.title = "PhanterPS2"
			self.frame = frame_adicionar_multiplos(self.title, [],(-1,-1), (800,600))
			self.frame.Show()
			self.SetTopWindow(self.frame)
			return True

	y = meu_programa()
	y.MainLoop()



