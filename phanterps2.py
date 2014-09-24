# -*- coding: utf-8 -*- 
# Copyright (c) 2014 PhanterJR
# https://github.com/PhanterJR
# Licença LGPL
import wx
import wx.html
import os
import logging
from phanterdefs import tradutor, Configuracoes, LocalizaArt, LocalizaJogos, convert_tamanho, eh_cover_art,\
    VerificaJogo, ManipulaUl, retirar_exitf_imagem, muda_nome_jogo, ManipulaCfgJogo
import glob
from contrib import pycrc32
import time
import hashlib

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
corrente = os.getcwd()
imagem_check = Configuracoes('imagem_check.cfg')
memoria = {}
memoria['tamanho_total_dos_jogos'] = 0
memoria['jogos_selecionados'] = 0
memoria['progresso'] = 0
memoria['selecionado_para_copiar'] = {}
memoria['selecionados_multiplos'] = {}


class MeuPrograma(wx.App):

    def OnInit(self):

        self.title = "PhanterPS2"
        self.frame = FramePrincipal(self.title, (-1, -1), (1024, 728))
        icone = wx.Icon(os.path.join(corrente, 'imagens', 'icon.ico'), wx.BITMAP_TYPE_ICO)
        self.frame.SetIcon(icone)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


class FramePrincipal(wx.Frame):
    def __init__(self, title, pos, size):
        wx.Frame.__init__(self, None, wx.ID_ANY, title, pos, size)
        if os.path.exists(os.path.join(corrente, 'language')):
            try:
                os.makedirs(os.path.join(corrente, 'language'))
                with (os.path.join(corrente, 'language', 'sample.lng'), 'w') as ricos:
                    ricos.write('') 
            except:
                pass
        self.lista_de_selecionados = []
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        self.pastadefault = conf_prog.leitor_configuracao('PADRAO')
        self.tamanho_vindo_do_filho = 0

        self.CopiarTaAtivado = False
        imagem1 = wx.Image(os.path.join(corrente, 'imagens', 'isops2.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        imagem2 = wx.Image(os.path.join(corrente, 'imagens', 'multips2.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        imagem3 = wx.Image(os.path.join(corrente, 'imagens', 'atualizar.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        imagem4 = wx.Image(os.path.join(corrente, 'imagens', 'config.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.imagem5 = wx.Image(os.path.join(corrente, 'imagens', 'sobre.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.splashbmp = wx.Image(os.path.join(corrente, 'imagens', 'processando.jpg'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        new_imagem1 = wx.ImageFromBitmap(imagem1).Scale(16, 16,
                                                        wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()  # diminui a imagem para 16x16#
        new_imagem2 = wx.ImageFromBitmap(imagem2).Scale(16, 16,
                                                        wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()  # diminui a imagem para 16x16#
        new_imagem3 = wx.ImageFromBitmap(imagem3).Scale(16, 16,
                                                        wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()  # diminui a imagem para 16x16#
        new_imagem4 = wx.ImageFromBitmap(imagem4).Scale(16, 16,
                                                        wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()  # diminui a imagem para 16x16#
        new_imagem5 = wx.ImageFromBitmap(self.imagem5).Scale(16, 16,
                                                             wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()  # diminui a imagem para 16x16#

        self.title = title

        barra_de_status = self.CreateStatusBar()
        self.SetStatusText(tradutor("Bem vindo ao PhanterPS2", dicionario))

        barra_de_ferramentas = self.CreateToolBar()
        barra_de_ferramentas.SetBackgroundColour('#BEBEBE')

        tool1 = barra_de_ferramentas.AddSimpleTool(
            wx.NewId(), imagem1,
            tradutor("Adicionar novo jogo ISO", dicionario),
            tradutor(u"Selecionar imagens ISO para adicionar a lista de jogos", dicionario))
        tool2 = barra_de_ferramentas.AddSimpleTool(
            wx.NewId(), imagem2,
            tradutor(u'Adicionar múltiplos jogos ISO', dicionario),
            tradutor(u'Selecionar vários ISOs para adicionar a lista de jogos', dicionario))
        tool3 = barra_de_ferramentas.AddSimpleTool(
            wx.NewId(), imagem3,
            tradutor("Atualizar", dicionario),
            tradutor(u"Atualizar lista de jogos", dicionario))
        tool4 = barra_de_ferramentas.AddSimpleTool(
            wx.NewId(), imagem4, tradutor(u"Configurações", dicionario),
            tradutor("Configurar o PhanterPS2", dicionario))
        tool5 = barra_de_ferramentas.AddSimpleTool(
            wx.NewId(), self.imagem5,
            tradutor("Sobre", dicionario),
            tradutor(u"Sobre o programa e autor", dicionario))

        barra_de_ferramentas.Realize()

        Barra_de_menu = wx.MenuBar()
        menu_arquivo = wx.Menu()

        item1_menu_arquivo = wx.MenuItem(menu_arquivo, wx.ID_ANY,
                                         tradutor("A&dicionar novo ISO\tCtrl+A", dicionario),
                                         tradutor(u"Selecionar imagens ISO para adicionar a lista de jogos",
                                                  dicionario))
        item1_menu_arquivo.SetBitmap(new_imagem1)
        item2_menu_arquivo = wx.MenuItem(menu_arquivo, wx.ID_ANY,
                                         tradutor(u'A&dicionar múltiplos jogos ISO\tCtrl+M', dicionario),
                                         tradutor(u'Selecionar vários ISOs para adicionar a lista de jogos',
                                                  dicionario))
        item2_menu_arquivo.SetBitmap(new_imagem2)
        item3_menu_arquivo = wx.MenuItem(menu_arquivo, wx.ID_ANY,
                                         tradutor("A&tualizar", dicionario),
                                         tradutor(u"Atualizar lista de jogos", dicionario))
        item3_menu_arquivo.SetBitmap(new_imagem3)
        item4_menu_arquivo = wx.MenuItem(menu_arquivo, wx.ID_ANY,
                                         tradutor(u"Configurações", dicionario),
                                         tradutor(u"Configurar o PhanterPS2", dicionario))
        item4_menu_arquivo.SetBitmap(new_imagem4)

        menu_arquivo.AppendItem(item1_menu_arquivo)
        menu_arquivo.AppendItem(item2_menu_arquivo)
        menu_arquivo.AppendItem(item3_menu_arquivo)
        menu_arquivo.AppendItem(item4_menu_arquivo)

        Barra_de_menu.Append(menu_arquivo, tradutor("&Arquivo", dicionario))

        menu_sobre = wx.Menu()

        item1_menu_sobre = wx.MenuItem(menu_sobre, wx.ID_ANY, tradutor(u"&Sobre\tF1", dicionario),
                                       tradutor("Sobre o PhanterPS2", dicionario))
        item1_menu_sobre.SetBitmap(new_imagem5)
        menu_sobre.AppendItem(item1_menu_sobre)
        Barra_de_menu.Append(menu_sobre, tradutor("Ajuda", dicionario))
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
        self.Bind(wx.EVT_CHECKBOX, self.dofilho2)
        self.Bind(wx.EVT_BUTTON, self.dofilho)
        self.Atualizar_refresh()
        arquivo_de_senha = os.path.join(corrente, 'pwd')
        if not os.path.exists(arquivo_de_senha):
            login = LoginDialog(self, True)
            login.CenterOnParent()
            login.ShowModal()
            wx.Yield()

        self.Layout()


    def Atualizar_refresh(self, refresh = False):
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        if refresh == True:
            meusplash = MeuSplash(self,ID=wx.ID_ANY, gauge=True)
            meusplash.painel_bmp.SetBitmap(self.splashbmp)
            meusplash.Texto.SetLabel(tradutor('Localizando jogos...', dicionario))
            meusplash.Show(True)
            wx.Yield()
        else:
            meusplash = MeuSplash(self,ID=wx.ID_ANY, title=tradutor('Iniciando o Programa', dicionario), gauge=True)
            meusplash.painel_bmp.SetBitmap(self.splashbmp)
            meusplash.Texto.SetLabel(tradutor('Iniciando o programa', dicionario))
            meusplash.Show(True)
            wx.Yield()
        zz = LocalizaJogos(self.pastadefault)
        self.jogos_e_info = zz.jogos_e_info
        self.listjogos = self.jogos_e_info[0]
        memoria['selecionado_para_copiar'] = {}


        if refresh == True:
            self.pastadefault = conf_prog.leitor_configuracao('PADRAO')
            self.painel_principal.Destroy()
        self.painel_principal = wx.Panel(self, wx.ID_ANY)  #Painel Pinricpal

        sizer_panel_titulo = wx.GridBagSizer(0, 0)  #sizers
        sizer_panel = wx.GridBagSizer(0, 100)
        self.arquivoiso = ""
        if refresh == True:
            self.SendSizeEvent()

        self.painel_cabecalho = wx.Panel(self.painel_principal, wx.ID_ANY,
                                         (0, 0), (-1, 25), style=wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)
        self.painel_cabecalho.Hide()
        text0 = wx.StaticText(self.painel_cabecalho, wx.ID_ANY,
                              tradutor(u"Lista de Jogos - Playstation 2", dicionario), (0, 0), style=wx.TE_RICH)
        font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        text0.SetFont(font)
        sizer_panel_titulo.Add(text0, (0, 0), (1, 1), wx.ALIGN_CENTER, 5)
        sizer_panel_titulo.AddGrowableCol(0)

        self.painel_cabecalho.SetSizerAndFit(sizer_panel_titulo)

        self.painel_scroll = wx.ScrolledWindow(self.painel_principal, wx.ID_ANY, (0, 0), (-1, 525))
        self.painel_scroll.Hide()
        sizer_jogos = wx.GridSizer(cols=2, hgap=0, vgap=0)
        meusplash.painel_bmp.SetBitmap(self.splashbmp)
        meusplash.Texto.SetLabel(tradutor('Localizando imagens', dicionario))
        wx.Yield()

        self.imagens_jogos = LocalizaArt(os.path.join(self.pastadefault, 'ART'))
        meuid = 0
        quantogauge = len(self.listjogos)
        meusplash.Texto.SetLabel(tradutor('Criando lista de jogos', dicionario))
        wx.Yield()
        meuid = 0
        for x in self.listjogos:

            meuid += 1

            valorgauge = int(float(meuid)/quantogauge*100)
            meusplash.barrinha.SetValue(valorgauge)
            wx.Yield()

            sizer_jogos.Add(PainelJogos(
                self.painel_scroll, wx.ID_NEW, (0, 0), (-1, 110),
                arquivo_do_jogo=x[0], codigo_do_jogo=x[1], nome_do_jogo=x[2], tamanho_do_jogo=x[3],
                partes=x[4], tipo_midia=x[5], lista_cover_art=self.imagens_jogos, Meu_ID=meuid),
                            0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
            if refresh == True:
                self.SendSizeEvent()

        #self.painel_principal.Show()
        self.painel_scroll.SetWindowStyleFlag(wx.ALIGN_CENTER | wx.ALL | wx.EXPAND | wx.BORDER_DOUBLE)
        self.painel_scroll.SetSizer(sizer_jogos)
        self.painel_scroll.SetScrollbars(1, 1, -1, -1)

        #rodapé
        self.painel_info_e_acao = wx.Panel(self.painel_principal, wx.ID_ANY, (0, 0), (-1, -1),
                                           style=wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)
        self.painel_info_e_acao.Hide()
        ############ caixa info da esquerda
        self.painel_info = wx.Panel(self.painel_info_e_acao, wx.ID_ANY, (0, 0), (-1, -1),
                                    style=wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)
        sizer_painel_info = wx.GridBagSizer(0, 0)
        textTilulo1 = wx.StaticText(self.painel_info, wx.ID_ANY, tradutor(u'INFORMAÇÕES GERAIS', dicionario),
                                    (0, 0), style = wx.ALIGN_CENTER | wx.TE_RICH)
        text1 = wx.StaticText(self.painel_info, wx.ID_ANY, tradutor(u"Total de jogos", dicionario),
                              (0, 0), style=wx.TE_RICH)
        form1 = wx.TextCtrl(self.painel_info, wx.ID_ANY, str(self.jogos_e_info[1]), (0, 0), style=wx.TE_RICH)
        form1.Enabled = False
        text2 = wx.StaticText(self.painel_info, wx.ID_ANY, tradutor(u"Tamanho total", dicionario),
                              (0, 0), style=wx.TE_RICH)
        form2 = wx.TextCtrl(self.painel_info, wx.ID_ANY, convert_tamanho(self.jogos_e_info[2]),
                            (0, 0), style=wx.TE_RICH)
        form2.Enabled = False
        sizer_painel_info.Add(textTilulo1, (0, 0), (1, 3), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
        sizer_painel_info.Add(text1, (1, 0), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_painel_info.Add(form1, (1, 1), (1, 2), wx.ALL | wx.EXPAND, 5)
        sizer_painel_info.Add(text2, (2, 0), (1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_painel_info.Add(form2, (2, 1), (1, 2), wx.ALL | wx.EXPAND, 5)
        self.painel_info.SetSizerAndFit(sizer_painel_info)
        sizer_painel_info.AddGrowableCol(2)

        ##########Caixa de ações
        self.painel_acao = wx.Panel(self.painel_info_e_acao, wx.ID_ANY, (0, 0), (-1, -1),
                               style=wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)

        textTilulo2 = wx.StaticText(self.painel_acao, wx.ID_ANY,
                                    tradutor(u'INFORMAÇÕES E AÇÕES DOS SELECIONADOS', dicionario),
                                    (0, 0), style=wx.ALIGN_CENTER | wx.TE_RICH)
        text3 = wx.StaticText(self.painel_acao, wx.ID_ANY,
                              tradutor(u"Total de jogos", dicionario),
                              (0, 0), style=wx.TE_RICH)
        self.form3 = wx.TextCtrl(self.painel_acao, wx.ID_ANY, '0', (0, 0), style=wx.TE_RICH)
        self.form3.Enabled = False
        text4 = wx.StaticText(self.painel_acao, wx.ID_ANY,
                              tradutor(u"Tamanho Total", dicionario), (0, 0),
                              style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.form4 = wx.TextCtrl(self.painel_acao, wx.ID_ANY,
                                 convert_tamanho(memoria['tamanho_total_dos_jogos']), (0, 0), style=wx.TE_RICH)
        self.form4.Enabled = False
        self.botao_deletar_tudo = wx.Button(self.painel_acao, wx.ID_ANY, tradutor(u'Deletar selecionados', dicionario), (0, 0))
        self.id_botao_deletar_tudo = self.botao_deletar_tudo.GetId()
        self.botao_deletar_tudo.Enabled = False

        self.Bind(wx.EVT_BUTTON, self.DeletarCopiar, self.botao_deletar_tudo)

        text5 = wx.StaticText(self.painel_acao, wx.ID_ANY,
                              tradutor(u"Pasta destino", dicionario), (0, 0),
                              style=wx.TE_RICH| wx.ALIGN_CENTER_VERTICAL)
        self.form5 = wx.TextCtrl(self.painel_acao, wx.ID_ANY, '', (0, 0), style=wx.TE_RICH)
        self.form5.Enabled = False
        self.botao_copiar_selecionados = wx.Button(self.painel_acao, wx.ID_ANY, '...', (0, 0), (30,-1))
        self.id_botao_copiar_selecionados = self.botao_copiar_selecionados.GetId()
        self.botao_copiar_selecionados.Enabled = False
        self.Bind(wx.EVT_BUTTON, self.PastaDestino, self.botao_copiar_selecionados)

        self.copiar_VMC = wx.CheckBox(self.painel_acao, wx.ID_ANY, tradutor('VMC',dicionario),(0 ,0))
        self.copiar_VMC.SetToolTipString(tradutor(u'Copia GenericVMC para o destino', dicionario))
        self.copiar_VMC.Enabled=False
        self.Bind(wx.EVT_CHECKBOX , self.Check, self.copiar_VMC)
        self.copia_padrao_iso = wx.CheckBox(self.painel_acao, wx.ID_ANY,
                                            tradutor(u'Copiar no padrão ISO', dicionario), (0 ,0))
        self.copia_padrao_iso.Enabled=False
        self.Bind(wx.EVT_CHECKBOX , self.Check, self.copia_padrao_iso)
        self.copia_padrao_iso.SetToolTipString(
            tradutor(u'Se marcado a cópia será no padrão ISO, caso contrário, será no padrão ul.cfg', dicionario))
        self.copiar_Capa = wx.CheckBox(self.painel_acao, wx.ID_ANY, tradutor('Capa',dicionario),(0 ,0))
        self.copiar_Capa.Enabled=False
        self.Bind(wx.EVT_CHECKBOX , self.Check, self.copiar_Capa)
        self.copiar_Capa.SetToolTipString(
            tradutor(u'Se houver, envia a capa do jogo ou a capa padrão se marcado', dicionario))
        self.copia_cfg = wx.CheckBox(self.painel_acao, wx.ID_ANY, tradutor('CFG', dicionario), (0 ,0))
        self.copia_cfg.Enabled=False
        self.Bind(wx.EVT_CHECKBOX , self.Check, self.copiar_Capa)
        self.copia_cfg.SetToolTipString(tradutor(u'Se houver, anvia o arquivo cfg do jogo se marcado', dicionario))

        sizer_painel_acao = wx.GridBagSizer(0, 0)
        sizer_painel_acao.Add(textTilulo2, (0, 0), (1, 9), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
        sizer_painel_acao.Add(text3, (1, 0), (1, 1), wx.ALL | wx.ALIGN_RIGHT| wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_painel_acao.Add(self.form3, (1, 1), (1, 1), wx.ALL | wx.EXPAND, 5)
        sizer_painel_acao.Add(text4, (1, 2), (1, 1), wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_painel_acao.Add(self.form4, (1, 3), (1, 1), wx.ALL | wx.EXPAND, 5)
        sizer_painel_acao.Add(self.copiar_VMC, (1, 4), (1, 1), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)
        sizer_painel_acao.Add(self.copiar_Capa, (1, 5), (1, 1), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)
        sizer_painel_acao.Add(self.copia_cfg, (1, 6), (1, 1), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)
        sizer_painel_acao.Add(self.copia_padrao_iso, (1, 7), (1, 2), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)
        sizer_painel_acao.Add(text5, (2, 0), (1, 1), wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL| wx.EXPAND, 5)
        sizer_painel_acao.Add(self.form5, (2, 1), (1, 5), wx.ALL | wx.EXPAND, 5)
        sizer_painel_acao.Add(self.botao_copiar_selecionados, (2, 6), (1, 1), wx.ALL | wx.EXPAND, 5)
        sizer_painel_acao.Add(self.botao_deletar_tudo, (2, 7), (1, 1), wx.ALL | wx.EXPAND, 5)
        self.painel_acao.SetSizerAndFit(sizer_painel_acao)
        sizer_painel_acao.AddGrowableCol(1)
        sizer_painel_acao.AddGrowableCol(3)

        #FIM Caixa de ações
        linha_vertical = wx.StaticLine(self.painel_info_e_acao, id=wx.ID_ANY, pos=(0, 0), size=(-1, -1),
                                        style=wx.LI_VERTICAL | wx.BORDER_DOUBLE)

        sizer_panel_rodape = wx.GridBagSizer(0,0)
        sizer_panel_rodape.Add(self.painel_info, (0,0),(1,2), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
        sizer_panel_rodape.Add(linha_vertical, (0, 2),(1, 1),  wx.ALL | wx.EXPAND, 5)
        sizer_panel_rodape.Add(self.painel_acao, (0,3),(1,6), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        sizer_panel_rodape.AddGrowableCol(1)
        sizer_panel_rodape.AddGrowableCol(3)
        sizer_panel_rodape.AddGrowableCol(4)
        sizer_panel_rodape.AddGrowableCol(6)

        self.painel_info_e_acao.SetSizerAndFit(sizer_panel_rodape)

        sizer_panel.Add(self.painel_cabecalho, (0, 0), (1, 1), wx.ALL | wx.EXPAND, 5)
        sizer_panel.Add(self.painel_scroll, (1, 0), (3, 1), wx.ALL | wx.EXPAND, 5)
        sizer_panel.Add(self.painel_info_e_acao, (4, 0), (1, 1), wx.ALL | wx.EXPAND, 5)
        sizer_panel.AddGrowableCol(0)
        sizer_panel.AddGrowableRow(1)
        self.painel_principal.SetSizerAndFit(sizer_panel)
        self.painel_cabecalho.Show()
        self.painel_scroll.Show()
        self.painel_info_e_acao.Show()

        self.Layout()
        self.CenterOnScreen()
        self.SendSizeEvent()

        meusplash.Destroy()



    def AbrirIso(self, event):
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        self.wildcard = "%s (*.iso)|*.iso" % (tradutor('Imagem ISO', dicionario))
        self.janeladlg = wx.FileDialog(self, tradutor(u"Selecionando Imagem...", dicionario), corrente, style=wx.OPEN,
                                       wildcard=self.wildcard)
        self.janeladlg.CenterOnParent()
        if self.janeladlg.ShowModal() == wx.ID_OK:
            self.arquivoiso = self.janeladlg.GetPaths()
            self.janeladlg.Destroy()
            self.ReadFile(self.arquivoiso[0])
            self.frame = FrameAdicionarIso(self, wx.ID_ANY,
                                              tradutor(u"Adicione o nome e código do jogo", dicionario),
                                              self.resultados[0], self.resultados[1], self.resultados[2],
                                              self.resultados[3], self.listjogos)
            self.frame.Show(True)

    def MultiIso(self, event):
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        self.wildcard = "%s (*.iso)|*.iso" % (tradutor('Imagem ISO', dicionario))
        self.janeladlg = wx.FileDialog(self, tradutor(u"Selecionando Imagens...", dicionario), corrente,
                                       style=wx.MULTIPLE, wildcard=self.wildcard)
        self.janeladlg.CenterOnParent()
        if self.janeladlg.ShowModal() == wx.ID_OK:
            self.arquivoiso = self.janeladlg.GetPaths()
            lis = []
            tam_tot = 0
            for d in self.arquivoiso:
                ver = VerificaJogo(d)
                res = ver.resultado_final
                tam_tot += res[3]
                uno = [res[0], res[1], res[2], res[3]]
                lis.append(uno)
            lista_de_jogoss = [lis, tam_tot]

            self.janeladlg.Destroy()
            self.frame = FrameAdicionarMultiplos(self, self.title, lista_de_jogoss[0], lista_de_jogoss[1], (-1, -1),
                                                   (1000, 400))
            self.frame.Show(True)

    def Atualizar(self, event):
        conf_prog = Configuracoes()
        self.pastadefault = conf_prog.leitor_configuracao('PADRAO')
        event.Skip()
        self.Atualizar_refresh(True)

    def ReadFile(self, arquivosiso):
        result = VerificaJogo(arquivosiso)
        resultados = result.resultado_final
        self.resultados = resultados

    def Sobre(self, event):
        x = FrameSobre()
        x.Show()

    def Config(self, event):
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        frame = FrameConfiguracao(self, -1, tradutor(u"Configurações", dicionario))
        frame.Show(True)

    def DeletarCopiar(self, event):
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        if self.CopiarTaAtivado == True:
            self.copiar_VMC.Enabled = True
            self.copia_padrao_iso.Enabled = True
            self.copiar_Capa.Enabled = True
            self.copia_cfg.Enabled = True
            destino = self.form5.GetValue()

            lista_de_arquivos = []
            memoria['selecionado_para_copiar']['vmc1'] = [[os.path.join(corrente,'generic_0.bin'), 'VMC', False, destino, 0, False, False]]
            memoria['selecionado_para_copiar']['vmc2'] = [[os.path.join(corrente,'generic_1.bin'), 'VMC', False, destino, 0, False, False]]

            for x in memoria['selecionado_para_copiar']:

                if memoria['selecionado_para_copiar'][x] == False:
                    lista_ini=[]
                else:
                    lista_ini = memoria['selecionado_para_copiar'][x]
                for y in lista_ini:

                    y[3] = destino
                    if y[1] == 'ulDVD' or y[1] == 'ulCD' or y[1] == 'DVD' or y[1] == 'CD':
                        if self.copia_padrao_iso.GetValue() == False:
                            y[6] = True
                        else:
                            y[6] = False
                        lista_de_arquivos.append(y)
                    else:
                        if y[1] == 'ART' and self.copiar_Capa.GetValue() == False:
                            pass
                        elif y[1] == 'ART' and self.copiar_Capa.GetValue() == True:
                            lista_de_arquivos.append(y)
                        elif y[1] == 'CFG' and self.copia_cfg.GetValue() == False:
                            pass
                        elif y[1] == 'CFG' and self.copia_cfg.GetValue() == True:
                            lista_de_arquivos.append(y)
                        elif y[1] == 'VMC' and self.copiar_VMC.GetValue() == False:
                            pass
                        elif y[1] == 'VMC' and self.copiar_VMC.GetValue() == True:
                            lista_de_arquivos.append(y)

            definitivo_kkk = ProgressCopia(self, tradutor('Copiando arquivos selecionados', dicionario),lista_de_arquivos)
            definitivo_kkk.Show()
            definitivo_kkk.iniciarcopia()
        else:
            login = LoginDialog(self, False)
            login.CenterOnParent()
            login.ShowModal()
            login.Destroy()
            if login.autorizado == True:

                lista_del = []
                for xz in memoria['selecionado_para_copiar']:

                    if memoria['selecionado_para_copiar'][xz] == False:
                        lista_inix=[]
                    else:
                        lista_inix = memoria['selecionado_para_copiar'][xz]
                    for yz in lista_inix:
                        if yz[1] == 'ulDVD' or yz[1] == 'ulCD' or yz[1] == 'DVD' or yz[1] == 'CD':
                            if not lista_inix ==[]:
                                lista_del.append(yz)
                for xw in lista_del:
                    if xw[1] == 'ulDVD' or xw[1] == 'ulCD':

                        end_base = os.path.dirname(xw[0][0])
                        deleta_ul = ManipulaUl()
                        novo_nome_zx = xw[5][12:]
                        deleta_ul.deletar_jogo_ul(end_base, novo_nome_zx)
                    else:
                        os.remove(xw[0])
        self.Atualizar_refresh(True)

    def PastaDestino(self, event):
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        dlg = wx.DirDialog(self, tradutor(u"Selecionando pasta destino...", dicionario), corrente, style=wx.OPEN)
        dlg.CenterOnParent()
        if dlg.ShowModal() == wx.ID_OK:
            self.CopiarTaAtivado = True
            self.valor_dialog = dlg.GetPath()
            self.form5.SetValue(self.valor_dialog)
            self.botao_deletar_tudo.SetForegroundColour(wx.GREEN)
            self.copiar_VMC.Enabled = True
            self.copia_padrao_iso.Enabled = True
            self.copiar_Capa.Enabled = True
            self.copia_cfg.Enabled = True
            self.botao_deletar_tudo.SetLabel(tradutor('Copiar selecionados', dicionario))

    def Check (self, event):
        pass

    def dofilho(self, event):

        conf_prog = Configuracoes()
        self.pastadefault = conf_prog.leitor_configuracao('PADRAO')
        self.Atualizar_refresh(True)

    def dofilho2(self, event):
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        self.form3.SetValue(str(memoria['jogos_selecionados']))
        self.form4.SetValue(convert_tamanho(memoria['tamanho_total_dos_jogos']))
        if self.form4.GetValue() == '0 KB':
            self.CopiarTaAtivado = False
            self.form5.SetValue('')
            self.botao_deletar_tudo.SetLabel(tradutor('Deletar selecionados', dicionario))
            self.botao_deletar_tudo.Enabled = False
            self.botao_copiar_selecionados.Enabled = False
            self.botao_deletar_tudo.SetForegroundColour(wx.BLACK)
            self.copiar_VMC.Enabled = False
            self.copia_padrao_iso.Enabled = False
            self.copiar_Capa.Enabled = False
            self.copia_cfg.Enabled = False

        else:
            if self.form5.GetValue() == '':
                self.botao_deletar_tudo.SetForegroundColour(wx.RED)
            self.botao_deletar_tudo.Enabled = True
            self.botao_copiar_selecionados.Enabled = True


class MeuSplash (wx.Frame):
    conf_prog = Configuracoes()
    dicionario = conf_prog.leitor_configuracao('DICIONARIO')
    def __init__(self, parent, ID=wx.ID_ANY , title=tradutor("Processando, Aguarde...", dicionario),
                style=wx.NO_BORDER | wx.SIMPLE_BORDER  ,
                duration=10500, bitmapfile=os.path.join(corrente, 'imagens', 'processando.jpg'), callback = None, gauge=False):


        bmp = wx.Image(bitmapfile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bitmap = bmp
        self.title = title
        self.gauge=gauge

        size = (bmp.GetWidth(), bmp.GetHeight()+50)
        width = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_X)
        height = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_Y)
        pos = ((width-size[0])/2, (height-size[1])/2)
        if pos[0] < 0:
            size = (wx.SystemSettings_GetSystemMetric(wx.SYS_SCREEN_X), size[1])
        if pos[1] < 0:
            size = (size[0], wx.SystemSettings_GetSystemMetric(wx.SYS_SCREEN_Y))

        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        icone = wx.Icon(os.path.join(corrente, 'imagens', 'icon.ico'), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icone)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseClick)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        #self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBG)
        sizer = wx.GridBagSizer(0,0)
        painel = wx.Panel(self, wx.ID_ANY, (0,0), (300,200))
        self.painel_bmp = wx.StaticBitmap(painel, wx.ID_ANY, self.bitmap, (0, 0))

        self.Texto = wx.StaticText(painel, wx.ID_ANY, self.title, (50, 153), (300, -1), style=wx.ALIGN_CENTER)
        font = wx.Font(15, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.Texto.SetFont(font)
        self.barrinha = wx.Gauge(painel, range=100, size=(290, 20))
        sizer.Add(self.painel_bmp, (0,0), (1,1), wx.ALL | wx.EXPAND, 0)
        sizer.Add(self.barrinha, (1,0), (1,1), wx.ALL| wx.EXPAND,5)
        painel.SetSizerAndFit(sizer)
        if self.gauge == False:
            print 'oxente'
            self.barrinha.Hide()

        class SplashTimer(wx.Timer):
            def __init__(self, targetFunction):
                self.Notify = targetFunction
                wx.Timer.__init__(self)

        if callback is None:
            callback = self.OnSplashExitDefault

        self.timer = SplashTimer(callback)
        self.timer.Start(duration, 1) # one-shot only

    #def OnPaint(self, event):
    #    pass


    def OnEraseBG(self, event):
        pass

    def OnSplashExitDefault(self, event=None):
        self.Close(True)

    def OnCloseWindow(self, event=None):
        self.Show(False)
        self.timer.Stop()
        del self.timer
        self.Destroy()
    def OnMouseClick(self, event):
        self.timer.Notify()


class PainelJogos(wx.Panel):
    def __init__(self, parent, ID, pos, size, arquivo_do_jogo, codigo_do_jogo, nome_do_jogo, tamanho_do_jogo, partes,
                 tipo_midia, lista_cover_art, Meu_ID):
        wx.Panel.__init__(self, parent, wx.ID_ANY, pos, size, wx.EXPAND)
        self.Meu_ID = Meu_ID
        self.arquivo_do_jogo = arquivo_do_jogo
        self.codigo_do_jogo = codigo_do_jogo
        self.nome_do_jogo = nome_do_jogo
        self.midia_tipo = 'CD' if tipo_midia == '12'  else 'DVD'
        self.parent = parent
        self.tamanho_total = 0
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        self.pastadefault = conf_prog.leitor_configuracao('PADRAO')


        self.configuracao_do_jogo = os.path.join(self.pastadefault, 'CFG', '%s.cfg' % (codigo_do_jogo))
        self.tamanho_do_jogo = tamanho_do_jogo
        self.cover_art = lista_cover_art.localiza_cover_art(codigo_do_jogo)
        self.endereco_da_imagem = os.path.join(self.cover_art[0], self.cover_art[1])
        # try:
        if imagem_check.leitor_configuracao(self.endereco_da_imagem) == 'OK':
            pass
        else:
            retirar_exitf_imagem(self.endereco_da_imagem)
            imagem_check.mudar_configuracao(self.endereco_da_imagem, 'OK')
        imagem5 = wx.Image(self.endereco_da_imagem, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        #except:
        #   imagem_check.mudar_configuracao(self.endereco_da_imagem, 'Falhou')
        #   imagem5 = wx.Image(os.path.join(corrente, 'imagens', 'erro.jpg'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        new_imagem5 = wx.ImageFromBitmap(imagem5).Scale(70, 100, wx.IMAGE_QUALITY_NORMAL).ConvertToBitmap()
        mask = wx.Mask(new_imagem5, wx.BLUE)
        new_imagem5.SetMask(mask)
        self.botao_imagem = wx.BitmapButton(self, wx.ID_ANY, new_imagem5, (0, 0), (80, 110))
        self.botao_imagem.SetToolTipString(tradutor(u"Clique na imagem para mudá-la", dicionario))
        self.Bind(wx.EVT_BUTTON, self.MudarImagem, self.botao_imagem)
        text0 = wx.StaticText(self, wx.ID_ANY, tradutor(u"Código:", dicionario), (0, 0),
                              style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.form0 = wx.TextCtrl(self, wx.ID_ANY, codigo_do_jogo, (0, 0), style=wx.TE_RICH)
        self.form0.Enabled = False
        texttipo = wx.StaticText(self, wx.ID_ANY, tradutor(u"Mídia:", dicionario), (0, 0),
                                 style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.formtipo = wx.TextCtrl(self, wx.ID_ANY, self.midia_tipo, (0, 0), style=wx.TE_RICH)
        self.formtipo.Enabled = False

        text1 = wx.StaticText(self, wx.ID_ANY, tradutor(u"Nome:", dicionario), (0, 0),
                              style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.form1 = wx.TextCtrl(self, wx.ID_ANY, nome_do_jogo, (0, 0), style=wx.TE_RICH)
        self.form1.Enabled = False
        text2 = wx.StaticText(self, wx.ID_ANY, tradutor("Arquivo:", dicionario), (0, 0),
                              style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.form2 = wx.TextCtrl(self, wx.ID_ANY, self.arquivo_do_jogo, (0, 0), style=wx.TE_RICH)
        ulcfg = False

        self.form2.Enabled = False
        if self.arquivo_do_jogo[-6:] == 'ul.cfg':
            ulcfg = True
            text2.SetForegroundColour(wx.RED)
            self.form2.SetForegroundColour(wx.RED)
            textpartes = wx.StaticText(self, wx.ID_ANY, tradutor(u"Partes:", dicionario), (0, 0),
                                       style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
            self.formpartes = wx.TextCtrl(self, wx.ID_ANY, partes, (0, 0), style=wx.TE_RICH)
            self.formpartes.Enabled = False
        text3 = wx.StaticText(self, wx.ID_ANY, tradutor("Tamanho:", dicionario), (0, 0),
                              style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.form3 = wx.TextCtrl(self, wx.ID_ANY, convert_tamanho(self.tamanho_do_jogo), (0, 0), style=wx.TE_RICH)
        self.form3.Enabled = False
        self.radio = wx.CheckBox(self, wx.ID_ANY, tradutor("Selecionar", dicionario))
        self.radio.SetToolTipString(tradutor(u'Selecionar este jogo', dicionario))
        self.Bind(wx.EVT_CHECKBOX, self.Selecionado, self.radio)
        self.botao_renomear = wx.Button(self, wx.ID_ANY, tradutor('Renomear', dicionario), (0, 0))
        self.botao_renomear.SetToolTipString(tradutor(u'Renomear nome do jogo', dicionario))
        self.Bind(wx.EVT_BUTTON, self.Renomear, self.botao_renomear)
        self.botao_deletar = wx.Button(self, wx.ID_ANY, tradutor('Deletar', dicionario), (0, 0))
        self.botao_deletar.SetToolTipString(tradutor(u'Deletar jogo', dicionario))
        self.Bind(wx.EVT_BUTTON, self.Deletar, self.botao_deletar)
        self.botao_config = wx.Button(self, wx.ID_ANY, tradutor(u'Configuração', dicionario), (0, 0))
        self.botao_config.SetToolTipString(tradutor(u'Abrir configuração específica do jogo', dicionario))
        self.Bind(wx.EVT_BUTTON, self.ConfiguracaoJogo, self.botao_config)
        self.botao_copiar_para = wx.Button(self, wx.ID_ANY, tradutor('Copiar para...', dicionario), (0, 0))
        self.botao_copiar_para.SetToolTipString(
            tradutor(u'Fazer uma cópia do jogo num dispositivo ou pasta diferente', dicionario))
        self.Bind(wx.EVT_BUTTON, self.CopiarPara, self.botao_copiar_para)
        linha_horizontal = wx.StaticLine(self, id=wx.ID_ANY, pos=(0, 0), size=(-1, -1),
                                         style=wx.LI_HORIZONTAL | wx.BORDER_DOUBLE)

        self.MeuGridsizer = wx.GridBagSizer(3, 5)

        self.MeuGridsizer.Add(self.botao_imagem, (0, 0), (4, 2), wx.ALL | wx.EXPAND, 2)
        self.MeuGridsizer.Add(text0, (0, 2), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.MeuGridsizer.Add(self.form0, (0, 3), (1, 1), wx.ALL | wx.EXPAND, 2)
        self.MeuGridsizer.Add(texttipo, (0, 4), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.MeuGridsizer.Add(self.formtipo, (0, 5), (1, 2), wx.ALL | wx.EXPAND, 2)
        self.MeuGridsizer.Add(text1, (1, 2), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.MeuGridsizer.Add(self.form1, (1, 3), (1, 4), wx.ALL | wx.EXPAND, 2)
        self.MeuGridsizer.Add(text2, (2, 2), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.MeuGridsizer.Add(self.form2, (2, 3), (1, 4 if not ulcfg else 1), wx.ALL | wx.EXPAND, 2)
        if ulcfg:
            self.MeuGridsizer.Add(textpartes, (2, 4), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
            self.MeuGridsizer.Add(self.formpartes, (2, 5), (1, 2), wx.ALL | wx.EXPAND, 2)

        self.MeuGridsizer.Add(text3, (3, 2), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.MeuGridsizer.Add(self.form3, (3, 3), (1, 4), wx.ALL | wx.EXPAND, 2)
        self.MeuGridsizer.Add(self.radio, (4, 0), (3, 2), wx.ALIGN_CENTER, 0)
        self.MeuGridsizer.Add(self.botao_renomear, (4, 2), (2, 1), wx.ALIGN_CENTER, 0)
        self.MeuGridsizer.Add(self.botao_deletar, (4, 3), (2, 1), wx.ALIGN_CENTER, 0)
        self.MeuGridsizer.Add(self.botao_config, (4, 4), (2, 1), wx.ALIGN_CENTER, 0)
        self.MeuGridsizer.Add(self.botao_copiar_para, (4, 5), (2, 2), wx.ALIGN_CENTER, 0)
        self.MeuGridsizer.Add(linha_horizontal, (7, 0), (1, 8), wx.ALIGN_CENTER | wx.EXPAND, 0)
        self.MeuGridsizer.AddGrowableCol(3)
        self.MeuGridsizer.AddGrowableCol(6)
        self.SetSizerAndFit(self.MeuGridsizer)
        self.Centre()
        self.Layout()

    def Renomear(self, event):
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        self.pastadefault = conf_prog.leitor_configuracao('PADRAO')
        if self.form1.Enabled == False:
            self.form1.Enabled = True
            self.botao_renomear.SetLabel("OK")
            self.acao_enderecodojogo = self.form2.GetValue()
            self.acao_codigo = self.form0.GetValue()
            self.acao_nomedojogoatual = self.form1.GetValue()

        elif self.form1.Enabled == True:
            if self.acao_nomedojogoatual == self.form1.GetValue():
                pass
            elif os.path.basename(self.arquivo_do_jogo) == 'ul.cfg':
                end_base = os.path.dirname(self.acao_enderecodojogo)
                muda_ul = ManipulaUl()
                novo_nome_zx = self.form1.GetValue()
                retoronoul = muda_ul.renomear_jogo_ul(end_base, self.acao_nomedojogoatual, novo_nome_zx)
                self.form1.Enabled = False
                self.form1.SetValue(retoronoul)
                if retoronoul == novo_nome_zx:
                    msgbox = wx.MessageDialog(self,
                                              tradutor(u'O nome do arquivo foi alterado com sucesso!', dicionario),
                                              tradutor('Sucesso!', dicionario), wx.OK | wx.ICON_INFORMATION)
                    msgbox.ShowModal()
                    msgbox.Destroy()
                else:
                    msg01 = tradutor(
                        u'O nome do arquivo foi alterado, mas como já havia um outro jogo com o mesmo nome, o programa renomeou para',
                        dicionario)
                    msg02 = u" %s" % (self.form1.GetValue())
                    msg = msg01 + msg02
                    msgbox = wx.MessageDialog(self, msg, tradutor('Sucesso!', dicionario), wx.OK | wx.ICON_INFORMATION)
                    msgbox.ShowModal()
                    msgbox.Destroy()
            else:
                novo_nome_zx = self.form1.GetValue()
                resultafinal = muda_nome_jogo(self.acao_enderecodojogo, novo_nome_zx)
                self.form2.SetValue(resultafinal[0])
                self.form1.SetValue(resultafinal[2])
                self.form1.Enabled = False
                if resultafinal[2] == novo_nome_zx:
                    msgbox = wx.MessageDialog(self,
                                              tradutor(u'O nome do arquivo foi alterado com sucesso!', dicionario),
                                              tradutor('Sucesso!', dicionario), wx.OK | wx.ICON_INFORMATION)
                    msgbox.ShowModal()
                    msgbox.Destroy()
                else:
                    msg01 = tradutor(
                        u'O nome do arquivo foi alterado, mas como já havia um outro jogo com o mesmo nome, o programa renomeou para',
                        dicionario)
                    msg02 = u" %s" % (self.form1.GetValue())
                    msg = msg01 + msg02
                    msgbox = wx.MessageDialog(self, msg, tradutor('Sucesso!', dicionario), wx.OK | wx.ICON_INFORMATION)
                    msgbox.ShowModal()
                    msgbox.Destroy()
                self.form2.SetValue(resultafinal[0])
                self.form1.SetValue(resultafinal[2])
                self.form1.Enabled = False

            self.form1.Enabled = False
            self.botao_renomear.SetLabel("Renomear")

    def Deletar(self, event):
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        self.pastadefault = conf_prog.leitor_configuracao('PADRAO')
        msgbox = wx.MessageDialog(self, 'Deletando', tradutor('Deletando jogo', dicionario),
                                  wx.YES_NO | wx.ICON_INFORMATION)
        resultado = msgbox.ShowModal()
        self.acao_enderecodojogo = self.form2.GetValue()
        if resultado == wx.ID_YES:
            if self.arquivo_do_jogo[-6:] == 'ul.cfg':
                end_base = os.path.dirname(self.acao_enderecodojogo)
                deleta_ul = ManipulaUl()
                novo_nome_zx = self.form1.GetValue()
                deleta_ul.deletar_jogo_ul(end_base, novo_nome_zx)
            else:
                os.remove(self.acao_enderecodojogo)
            self.form0.SetValue('')
            self.form1.SetValue('')
            self.form2.SetValue('')
            self.form3.SetValue('')

            self.botao_renomear.Enabled = False
            self.botao_deletar.Enabled = False
            self.botao_copiar_para.Enabled = False
            self.botao_config.Enabled = False
            self.radio.Enabled = False

            self.SetBackgroundColour(wx.RED)

            self.form1.SetBackgroundColour(wx.RED)
            self.form2.SetBackgroundColour(wx.RED)
            self.form3.SetBackgroundColour(wx.RED)

            i = wx.Image(os.path.join(corrente, 'imagens', 'deletado.jpg'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            isv = wx.ImageFromBitmap(i).Scale(70, 100, wx.IMAGE_QUALITY_NORMAL).ConvertToBitmap()
            self.botao_imagem.SetBitmapDisabled(isv)
            self.botao_imagem.Enabled = False
            self.Refresh()

        elif resultado == wx.ID_NO:
            pass
            msgbox.Destroy()

    def ConfiguracaoJogo(self, event):
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        self.pastadefault = conf_prog.leitor_configuracao('PADRAO')
        nome_do_jogo = self.form1.GetValue()
        codigo_do_jogo = self.form0.GetValue()
        endereco_config = self.configuracao_do_jogo

        self.obj_config = FrameConfiguracaoJogo(self, wx.ID_ANY, tradutor(u'Configuração do Jogo', dicionario),
                                             endereco_arquivo_cfg=endereco_config, nome_do_jogo=nome_do_jogo)
        self.obj_config.Show()
        self.obj_config.CenterOnParent()

    def CopiarPara(self, event):
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        nome_do_jogo = self.form1.GetValue()
        comparador = os.path.basename(self.form2.GetValue())
        if comparador == 'ul.cfg':
            tipo = 'ul%s' % (self.formtipo.GetValue())
        else:
            tipo = self.formtipo.GetValue()

        self.objcopiar = CopiarPara(self, wx.ID_ANY, tradutor('Copiar para...', dicionario), self.form2.GetValue(),
                                     self.form0.GetValue(), nome_do_jogo, tamanho_do_jogo=self.tamanho_do_jogo,
                                     imagem=self.endereco_da_imagem, cfg=self.configuracao_do_jogo, tipo_origem=tipo,
                                     tipo_destino='')
        self.objcopiar.Show()
        self.objcopiar.CenterOnParent()

    def MudarImagem(self, event):
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        self.pastadefault = conf_prog.leitor_configuracao('PADRAO')
        wildcardx = "%s (*.jpg)|*.jpg|%s (*.png)|*.png" % (
        tradutor('Imagem jpg', dicionario), tradutor('Imagem png', dicionario))
        dlg = wx.FileDialog(self, tradutor(u"Selecionando Imagem...", dicionario),
                            os.path.dirname(self.endereco_da_imagem), style=wx.OPEN, wildcard=wildcardx)
        dlg.CenterOnParent()
        if dlg.ShowModal() == wx.ID_OK:
            self.arquivoimg = dlg.GetPath()
            dlg.Destroy()
            if not self.endereco_da_imagem == self.arquivoimg[0]:
                retirar_exitf_imagem(self.arquivoimg)
                extencao = self.arquivoimg.split('.')[-1]
                pasta_art = conf_prog.leitor_configuracao(chave='pasta_ART')
                nome_da_imagem = "%s_COV.%s" % (self.codigo_do_jogo, extencao)
                with open(self.arquivoimg, 'rb') as imgdfg:
                    conteudo = imgdfg.read()

                    destinodfg = os.path.join(pasta_art, nome_da_imagem)

                    with open(destinodfg, 'wb') as binaimagem:
                        binaimagem.write(conteudo)

                imagem_check.mudar_configuracao(destinodfg, 'OK')
                i = wx.Image(os.path.join(pasta_art, nome_da_imagem), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                isv = wx.ImageFromBitmap(i).Scale(70, 100, wx.IMAGE_QUALITY_NORMAL).ConvertToBitmap()
                self.botao_imagem.SetBitmap(isv)
                self.Refresh()
            dlg.Destroy()

    def Selecionado(self, event):

        valor_do_radio = self.radio.GetValue()
        atual = memoria['tamanho_total_dos_jogos']
        selecionados = memoria['jogos_selecionados']
        tipo = self.formtipo.GetValue()
        if valor_do_radio == True:
            origem = self.form2.GetValue()
            nome = '%s.%s' % (self.codigo_do_jogo, self.nome_do_jogo)
            if os.path.basename(origem) == 'ul.cfg':
                baseghj = os.path.dirname(origem)
                nome_crc = 'ul.%08X.%s.*' % (pycrc32.crc32(self.nome_do_jogo), self.codigo_do_jogo)
                partes = glob.glob(os.path.join(baseghj, nome_crc))
                origem = partes
                tipo = 'ul%s' % tipo
            endereco_da_imagem = os.path.join(self.cover_art[0], self.cover_art[1])
            endereco_do_config = self.configuracao_do_jogo
            criando_lista = []
            if os.path.exists(endereco_da_imagem):
                iiiimagem = [endereco_da_imagem, 'ART', False, self.pastadefault, 0, False, False]
                nome_iiimagem = os.path.basename(endereco_da_imagem)
                if nome_iiimagem == 'sample.jpg':
                    iiiimagem[5] = '%s_COV' %self.codigo_do_jogo
                elif nome_iiimagem == 'erro.jpg':
                    iiiimagem[0] = os.path.join(corrente, 'imagens', 'sample.jpg')
                    iiiimagem[5] = '%s_COV' %self.codigo_do_jogo
                criando_lista.append(iiiimagem)
            if os.path.exists(endereco_do_config):
                ppp_cfg = [endereco_do_config, 'CFG', False, self.pastadefault, 0, False, False]
                criando_lista.append(ppp_cfg)
            criando_lista.append([origem, tipo, False, self.pastadefault, 0, nome, False])

            memoria['selecionado_para_copiar'][self.Meu_ID] = criando_lista

            atual += self.tamanho_do_jogo
            selecionados += 1
        elif valor_do_radio == False:
            memoria['selecionado_para_copiar'][self.Meu_ID] = False
            atual -= self.tamanho_do_jogo
            selecionados -= 1
        memoria['tamanho_total_dos_jogos'] = atual
        memoria['jogos_selecionados'] = selecionados
        wx.PostEvent(self.parent, event)


class FrameAdicionarMultiplos(wx.Frame):
    def __init__(self, parent, title, lista_de_jogos, total_geral, pos, size):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, pos, size)
        
        icone = wx.Icon(os.path.join(corrente, 'imagens', 'icon.ico'), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icone)
        self.listjogos = lista_de_jogos
        self.lista_de_selecionados = []
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        self.pastadefault = conf_prog.leitor_configuracao('PADRAO')
        self.tamanho_vindo_do_filho = 0

        self.painel_principal = wx.Panel(self, wx.ID_ANY)  #Painel Pinricpal

        sizer_panel_titulo = wx.GridBagSizer(0, 0)  #sizers
        sizer_panel = wx.GridBagSizer(0, 100)

        sizer_panel_rodape = wx.GridSizer(cols=1, hgap=0, vgap=0)

        self.painel_cabecalho = wx.Panel(self.painel_principal, wx.ID_ANY, (0, 0), (-1, 25),
                                         style=wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)
        texttitulo = wx.StaticText(self.painel_cabecalho, wx.ID_ANY, tradutor(u"Copiando multiplos jogos", dicionario),
                              (0, 0), style=wx.TE_RICH | wx.ALIGN_CENTER)
        textcod = wx.StaticText(self.painel_cabecalho, wx.ID_ANY,
                                tradutor(u"Código", dicionario), (0, 0), (85, -1),
                                style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        textnome = wx.StaticText(self.painel_cabecalho, wx.ID_ANY,
                                 tradutor(u"Nome", dicionario), (0, 0), (250,-1),
                                 style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        textorigem = wx.StaticText(self.painel_cabecalho, wx.ID_ANY,
                                   tradutor("Arquivo", dicionario), (0, 0),(200,-1),
                                   style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        texttamanho = wx.StaticText(self.painel_cabecalho, wx.ID_ANY,
                                    tradutor("Tamanho", dicionario), (0, 0), (120,-1),
                                    style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        textstatus = wx.StaticText(self.painel_cabecalho, wx.ID_ANY,
                                   tradutor("Status", dicionario), (0, 0),(50,-1),
                                   style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        textradio0 = wx.StaticText(self.painel_cabecalho, wx.ID_ANY,'', (0, 0),(100,-1),
                                   style=wx.TE_RICH | wx.ALIGN_CENTER)
        textradio1 = wx.StaticText(self.painel_cabecalho, wx.ID_ANY, '', (0, 0), (100,-1),
                                   style=wx.TE_RICH| wx.ALIGN_CENTER)

        font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        texttitulo.SetFont(font)
        sizer_panel_titulo.Add(texttitulo, (0, 0), (1, 8), wx.ALL|wx.ALIGN_CENTER|wx.EXPAND, 5)
        sizer_panel_titulo.Add(textcod,(1, 0), (1, 1), wx.ALL|wx.ALIGN_LEFT|wx.EXPAND, 5)
        sizer_panel_titulo.Add(textnome,(1, 1), (1, 1), wx.ALL|wx.ALIGN_LEFT|wx.EXPAND, 5)
        sizer_panel_titulo.Add(textorigem,(1, 2), (1, 2), wx.ALL|wx.ALIGN_LEFT|wx.EXPAND, 5)
        sizer_panel_titulo.Add(texttamanho,(1, 4), (1, 1), wx.ALL|wx.ALIGN_LEFT|wx.EXPAND, 5)
        sizer_panel_titulo.Add(textstatus,(1, 5), (1, 1), wx.ALL|wx.ALIGN_LEFT|wx.EXPAND, 5)
        sizer_panel_titulo.Add(textradio0,(1, 6), (1, 1), wx.ALL|wx.ALIGN_LEFT|wx.EXPAND, 5)
        sizer_panel_titulo.Add(textradio1,(1, 7), (1, 1), wx.ALL|wx.ALIGN_LEFT|wx.EXPAND, 5)
        sizer_panel_titulo.AddGrowableCol(3)
        self.painel_cabecalho.SetSizerAndFit(sizer_panel_titulo)

        self.painel_scroll = wx.ScrolledWindow(self.painel_principal, wx.ID_ANY, (0, 0), (-1, 200))
        sizer_jogos = wx.BoxSizer(wx.VERTICAL)
        self.imagens_jogos = LocalizaArt(os.path.join(self.pastadefault, 'ART'))
        wx.Yield()
        linha_horizontal = wx.StaticLine(self.painel_scroll, id=wx.ID_ANY, pos=(0, 0), size=(-1, -1),
                                         style=wx.LI_HORIZONTAL | wx.BORDER_DOUBLE)
        sizer_jogos.Add(linha_horizontal, 0, wx.ALIGN_CENTER, 5)
        self.tamanho_selecionado = 0
        tot_selecionado = 0
        id_jogos = 0

        for x in self.listjogos:
            id_jogos += 1
            ppp = PainelListaDeJogos(self.painel_scroll, wx.ID_NEW, (0, 0), (-1, -1),
                                        arquivo_do_jogo=x[0], codigo_do_jogo=x[1],
                                        nome_do_jogo=x[2],
                                        tamanho_do_jogo=x[3], Meu_ID=id_jogos)
            sizer_jogos.Add(ppp, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 0)
            self.SendSizeEvent()
            if not ppp.tamanho_computado == 0:
                tot_selecionado += 1

        self.painel_scroll.SetWindowStyleFlag(wx.ALIGN_CENTER | wx.ALL | wx.EXPAND | wx.BORDER_DOUBLE)
        self.painel_scroll.SetSizer(sizer_jogos)
        self.painel_scroll.SetScrollbars(1, 1, -1, -1)

        #rodapé
        self.painel_botao_confirmar = wx.Panel(self.painel_principal, wx.ID_ANY, (0, 0), (-1, -1),
                                               style=wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)

        self.botao_confirmar = wx.Button(self.painel_botao_confirmar, wx.ID_ANY, 'OK')
        self.Bind(wx.EVT_BUTTON, self.Confirmar, self.botao_confirmar)
        sizer_panel_rodape.Add(self.botao_confirmar, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.painel_botao_confirmar.SetSizerAndFit(sizer_panel_rodape)

        sizer_panel.Add(self.painel_cabecalho, (0, 0), (1, 1), wx.ALL | wx.EXPAND, 5)
        sizer_panel.Add(self.painel_scroll, (1, 0), (3, 1), wx.ALL | wx.EXPAND, 5)
        sizer_panel.Add(self.painel_botao_confirmar, (4, 0), (1, 1), wx.ALL | wx.EXPAND, 5)
        sizer_panel.AddGrowableCol(0)
        sizer_panel.AddGrowableRow(1)
        self.painel_principal.SetSizerAndFit(sizer_panel)

        self.Layout()
        self.CenterOnScreen()
        self.SendSizeEvent()

    def Confirmar(self, event):
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        self.pastadefault = conf_prog.leitor_configuracao('PADRAO')
        lista_de_arquivos = []
        for x in memoria['selecionados_multiplos']:
            if memoria['selecionados_multiplos'][x] == False:
                lista_ini=[]
            else:
                lista_ini = memoria['selecionados_multiplos'][x]
            for y in lista_ini:
                lista_de_arquivos.append(y)
        definitivo_kkk = ProgressCopia(self, tradutor('Copiando arquivos selecionados', dicionario),lista_de_arquivos)
        definitivo_kkk.Show()
        definitivo_kkk.CenterOnParent()
        definitivo_kkk.iniciarcopia()
        self.Destroy()


class PainelListaDeJogos(wx.Panel):
    def __init__(self, parent, ID, pos, size, arquivo_do_jogo, codigo_do_jogo,
                 nome_do_jogo, tamanho_do_jogo, Meu_ID):
        wx.Panel.__init__(self, parent, wx.ID_ANY, pos, size, wx.EXPAND)
        self.Meu_ID = Meu_ID
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        self.pastadefault = conf_prog.leitor_configuracao('PADRAO')
        self.arquivo_do_jogo = arquivo_do_jogo
        self.codigo_do_jogo = codigo_do_jogo[0]
        self.parent = parent
        self.tamanho_total = 0
        self.tamanho_do_jogo = tamanho_do_jogo
        self.tamanho_computado = tamanho_do_jogo
        fatiar = False
        if tamanho_do_jogo > 1024 * 1024 * 750:
            tipo_pio = 'DVD'
            if tamanho_do_jogo > 1024 * 1024 * 1024 * 1024:
                fatiar = True
                tipo_pio = 'DVD'
        else:
            tipo_pio = 'CD'

        if codigo_do_jogo[0] == False or codigo_do_jogo[1] != True:
            self.status = u'ERRO'
            self.codigo_do_jogo = 'XXXX_000.00'
            self.tamanho_computado = 0
        else:
            self.status = 'OK'

        self.form0 = wx.TextCtrl(self, wx.ID_ANY, self.codigo_do_jogo, (0, 0), (85, -1), style=wx.TE_RICH)
        self.Bind(wx.EVT_TEXT, self.MudarCodigoNome, self.form0)
        if not self.status == "OK":
            self.form0.SetToolTipString(tradutor(u'Digite um código Válido', dicionario))


        self.form1 = wx.TextCtrl(self, wx.ID_ANY, nome_do_jogo[0], (0, 0), (250, -1), style=wx.TE_RICH)
        self.Bind(wx.EVT_TEXT, self.MudarCodigoNome, self.form1)
        if not nome_do_jogo[0] == 'NOME_DO_JOGO':
            self.form1.SetToolTipString(tradutor(u'Digite um nome para o jogo', dicionario))
        codigo_e_nome_encontrado = '%s.%s' %(self.codigo_do_jogo, nome_do_jogo[0])
        self.organizando_dados_para_gravacao = [arquivo_do_jogo[0], tipo_pio, False, self.pastadefault, 0, codigo_e_nome_encontrado, fatiar]

        self.form2 = wx.TextCtrl(self, wx.ID_ANY, self.arquivo_do_jogo[0], (0, 0),(200,-1), style=wx.TE_RICH)
        self.form2.Enabled = False
        self.form2.SetToolTipString(self.arquivo_do_jogo[0])

        self.form3 = wx.TextCtrl(self, wx.ID_ANY, convert_tamanho(self.tamanho_do_jogo), (0, 0),(120,-1),style=wx.TE_RICH)
        self.form3.Enabled = False
        self.checkpadrao = wx.CheckBox(self, wx.ID_ANY,tradutor(u'Padrão de cópia', dicionario),(0,0),(100,-1), style = wx.ALIGN_CENTER)
        self.checkselecionado = wx.CheckBox(self, wx.ID_ANY,tradutor('Selecionado', dicionario),(0,0),(100,-1), style = wx.ALIGN_CENTER)
        if fatiar == True:
           self.checkpadrao.SetValue(True)
        self.checkpadrao.SetToolTipString(tradutor(u'O ISO será convertivo para o padrao ul.cfg se marcado, caso contrário, será no padrão ISO', dicionario))

        if self.status == "OK":
            self.checkselecionado.SetValue(True)
            self.checkselecionado.SetToolTipString(tradutor(u'O jogo passou, desmarque se quer desistir de copiar', dicionario))
        else:
            self.checkselecionado.SetValue(False)
            self.checkselecionado.SetToolTipString(tradutor(u'Marque se tiver certeza que é um jogo válido', dicionario))

        self.Bind(wx.EVT_CHECKBOX, self.Selecionado, self.checkpadrao)
        self.Bind(wx.EVT_CHECKBOX, self.Selecionado, self.checkselecionado)

        self.form4 = wx.TextCtrl(self, wx.ID_ANY, self.status, (0, 0), (50, -1), style=wx.TE_RICH)
        self.form4.Enabled = False
        linha = wx.StaticLine(self, id=wx.ID_ANY, pos=(0, 0), size=(-1, -1),
                              style=wx.LI_HORIZONTAL | wx.BORDER_DOUBLE)

        self.MeuGridsizer = wx.GridBagSizer(0, 5)

        self.MeuGridsizer.Add(self.form0, (0, 0), (1, 1), wx.ALL | wx.EXPAND, 0)
        self.MeuGridsizer.Add(self.form1, (0, 1), (1, 1), wx.ALL | wx.EXPAND, 0)
        self.MeuGridsizer.Add(self.form2, (0, 2), (1, 2), wx.ALL | wx.EXPAND, 0)
        self.MeuGridsizer.Add(self.form3, (0, 4), (1, 1), wx.ALL | wx.EXPAND, 0)
        self.MeuGridsizer.Add(self.form4, (0, 5), (1, 1), wx.ALL | wx.EXPAND, 0)
        self.MeuGridsizer.Add(self.checkpadrao, (0, 6), (1, 1), wx.ALL | wx.EXPAND|  wx.ALIGN_CENTER, 5)
        self.MeuGridsizer.Add(self.checkselecionado, (0, 7), (1, 1), wx.ALL | wx.EXPAND|  wx.ALIGN_CENTER, 5)
        self.MeuGridsizer.Add(linha, (1, 0), (1, 8), wx.ALL | wx.EXPAND, 5)
        self.MeuGridsizer.AddGrowableCol(3)

        self.SetSizerAndFit(self.MeuGridsizer)
        memoria['selecionados_multiplos'][self.Meu_ID] = [self.organizando_dados_para_gravacao]
        self.Centre()
        self.Layout()

    def MudarCodigoNome(self, event):
        dados_da_memoria = memoria['selecionados_multiplos'][self.Meu_ID]
        if not self.checkselecionado.GetValue()==False:
            code = self.form0.GetValue()
            nome = self.form1.GetValue()
            dados_da_memoria[0][5] = u'%s.%s' %(code, nome)


    def Selecionado(self, event):
        valor_do_radio = self.checkselecionado.GetValue()
        if valor_do_radio == True:
            nomelk = u'%s.%s' %(self.form0.GetValue(), self.form1.GetValue())
            self.organizando_dados_para_gravacao[5] = nomelk
            if self.checkpadrao.GetValue() == True:
                self.organizando_dados_para_gravacao[6] = True
            else:
                self.organizando_dados_para_gravacao[6] = False

            memoria['selecionados_multiplos'][self.Meu_ID] = [self.organizando_dados_para_gravacao]
        else:
            memoria['selecionados_multiplos'][self.Meu_ID] = False


class FrameSobre(wx.Frame):
    def __init__(self):
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        wx.Frame.__init__(self, None, wx.ID_ANY, tradutor('Sobre', dicionario), (-1, -1), (400, 400),
                          style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        icone = wx.Icon(os.path.join(corrente, 'imagens', 'icon.ico'), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icone)

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
        sizer.Add(html, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(button1, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Layout()
        self.Bind(wx.EVT_BUTTON, self.destruir, button1)
        self.CenterOnScreen()  # coloca no centro da tela

    def destruir(self, event):
        self.Destroy()


class FrameConfiguracao(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.parent = parent
        icone = wx.Icon(os.path.join(corrente, 'imagens', 'icon.ico'), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icone)
        painel = wx.Panel(self, wx.ID_ANY, (0, 0), (400, 300))
        conf_prog = Configuracoes()
        config_pasta_jogos = conf_prog.leitor_configuracao('PADRAO')
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        self.estado = config_pasta_jogos

        text0 = wx.StaticText(painel, wx.ID_ANY,
                              tradutor(u"Pasta de jogos", dicionario), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)

        self.form0 = wx.TextCtrl(painel, wx.ID_ANY, config_pasta_jogos, (0, 0), (250, -1))
        self.form0.Enabled = False
        botao0 = wx.Button(painel, wx.ID_ANY, '...', (0, 0), (20, 20))
        botao0.SetToolTipString(tradutor(u'Selecione uma pasta padrão para ser armazenado os jogos de PS2', dicionario))
        self.Bind(wx.EVT_BUTTON, self.PegaPastaJogo, botao0)
        text1 = wx.StaticText(painel, wx.ID_ANY,
                              tradutor(u"Arquivos de Tradução", dicionario), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)
        self.form1 = wx.TextCtrl(painel, wx.ID_ANY, dicionario, (0, 0), (250, -1))
        if not self.form1.GetValue() == '':
            self.form1.Enabled = True
        else:
            self.form1.Enabled = False
        botao1 = wx.Button(painel, wx.ID_ANY, '...', (0, 0), (20, 20))
        botao1.SetToolTipString(tradutor(u'Escolha um arquivo de tradução, para pt-BR deixe vazio', dicionario))
        self.Bind(wx.EVT_BUTTON, self.PegaArquivoTradu, botao1)
        linha_horizontal = wx.StaticLine(painel, id=wx.ID_ANY, pos=(0, 0), size=(-1, -1),
                                         style=wx.LI_HORIZONTAL | wx.BORDER_DOUBLE, name='wx.StaticLineNameStr')
        text2 = wx.StaticText(painel, wx.ID_ANY,
                              tradutor(u"Pasta de DVD", dicionario), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)

        self.form2 = wx.TextCtrl(painel, wx.ID_ANY, os.path.join(config_pasta_jogos, 'DVD'), (0, 0), (250, -1))
        self.form2.Enabled = False
        text3 = wx.StaticText(painel, wx.ID_ANY,
                              tradutor(u"Pasta de CD", dicionario), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)
        self.form3 = wx.TextCtrl(painel, wx.ID_ANY, os.path.join(config_pasta_jogos, 'CD'), (0, 0), (250, -1))
        self.form3.Enabled = False
        text4 = wx.StaticText(painel, wx.ID_ANY,
                              tradutor(u"Pasta de capas", dicionario), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)
        self.form4 = wx.TextCtrl(painel, wx.ID_ANY, os.path.join(config_pasta_jogos, 'ART'), (0, 0), (250, -1))
        self.form4.Enabled = False
        text5 = wx.StaticText(painel, wx.ID_ANY,
                              tradutor(u"Pasta de configurações", dicionario), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)
        self.form5 = wx.TextCtrl(painel, wx.ID_ANY, os.path.join(config_pasta_jogos, 'CFG'), (0, 0), (250, -1))
        self.form5.Enabled = False



        botaook = wx.Button(painel, wx.ID_OK, 'OK', (0, 0))
        self.Bind(wx.EVT_BUTTON, self.Confirmar, botaook)

        sizer = wx.GridBagSizer(0, 10)
        sizer2 = wx.GridBagSizer(0, 0)

        sizer.Add(text0, (1, 1), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.form0, (1, 2), (1, 2), wx.ALL | wx.EXPAND, 2)
        sizer.Add(botao0, (1, 4), (1, 4), wx.ALL, 2)
        sizer.Add(text1, (2, 1), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.form1, (2, 2), (1, 2), wx.ALL | wx.EXPAND, 2)
        sizer.Add(botao1, (2, 4), (1, 4), wx.ALL, 2)
        sizer.Add(linha_horizontal, (3, 1), (1, 5), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 4)
        sizer.Add(text2, (4, 1), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.form2, (4, 2), (1, 2), wx.ALL | wx.EXPAND, 2)
        sizer.Add(text3, (5, 1), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.form3, (5, 2), (1, 2), wx.ALL | wx.EXPAND, 2)
        sizer.Add(text4, (6, 1), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.form4, (6, 2), (1, 2), wx.ALL | wx.EXPAND, 2)
        sizer.Add(text5, (7, 1), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.form5, (7, 2), (1, 2), wx.ALL | wx.EXPAND, 2)
        sizer.Add(botaook, (9, 0), (2, 7), wx.ALL | wx.ALIGN_CENTER, 10)

        painel.SetSizerAndFit(sizer)
        sizer2.Add(painel, (0, 0), (1, 1), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER)
        sizer2.AddGrowableCol(0)
        sizer2.AddGrowableRow(0)
        self.SetSizerAndFit(sizer2)
        self.Centre()

    def PegaPastaJogo(self, event):

        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        dlg = wx.DirDialog(self, tradutor(u"Selecionando pasta de jogos...", dicionario), corrente, style=wx.OPEN)
        dlg.CenterOnParent()
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

    def PegaArquivoTradu(self, event):

        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        self.wildcard2 = u"%s (*.lng)|*.lng" % (tradutor(u'Arquivo de Tradução', dicionario))
        dlg2 = wx.FileDialog(self, tradutor(u'Selecionando arquivo de tradução', dicionario), corrente, style=wx.OPEN,
                             wildcard=self.wildcard2)
        dlg2.CenterOnParent()
        if dlg2.ShowModal() == wx.ID_OK:
            valor_dialog = dlg2.GetPath()
            self.form1.Enabled = True
            self.form1.SetValue(valor_dialog)

    def Confirmar(self, event):
        conf_prog = Configuracoes()
        confg1 = self.form0.GetValue()
        confg2 = self.form1.GetValue()
        conf_prog.mudar_configuracao('PADRAO', confg1)
        conf_prog.mudar_configuracao('DICIONARIO', confg2)
        self.DVD = self.form2.GetValue()
        self.CD = self.form3.GetValue()
        self.ART = self.form4.GetValue()
        self.CFG = self.form5.GetValue()

        lista_de_diretorios = [['DVD', self.DVD], ['CD', self.CD], ['ART', self.ART],
                               ['CFG', self.CFG]]
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


class FrameAdicionarIso(wx.Frame):
    def __init__(self, parent, ID, title, endereco=('', False), codigo_do_jogo=(False, False),
                 nome_do_jogo=('NOVO_JOGO', True), tamanho_do_jogo=0, lista_de_jogos=[]):
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)


        conf_prog = Configuracoes()
        self.config_pasta_jogos = conf_prog.leitor_configuracao('PADRAO')
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        texto_adicional = '\n\n%s' % tradutor(
            u'OBSERVAÇÃO: Caso coloque um nome já usado o programa se encarregará de por um nome válido, Ex.:XXX_000.00.NOME_DO_ARQUIVO - 01',
            dicionario)
        for procus in lista_de_jogos:
            if procus[1] == codigo_do_jogo[0]:
                texto1 = procus[2]
                texto2 = procus[0]
                T1 = tradutor(u'OBSERVAÇÃO: Já existe uma jogo com esse mesmo código localizado em', dicionario)
                T2 = tradutor(u'de nome', dicionario)
                T3 = tradutor(u'e tamanho', dicionario)
                texto_adicional = u'\n\n%s "%s" %s "%s" %s "%s". O programa se encarregará de colocar um nome válido. Ex.: XXX_000.00.NOME_DO_ARQUIVO - 01' % (
                T1, texto2, T2, texto1, T3, convert_tamanho(procus[3]))

        icone = wx.Icon(os.path.join(corrente, 'imagens', 'icon.ico'), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icone)
        self.parent = parent
        self.endereco_do_jogo = endereco[0]
        self.codigo_do_jogo = codigo_do_jogo
        self.nome_do_jogo = nome_do_jogo[0]
        self.tamanho_do_jogo = convert_tamanho(tamanho_do_jogo)

        self.midia_origem = ['CD', 'DVD']
        self.padrao_destino = ['ISO', 'ul.cfg']

        if self.codigo_do_jogo[0] == False and self.codigo_do_jogo[1] == False:
            texto_info = tradutor(
                u"ATENÇÃO: O arquivo ISO selecionado não passou na checagem. Ao abrir o arquivo não foi encontrado o arquivo código característicos dos jogos de PS2. Isso pode ocorrer em jogos que possui alguma proteção.",
                dicionario)
        elif not self.codigo_do_jogo[0] == False and self.codigo_do_jogo[1] == False:
            texto_info = tradutor(u"O arquivo ISO selecionado não passou no teste, ", dicionario) + " " + tradutor(
                u"Ao abrir o arquivo não foi encontrado o arquivo código característicos dos jogos de PS2. Porém no nome do ISO selecionado apresenta um código válido.",
                dicionario)
        elif self.codigo_do_jogo[0] == False and self.codigo_do_jogo[1] == True:
            texto_info = tradutor(
                u"O arquivo ISO passou no teste. O código sugerido acima foi encontrado em seu interior.", dicionario)
        else:
            texto_info = tradutor(
                u"A checagem do arquivo ISO ocorreu sem problemas. O código sugerido acima foi encontrado em seu interior.",
                dicionario)
        texto_info += texto_adicional

        painel = wx.Panel(self, wx.ID_ANY, (0, 0), (400, 300))
        text0 = wx.StaticText(painel, wx.ID_ANY,
                              tradutor(u"Código do jogo", dicionario), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)
        self.form0 = wx.TextCtrl(painel, wx.ID_ANY,
                                 self.codigo_do_jogo[0] if not self.codigo_do_jogo[0] == False else '', (0, 0),
                                 (250, -1))
        self.form0.SetToolTipString(
            tradutor(u'Código do jogo, em caso de falha, coloque o código manualmente', dicionario))
        text1 = wx.StaticText(painel, wx.ID_ANY,
                              tradutor(u"Nome do jogo", dicionario), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)
        self.form1 = wx.TextCtrl(painel, wx.ID_ANY, self.nome_do_jogo, (0, 0), (250, -1))
        self.form1.SetToolTipString(tradutor(u'Adicionar nome do jogo', dicionario))
        text2 = wx.StaticText(painel, wx.ID_ANY,
                              tradutor(u"Tamanho do jogo", dicionario), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)
        self.form2 = wx.TextCtrl(painel, wx.ID_ANY, self.tamanho_do_jogo, (0, 0), (250, -1))
        self.form2.Enabled = False
        self.radius1 = wx.RadioBox(painel, wx.ID_ANY, tradutor(u"Mídia", dicionario), wx.DefaultPosition,
                                   wx.DefaultSize,
                                   self.midia_origem, 2, wx.RA_SPECIFY_ROWS)
        self.radius1.SetToolTipString(tradutor(u'Mídia detectada por tamanho, caso deseje escolha outro', dicionario))
        self.radius2 = wx.RadioBox(painel, wx.ID_ANY, tradutor(u'Padrão', dicionario), wx.DefaultPosition,
                                   wx.DefaultSize,
                                   self.padrao_destino, 2, wx.RA_SPECIFY_ROWS)
        self.radius2.SetToolTipString(tradutor(u'ul.cfg divide em partes, ISO copia inteiro', dicionario))

        if tamanho_do_jogo > 1024 * 1024 * 750:
            self.radius1.SetSelection(1)
            self.radius2.SetSelection(0)
            if tamanho_do_jogo > 1024 * 1024 * 1024 * 1024:
                self.radius1.SetSelection(1)
                self.radius2.SetSelection(1)
        else:
            self.radius1.SetSelection(0)
            self.radius2.SetSelection(0)

        linha_horizontal = wx.StaticLine(painel, id=wx.ID_ANY, pos=(0, 0), size=(-1, -1),
                                         style=wx.LI_HORIZONTAL | wx.BORDER_DOUBLE)

        text3 = wx.StaticText(painel, wx.ID_ANY, texto_info, (0, 0), style=wx.ALIGN_CENTER | wx.TE_MULTILINE)
        text3.Wrap(400)

        botaook = wx.Button(painel, wx.ID_OK, 'OK', (0, 0))
        botaocancelar = wx.Button(painel, wx.ID_CANCEL, tradutor('CANCELAR', dicionario), (0, 0))
        self.Bind(wx.EVT_BUTTON, self.Confirmar, botaook)

        self.Bind(wx.EVT_BUTTON, self.Cancelar, botaocancelar)

        sizer_botoes = wx.GridSizer(cols=2, hgap=30, vgap=0)
        sizer_botoes.Add(botaook, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
        sizer_botoes.Add(botaocancelar, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        sizer = wx.GridBagSizer(10, 10)
        sizer.Add(text0, (1, 1), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.form0, (1, 2), (1, 1), wx.ALL | wx.EXPAND, 2)
        sizer.Add(text1, (2, 1), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.form1, (2, 2), (1, 1), wx.ALL | wx.EXPAND, 2)
        sizer.Add(text2, (3, 1), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.form2, (3, 2), (1, 1), wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.radius1, (1, 3), (3, 2), wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.radius2, (1, 5), (3, 2), wx.ALL | wx.EXPAND, 2)
        sizer.Add(linha_horizontal, (4, 0), (1, 9), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 4)
        sizer.Add(text3, (5, 0), (2, 9), wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(sizer_botoes, (7, 0), (2, 9), wx.ALL | wx.ALIGN_CENTER | wx.EXPAND, 10)

        sizer.AddGrowableRow(5)
        painel.SetSizerAndFit(sizer)

        sizer2 = wx.GridBagSizer(0, 0)
        sizer2.Add(painel, (0, 0), (1, 1), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER)
        sizer2.AddGrowableCol(0)
        sizer2.AddGrowableRow(0)
        self.SetSizerAndFit(sizer2)
        self.Centre()

    def Pega_pasta_jogo(self, event):
        pass

    def Confirmar(self, event):
        origem = self.endereco_do_jogo
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        valor_midia = self.radius1.GetSelection()
        valor_padrao = self.radius2.GetSelection()
        midia_temp = self.midia_origem[valor_midia]
        tipo = midia_temp
        checado = False
        destino = self.config_pasta_jogos
        tamanho = 0
        nome = u"%s.%s" % (self.form0.GetValue(), self.form1.GetValue())

        fatiar = True if valor_padrao == 1 else False

        # '(origem, tipo, checado, destino, tamanho, nome, fatiar)'
        mensagem = tradutor('Copiando ', dicionario)

        self.Progress = ProgressCopia(self, u'%s%s' % (mensagem, self.form1.GetValue()),
                                       [[origem, tipo, checado, destino, tamanho, nome, fatiar]],
                                       cancelar_ativo=True)
        self.Progress.Show()
        self.Progress.CenterOnParent()
        self.Progress.iniciarcopia()
        self.Destroy()

    def Cancelar(self, event):
        self.Destroy()


class CopiarPara(wx.Frame):
    def __init__(self, parent, ID, title, endereco_do_jogo, codigo_do_jogo, nome_do_jogo, tamanho_do_jogo=0,
                 imagem=False, cfg=False, tipo_origem='', tipo_destino=''):
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        icone = wx.Icon(os.path.join(corrente, 'imagens', 'icon.ico'), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icone)
        self.endereco_do_jogo = endereco_do_jogo
        self.codigo_do_jogo = codigo_do_jogo
        self.nome_do_jogo = nome_do_jogo
        self.tamanho_do_jogo = tamanho_do_jogo
        self.imagem = imagem
        self.cfg = cfg
        self.tipo_origem = tipo_origem
        self.tipo_destino = tipo_destino
        self.lista_a_ser_copiada = []

        painel = wx.Panel(self, wx.ID_ANY, (0, 0), (400, 300))

        text0 = wx.StaticText(painel, wx.ID_ANY,
                              tradutor(u"Destino", dicionario), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)
        self.form0 = wx.TextCtrl(painel, wx.ID_ANY, '', (0, 0), (250, -1))
        self.form0.Enabled = False
        botao0 = wx.Button(painel, wx.ID_ANY, '...', (0, 0), (20, 20))
        botao0.SetToolTipString(tradutor(u'Escolha um drive ou pasta destino para o jogo', dicionario))
        self.Bind(wx.EVT_BUTTON, self.PegaPastaDestino, botao0)
        if tipo_origem == 'ul.cfg':
            texto1 = tradutor(u'Copiar no padrão ul.cfg', dicionario)
            texto2 = tradutor(u'Converter ao padrão ISO', dicionario)
        else:
            texto1 = tradutor(u'Converter ao padrão ul.cfg', dicionario)
            texto2 = tradutor(u'Copiar no padrão ISO', dicionario)
        self.midia = [texto1, texto2]

        self.radius1 = wx.RadioBox(painel, wx.ID_ANY, tradutor(u"Padrão de cópia.", dicionario), wx.DefaultPosition,
                                   wx.DefaultSize,
                                   self.midia, 2, wx.RA_SPECIFY_ROWS | wx.ALIGN_CENTER)
        self.check1 = wx.CheckBox(painel, wx.ID_ANY, tradutor("Copiar imagem de capa", dicionario))
        self.check2 = wx.CheckBox(painel, wx.ID_ANY, tradutor("Copiar arquivo cfg", dicionario))
        self.check3 = wx.CheckBox(painel, wx.ID_ANY, tradutor("Criar genericVMC vazio", dicionario))
        self.check3.SetToolTipString(tradutor(u'Implicará na edição do arquivo cfg do jogo', dicionario))

        self.botaook = wx.Button(painel, wx.ID_OK, 'OK', (0, 0))
        self.botaook.Enabled = False
        self.Bind(wx.EVT_BUTTON, self.Confirmar, self.botaook)

        sizer = wx.GridBagSizer(0, 10)
        sizer2 = wx.GridBagSizer(0, 0)

        sizer.Add(text0, (1, 1), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.form0, (1, 2), (1, 2), wx.ALL | wx.EXPAND, 2)
        sizer.Add(botao0, (1, 4), (1, 4), wx.ALL, 2)
        sizer.Add(self.radius1, (3, 1), (3, 2), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check1, (3, 3), (1, 2), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check2, (4, 3), (1, 2), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check3, (5, 3), (1, 2), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 2)
        sizer.Add(self.botaook, (7, 1), (2, 5), wx.ALL | wx.ALIGN_CENTER, 10)

        self.radius1.Enabled = False
        self.check1.Enabled = False
        self.check2.Enabled = False
        self.check3.Enabled = False

        self.check1.SetValue(False)
        self.check2.SetValue(False)
        self.check3.SetValue(False)

        painel.SetSizerAndFit(sizer)
        sizer2.Add(painel, (0, 0), (1, 1), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER)
        sizer2.AddGrowableCol(0)
        sizer2.AddGrowableRow(0)
        self.SetSizerAndFit(sizer2)
        self.Centre()

    def PegaPastaDestino(self, event):
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')

        dlg = wx.DirDialog(self, tradutor(u"Selecionando pasta destino...", dicionario), corrente, style=wx.OPEN)
        dlg.CenterOnParent()
        if dlg.ShowModal() == wx.ID_OK:
            self.valor_dialog = dlg.GetPath()
            self.form0.SetValue(self.valor_dialog)
            self.check3.Enabled = True
            self.check3.SetToolTipString(tradutor(u'Adicionar um Virtual Memory Card vazio ao destino', dicionario))

            self.botaook.Enabled = True
            self.radius1.Enabled = True
            self.radius1.SetToolTipString(tradutor(u'ul.cfg divide em partes, ISO copia inteiro', dicionario))
            if not self.imagem == False:
                origem_imagem = self.imagem
                nome_imagemzd = False
                self.check1.Enabled = True
                self.check1.SetToolTipString(
                    tradutor(u'Uma imagem foi localizada, se marcado será adicionada', dicionario))
                self.check1.SetValue(True)
                if not eh_cover_art(self.imagem):
                    self.check1.SetToolTipString(
                        tradutor(u'Não foi localizado imagem, se marcado será adicionado a imagem padrão', dicionario))
                    self.check1.SetValue(False)
                    nome_imagemzd = "%s_COV" % self.codigo_do_jogo
                    origem_imagem = os.path.join(corrente, 'imagens', 'sample.jpg')

                self.copiar_imagemzd = [origem_imagem, 'ART', False, self.form0.GetValue(), 0, nome_imagemzd, False]
            if not self.cfg == False:
                self.check2.Enabled = True
                self.check2.SetToolTipString(
                    tradutor(u'Uma arquivo cfg foi localizado, se marcado será adicionado', dicionario))
                self.check2.SetValue(True)

                self.copiar_cfgzd = [self.cfg, 'CFG', False, self.form0.GetValue(), 0, False, False]


    def Confirmar(self, event):
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')
        if self.form0.GetValue() == '':
            msgbox = wx.MessageDialog(self,
                                      tradutor(u'Escolhar um dispositivo ou pasta como destino da cópia.', dicionario),
                                      tradutor(u'Atenção!', dicionario), wx.OK | wx.ICON_INFORMATION)
            resultado = msgbox.ShowModal()
        else:
            if self.check2.GetValue() == True:
                self.lista_a_ser_copiada.append(self.copiar_cfgzd)
            if self.check1.GetValue() == True:
                self.lista_a_ser_copiada.append(self.copiar_imagemzd)
            if self.check3.GetValue() == True:
                genericvmc1 = os.path.join(corrente, 'generic_0.bin')
                genericvmc2 = os.path.join(corrente, 'generic_1.bin')
                self.lista_a_ser_copiada.append([genericvmc1, 'VMC', False, self.form0.GetValue(), 0, False, False])
                self.lista_a_ser_copiada.append([genericvmc2, 'VMC', False, self.form0.GetValue(), 0, False, False])

            origem = self.endereco_do_jogo
            tipo = self.tipo_origem
            checado = False
            destino = self.valor_dialog
            tamanho = 0
            nome = u"%s.%s" % (self.codigo_do_jogo, self.nome_do_jogo)
            fatiar = True if self.radius1.GetSelection() == 0 else False

            if os.path.basename(origem) == 'ul.cfg':
                baseghj = os.path.dirname(origem)
                nome_crc = 'ul.%08X.%s.*' % (pycrc32.crc32(self.nome_do_jogo), self.codigo_do_jogo)
                partes = glob.glob(os.path.join(baseghj, nome_crc))
                origem = partes
            conf_final = [origem, tipo, checado, destino, tamanho, nome, fatiar]
            self.lista_a_ser_copiada.append(conf_final)
            mensagem = tradutor('Copiando ', dicionario)
            self.Progress = ProgressCopia(self, u'%s%s' % (mensagem, nome),
                                           self.lista_a_ser_copiada, cancelar_ativo=True)
            self.Progress.Show()
            self.Progress.CenterOnParent()
            self.Progress.iniciarcopia()
            self.Destroy()


class FrameConfiguracaoJogo(wx.Frame):
    def __init__(self, parent, ID, title, endereco_arquivo_cfg, nome_do_jogo):
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        icone = wx.Icon(os.path.join(corrente, 'imagens', 'icon.ico'), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icone)
        self.endereco_arquivo_cfg = endereco_arquivo_cfg
        self.nome_do_jogo = nome_do_jogo
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')

        self.manipula_cfg_jogo = ManipulaCfgJogo(endereco_arquivo_cfg)

        self.info_Nome_do_jogo = self.manipula_cfg_jogo.leitor_cfg('Title')
        self.info_sistema_de_video = self.manipula_cfg_jogo.leitor_cfg('Region')
        self.info_stilo_do_jogo = self.manipula_cfg_jogo.leitor_cfg('Genre')
        self.info_testado_em = self.manipula_cfg_jogo.leitor_cfg('Compatibility')

        self.info_descricao = self.manipula_cfg_jogo.leitor_cfg('Description')
        self.info_numero_jogadores = self.manipula_cfg_jogo.leitor_cfg('Players')

        self.info_avaliacao = self.manipula_cfg_jogo.leitor_cfg('rating')
        self.info_lancamento = self.manipula_cfg_jogo.leitor_cfg('Release')
        self.info_tamvideo = self.manipula_cfg_jogo.leitor_cfg('Scan')
        self.info_classificacao = self.manipula_cfg_jogo.leitor_cfg('Esrb')
        self.info_proporcao_imagem = self.manipula_cfg_jogo.leitor_cfg('Aspect')

        self.info_desenvolvedor = self.manipula_cfg_jogo.leitor_cfg('Developer')

        self.comp_callbacktimer = self.manipula_cfg_jogo.leitor_cfg('$CallbackTimer')
        self.comp_AltStartup = self.manipula_cfg_jogo.leitor_cfg('$AltStartup')
        self.comp_dnas = self.manipula_cfg_jogo.leitor_cfg("$DNAS")
        self.comp_xfg = self.manipula_cfg_jogo.leitor_cfg("$Compatibility")

        if self.comp_xfg == '':
            self.comp_compatibilidade = [0]
        else:
            self.comp_compatibilidade = self.manipula_cfg_jogo.leitor_compatibilidade(int(self.comp_xfg))

        self.config_vmc0 = self.manipula_cfg_jogo.leitor_cfg('$VMC_0')
        self.config_vmc1 = self.manipula_cfg_jogo.leitor_cfg('$VMC_1')

        painel = wx.Panel(self, wx.ID_ANY, (0, 0), (400, 300))

        self.text0 = wx.StaticText(painel, wx.ID_ANY, tradutor(u"Informações do jogo", dicionario), (0, 0),
                                   style=wx.TE_RICH)
        font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.text0.SetFont(font)

        self.text1 = wx.StaticText(painel, wx.ID_ANY,
                                   tradutor(u"Nome do jogo", dicionario), (0, 0),
                                   style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.form1 = wx.TextCtrl(painel, wx.ID_ANY, self.nome_do_jogo, (0, 0), (200, -1), style=wx.TE_RICH)
        self.form1.Enabled = False
        self.text2 = wx.StaticText(painel, wx.ID_ANY, tradutor(u"Descrição", dicionario), (0, 0),
                                   style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.form2 = wx.TextCtrl(painel, wx.ID_ANY, self.info_descricao, (0, 0), (200, 50),
                                 style=wx.TE_RICH| wx.TE_MULTILINE)
        self.form2.Enabled = True
        self.text3 = wx.StaticText(painel, wx.ID_ANY, tradutor(u"Sistema de imagem", dicionario), (0, 0),
                                   style=wx.TE_RICH)
        self.form3 = wx.TextCtrl(painel, wx.ID_ANY, self.info_sistema_de_video, (0, 0), (150, -1), style=wx.TE_RICH)
        self.form3.Enabled = False
        self.textgenero = wx.StaticText(painel, wx.ID_ANY,
                                        tradutor(u"Gênero", dicionario), (0, 0),
                                        style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.formgenero = wx.TextCtrl(painel, wx.ID_ANY, self.info_stilo_do_jogo, (0, 0), (150, -1), style=wx.TE_RICH)
        self.formgenero.Enabled = True
        self.formgenero.SetToolTipString(tradutor(u'Ex. Corrida, Luta, Aventura, FPS, etc.', dicionario))
        self.text4 = wx.StaticText(painel, wx.ID_ANY, tradutor(u"Numero de jogadores", dicionario), (0, 0),
                                   style=wx.TE_RICH)
        self.form4 = wx.TextCtrl(painel, wx.ID_ANY, self.info_numero_jogadores, (0, 0), (50, -1), style=wx.TE_RICH)
        self.form4.Enabled = True
        self.form4.SetToolTipString(tradutor(u'Quantidade de jogadores máximos no jogo', dicionario))
        self.text5 = wx.StaticText(painel, wx.ID_ANY, tradutor(u"Compatibilidade", dicionario), (0, 0), (-1, -1),
                                   style=wx.TE_RICH)
        self.form5 = wx.TextCtrl(painel, wx.ID_ANY, self.info_testado_em, (0, 0), (200, -1), style=wx.TE_RICH)
        self.form5.Enabled = True
        self.form5.SetToolTipString(
            tradutor(u'Lista dos dispositivos que o jogo funcionou Ex. REDE, USB, HD', dicionario))
        self.textrating = wx.StaticText(painel, wx.ID_ANY, tradutor(u"Avaliação", dicionario), (0, 0), (-1, -1),
                                        style=wx.TE_RICH)
        self.formrating = wx.TextCtrl(painel, wx.ID_ANY, self.info_avaliacao, (0, 0), (200, -1), style=wx.TE_RICH)
        self.formrating.Enabled = True
        self.formrating.SetToolTipString(tradutor(u'Valor de 1 a 5', dicionario))
        self.textRelease = wx.StaticText(painel, wx.ID_ANY, tradutor(u"Lançamento", dicionario), (0, 0), (-1, -1),
                                         style=wx.TE_RICH)
        self.formRelease = wx.TextCtrl(painel, wx.ID_ANY, self.info_lancamento, (0, 0), (200, -1), style=wx.TE_RICH)
        self.formRelease.Enabled = True
        self.formRelease.SetToolTipString(tradutor(u'Ano de lançamento do jogo', dicionario))
        self.textScan = wx.StaticText(painel, wx.ID_ANY, tradutor(u"Tamanho da tela", dicionario), (0, 0),
                                      style=wx.TE_RICH)
        self.formScan = wx.TextCtrl(painel, wx.ID_ANY, self.info_tamvideo, (0, 0), (200, -1), style=wx.TE_RICH)
        self.formScan.Enabled = True
        self.formScan.SetToolTipString(tradutor(u'Dimensões da largura', dicionario))
        self.textEsrb = wx.StaticText(painel, wx.ID_ANY, tradutor(u"Classificação", dicionario), (0, 0),
                                      style=wx.TE_RICH)
        self.formEsrb = wx.TextCtrl(painel, wx.ID_ANY, self.info_classificacao, (0, 0), (200, -1), style=wx.TE_RICH)
        self.formEsrb.Enabled = True
        self.formEsrb.SetToolTipString(tradutor(u'Classificação indicativa Ex. Criança, Adulto', dicionario))
        self.textAspect = wx.StaticText(painel, wx.ID_ANY, tradutor(u"Formato da tela", dicionario), (0, 0), (-1, -1),
                                        style=wx.TE_RICH)
        self.formAspect = wx.TextCtrl(painel, wx.ID_ANY, self.info_proporcao_imagem, (0, 0), (200, -1),
                                      style=wx.TE_RICH)
        self.formAspect.Enabled = True
        self.formAspect.SetToolTipString(tradutor(u'Compatibilidade com telas Widescreen', dicionario))
        self.textDeveloper = wx.StaticText(painel, wx.ID_ANY, tradutor(u"Desenvolvedor", dicionario), (0, 0),
                                           style=wx.TE_RICH)
        self.formDeveloper = wx.TextCtrl(painel, wx.ID_ANY, self.info_desenvolvedor, (0, 0), (200, -1),
                                         style=wx.TE_RICH)
        self.formDeveloper.Enabled = True
        self.formDeveloper.SetToolTipString(tradutor(u'Desenvolvedor do jogo', dicionario))
        self.textcallbacktimer = wx.StaticText(painel, wx.ID_ANY, tradutor(u"Callback timer", dicionario), (0, 0),
                                               style=wx.TE_RICH)
        self.formcallbacktimer = wx.TextCtrl(painel, wx.ID_ANY, self.comp_callbacktimer, (0, 0), (200, -1),
                                             style=wx.TE_RICH)
        self.formcallbacktimer.Enabled = True
        self.formcallbacktimer.SetToolTipString(tradutor(u'Aplicar um atraso para as funções CDVD', dicionario))
        self.textAltStartup = wx.StaticText(painel, wx.ID_ANY, tradutor(u"Arquivo de arranque", dicionario), (0, 0),
                                            style=wx.TE_RICH)
        self.formAltStartup = wx.TextCtrl(painel, wx.ID_ANY, self.comp_AltStartup, (0, 0), (200, -1), style=wx.TE_RICH)
        self.formAltStartup.Enabled = True
        self.formAltStartup.SetToolTipString(tradutor(u'Apontar o arquivo ELF que inicia o jogo', dicionario))
        self.textdnas = wx.StaticText(painel, wx.ID_ANY, tradutor(u"ID DNA", dicionario), (0, 0),
                                      style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.formdnas = wx.TextCtrl(painel, wx.ID_ANY, self.comp_dnas, (0, 0), (200, -1), style=wx.TE_RICH)
        self.formdnas.SetToolTipString(tradutor(u'ID para jogar pela internet', dicionario))
        self.formdnas.Enabled = True

        linha_horizontal = wx.StaticLine(painel, id=wx.ID_ANY, pos=(0, 0), size=(-1, -1),
                                         style=wx.LI_HORIZONTAL | wx.BORDER_DOUBLE)
        self.text6 = wx.StaticText(painel, wx.ID_ANY,
                                   tradutor(u"Configurações de compatibilidade", dicionario), (0, 0))
        self.text6.SetFont(font)

        self.check1 = wx.CheckBox(painel, wx.ID_ANY, tradutor("Modo 1", dicionario))
        self.check1.SetToolTipString(tradutor(u'Ler core alternativo', dicionario))
        self.check2 = wx.CheckBox(painel, wx.ID_ANY, tradutor("Modo 2", dicionario))
        self.check2.SetToolTipString(tradutor(u'Método alternativo de leitura de dados', dicionario))
        self.check3 = wx.CheckBox(painel, wx.ID_ANY, tradutor("Modo 3", dicionario))
        self.check3.SetToolTipString(tradutor(u'Desprender chamadas do sistema', dicionario))
        self.check4 = wx.CheckBox(painel, wx.ID_ANY, tradutor("Modo 4", dicionario))
        self.check4.SetToolTipString(tradutor(u'Modo PPS 0', dicionario))
        self.check5 = wx.CheckBox(painel, wx.ID_ANY, tradutor("Modo 5", dicionario))
        self.check5.SetToolTipString(tradutor(u'Desabilitar DVD-DL', dicionario))
        self.check6 = wx.CheckBox(painel, wx.ID_ANY, tradutor("Modo 6", dicionario))
        self.check6.SetToolTipString(tradutor(u'Desabilitar IGR', dicionario))
        self.check7 = wx.CheckBox(painel, wx.ID_ANY, tradutor("Modo 7", dicionario))
        self.check7.SetToolTipString(tradutor(u'Usar hack IOP threading', dicionario))
        self.check8 = wx.CheckBox(painel, wx.ID_ANY, tradutor("Modo 8", dicionario))
        self.check8.SetToolTipString(tradutor(u'Esconder módulo dev9', dicionario))

        for check in self.comp_compatibilidade:
            if check == 1:
                self.check1.SetValue(True)
            if check == 2:
                self.check2.SetValue(True)
            if check == 4:
                self.check3.SetValue(True)
            if check == 8:
                self.check4.SetValue(True)
            if check == 16:
                self.check5.SetValue(True)
            if check == 32:
                self.check6.SetValue(True)
            if check == 64:
                self.check7.SetValue(True)
            if check == 128:
                self.check8.SetValue(True)
            else:
                pass

        linha_horizontal2 = wx.StaticLine(painel, id=wx.ID_ANY, pos=(0, 0), size=(-1, -1),
                                          style=wx.LI_HORIZONTAL | wx.BORDER_DOUBLE)

        self.text7 = wx.StaticText(painel, wx.ID_ANY,
                                   tradutor(u"Configuração do VMC", dicionario), (0, 0),
                                   style= wx.ALIGN_CENTER_VERTICAL)
        self.text7.SetFont(font)
        self.text8 = wx.StaticText(painel, wx.ID_ANY,
                                   tradutor(u"Virtual Memory Card 1", dicionario), (0, 0))
        self.form8 = wx.TextCtrl(painel, wx.ID_ANY, self.config_vmc0, (0, 0), (200, -1))
        self.form8.Enabled = False
        self.text9 = wx.StaticText(painel, wx.ID_ANY,
                                   tradutor(u"Virtual Memory Card 2", dicionario), (0, 0),
                                   style= wx.ALIGN_CENTER_VERTICAL)
        self.form9 = wx.TextCtrl(painel, wx.ID_ANY, self.config_vmc1, (0, 0), (200, -1))
        self.form9.Enabled = False

        self.botaook = wx.Button(painel, wx.ID_OK, 'OK', (0, 0))
        self.Bind(wx.EVT_BUTTON, self.Confirmar, self.botaook)

        sizer = wx.GridBagSizer(0, 10)
        sizer2 = wx.GridBagSizer(0, 0)

        sizer.Add(self.text0, (1, 0), (1, 6), wx.ALIGN_CENTER, 2)
        sizer.Add(self.text1, (3, 1), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.form1, (3, 2), (1, 3), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.text2, (5, 1), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.form2, (5, 2), (2, 3), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.text3, (4, 1), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.form3, (4, 2), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.textgenero, (4, 3), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.formgenero, (4, 4), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.text4, (7, 1), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.form4, (7, 2), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.text5, (7, 3), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.form5, (7, 4), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)

        sizer.Add(self.textDeveloper, (8, 1), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.formDeveloper, (8, 2), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)

        sizer.Add(self.textRelease, (8, 3), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.formRelease, (8, 4), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.textScan, (9, 1), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.formScan, (9, 2), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.textAspect, (9, 3), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.formAspect, (9, 4), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.textEsrb, (10, 1), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.formEsrb, (10, 2), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.textrating, (10, 3), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.formrating, (10, 4), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)

        sizer.Add(linha_horizontal, (12, 0), (1, 6), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 2)
        sizer.Add(self.text6, (13, 0), (1, 6), wx.ALIGN_CENTER, 2)

        sizer.Add(self.check1, (15, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check2, (15, 2), (1, 1), wx.ALL | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check3, (16, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check4, (16, 2), (1, 1), wx.ALL | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check5, (17, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check6, (17, 2), (1, 1), wx.ALL | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check7, (18, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check8, (18, 2), (1, 1), wx.ALL | wx.ALIGN_CENTER, 2)
        sizer.Add(self.textcallbacktimer, (15, 3), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.formcallbacktimer, (15, 4), (1, 1), wx.ALL | wx.ALIGN_CENTER | wx.EXPAND, 2)
        sizer.Add(self.textAltStartup, (16, 3), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.formAltStartup, (16, 4), (1, 1), wx.ALL | wx.ALIGN_CENTER | wx.EXPAND, 2)
        sizer.Add(self.textdnas, (17, 3), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.formdnas, (17, 4), (1, 1), wx.ALL | wx.ALIGN_CENTER | wx.EXPAND, 2)

        sizer.Add(linha_horizontal2, (20, 0), (1, 6), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 2)
        sizer.Add(self.text7, (21, 0), (1, 6), wx.ALIGN_CENTER, 2)

        sizer.Add(self.text8, (23, 1), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.form8, (23, 2), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.text9, (23, 3), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.form9, (23, 4), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)

        sizer.Add(self.botaook, (25, 0), (2, 5), wx.ALL | wx.ALIGN_CENTER, 10)

        painel.SetSizerAndFit(sizer)
        sizer2.Add(painel, (0, 0), (1, 1), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER)
        sizer2.AddGrowableCol(0)
        sizer2.AddGrowableRow(0)
        self.SetSizerAndFit(sizer2)
        self.Centre()


    def Confirmar(self, event):
        some = 0

        if self.check1.GetValue() == True:
            some += 1
        if self.check2.GetValue() == True:
            some += 2
        if self.check3.GetValue() == True:
            some += 4
        if self.check4.GetValue() == True:
            some += 8
        if self.check5.GetValue() == True:
            some += 16
        if self.check6.GetValue() == True:
            some += 32
        if self.check7.GetValue() == True:
            some += 64
        if self.check8.GetValue() == True:
            some += 128
        if some == 0:
            some = ''

        self.manipula_cfg_jogo.mudar_dict_cfg('Title', self.nome_do_jogo)
        self.manipula_cfg_jogo.mudar_dict_cfg('Region', self.info_sistema_de_video)
        self.manipula_cfg_jogo.mudar_dict_cfg('Genre', self.formgenero.GetValue())

        self.manipula_cfg_jogo.mudar_dict_cfg('Compatibility', self.form5.GetValue())
        self.manipula_cfg_jogo.mudar_dict_cfg('rating', self.formrating.GetValue())
        self.manipula_cfg_jogo.mudar_dict_cfg('Description', self.form2.GetValue())
        self.manipula_cfg_jogo.mudar_dict_cfg('Players', self.form4.GetValue())
        self.manipula_cfg_jogo.mudar_dict_cfg('Release', self.formRelease.GetValue())
        self.manipula_cfg_jogo.mudar_dict_cfg('Scan', self.formScan.GetValue())
        self.manipula_cfg_jogo.mudar_dict_cfg('Esrb', self.formEsrb.GetValue())
        self.manipula_cfg_jogo.mudar_dict_cfg('Aspect', self.formAspect.GetValue())

        self.manipula_cfg_jogo.mudar_dict_cfg('Developer', self.formDeveloper.GetValue())

        self.manipula_cfg_jogo.mudar_dict_cfg('$CallbackTimer', self.formcallbacktimer.GetValue())
        self.manipula_cfg_jogo.mudar_dict_cfg('$AltStartup', self.formAltStartup.GetValue())
        self.manipula_cfg_jogo.mudar_dict_cfg("$Compatibility", some)
        self.manipula_cfg_jogo.mudar_dict_cfg("$DNAS", self.formdnas.GetValue())
        self.manipula_cfg_jogo.mudar_dict_cfg('$VMC_0', self.form8.GetValue())
        self.manipula_cfg_jogo.mudar_dict_cfg('$VMC_1', self.form9.GetValue())

        self.manipula_cfg_jogo.gravar_em_arquivo()
        self.Destroy()


class ProgressCopia(wx.Dialog):
    def __init__(self, parent, title, lista_de_arquivos, cancelar_ativo=True):
        wx.Dialog.__init__(self, parent, title=title, style=wx.CAPTION)
        """ O ProgressDialog é responsável pela gravação de arquivos, sendo que durante a cópia é apresentado uma
            barra de progresso.
            Exemplo de uso:

            self.ProgressDialog = ProgressCopia(None, u'Título', Lista_de_arquivos)
            self.ProgressDialog.Show()
            self.frame.iniciarcopia()

            sendo que CADA ITEM deve estar organizado da seguinte maneira:
            (origem, tipo, checado, destino, tamanho, nome, fatiar)

            origem = endereço do arquivo a ser copiado ou lista de endereços
                    OBS.:   Caso se trate de uma lista de endereços, caso 'fatiar = False' as partes serão juntas em 1 so arquivo.
                            Caso contrário serão copiados arquivo po arquivo.
            tipo = defino o tipo de arquivo, serão tratados os tipos: ART, DVD, CD, VMC, CFG, ulCD e ulDVD.
                    OBS.:   Caso não seja nenhum desses tipos acima serão copiados da forma como se encontram.
            checado = O arquivo passará por uma checagem retornando True se estiver tudo OK. False é o padrão.
            destino = Pasta onde serão copiado(s) o(s) arquivo(s)
            tamanho = O programa irá calcular o tamanho e por aqui. O padrão é 0.
            nome = nome do arquivo destino, se False será usado a da origem
            fatiar = Se True fatia o arquivo em padaços de 1 giga enumerando cada fatia
        """
        self.BUFFER = 1024
        self.tamanho_maximo_fatia = 1073741824
        self.tamanho_total = 0
        self.dados_gravados_total = 0
        self.quant = len(lista_de_arquivos)
        conf_prog = Configuracoes()
        dicionario = conf_prog.leitor_configuracao('DICIONARIO')

        self.mensagem1 = tradutor('Copiando arquivo', dicionario)
        self.mensagem2 = tradutor('de', dicionario)
        self.progresso = 0
        self.acabouse = False
        self.lista_de_arquivos = lista_de_arquivos
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.gauge = wx.Gauge(self, range=100, size=(300, 30))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.textinfo = wx.StaticText(self, wx.ID_ANY, '%s 1 %s %s' % (self.mensagem1, self.mensagem2, self.quant),
                                      (0, 0), style=wx.TE_RICH)
        sizer.Add(self.textinfo, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        sizer.Add(self.gauge, 0, wx.ALL, 10)
        if cancelar_ativo:
            self.cancel = wx.Button(self, wx.ID_CANCEL, tradutor("&Cancelar", dicionario))
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

    def iniciarcopia(self):
        """
            Inicia a copia dos arquivos
        """
        cont_files = 0
        wx.Yield()
        self.cancel.SetDefault()
        for y in self.lista_de_arquivos:
            self.tamanho_total += self.calcula_tamanho(y)
        for x in self.lista_de_arquivos:
            wx.Yield()
            cont_files += 1
            self.prepara_destino(x)
            self.checa_se_existe(x)
            self.criar_nome_destino(x)

            self.textinfo.SetLabel('%s %s %s %s' % (self.mensagem1, cont_files, self.mensagem2, self.quant))

            endereco_de_origem = x[0]
            tipo_de_arquivo = x[1]
            checado = x[2]
            destino = x[3]
            tamanho = x[4]
            novo_nome = x[5]
            fatiar = x[6]
            self.arquivo_destino = os.path.join(destino, novo_nome)
            if fatiar == True and tipo_de_arquivo != 'ulCD' and tipo_de_arquivo != 'ulDVD':

                fatias = 0
                with open(endereco_de_origem, 'rb') as origem_aberto:
                    while True:
                        self.arquivo_destino = os.path.join(destino, '%s.%02d' % (novo_nome, fatias))
                        self.destino_aberto = open(self.arquivo_destino, 'wb')
                        self.dados_gravados = 0
                        while self.dados_gravados < self.tamanho_maximo_fatia:

                            datax = origem_aberto.read(self.BUFFER)
                            if datax:
                                self.destino_aberto.write(datax)
                                self.dados_gravados += self.BUFFER
                                self.dados_gravados_total += self.BUFFER
                                self.progresso = int(
                                    (float(self.dados_gravados_total) / float(self.tamanho_total)) * 100)
                                self.gauge.SetValue(self.progresso)
                                wx.Yield()
                            else:
                                break

                        fatias += 1
                        if datax:
                            pass
                        else:
                            break
            else:
                self.tamanho_desse_arquivo = tamanho
                if fatiar == True and type(endereco_de_origem) == list:
                    contgh = 0

                    for g in endereco_de_origem:
                        s = os.stat(g)
                        self.tamanho_desse_arquivo = s.st_size
                        self.arquivo_destino2 = "%s.%02d" % (self.arquivo_destino, contgh)

                        with open(self.arquivo_destino2, "wb") as self.destino_aberto:
                            with open(g, "rb") as origem_aberto:

                                while True:
                                    y = origem_aberto.read(self.BUFFER)
                                    self.tamanho_desse_arquivo -= self.BUFFER
                                    self.dados_gravados_total += self.BUFFER
                                    self.progresso = int(
                                        (float(self.dados_gravados_total) / float(self.tamanho_total)) * 100)
                                    self.gauge.SetValue(self.progresso)
                                    wx.Yield()
                                    try:
                                        self.destino_aberto.write(y)
                                    except ValueError:
                                        break
                                    if not self.tamanho_desse_arquivo > 0:
                                        break
                        contgh += 1
                else:
                    if not type(endereco_de_origem) == list:
                        endereco_de_origem = [endereco_de_origem]

                    with open(self.arquivo_destino, "wb") as self.destino_aberto:

                        for f in endereco_de_origem:
                            s = os.stat(f)
                            self.tamanho_desse_arquivo = s.st_size
                            with open(f, "rb") as origem_aberto:

                                while True:
                                    y = origem_aberto.read(self.BUFFER)
                                    self.tamanho_desse_arquivo -= self.BUFFER
                                    self.dados_gravados_total += self.BUFFER
                                    self.progresso = int(
                                        (float(self.dados_gravados_total) / float(self.tamanho_total)) * 100)
                                    self.gauge.SetValue(self.progresso)
                                    wx.Yield()
                                    try:
                                        self.destino_aberto.write(y)
                                    except ValueError:
                                        break
                                    if not self.tamanho_desse_arquivo > 0:
                                        break

        self.Destroy()

    def prepara_destino(self, item):
        """
            Prepara a pasta destino
        """
        if item[1] == 'DVD' and item[6] == False:
            item[3] = os.path.join(item[3], 'DVD')
        elif item[1] == 'CD' and item[6] == False:
            item[3] = os.path.join(item[3], 'CD')
        if item[1] == 'ulDVD' and item[6] == False:
            item[3] = os.path.join(item[3], 'DVD')
        elif item[1] == 'ulCD' and item[6] == False:
            item[3] = os.path.join(item[3], 'CD')
        elif item[1] == 'ART' and item[6] == False:
            item[3] = os.path.join(item[3], 'ART')
        elif item[1] == 'CFG' and item[6] == False:
            item[3] = os.path.join(item[3], 'CFG')
        elif item[1] == 'VMC' and item[6] == False:
            item[3] = os.path.join(item[3], 'VMC')

        if not os.path.exists(item[3]):
            try:
                os.makedirs(item[3])
            except:
                pass

    def checa_se_existe(self, item):
        """
            Checa se a origem existe
        """
        if item[1] == 'ulDVD' or item[1] == 'ulCD':
            item[2] = True
            for x in item[0]:
                if not os.path.exists(x):
                    item[2] = False
        else:
            if os.path.exists(item[0]):
                item[2] = True

    def calcula_tamanho(self, item):
        """
            Calcula o tamanho em bytes do arquivo ou grupo de arquivo
        """
        if item[1] == 'ulDVD' or item[1] == 'ulCD':
            v = 0
            for y in item[0]:
                z = os.stat(y)
                v += z.st_size

        else:
            x = os.stat(item[0])
            v = x.st_size
        item[4] = v
        return v

    def criar_nome_destino(self, item):

        """
            Verifica se o destino já existe, se sim cria um novo nome.
        """
        destino = item[3]
        nome = item[5]
        origem = item[0]
        if type(origem) == list:
            origem = origem[0]

        nome_origem_com_extensao = os.path.basename(origem)

        extensao = nome_origem_com_extensao.split('.')[-1]
        cor = (len(extensao) + 1) * (-1)
        apenas_nome_origem = nome_origem_com_extensao[:cor]

        if item[1] != 'DVD' and item[1] != 'CD' and item[1] != 'ulCD' and item[1] != 'ulDVD':
            if nome == False:
                nome = apenas_nome_origem
                nome_base = nome
                nome = "%s.%s" % (nome_base, extensao)
                cont = 0
                if item[1] == 'VMC':
                    while os.path.exists(os.path.join(destino, nome)):
                        if os.path.exists(os.path.join(destino, '%s.bkp' % nome)):
                            os.remove(os.path.join(destino, '%s.bkp' % nome))
                        os.rename(os.path.join(destino, nome), os.path.join(destino, '%s.bkp' % nome))
                    item[5] = nome
                elif item[1] == 'CFG' or item[1] == 'ART':
                    if os.path.exists(os.path.join(destino, nome)):
                        os.remove(os.path.join(destino, nome))
                    item[5] = nome
                else:
                    while os.path.exists(os.path.join(destino, nome)):
                        cont += 1
                        nome = '%s - %02d.%s' % (nome_base, cont, extensao)
                    item[5] = nome
            else:
                nome_base = nome
                nome = "%s.%s" % (nome_base, extensao)
                cont = 0
                while os.path.exists(os.path.join(destino, nome)):
                    cont += 1
                    nome = '%s - %02d.%s' % (nome_base, cont, extensao)
                item[5] = nome

        else:
            if item[6] == True:

                apenas_nome = nome[12:]
                apenas_codigo = nome[0:11]
                nome_base = 'ul.%08X.%s' % (pycrc32.crc32(apenas_nome), apenas_codigo)
                nome = "%s.00" % (nome_base)
                cont = 0
                novo_nome_ul = apenas_nome
                nom = nome_base

                while os.path.exists(os.path.join(destino, nome)):
                    cont += 1
                    novo_nome_ul = "%s - %02d" % (apenas_nome, cont)
                    nom = 'ul.%08X.%s' % (pycrc32.crc32(novo_nome_ul), apenas_codigo)
                    nome = '%s.00' % (nom)
                nomeul_apenas_nome = novo_nome_ul
                nomeul_sem_extensao = nom
                nomeul_com_extensao = nome
                item[5] = nomeul_sem_extensao

                conteudo_ul = ''
                if os.path.exists(os.path.join(destino, 'ul.cfg')):
                    with open(os.path.join(destino, 'ul.cfg'), 'r') as ulaberto:
                        conteudo_ul = ulaberto.read()
                        conteudo_ul = conteudo_ul

                with open(os.path.join(destino, 'ul.cfg'), 'w') as ulaberto2:
                    ul = ManipulaUl()
                    partes = int(item[4] / 1073741824) + 1
                    novo_ul = ul.criar_nome_ul(apenas_codigo, novo_nome_ul,
                                               'CD' if item[1] == 'CD' or item[1] == 'ulCD' else 'DVD', partes)
                    conteudo_ul2 = '%s%s' % (conteudo_ul.decode('utf-8'), novo_ul)
                    ulaberto2.write(conteudo_ul2.encode('utf-8'))
            else:

                nome_base = nome
                nome = "%s.iso" % (nome_base)
                cont = 0
                while os.path.exists(os.path.join(destino, nome)):
                    cont += 1
                    nome = '%s - %02d.iso' % (nome_base, cont)
                item[5] = nome


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
            self.destino_aberto.close()
            time.sleep(2)
            os.remove(self.arquivo_destino)
            self.Destroy()


class LoginDialog(wx.Dialog):

    def __init__(self, parent, nova_senha=False):
        """self, Window parent, int id=-1, String title=EmptyString,
            Point pos=DefaultPosition, Size size=DefaultSize,
            long style=DEFAULT_DIALOG_STYLE, String name=DialogNameStr"""
        wx.Dialog.__init__(self, parent, wx.ID_ANY, u"Autorização", (-1, -1), (300, 150))
        self.autorizado = False
        if nova_senha == True:
            self.SetTitle('Adicione uma senha administrativa')

        self.nova_senha = nova_senha
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        textsenha = wx.StaticText(self, label="Nome:")
        self.formlogin = wx.TextCtrl(self)
        self.addWidgets(textsenha, self.formlogin)

        textsenha = wx.StaticText(self, label="Senha:")
        self.formsenha = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        self.addWidgets(textsenha, self.formsenha)

        okBtn = wx.Button(self, wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.Confirmar, okBtn)
        btnSizer.Add(okBtn, 0, wx.CENTER|wx.ALL, 5)
        cancelBtn = wx.Button(self, wx.ID_CANCEL)
        btnSizer.Add(cancelBtn, 0, wx.CENTER|wx.ALL, 5)

        self.mainSizer.Add(btnSizer, 0, wx.CENTER)
        self.SetSizer(self.mainSizer)

    def Confirmar(self, event):
        arquivo_de_senha = os.path.join(corrente,'pwd')
        login = self.formlogin.GetValue()
        senha = self.formsenha.GetValue()
        senha_hash = hashlib.sha224(senha).hexdigest()
        if self.nova_senha == False:
            if os.path.exists(arquivo_de_senha):
                with open(arquivo_de_senha, 'r') as lendopass:
                    aberto = lendopass.readlines()
                    for x in aberto:
                        splitando = x.split(' = ')
                        if len(splitando) == 2:
                            login_no_arquivo = splitando[0]
                            if login == login_no_arquivo:
                                senha_no_arquivo = splitando[1][0:56]
                                if senha_hash == senha_no_arquivo:
                                    self.autorizado = True
            else:
                login_padrao = 'admin'
                senha_padrao = hashlib.sha224("admin").hexdigest()
                if login == login_padrao and senha_hash == senha_padrao:
                    self.autorizado = True

        else:
            if os.path.exists(arquivo_de_senha):
                with open(arquivo_de_senha, 'r') as lendopass:
                    aberto = lendopass.read()
            else:
                aberto = ''

            with open(arquivo_de_senha, 'w') as escrevendopass:
                novo_texto = "%s = %s" %(login, senha_hash)
                escrevendo = '%s\n%s' %(aberto, novo_texto)
                escrevendopass.write(escrevendo)
        self.Destroy()


    def addWidgets(self, lbl, txt):
        """
        """
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(lbl, 0, wx.ALL|wx.CENTER, 5)
        sizer.Add(txt, 1, wx.EXPAND|wx.ALL, 5)
        self.mainSizer.Add(sizer, 0, wx.EXPAND)

if __name__ == '__main__':
    y = MeuPrograma()
    y.MainLoop()



