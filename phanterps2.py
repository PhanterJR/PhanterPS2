# -*- coding: utf-8 -*- 
# Versão 1.1
# Copyright (c) 2014 PhanterJR
# https://github.com/PhanterJR
# Licença LGPL

import wx
import wx.html
import os
from phanterdefs import Dicionario, Configuracoes, LocalizaArt, LocalizaJogos, convert_tamanho,\
    VerificaJogo, ManipulaUl, muda_nome_jogo, ManipulaCfgJogo, deletararquivos
import glob
from contrib import pycrc32
import time
import hashlib
import webbrowser

corrente = os.getcwd()
memoria = dict()
memoria['tamanho_total_dos_jogos'] = 0
memoria['jogos_selecionados'] = 0
memoria['progresso'] = 0
memoria['selecionado_para_copiar'] = {}
memoria['selecionados_multiplos'] = {}
memoria['configuracao'] = {}
memoria['arquivo_configuracao'] = {}
memoria['arquivo_imagemcheck'] = {}
memoria['end_arquivo_senha'] = {}
memoria['end_linguagem'] = {}

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

        PastaConfProgrm = os.path.join(wx.StandardPaths.Get().GetUserConfigDir())
        EndPastaPadraoConf = os.path.join(PastaConfProgrm , 'phanterps2')
        memoria['end_arquivo_senha'] = os.path.join(PastaConfProgrm , 'phanterps2')
        memoria['end_linguagem'] = os.path.join(PastaConfProgrm , 'phanterps2', 'linguagem')
        pasta_documentos = os.path.join(wx.StandardPaths.Get().GetDocumentsDir())
        
        if not os.path.exists(EndPastaPadraoConf):
            os.makedirs(os.path.join(EndPastaPadraoConf, 'linguagem'))

            with open(os.path.join(EndPastaPadraoConf, 'phanterps2.cfg'), 'w') as arquivo_cfg:
                arquivo_cfg.write("")

            self.conf_prog2 = Configuracoes(os.path.join(EndPastaPadraoConf, 'phanterps2.cfg'))
            self.conf_prog2.mudar_configuracao('DVD', os.path.join(pasta_documentos,'PhanterPS2','DVD'))
            self.conf_prog2.mudar_configuracao('CD', os.path.join(pasta_documentos,'PhanterPS2','CD'))
            self.conf_prog2.mudar_configuracao('CFG', os.path.join(pasta_documentos,'PhanterPS2','CFG'))
            self.conf_prog2.mudar_configuracao('ART', os.path.join(pasta_documentos,'PhanterPS2','ART'))
            self.conf_prog2.mudar_configuracao('PADRAO', os.path.join(pasta_documentos,'PhanterPS2'))
            self.conf_prog2.mudar_configuracao('DICIONARIO', "")
            self.conf_prog2.mudar_configuracao('CLASSIFICACAO_CAMPO', "")
            self.conf_prog2.mudar_configuracao('CLASSIFICACAO_ORDEM', "")
            self.conf_prog2.mudar_configuracao('CLASSIFICACAO_DEFAULT', "")
            memoria['configuracao'] = self.conf_prog2.config

            memoria['arquivo_configuracao'] = os.path.join(EndPastaPadraoConf, 'phanterps2.cfg')

            with open(os.path.join(EndPastaPadraoConf, 'imagemcheck.cfg'), 'w') as arquivo_cfg:
                padrao = ""
                arquivo_cfg.write(padrao)

            memoria['arquivo_imagemcheck'] = os.path.join(EndPastaPadraoConf, 'imagemcheck.cfg')
            vlista_cover_ART = LocalizaArt(memoria['configuracao']['ART'])
            vlista_cover_ART.retirar_exitf_imagem(vlista_cover_ART.lista_conver)

        else:
            if not os.path.join(EndPastaPadraoConf, 'linguagem'):
                os.makedirs(os.path.join(EndPastaPadraoConf, 'linguagem'))
            if not os.path.exists(os.path.join(EndPastaPadraoConf, 'phanterps2.cfg')):

                with open(os.path.join(EndPastaPadraoConf, 'phanterps2.cfg'), 'w') as arquivo_cfg:
                    arquivo_cfg.write("")

                self.conf_prog2 = Configuracoes(os.path.join(EndPastaPadraoConf, 'phanterps2.cfg'))
                self.conf_prog2.mudar_configuracao('DVD', os.path.join(pasta_documentos,'PhanterPS2','DVD'))
                self.conf_prog2.mudar_configuracao('CD', os.path.join(pasta_documentos,'PhanterPS2','CD'))
                self.conf_prog2.mudar_configuracao('CFG', os.path.join(pasta_documentos,'PhanterPS2','CFG'))
                self.conf_prog2.mudar_configuracao('ART', os.path.join(pasta_documentos,'PhanterPS2','ART'))
                self.conf_prog2.mudar_configuracao('PADRAO', os.path.join(pasta_documentos,'PhanterPS2'))
                self.conf_prog2.mudar_configuracao('DICIONARIO', "")
                self.conf_prog2.mudar_configuracao('CLASSIFICACAO_CAMPO', "")
                self.conf_prog2.mudar_configuracao('CLASSIFICACAO_ORDEM', "")
                self.conf_prog2.mudar_configuracao('CLASSIFICACAO_DEFAULT', "")
                self.conf_prog2 = Configuracoes(os.path.join(EndPastaPadraoConf, 'phanterps2.cfg'))
                memoria['configuracao'] = self.conf_prog2.config

                memoria['arquivo_configuracao'] = os.path.join(EndPastaPadraoConf, 'phanterps2.cfg')

            else:
                if not os.path.join(EndPastaPadraoConf, 'linguagem'):
                    os.makedirs(os.path.join(EndPastaPadraoConf, 'linguagem'))
                self.conf_prog2 = Configuracoes(os.path.join(EndPastaPadraoConf, 'phanterps2.cfg'))
                self.conf_prog = self.conf_prog2.config
                como_set_dic = self.conf_prog['DICIONARIO']
                if not como_set_dic == "":
                    if como_set_dic[0] == '#':
                        self.conf_prog2.mudar_configuracao('DICIONARIO', os.path.join(EndPastaPadraoConf,'linguagem',como_set_dic[1:]))

                if self.conf_prog['DVD'] == '':
                    self.conf_prog2.mudar_configuracao('DVD', os.path.join(pasta_documentos,'PhanterPS2','DVD'))
                if self.conf_prog['CD'] == '':
                    self.conf_prog2.mudar_configuracao('CD', os.path.join(pasta_documentos,'PhanterPS2','CD'))
                if self.conf_prog['CFG'] == '':
                    self.conf_prog2.mudar_configuracao('CFG', os.path.join(pasta_documentos,'PhanterPS2','CFG'))
                if self.conf_prog['ART'] == '':
                    self.conf_prog2.mudar_configuracao('ART', os.path.join(pasta_documentos,'PhanterPS2','ART'))
                if self.conf_prog['PADRAO'] == '':
                    self.conf_prog2.mudar_configuracao('PADRAO', os.path.join(pasta_documentos,'PhanterPS2'))
                self.conf_prog2 = Configuracoes(os.path.join(EndPastaPadraoConf, 'phanterps2.cfg'))
                memoria['configuracao'] = self.conf_prog2.config

                memoria['arquivo_configuracao'] = os.path.join(EndPastaPadraoConf, 'phanterps2.cfg')

            if not os.path.exists(os.path.join(EndPastaPadraoConf, 'imagemcheck.cfg')):
                with open(os.path.join(EndPastaPadraoConf, 'imagemcheck.cfg'), 'w') as arquivo_cfg:
                    padrao = ""
                    arquivo_cfg.write(padrao)
            memoria['arquivo_imagemcheck'] = os.path.join(EndPastaPadraoConf, 'imagemcheck.cfg')
            vlista_cover_ART = LocalizaArt(memoria['configuracao']['ART'])
            vlista_cover_ART.retirar_exitf_imagem(vlista_cover_ART.lista_conver)
            leinto_confi = Configuracoes(os.path.join(EndPastaPadraoConf, 'imagemcheck.cfg'))
            for asjko in vlista_cover_ART.lista_conver:
                if not leinto_confi.leitor_configuracao(asjko) == 'OK':
                    leinto_confi.mudar_configuracao(asjko, 'OK')

        self.splashbmp = wx.Image(os.path.join(corrente, 'imagens', 'splash.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.conf_prog = Configuracoes(memoria['arquivo_configuracao'])
        self.dicionario = memoria['configuracao']['DICIONARIO']
        self.Tradutor = Dicionario(self.dicionario)
        self.meusplash = MeuSplash(self,ID=wx.ID_ANY, title=self.Tradutor.tradutor('Iniciando o programa'), gauge=True)
        self.meusplash.painel_bmp.SetBitmap(self.splashbmp)
        self.meusplash.Texto.SetLabel(self.Tradutor.tradutor('Iniciando o programa'))
        self.meusplash.Show(True)
        self.meusplash.painel_bmp.SetBitmap(self.splashbmp)
        self.meusplash.Texto.SetLabel(self.Tradutor.tradutor('Iniciando o programa'))
        wx.Yield()
        self.lista_de_selecionados = []
        
        self.pastadefault = memoria['configuracao']['PADRAO']
        self.fp_default_campo =  memoria['configuracao']['CLASSIFICACAO_CAMPO']
        self.fp_default_ordem =  memoria['configuracao']['CLASSIFICACAO_ORDEM']
        self.fp_classificacao_default =  memoria['configuracao']['CLASSIFICACAO_DEFAULT']
        self.tamanho_vindo_do_filho = 0
        self.counter_click_popup = 0
        self.CopiarTaAtivado = False
        fp_imagem_iso = wx.Image(os.path.join(corrente, 'imagens', 'isops2.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        fp_imagem_multiiso = wx.Image(os.path.join(corrente, 'imagens', 'multips2.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        fp_imagem_atualizar = wx.Image(os.path.join(corrente, 'imagens', 'atualizar.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        fp_imagem_config_progr = wx.Image(os.path.join(corrente, 'imagens', 'config.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.fp_imagem_sobre = wx.Image(os.path.join(corrente, 'imagens', 'sobre.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        fp_imagem_admin = wx.Image(os.path.join(corrente, 'imagens', 'admin.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        fp_imagem_classificacao = wx.Image(os.path.join(corrente, 'imagens', 'classificar.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        fp_imagem_checks = wx.Image(os.path.join(corrente, 'imagens', 'checks.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()

        

        # diminui a imagem para 16x16#
        new_fp_imagem_iso = wx.ImageFromBitmap(fp_imagem_iso).Scale(16, 16, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        new_fp_imagem_multiiso = wx.ImageFromBitmap(fp_imagem_multiiso).Scale(16, 16, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        new_fp_imagem_atualizar = wx.ImageFromBitmap(fp_imagem_atualizar).Scale(16, 16, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        new_fp_imagem_config_progr = wx.ImageFromBitmap(fp_imagem_config_progr).Scale(16, 16, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        new_fp_imagem_sobre = wx.ImageFromBitmap(self.fp_imagem_sobre).Scale(16, 16, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        new_fp_imagem_admin = wx.ImageFromBitmap(fp_imagem_admin).Scale(16, 16, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        new_fp_imagem_classificacao = wx.ImageFromBitmap(fp_imagem_classificacao).Scale(16, 16, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        new_fp_imagem_checks = wx.ImageFromBitmap(fp_imagem_checks).Scale(16,16, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()

        self.title = title

        barra_de_status = self.CreateStatusBar()
        self.SetStatusText(self.Tradutor.tradutor("Bem vindo ao PhanterPS2"))

        barra_de_ferramentas = self.CreateToolBar()
        barra_de_ferramentas.SetBackgroundColour('#BEBEBE')

        fp_tool_abririso = barra_de_ferramentas.AddSimpleTool(
            wx.NewId(), fp_imagem_iso,
            self.Tradutor.tradutor("Adicionar novo jogo ISO"),
            self.Tradutor.tradutor(u"Selecionar imagens ISO para adicionar a lista de jogos"))
        fp_tool_multiso = barra_de_ferramentas.AddSimpleTool(
            wx.NewId(), fp_imagem_multiiso,
            self.Tradutor.tradutor(u'Adicionar múltiplos jogos ISO'),
            self.Tradutor.tradutor(u'Selecionar vários ISOs para adicionar a lista de jogos'))
        fp_tool_atualizar = barra_de_ferramentas.AddSimpleTool(
            wx.NewId(), fp_imagem_atualizar,
            self.Tradutor.tradutor("Atualizar"),
            self.Tradutor.tradutor(u"Atualizar lista de jogos"))
        fp_tool_configuracoes = barra_de_ferramentas.AddSimpleTool(
            wx.NewId(), fp_imagem_config_progr, self.Tradutor.tradutor(u"Configurações"),
            self.Tradutor.tradutor("Configurar o PhanterPS2"))
        fp_tool_classificar = barra_de_ferramentas.AddSimpleTool(
            wx.NewId(), fp_imagem_classificacao,
            self.Tradutor.tradutor('Classificar'),
            self.Tradutor.tradutor(u'Classificar em ordem crescente ou decrescente os campos'))
        fp_tool_checks = barra_de_ferramentas.AddSimpleTool(
            wx.NewId(), fp_imagem_checks,
            self.Tradutor.tradutor('Desmarcar todos os Checkboxes'),
            self.Tradutor.tradutor(u'Desmarca todos os checkboxes dos jogos'))
        fp_tool_senha = barra_de_ferramentas.AddSimpleTool(
            wx.NewId(), fp_imagem_admin,
            self.Tradutor.tradutor('Mudar senha'),
            self.Tradutor.tradutor(u'Adiciona uma senha para administração'))

        fp_tool_sobre = barra_de_ferramentas.AddSimpleTool(
            wx.NewId(), self.fp_imagem_sobre,
            self.Tradutor.tradutor("Sobre"),
            self.Tradutor.tradutor(u"Sobre o programa e autor"))


        barra_de_ferramentas.Realize()

        Barra_de_menu = wx.MenuBar()
        menu_arquivo = wx.Menu()

        item1_menu_arquivo = wx.MenuItem(menu_arquivo, wx.ID_ANY,
                                         self.Tradutor.tradutor("A&dicionar novo ISO\tCtrl+A"),
                                         self.Tradutor.tradutor(u"Selecionar imagens ISO para adicionar a lista de jogos"))
        item1_menu_arquivo.SetBitmap(new_fp_imagem_iso)
        item2_menu_arquivo = wx.MenuItem(menu_arquivo, wx.ID_ANY,
                                         self.Tradutor.tradutor(u'Adicionar &múltiplos jogos ISO\tCtrl+M'),
                                         self.Tradutor.tradutor(u'Selecionar vários ISOs para adicionar a lista de jogos'))
        item2_menu_arquivo.SetBitmap(new_fp_imagem_multiiso)
        item3_menu_arquivo = wx.MenuItem(menu_arquivo, wx.ID_ANY,
                                         self.Tradutor.tradutor("A&tualizar"),
                                         self.Tradutor.tradutor(u"Atualizar lista de jogos"))
        item3_menu_arquivo.SetBitmap(new_fp_imagem_atualizar)


        menu_arquivo.AppendItem(item1_menu_arquivo)
        menu_arquivo.AppendItem(item2_menu_arquivo)
        menu_arquivo.AppendItem(item3_menu_arquivo)


        Barra_de_menu.Append(menu_arquivo, self.Tradutor.tradutor("&Arquivo"))

        menu_configuracoes = wx.Menu()

        item1_menu_configuracoes = wx.MenuItem(menu_configuracoes, wx.ID_ANY,
                                         self.Tradutor.tradutor(u"Configurações"),
                                         self.Tradutor.tradutor(u"Configurar o PhanterPS2"))
        item1_menu_configuracoes.SetBitmap(new_fp_imagem_config_progr)

        item2_menu_configuracoes = wx.MenuItem(menu_configuracoes, wx.ID_ANY,
                                self.Tradutor.tradutor('Classificar'),
                                self.Tradutor.tradutor(u'Classificar em ordem crescente ou decrescente os campos'))
        item2_menu_configuracoes.SetBitmap(new_fp_imagem_classificacao)

        item3_menu_configuracoes = wx.MenuItem(menu_configuracoes, wx.ID_ANY,
                                self.Tradutor.tradutor('Desmarcar todos os Checkboxes'),
                                self.Tradutor.tradutor(u'Desmarca todos os checkboxes dos jogos'))
        item3_menu_configuracoes.SetBitmap(new_fp_imagem_checks)

        item4_menu_configuracoes = wx.MenuItem(menu_configuracoes, wx.ID_ANY,
                                self.Tradutor.tradutor('Mudar senha'),
                                self.Tradutor.tradutor(u'Adiciona uma senha para administração'))
        item4_menu_configuracoes.SetBitmap(new_fp_imagem_admin)

        menu_configuracoes.AppendItem(item1_menu_configuracoes)
        menu_configuracoes.AppendItem(item2_menu_configuracoes)
        menu_configuracoes.AppendItem(item3_menu_configuracoes)
        menu_configuracoes.AppendItem(item4_menu_configuracoes)


        menu_sobre = wx.Menu()

        item1_menu_sobre = wx.MenuItem(menu_sobre, wx.ID_ANY, self.Tradutor.tradutor(u"&Sobre\tF1"),
                                       self.Tradutor.tradutor("Sobre o PhanterPS2"))
        item1_menu_sobre.SetBitmap(new_fp_imagem_sobre)
        menu_sobre.AppendItem(item1_menu_sobre)
        Barra_de_menu.Append(menu_configuracoes, self.Tradutor.tradutor(u'Configurações'))
        Barra_de_menu.Append(menu_sobre, self.Tradutor.tradutor("Ajuda"))
        self.Bind(wx.EVT_MENU, self.AbrirIso, item1_menu_arquivo)
        self.Bind(wx.EVT_MENU, self.MultiIso, item2_menu_arquivo)
        self.Bind(wx.EVT_MENU, self.Atualizar, item3_menu_arquivo)
        self.Bind(wx.EVT_MENU, self.Config, item1_menu_configuracoes)
        self.Bind(wx.EVT_MENU, self.classificar_campos, item2_menu_configuracoes)
        self.Bind(wx.EVT_MENU, self.checks, item3_menu_configuracoes)
        self.Bind(wx.EVT_MENU, self.mudarsenha, item4_menu_configuracoes)
        self.Bind(wx.EVT_MENU, self.Sobre, item1_menu_sobre)
        self.Bind(wx.EVT_TOOL, self.AbrirIso, fp_tool_abririso)
        self.Bind(wx.EVT_TOOL, self.MultiIso, fp_tool_multiso)
        self.Bind(wx.EVT_TOOL, self.Atualizar, fp_tool_atualizar)
        self.Bind(wx.EVT_TOOL, self.Config, fp_tool_configuracoes)
        self.Bind(wx.EVT_TOOL, self.Sobre, fp_tool_sobre)
        self.Bind(wx.EVT_TOOL, self.classificar_campos, fp_tool_classificar)
        self.Bind(wx.EVT_TOOL, self.checks, fp_tool_checks)
        self.Bind(wx.EVT_TOOL, self.mudarsenha, fp_tool_senha)
        self.SetMenuBar(Barra_de_menu)
        self.Bind(wx.EVT_CHECKBOX, self.dofilho2)
        self.Bind(wx.EVT_BUTTON, self.dofilho)

        if self.fp_classificacao_default == "0" or self.fp_classificacao_default == 0:
            self.fp_default_campo=False
            self.fp_default_ordem='crescente' 


        self.atualizar_refresh(refresh = False, classificacao = self.fp_default_campo, modo = self.fp_default_ordem)
        arquivo_de_senha = os.path.join(memoria['end_arquivo_senha'], 'pwd')
        if not os.path.exists(arquivo_de_senha):
            self.SetStatusText(self.Tradutor.tradutor(u"Ainda não foi definido uma senha para o administador - nome: admin, senha: admin"))

        self.Layout()

    def atualizar_refresh(self, refresh = False, classificacao = False, modo = 'crescente'):

        self.counter_click_popup=0
        self.conf_prog = Configuracoes(memoria['arquivo_configuracao'])
        self.dicionario = memoria['configuracao']['DICIONARIO']
        self.Tradutor = Dicionario(self.dicionario)
        if refresh is True:
            self.meusplash = MeuSplash(self,ID=wx.ID_ANY,title=self.Tradutor.tradutor("Processando, Aguarde..."), gauge=True)
            self.meusplash.painel_bmp.SetBitmap(self.splashbmp)
            self.meusplash.Texto.SetLabel(self.Tradutor.tradutor('Localizando jogos...'))
            self.meusplash.Show(True)
            wx.Yield()

        fp_jogos_encontrados = LocalizaJogos(self.pastadefault)

        self.jogos_e_info = fp_jogos_encontrados.ordem_alfabetica(classificacao, modo)

        self.listjogos = self.jogos_e_info[0]
        if refresh is True:
            self.pastadefault = memoria['configuracao']['PADRAO']
            self.painel_principal.Destroy()
        self.painel_principal = wx.Panel(self, wx.ID_ANY)  #Painel Pinricpal
        self.Default_color_painel_jogo = self.painel_principal.GetBackgroundColour()

        sizer_panel_titulo = wx.GridBagSizer(0, 0)  #sizers
        sizer_panel = wx.GridBagSizer(0, 100)
        self.arquivoiso = ""
        if refresh is True:
            self.SendSizeEvent()

        self.painel_cabecalho = wx.Panel(self.painel_principal, wx.ID_ANY,
                                         (0, 0), (-1, 25), style=wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)
        self.painel_cabecalho.Hide()
        text0 = wx.StaticText(self.painel_cabecalho, wx.ID_ANY,
                              self.Tradutor.tradutor(u"Lista de Jogos - Playstation 2"), (0, 0), style=wx.TE_RICH)
        font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        text0.SetFont(font)
        sizer_panel_titulo.Add(text0, (0, 0), (1, 1), wx.ALIGN_CENTER, 5)
        sizer_panel_titulo.AddGrowableCol(0)

        self.painel_cabecalho.SetSizerAndFit(sizer_panel_titulo)
 
        self.painel_scroll = wx.ScrolledWindow(self.painel_principal, wx.ID_ANY, (0, 0), (-1, 525), style = wx.HSCROLL | wx.VSCROLL )
        self.painel_scroll.Hide()
        
        self.meusplash.painel_bmp.SetBitmap(self.splashbmp)
        self.meusplash.Texto.SetLabel(self.Tradutor.tradutor('Localizando imagens'))
        wx.Yield()
        self.imagens_jogos = LocalizaArt(os.path.join(self.pastadefault, 'ART'))
        meuid = 0
        quantogauge = len(self.listjogos)
        self.meusplash.painel_bmp.SetBitmap(self.splashbmp)
        self.meusplash.Texto.SetLabel(self.Tradutor.tradutor('Criando lista de jogos'))
        wx.Yield()
        self.list_de_checks = []
        if len(self.listjogos) < 8:
            sizer_jogos = wx.GridSizer(cols=1, hgap=0, vgap=0)
        else:
            sizer_jogos = wx.GridSizer(cols=2, hgap=0, vgap=0)
        
        for x in self.listjogos:
            meuid += 1
            valorgauge = int(float(meuid)/quantogauge*100)
            self.meusplash.barrinha.SetValue(valorgauge)
            wx.Yield()
            self.painel_jogo = PainelJogos(
                self.painel_scroll, wx.ID_NEW, (0, 0), (-1, 110),
                arquivo_do_jogo=x[0], codigo_do_jogo=x[1], nome_do_jogo=x[2], tamanho_do_jogo=x[3],
                partes=x[4], tipo_midia=x[5], lista_cover_art=self.imagens_jogos, Meu_ID=meuid)
            self.list_de_checks.append(self.painel_jogo)
            sizer_jogos.Add(self.painel_jogo, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
            if refresh == True:
                self.SendSizeEvent()
            if not 50%meuid:
                self.meusplash.painel_bmp.SetBitmap(self.splashbmp)
                self.meusplash.Texto.SetLabel(self.Tradutor.tradutor('Localizando jogos...'))
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
        textTilulo1 = wx.StaticText(self.painel_info, wx.ID_ANY, self.Tradutor.tradutor(u'INFORMAÇÕES GERAIS'),
                                    (0, 0), style = wx.ALIGN_CENTER | wx.TE_RICH)
        text1 = wx.StaticText(self.painel_info, wx.ID_ANY, self.Tradutor.tradutor(u"Total de jogos"),
                              (0, 0), style=wx.TE_RICH)
        form1 = wx.TextCtrl(self.painel_info, wx.ID_ANY, str(self.jogos_e_info[1]), (0, 0), style=wx.TE_RICH)
        form1.Enabled = False
        text2 = wx.StaticText(self.painel_info, wx.ID_ANY, self.Tradutor.tradutor(u"Tamanho total"),
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
                                    self.Tradutor.tradutor(u'INFORMAÇÕES E AÇÕES DOS SELECIONADOS'),
                                    (0, 0), style=wx.ALIGN_CENTER | wx.TE_RICH)
        text3 = wx.StaticText(self.painel_acao, wx.ID_ANY,
                              self.Tradutor.tradutor(u"Total de jogos"),
                              (0, 0), style=wx.TE_RICH)
        self.form3 = wx.TextCtrl(self.painel_acao, wx.ID_ANY, '0', (0, 0), style=wx.TE_RICH)
        self.form3.Enabled = False
        text4 = wx.StaticText(self.painel_acao, wx.ID_ANY,
                              self.Tradutor.tradutor(u"Tamanho Total"), (0, 0),
                              style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.form4 = wx.TextCtrl(self.painel_acao, wx.ID_ANY,
                                 convert_tamanho(memoria['tamanho_total_dos_jogos']), (0, 0), style=wx.TE_RICH)
        self.form4.Enabled = False
        self.botao_deletar_tudo = wx.Button(self.painel_acao, wx.ID_ANY, self.Tradutor.tradutor(u'Deletar selecionados'), (0, 0))
        self.id_botao_deletar_tudo = self.botao_deletar_tudo.GetId()
        self.botao_deletar_tudo.Enabled = False

        self.Bind(wx.EVT_BUTTON, self.DeletarCopiar, self.botao_deletar_tudo)

        text5 = wx.StaticText(self.painel_acao, wx.ID_ANY,
                              self.Tradutor.tradutor(u"Pasta destino"), (0, 0),
                              style=wx.TE_RICH| wx.ALIGN_CENTER_VERTICAL)
        self.form5 = wx.TextCtrl(self.painel_acao, wx.ID_ANY, '', (0, 0), style=wx.TE_RICH)
        self.form5.Enabled = False

        self.fp_img_abrir = wx.Image(os.path.join(corrente, 'imagens', 'abrir.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.fp_botao_abrir = wx.BitmapButton(self.painel_acao, wx.ID_ANY, self.fp_img_abrir, (0, 0))

        self.id_botao_copiar_selecionados = self.fp_botao_abrir.GetId()
        self.fp_botao_abrir.Enabled = False
        self.Bind(wx.EVT_BUTTON, self.PastaDestino, self.fp_botao_abrir)

        self.copiar_VMC = wx.CheckBox(self.painel_acao, wx.ID_ANY, self.Tradutor.tradutor('VMC'),(0 ,0))
        self.copiar_VMC.SetToolTipString(self.Tradutor.tradutor(u'Se ativado, copiar um Virtual Memory Card vazio, se já existir um no destino, será renomeado'))
        self.copiar_VMC.Enabled=False
        self.copia_padrao_iso = wx.CheckBox(self.painel_acao, wx.ID_ANY,
                                            self.Tradutor.tradutor(u'Copiar no Formato ISO'), (0 ,0))
        self.copia_padrao_iso.Enabled=False
        self.copia_padrao_iso.SetToolTipString(
            self.Tradutor.tradutor(u'A cópia será no formato ISO se ativado, caso contrário, será no formato UL'))
        self.copiar_Capa = wx.CheckBox(self.painel_acao, wx.ID_ANY, self.Tradutor.tradutor('Capa'),(0 ,0))
        self.copiar_Capa.Enabled=False
        self.copiar_Capa.SetToolTipString(
            self.Tradutor.tradutor(u'Se ativado, copia a capa do jogo se existir ou a capa padrão'))
        self.copia_cfg = wx.CheckBox(self.painel_acao, wx.ID_ANY, self.Tradutor.tradutor('CFG'), (0 ,0))
        self.copia_cfg.Enabled=False
        self.copia_cfg.SetToolTipString(self.Tradutor.tradutor(u'Se ativado, copia o arquivo de configuração do jogo'))

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
        sizer_painel_acao.Add(self.fp_botao_abrir, (2, 6), (1, 1), wx.ALL | wx.EXPAND, 5)
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
        self.meusplash.Destroy()
    
    def AbrirIso(self, event):
        self.wildcard = "%s (*.iso)|*.iso" % (self.Tradutor.tradutor('Imagem ISO'))
        past_oui = memoria['configuracao']['PADRAO']
        self.janeladlg = wx.FileDialog(self, self.Tradutor.tradutor(u"Selecionando Imagem..."), past_oui, style=wx.OPEN,
                                       wildcard=self.wildcard)
        self.janeladlg.CenterOnParent()
        if self.janeladlg.ShowModal() == wx.ID_OK:
            self.arquivoiso = self.janeladlg.GetPaths()
            self.janeladlg.Destroy()
            result = VerificaJogo(self.arquivoiso[0])
            resultados = result.resultado_final
            self.resultados = resultados

            self.frame = FrameAdicionarIso(self, wx.ID_ANY,
                                              self.Tradutor.tradutor(u"Adicione o nome e código do jogo"),
                                              self.resultados[0], self.resultados[1], self.resultados[2],
                                              self.resultados[3], self.resultados[4], self.listjogos)          
            self.frame.Show(True)

    def MultiIso(self, event):
        self.wildcard = "%s (*.iso)|*.iso" % (self.Tradutor.tradutor('Imagem ISO'))
        past_oui = memoria['configuracao']['PADRAO']
        self.janeladlg = wx.FileDialog(self, self.Tradutor.tradutor(u"Selecionando Imagens..."), past_oui,
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
                uno = [res[0], res[1], res[2], res[3], res[4]]
                lis.append(uno)
            lista_de_jogoss = [lis, tam_tot]

            self.janeladlg.Destroy()
            self.frame = FrameAdicionarMultiplos(self, self.title, lista_de_jogoss[0], lista_de_jogoss[1], (-1, -1),
                                                   (1000, 400))
            self.frame.Show(True)

    def Atualizar(self, event):
        self.fp_default_campo = self.conf_prog.leitor_configuracao('CLASSIFICACAO_CAMPO')
        self.fp_default_ordem = self.conf_prog.leitor_configuracao('CLASSIFICACAO_ORDEM')
        self.atualizaremanterchecks(True, self.fp_default_campo, self.fp_default_ordem)
           
    def atualizaremanterchecks(self, refresh = False, classificacao = False, modo = 'crescente'):
        self.pastadefault = memoria['configuracao']['PADRAO']
        lista = self.list_de_checks

        total_games = self.form3.GetValue()
        if total_games != '0':
            total_size = self.form4.GetValue()
            label_botao_dele = self.botao_deletar_tudo.GetLabel()

        new_lista = []
        for x in lista:
            endereco = x.form_arq_origem.GetValue()
            codigo = x.pj_codigoj.GetValue()
            nome = x.form_nomejogo.GetValue()
            tamanho = x.form_tamanho_arq.GetValue()
            check = x.check_selecionado.GetValue()
            new_lista.append([[endereco, codigo, nome, tamanho], check])
        self.atualizar_refresh(refresh = refresh, classificacao = classificacao, modo = modo)
        lista2 = self.list_de_checks
        for x in lista2:
            endereco = x.form_arq_origem.GetValue()
            codigo = x.pj_codigoj.GetValue()
            nome = x.form_nomejogo.GetValue()
            tamanho = x.form_tamanho_arq.GetValue()
            check = x.check_selecionado.GetValue()
            pegalista=[endereco, codigo, nome, tamanho]
            for y in new_lista:
                if pegalista == y[0]:
                    x.check_selecionado.SetValue(y[1])
                    if y[1] == True:
                        self.Default_color_painel_jogo = x.GetBackgroundColour()
                        x.SetBackgroundColour('#9BCD9B')
                        x.form_nomejogo.SetBackgroundColour('#9BCD9B')
                        x.form_arq_origem.SetBackgroundColour('#9BCD9B')
                        x.form_tamanho_arq.SetBackgroundColour('#9BCD9B')
                        x.Refresh()

        if total_games != '0':
            self.form3.SetValue(total_games)
            self.form4.SetValue(total_size)
            #self.form5
            self.fp_botao_abrir.Enabled = True
            self.botao_deletar_tudo.Enabled = True
            self.botao_deletar_tudo.SetLabel(label_botao_dele)
            self.botao_deletar_tudo.SetForegroundColour(wx.RED)      

    def classificar_campos(self, event):
        frame_classificar_campos = FrameClassificacao(self, title = self.Tradutor.tradutor(u"Escolha como deve ser classificado"))
        frame_classificar_campos.ShowModal()

    def mudarsenha(self, event):
        login = FrameLogin(self, title =  self.Tradutor.tradutor(u"A ação deve ser autorizada"), nova_senha=True)
        login.CenterOnParent()
        login.ShowModal()

    def Sobre(self, event):
        x = FrameSobre(title = self.Tradutor.tradutor('Sobre'))
        x.Show()

    def Config(self, event):
        frame = FrameConfiguracao(self, -1, self.Tradutor.tradutor(u"Configurações"))
        frame.Show(True)

    def DeletarCopiar(self, event):
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

            self.Progress = ProgressCopia(self, self.Tradutor.tradutor('Copiando arquivos selecionados'),lista_de_arquivos)
            self.Progress.Show()
            self.Progress.iniciarcopia()
            if not self.Progress.cancelado == False:
                deletararquivos(self.Progress.cancelado[0], self.Progress.cancelado[1])
        else:
            login = FrameLogin(self, title=self.Tradutor.tradutor(u"A ação deve ser autorizada"), nova_senha=False)
            login.CenterOnParent()
            login.ShowModal()
            #login.Destroy()
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
                        try:
                            os.remove(xw[0])
                        except WindowsError:
                            assert False, "Phan 02"
                self.fp_default_campo = self.conf_prog.leitor_configuracao('CLASSIFICACAO_CAMPO')
                self.fp_default_ordem = self.conf_prog.leitor_configuracao('CLASSIFICACAO_ORDEM')
                self.atualizaremanterchecks(True, self.fp_default_campo, self.fp_default_ordem)

    def PastaDestino(self, event):
        past_oui = memoria['configuracao']['PADRAO']
        dlg = wx.DirDialog(self, self.Tradutor.tradutor(u"Selecionando pasta destino..."), past_oui, style=wx.OPEN)
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
            self.botao_deletar_tudo.SetLabel(self.Tradutor.tradutor('Copiar selecionados'))

    def checks(self, event):
        self.apagar_checks_value()


    def apagar_checks_value(self):
        self.counter_click_popup = 0
        memoria['jogos_selecionados'] = 0
        memoria['selecionado_para_copiar'] = {}
        memoria['tamanho_total_dos_jogos'] = 0
        self.form3.SetValue('0')
        self.form4.SetValue('0 KB')
        self.CopiarTaAtivado = False
        self.form5.SetValue('')
        self.botao_deletar_tudo.SetLabel(self.Tradutor.tradutor('Deletar selecionados'))
        self.botao_deletar_tudo.Enabled = False
        self.fp_botao_abrir.Enabled = False
        self.botao_deletar_tudo.SetForegroundColour(wx.BLACK)
        self.copiar_VMC.Enabled = False
        self.copia_padrao_iso.Enabled = False
        self.copiar_Capa.Enabled = False
        self.copia_cfg.Enabled = False
        lista = self.list_de_checks
        for x in lista:
            x.check_selecionado.SetValue(False) #################################################33
            x.SetBackgroundColour(self.Default_color_painel_jogo)
            x.form_nomejogo.SetBackgroundColour(self.Default_color_painel_jogo)
            x.form_arq_origem.SetBackgroundColour(self.Default_color_painel_jogo)
            x.form_tamanho_arq.SetBackgroundColour(self.Default_color_painel_jogo)
            x.Refresh()

    
    def dofilho(self, event):
        self.conf_prog = Configuracoes(memoria['arquivo_configuracao'])
        self.dicionario = memoria['configuracao']['DICIONARIO']
        self.Tradutor = Dicionario(self.dicionario)
        self.pastadefault = memoria['configuracao']['PADRAO']
        self.fp_default_campo = self.conf_prog.leitor_configuracao('CLASSIFICACAO_CAMPO')
        self.fp_default_ordem = self.conf_prog.leitor_configuracao('CLASSIFICACAO_ORDEM')
        self.atualizaremanterchecks(True, self.fp_default_campo, self.fp_default_ordem)

    def dofilho2(self, event):
        self.form3.SetValue(str(memoria['jogos_selecionados']))
        self.form4.SetValue(convert_tamanho(memoria['tamanho_total_dos_jogos']))
        if self.form4.GetValue() == '0 KB':
            self.CopiarTaAtivado = False
            self.form5.SetValue('')
            self.botao_deletar_tudo.SetLabel(self.Tradutor.tradutor('Deletar selecionados'))
            self.botao_deletar_tudo.Enabled = False
            self.fp_botao_abrir.Enabled = False
            self.botao_deletar_tudo.SetForegroundColour(wx.BLACK)
            self.copiar_VMC.Enabled = False
            self.copia_padrao_iso.Enabled = False
            self.copiar_Capa.Enabled = False
            self.copia_cfg.Enabled = False

        else:
            if self.counter_click_popup == 0:
                win = PopUp(self, wx.SIMPLE_BORDER)
                pos = self.fp_botao_abrir.ClientToScreen( (40,-5) )
                win.Position(pos, (400, 300))
                win.Popup()
            self.counter_click_popup += 1

            if self.form5.GetValue() == '':
                self.botao_deletar_tudo.SetForegroundColour(wx.RED)
            self.botao_deletar_tudo.Enabled = True
            self.fp_botao_abrir.Enabled = True
            if self.form5.GetValue() == '':
                self.botao_deletar_tudo.SetForegroundColour(wx.RED)
            self.botao_deletar_tudo.Enabled = True
            self.fp_botao_abrir.Enabled = True


class MeuSplash (wx.Frame):

    def __init__(self, parent, ID , title,
        style=wx.NO_BORDER | wx.SIMPLE_BORDER,
        duration=105000, bitmapfile=os.path.join(corrente, 'imagens', 'splash.png'),
        callback = None, gauge=False):

        self.conf_prog = Configuracoes(memoria['arquivo_configuracao'])
        self.dicionario = memoria['configuracao']['DICIONARIO']
        self.Tradutor = Dicionario(self.dicionario)
        bmp = wx.Image(bitmapfile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bitmap = bmp
        self.title = title
        self.gauge=gauge

        size = (bmp.GetWidth(), bmp.GetHeight()+40)
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
        painel = wx.Panel(self, wx.ID_ANY, (0,0))
        painel.SetBackgroundColour(wx.WHITE)
        self.painel_gauge = wx.Panel(self, wx.ID_ANY, (0,0), (400,40))

        self.painel_gauge.SetBackgroundColour(wx.BLACK)
        self.painel_bmp = wx.StaticBitmap(painel, wx.ID_ANY, self.bitmap, (0, 0))

        self.Texto = wx.StaticText(painel, wx.ID_ANY, self.title, (50, 153), (300, -1), style=wx.ALIGN_CENTER)
        font = wx.Font(15, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.Texto.SetFont(font)
        sizer_gauge = wx.GridBagSizer(2,2)
        self.barrinha = wx.Gauge(self.painel_gauge, range=100, pos = (2,1), size=(395, 20))
        sizer_gauge.Add(self.barrinha, (0,0), (1,2), wx.ALL | wx.EXPAND,2)
        self.painel_gauge.SetSizerAndFit(sizer_gauge)
        sizer.Add(self.painel_bmp, (0,0), (1,1), wx.ALL | wx.EXPAND, 0)
        sizer.Add(self.painel_gauge, (1,0), (1,1), wx.ALL| wx.EXPAND,0)
        painel.SetSizerAndFit(sizer)
        if self.gauge == False:
            self.barrinha.Hide()

        class SplashTimer(wx.Timer):
            def __init__(self, targetFunction):
                self.Notify = targetFunction
                wx.Timer.__init__(self)

        if callback is None:
            callback = self.OnSplashExitDefault

        self.timer = SplashTimer(callback)
        self.timer.Start(duration, 1) # one-shot only

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
        #self.conf_prog = Configuracoes(memoria['arquivo_configuracao'])
        self.dicionario = memoria['configuracao']['DICIONARIO']
        self.Tradutor = Dicionario(self.dicionario)
        self.Meu_ID = Meu_ID
        self.arquivo_do_jogo = arquivo_do_jogo
        self.codigo_do_jogo = codigo_do_jogo
        self.nome_do_jogo = nome_do_jogo
        self.midia_tipo = 'CD' if tipo_midia == '12'  else 'DVD'
        self.parent = parent
        self.tamanho_total = 0
        self.pastadefault = memoria['configuracao']['PADRAO']
        self.painel_imagens_info = wx.Panel(self, wx.ID_ANY)
        self.painel_botoes = wx.Panel(self, wx.ID_ANY)
        self.configuracao_do_jogo = os.path.join(self.pastadefault, 'CFG', '%s.cfg' % (codigo_do_jogo))
        self.tamanho_do_jogo = tamanho_do_jogo
        self.cover_art = lista_cover_art.localiza_cover_art(codigo_do_jogo)
        self.endereco_da_imagem = os.path.join(self.cover_art[0], self.cover_art[1])

        imagemcover = wx.Image(self.endereco_da_imagem, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        new_imagemcover = wx.ImageFromBitmap(imagemcover).Scale(70, 100, wx.IMAGE_QUALITY_NORMAL).ConvertToBitmap()
        mask = wx.Mask(new_imagemcover, wx.BLUE)
        new_imagemcover.SetMask(mask)
        self.botao_imagem = wx.BitmapButton(self, wx.ID_ANY, new_imagemcover, (0, 0), (80, 110))
        self.botao_imagem.SetToolTipString(self.Tradutor.tradutor(u"Clique na imagem para mudá-la"))
        self.Bind(wx.EVT_BUTTON, self.MudarImagem, self.botao_imagem)
        text0 = wx.StaticText(self, wx.ID_ANY, self.Tradutor.tradutor(u"Código:"), (0, 0), (50,20),
                              style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.pj_codigoj = wx.TextCtrl(self, wx.ID_ANY, codigo_do_jogo, (0, 0), style=wx.TE_RICH)
        self.pj_codigoj.Enabled = False
        if self.midia_tipo == 'CD':
            imagemcd = wx.Image(os.path.join(corrente, 'imagens', 'MidiaCD.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            imagem_midia = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY,imagemcd, (0, 0))
        else:
            imagemdvd = wx.Image(os.path.join(corrente, 'imagens', 'MidiaDVD.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            imagem_midia = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY,imagemdvd, (0, 0))
        self.sistema_de_video = ""
        codfatiado = self.codigo_do_jogo[2:4]
        toolcfg = ManipulaCfgJogo(self.configuracao_do_jogo)
        if os.path.exists(self.configuracao_do_jogo):
            ntscoupal = toolcfg.leitor_cfg('Region')
            if ntscoupal == '':
                if codfatiado == 'ES':
                    self.sistema_de_video = 'PAL'
                elif codfatiado == 'US':
                    self.sistema_de_video = 'NTSC'
                else:
                    tool_jogo = VerificaJogo(self.arquivo_do_jogo)
                    self.sistema_de_video = tool_jogo.pega_sistema_de_video()
                toolcfg.mudar_dict_cfg('Region',self.sistema_de_video)
                toolcfg.gravar_em_arquivo()
            else:
                self.sistema_de_video = ntscoupal

            avalicfg = toolcfg.leitor_cfg('Rating')
            if avalicfg == "1" or avalicfg == 1:
                imagemaval1 = wx.Image(os.path.join(corrente, 'imagens', 'aval1.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                self.imagem_avaliacao = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY,imagemaval1, (0, 0))
            elif avalicfg == '2' or avalicfg == 2:
                imagemaval2 = wx.Image(os.path.join(corrente, 'imagens', 'aval2.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                self.imagem_avaliacao = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY,imagemaval2, (0, 0))
            elif avalicfg == '3' or avalicfg ==  3:
                imagemaval3 = wx.Image(os.path.join(corrente, 'imagens', 'aval3.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                self.imagem_avaliacao = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY,imagemaval3, (0, 0))
            elif avalicfg == '4' or avalicfg ==  4:
                imagemaval4 = wx.Image(os.path.join(corrente, 'imagens', 'aval4.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                self.imagem_avaliacao = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY,imagemaval4, (0, 0))
            elif avalicfg == '5' or avalicfg ==  5:
                imagemaval5 = wx.Image(os.path.join(corrente, 'imagens', 'aval5.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                self.imagem_avaliacao = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY,imagemaval5, (0, 0))
            else:
                imagemaval = wx.Image(os.path.join(corrente, 'imagens', 'aval.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                self.imagem_avaliacao = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY,imagemaval, (0, 0))
        else:
            imagemaval = wx.Image(os.path.join(corrente, 'imagens', 'aval.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.imagem_avaliacao = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY,imagemaval, (0, 0))
            with open(self.configuracao_do_jogo, 'w') as tomate:
                textotomate = "Title=%s\nRegion=\nRating=\n" % self.nome_do_jogo
                tomate.write(textotomate)
            if codfatiado == 'ES':
                self.sistema_de_video = 'PAL'
            elif codfatiado == 'US':
                self.sistema_de_video = 'NTSC'
            else:
                tool_jogo = VerificaJogo(self.arquivo_do_jogo)
                self.sistema_de_video = tool_jogo.pega_sistema_de_video()
                toolcfg = ManipulaCfgJogo(self.configuracao_do_jogo)
            toolcfg.mudar_dict_cfg('Region',self.sistema_de_video)
            toolcfg.gravar_em_arquivo()

        if self.sistema_de_video == 'PAL':
            imagempal = wx.Image(os.path.join(corrente, 'imagens', 'PAL.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            imagemsistema = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY, imagempal, (0, 0))
        elif self.sistema_de_video == 'NTSC':
            imagemntsc = wx.Image(os.path.join(corrente, 'imagens', 'NTSC.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            imagemsistema = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY, imagemntsc, (0, 0))
        else:
            imagemduvida = wx.Image(os.path.join(corrente, 'imagens', 'semsv.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            imagemsistema = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY, imagemduvida, (0, 0))

        self.quant_players = toolcfg.leitor_cfg('Players')

        if self.quant_players == 1 or self.quant_players == "1":
            pj_imagemplayers_p1 = wx.Image(os.path.join(corrente, 'imagens', '1P.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.pj_imagemplayers = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY, pj_imagemplayers_p1, (0, 0))
        elif self.quant_players == 2 or self.quant_players == "2":
            pj_imagemplayers_p2 = wx.Image(os.path.join(corrente, 'imagens', '2P.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.pj_imagemplayers = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY, pj_imagemplayers_p2, (0, 0))
        else:
            pj_imagemplayers_naosei = wx.Image(os.path.join(corrente, 'imagens', 'quantosplayers.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.pj_imagemplayers = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY, pj_imagemplayers_naosei, (0, 0))                 

        self.pj_esrb = toolcfg.leitor_cfg('Esrb')
        if not self.pj_esrb == "":
            try:
                self.pj_esrb = int(self.pj_esrb)
            except:
                self.pj_esrb=""

        if self.pj_esrb == '':
            pj_imagem_semesbr = wx.Image(os.path.join(corrente, 'imagens', 'semesrb.png'),
                                         wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.pj_imagem_esrb = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY, pj_imagem_semesbr, (0, 0))           
        elif self.pj_esrb < 10:
            pj_imagem_esrb_menos10 = wx.Image(os.path.join(corrente, 'imagens', 'esrb_livre.png'),
                                              wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.pj_imagem_esrb = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY, pj_imagem_esrb_menos10, (0, 0))              
        elif self.pj_esrb < 13:
            pj_imagem_esrb_menos13 = wx.Image(os.path.join(corrente, 'imagens', 'esrb_10.png'),
                                              wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.pj_imagem_esrb = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY, pj_imagem_esrb_menos13, (0, 0))  
        elif self.pj_esrb < 17:
            pj_imagem_esrb_menos17 = wx.Image(os.path.join(corrente, 'imagens', 'esrb_13.png'),
                                              wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.pj_imagem_esrb = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY, pj_imagem_esrb_menos17, (0, 0))  
        elif self.pj_esrb < 18:
            pj_imagem_esrb_menos18 = wx.Image(os.path.join(corrente, 'imagens', 'esrb_17.png'),
                                              wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.pj_imagem_esrb = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY, pj_imagem_esrb_menos18, (0, 0)) 
        elif self.pj_esrb > 17:
            pj_imagem_esrb_18 = wx.Image(os.path.join(corrente, 'imagens', 'esrb_18.png'),
                                         wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.pj_imagem_esrb = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY, pj_imagem_esrb_18, (0, 0))  
        else:
            pj_imagem_semesbr = wx.Image(os.path.join(corrente, 'imagens', 'semesrb.png'),
                                         wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.pj_imagem_esrb = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY, pj_imagem_semesbr, (0, 0))


        text1 = wx.StaticText(self, wx.ID_ANY, self.Tradutor.tradutor(u"Nome:"), (0, 0),
                              style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.form_nomejogo = wx.TextCtrl(self, wx.ID_ANY, nome_do_jogo, (0, 0), style=wx.TE_RICH)
        self.form_nomejogo.Enabled = False
        text2 = wx.StaticText(self, wx.ID_ANY, self.Tradutor.tradutor("Arquivo:"), (0, 0),
                              style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.form_arq_origem = wx.TextCtrl(self, wx.ID_ANY, self.arquivo_do_jogo, (0, 0), style=wx.TE_RICH)
        ulcfg = False

        self.form_arq_origem.Enabled = False
        if self.arquivo_do_jogo[-6:] == 'ul.cfg':
            pj_imagem_formato_ul = wx.Image(os.path.join(corrente,'imagens', 'UL.png'),
                                            wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            pj_imagem_formato = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY, pj_imagem_formato_ul, (0, 0))
            ulcfg = True
            text2.SetForegroundColour(wx.RED)
            self.form_arq_origem.SetForegroundColour(wx.RED)
            textpartes = wx.StaticText(self, wx.ID_ANY, self.Tradutor.tradutor(u"Partes:"), (0, 0),
                                       style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
            self.formpartes = wx.TextCtrl(self, wx.ID_ANY, partes, (0, 0), style=wx.TE_RICH)
            self.formpartes.Enabled = False
        else:
            pj_imagem_formato_iso = wx.Image(os.path.join(corrente,'imagens', 'ISO.png'),
                                             wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            pj_imagem_formato = wx.StaticBitmap(self.painel_imagens_info, wx.ID_ANY, pj_imagem_formato_iso, (0, 0))

        text3 = wx.StaticText(self, wx.ID_ANY, self.Tradutor.tradutor("Tamanho:"), (0, 0),
                              style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.form_tamanho_arq = wx.TextCtrl(self, wx.ID_ANY, convert_tamanho(self.tamanho_do_jogo), (0, 0), style=wx.TE_RICH)
        self.form_tamanho_arq.Enabled = False
        self.check_selecionado = wx.CheckBox(self.painel_botoes, wx.ID_ANY, self.Tradutor.tradutor("Selecionar"))
        self.check_selecionado.SetToolTipString(self.Tradutor.tradutor(u'Selecionar este jogo'))
        self.Bind(wx.EVT_CHECKBOX, self.Selecionado, self.check_selecionado)
        self.botao_renomear = wx.Button(self.painel_botoes, wx.ID_ANY, self.Tradutor.tradutor('Renomear'), (0, 0))
        self.botao_renomear.SetToolTipString(self.Tradutor.tradutor(u'Renomear nome do jogo'))
        self.Bind(wx.EVT_BUTTON, self.Renomear, self.botao_renomear)
        self.botao_deletar = wx.Button(self.painel_botoes, wx.ID_ANY, self.Tradutor.tradutor('Deletar'), (0, 0))
        self.botao_deletar.SetToolTipString(self.Tradutor.tradutor(u'Deletar jogo'))
        self.Bind(wx.EVT_BUTTON, self.Deletar, self.botao_deletar)
        self.botao_config = wx.Button(self.painel_botoes, wx.ID_ANY, self.Tradutor.tradutor(u'Configuração'), (0, 0))
        self.botao_config.SetToolTipString(self.Tradutor.tradutor(u'Abrir configuração específica do jogo'))
        self.Bind(wx.EVT_BUTTON, self.ConfiguracaoJogo, self.botao_config)
        self.botao_copiar_para = wx.Button(self.painel_botoes, wx.ID_ANY, self.Tradutor.tradutor('Copiar para...'), (0, 0))
        self.botao_copiar_para.SetToolTipString(
            self.Tradutor.tradutor(u'Fazer uma cópia do jogo num dispositivo ou pasta diferente'))
        self.Bind(wx.EVT_BUTTON, self.CopiarPara, self.botao_copiar_para)
        
        linha_horizontal = wx.StaticLine(self, id=wx.ID_ANY, pos=(0, 0), size=(-1, -1),
                                         style=wx.LI_HORIZONTAL | wx.BORDER_DOUBLE)

        self.MeuGridsizer = wx.GridBagSizer(3, 5)
        
        sizer_imagens_info = wx.BoxSizer(wx.HORIZONTAL)
        sizer_imagens_info.Add(imagem_midia, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        sizer_imagens_info.Add(imagemsistema, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        sizer_imagens_info.Add(self.imagem_avaliacao, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        sizer_imagens_info.Add(self.pj_imagemplayers, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        sizer_imagens_info.Add(pj_imagem_formato, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        sizer_imagens_info.Add(self.pj_imagem_esrb, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        self.painel_imagens_info.SetSizerAndFit(sizer_imagens_info)


        sizer_botoes =wx.BoxSizer(wx.HORIZONTAL)
        sizer_botoes.Add(self.check_selecionado, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        sizer_botoes.Add(self.botao_renomear, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        sizer_botoes.Add(self.botao_deletar, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        sizer_botoes.Add(self.botao_config, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        sizer_botoes.Add(self.botao_copiar_para, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        self.painel_botoes.SetSizerAndFit(sizer_botoes)

        self.MeuGridsizer.Add(self.botao_imagem,        (0, 0), (4, 2), wx.ALL | wx.EXPAND, 2)
        self.MeuGridsizer.Add(self.painel_imagens_info, (0, 2), (1, 6), wx.ALL | wx.ALIGN_CENTER , 1)
        self.MeuGridsizer.Add(text0,                    (1, 2), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.MeuGridsizer.Add(self.pj_codigoj,          (1, 3), (1, 1), wx.ALL | wx.EXPAND, 2)

        self.MeuGridsizer.Add(text1,                    (1, 4), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.MeuGridsizer.Add(self.form_nomejogo,       (1, 5), (1, 3), wx.ALL | wx.EXPAND, 2)
        self.MeuGridsizer.Add(text2,                    (2, 2), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.MeuGridsizer.Add(self.form_arq_origem,     (2, 3), (1, 5), wx.ALL | wx.EXPAND, 2)

        self.MeuGridsizer.Add(text3,                    (3, 2), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.MeuGridsizer.Add(self.form_tamanho_arq,    (3, 3), (1, 5 if not ulcfg else 1), wx.ALL | wx.EXPAND, 2)
        if ulcfg:
            self.MeuGridsizer.Add(textpartes,           (3, 4), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
            self.MeuGridsizer.Add(self.formpartes,      (3, 5), (1, 3), wx.ALL | wx.EXPAND, 2)

        self.MeuGridsizer.Add(self.painel_botoes,       (4, 0), (1, 8), wx.ALIGN_CENTER, 0)

        self.MeuGridsizer.Add(linha_horizontal,         (5, 0), (1, 8), wx.ALIGN_CENTER | wx.EXPAND, 0)
        self.MeuGridsizer.AddGrowableCol(6)
        self.SetSizerAndFit(self.MeuGridsizer)
        self.Centre()
        self.Layout()

    def Renomear(self, event):

        self.pastadefault = memoria['configuracao']['PADRAO']
        if self.form_nomejogo.Enabled == False:
            self.form_nomejogo.Enabled = True
            self.botao_renomear.SetLabel("OK")
            self.acao_enderecodojogo = self.form_arq_origem.GetValue()
            self.acao_codigo = self.pj_codigoj.GetValue()
            self.acao_nomedojogoatual = self.form_nomejogo.GetValue()

        elif self.form_nomejogo.Enabled == True:
            if self.acao_nomedojogoatual == self.form_nomejogo.GetValue():
                pass
            elif os.path.basename(self.arquivo_do_jogo) == 'ul.cfg':
                end_base = os.path.dirname(self.acao_enderecodojogo)
                muda_ul = ManipulaUl()
                novo_nome_zx = self.form_nomejogo.GetValue()
                retoronoul = muda_ul.renomear_jogo_ul(end_base, self.acao_nomedojogoatual, novo_nome_zx)
                self.form_nomejogo.Enabled = False
                self.form_nomejogo.SetValue(retoronoul)
                if retoronoul == novo_nome_zx:
                    msgbox = wx.MessageDialog(self,
                                              self.Tradutor.tradutor(u'O nome do arquivo foi alterado com sucesso!'),
                                              self.Tradutor.tradutor('Sucesso!'), wx.OK | wx.ICON_INFORMATION)
                    msgbox.ShowModal()
                    msgbox.Destroy()
                else:
                    msg01 = self.Tradutor.tradutor(
                        u'O nome do arquivo foi alterado, mas como já havia um outro jogo com o mesmo nome, o programa renomeou para')
                    msg02 = u" %s" % (self.form_nomejogo.GetValue())
                    msg = msg01 + msg02
                    msgbox = wx.MessageDialog(self, msg, self.Tradutor.tradutor('Sucesso!'), wx.OK | wx.ICON_INFORMATION)
                    msgbox.ShowModal()
                    msgbox.Destroy()
            else:
                novo_nome_zx = self.form_nomejogo.GetValue()
                resultafinal = muda_nome_jogo(self.acao_enderecodojogo, novo_nome_zx)
                self.form_arq_origem.SetValue(resultafinal[0])
                self.form_nomejogo.SetValue(resultafinal[2])
                self.form_nomejogo.Enabled = False
                if resultafinal[2] == novo_nome_zx:
                    msgbox = wx.MessageDialog(self,
                                              self.Tradutor.tradutor(u'O nome do arquivo foi alterado com sucesso!'),
                                              self.Tradutor.tradutor('Sucesso!'), wx.OK | wx.ICON_INFORMATION)
                    msgbox.ShowModal()
                    msgbox.Destroy()
                else:
                    msg01 = self.Tradutor.tradutor(
                        u'O nome do arquivo foi alterado, mas como já havia um outro jogo com o mesmo nome, o programa renomeou para')
                    msg02 = u" %s" % (self.form_nomejogo.GetValue())
                    msg = msg01 + msg02
                    msgbox = wx.MessageDialog(self, msg, self.Tradutor.tradutor('Sucesso!'), wx.OK | wx.ICON_INFORMATION)
                    msgbox.ShowModal()
                    msgbox.Destroy()
                self.form_arq_origem.SetValue(resultafinal[0])
                self.form_nomejogo.SetValue(resultafinal[2])
                self.form_nomejogo.Enabled = False

            self.form_nomejogo.Enabled = False
            self.botao_renomear.SetLabel("Renomear")

    def Deletar(self, event):

        self.pastadefault = memoria['configuracao']['PADRAO']
        login = FrameLogin(self, title=self.Tradutor.tradutor(u"A ação deve ser autorizada"), nova_senha=False)
        login.CenterOnParent()
        login.ShowModal()
        #login.Destroy()

        self.acao_enderecodojogo = self.form_arq_origem.GetValue()
        if login.autorizado == True:
            memoria['selecionado_para_copiar'][self.Meu_ID] = False
            if self.arquivo_do_jogo[-6:] == 'ul.cfg':
                end_base = os.path.dirname(self.acao_enderecodojogo)
                deleta_ul = ManipulaUl()
                novo_nome_zx = self.form_nomejogo.GetValue()
                deleta_ul.deletar_jogo_ul(end_base, novo_nome_zx)
            else:
                os.remove(self.acao_enderecodojogo)
            self.pj_codigoj.SetValue('')
            self.form_nomejogo.SetValue('')
            self.form_arq_origem.SetValue('')
            self.form_tamanho_arq.SetValue('')

            self.botao_renomear.Enabled = False
            self.botao_deletar.Enabled = False
            self.botao_copiar_para.Enabled = False
            self.botao_config.Enabled = False
            self.check_selecionado.Enabled = False

            self.SetBackgroundColour(wx.RED)

            self.form_nomejogo.SetBackgroundColour(wx.RED)
            self.form_arq_origem.SetBackgroundColour(wx.RED)
            self.form_tamanho_arq.SetBackgroundColour(wx.RED)

            i = wx.Image(os.path.join(corrente, 'imagens', 'deletado.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            isv = wx.ImageFromBitmap(i).Scale(70, 100, wx.IMAGE_QUALITY_NORMAL).ConvertToBitmap()
            self.botao_imagem.SetBitmapDisabled(isv)
            self.botao_imagem.Enabled = False
            self.Refresh()

    def ConfiguracaoJogo(self, event):

        self.pastadefault = memoria['configuracao']['PADRAO']
        nome_do_jogo = self.form_nomejogo.GetValue()
        codigo_do_jogo = self.pj_codigoj.GetValue()
        endereco_config = self.configuracao_do_jogo

        self.obj_config = FrameConfiguracaoJogo(self, wx.ID_ANY, self.Tradutor.tradutor(u'Configuração do Jogo'),
                                             endereco_arquivo_cfg=endereco_config, nome_do_jogo=nome_do_jogo)
        self.obj_config.Show()
        self.obj_config.CenterOnParent()

    def CopiarPara(self, event):

        nome_do_jogo = self.form_nomejogo.GetValue()
        comparador = os.path.basename(self.form_arq_origem.GetValue())
        if comparador == 'ul.cfg':
            tipo = 'ul%s' % (self.midia_tipo)
        else:
            tipo = self.midia_tipo

        self.objcopiar = CopiarPara(self, wx.ID_ANY, self.Tradutor.tradutor('Copiar para...'), self.form_arq_origem.GetValue(),
                                     self.pj_codigoj.GetValue(), nome_do_jogo, tamanho_do_jogo=self.tamanho_do_jogo,
                                     imagem=self.endereco_da_imagem, cfg=self.configuracao_do_jogo, tipo_origem=tipo,
                                     tipo_destino='')
        self.objcopiar.Show()
        self.objcopiar.CenterOnParent()

    def MudarImagem(self, event):

        self.pastadefault = memoria['configuracao']['PADRAO']
        wildcardx = "%s (*.jpg)|*.jpg|%s (*.png)|*.png" % (
                                                            self.Tradutor.tradutor('Imagem jpg'), 
                                                            self.Tradutor.tradutor('Imagem png'))
        dlg = wx.FileDialog(self, self.Tradutor.tradutor(u"Selecionando Imagem..."),
                            os.path.dirname(self.endereco_da_imagem), style=wx.OPEN, wildcard=wildcardx)
        dlg.CenterOnParent()
        if dlg.ShowModal() == wx.ID_OK:
            self.arquivoimg = dlg.GetPath()
            if not self.endereco_da_imagem == self.arquivoimg[0]:
                try:
                    ret_exif = LocalizaArt().retirar_exitf_imagem(self.arquivoimg)
                except IOError:
                    self.arquivoimg = os.path.join(corrente, 'imagens', 'erro.png')
                extencao = self.arquivoimg.split('.')[-1]
                pasta_art = memoria['configuracao']['ART']
                nome_da_imagem = "%s_COV.%s" % (self.codigo_do_jogo, extencao)
                with open(self.arquivoimg, 'rb') as imgdfg:
                    conteudo = imgdfg.read()
                    destinodfg = os.path.join(pasta_art, nome_da_imagem)
                    with open(os.path.join(self.pastadefault, 'ART', destinodfg), 'wb') as binaimagem:
                        binaimagem.write(conteudo)
                leinto_confi = Configuracoes(os.path.join(memoria['arquivo_imagemcheck']))
                leinto_confi.mudar_configuracao(destinodfg, 'OK')
                i = wx.Image(os.path.join(pasta_art, nome_da_imagem), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                isv = wx.ImageFromBitmap(i).Scale(70, 100, wx.IMAGE_QUALITY_NORMAL).ConvertToBitmap()
                self.botao_imagem.SetBitmap(isv)
                self.Refresh()
            dlg.Destroy()

    def Selecionado(self, event):

        valor_do_radio = self.check_selecionado.GetValue()
        atual = memoria['tamanho_total_dos_jogos']
        selecionados = memoria['jogos_selecionados']
        tipo = self.midia_tipo
        coratual = self.parent.GetBackgroundColour()
        if valor_do_radio == True:
            
            self.SetBackgroundColour('#9BCD9B')
            self.form_nomejogo.SetBackgroundColour('#9BCD9B')
            self.form_arq_origem.SetBackgroundColour('#9BCD9B')
            self.form_tamanho_arq.SetBackgroundColour('#9BCD9B')
            self.Refresh()
            origem = self.form_arq_origem.GetValue()
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
                if nome_iiimagem == 'sample.png':
                    iiiimagem[5] = '%s_COV' %self.codigo_do_jogo
                elif nome_iiimagem == 'erro.png':
                    iiiimagem[0] = os.path.join(corrente, 'imagens', 'sample.png')
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
            self.SetBackgroundColour(coratual)
            self.form_nomejogo.SetBackgroundColour(coratual)
            self.form_arq_origem.SetBackgroundColour(coratual)
            self.form_tamanho_arq.SetBackgroundColour(coratual)
            self.Refresh()
            memoria['selecionado_para_copiar'][self.Meu_ID] = False
            atual -= self.tamanho_do_jogo
            selecionados -= 1
        memoria['tamanho_total_dos_jogos'] = atual
        memoria['jogos_selecionados'] = selecionados
        wx.PostEvent(self.parent, event)


class FrameAdicionarMultiplos(wx.Frame):

    def __init__(self, parent, title, lista_de_jogos, total_geral, pos, size):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, pos, size)
        self.conf_prog = Configuracoes(memoria['arquivo_configuracao'])
        self.dicionario = memoria['configuracao']['DICIONARIO']
        self.Tradutor = Dicionario(self.dicionario)
        self.parent = parent
        icone = wx.Icon(os.path.join(corrente, 'imagens', 'icon.ico'), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icone)
        self.listjogos = lista_de_jogos
        self.lista_de_selecionados = []
        self.pastadefault = memoria['configuracao']['PADRAO']
        self.tamanho_vindo_do_filho = 0

        self.painel_principal = wx.Panel(self, wx.ID_ANY)  #Painel Pinricpal

        sizer_panel_titulo = wx.GridBagSizer(0, 0)  #sizers
        sizer_panel = wx.GridBagSizer(0, 100)

        sizer_panel_rodape = wx.GridSizer(cols=1, hgap=0, vgap=0)

        self.painel_cabecalho = wx.Panel(self.painel_principal, wx.ID_ANY, (0, 0), (-1, 25),
                                         style=wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)
        texttitulo = wx.StaticText(self.painel_cabecalho, wx.ID_ANY, self.Tradutor.tradutor(u"Copiando multiplos jogos"),
                              (0, 0), style=wx.TE_RICH | wx.ALIGN_CENTER)

        font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        texttitulo.SetFont(font)
        sizer_panel_titulo.Add(texttitulo, (0, 0), (1, 8), wx.ALL|wx.ALIGN_CENTER|wx.EXPAND, 5)

        sizer_panel_titulo.AddGrowableCol(0)
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
                                        tamanho_do_jogo=x[3], sistema_de_video = x[4],Meu_ID=id_jogos)
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
        self.pastadefault = memoria['configuracao']['PADRAO']
        lista_de_arquivos = []

        for x in memoria['selecionados_multiplos']:
            if memoria['selecionados_multiplos'][x] == False:
                lista_ini=[]
            else:
                lista_ini = memoria['selecionados_multiplos'][x]
            for y in lista_ini:
                lista_de_arquivos.append(y)

        for uis in lista_de_arquivos:
            dest_cfg = os.path.join(self.pastadefault,'CFG')
            cd_cfg = uis[5][:11]
            ap_nome_cfg = uis[5][12:]
            nom_cfg = u"%s.cfg" % (cd_cfg)

            sis_cfg = uis[7]

            if not os.path.exists(os.path.join(dest_cfg, nom_cfg)):
                texto_cfg = "Title=%s\nRegion=%s\n" % (ap_nome_cfg, sis_cfg)
                with open(os.path.join(dest_cfg, nom_cfg),'w') as grav_cfg:
                    grav_cfg.write(texto_cfg.encode('utf-8'))
            else:
                Configuracoes(os.path.join(destino, "CFG", nome_cfg)).mudar_configuracao('Region', sis_cfg)
                Configuracoes(os.path.join(destino, "CFG", nome_cfg)).mudar_configuracao('Title', ap_nome_cfg)
        self.Progress = ProgressCopia(self,
                                        self.Tradutor.tradutor('Copiando arquivos selecionados'), lista_de_arquivos)
        self.Progress.Show()
        self.Progress.CenterOnParent()
        self.Progress.iniciarcopia()
       
        if not self.Progress.cancelado == False:
            deletararquivos(self.Progress.cancelado[0], self.Progress.cancelado[1])
        self.parent.apagar_checks_value()
        wx.PostEvent(self.parent, event)
        self.Destroy()


class PainelListaDeJogos(wx.Panel):

    def __init__(self, parent, ID, pos, size, arquivo_do_jogo, codigo_do_jogo,
                 nome_do_jogo, tamanho_do_jogo, sistema_de_video, Meu_ID):
        wx.Panel.__init__(self, parent, wx.ID_ANY, pos, size, wx.EXPAND)
        self.conf_prog = Configuracoes(memoria['arquivo_configuracao'])
        self.dicionario = memoria['configuracao']['DICIONARIO']
        self.Tradutor = Dicionario(self.dicionario)
        self.Meu_ID = Meu_ID
        self.pastadefault = memoria['configuracao']['PADRAO']
        self.arquivo_do_jogo = arquivo_do_jogo
        self.codigo_do_jogo = codigo_do_jogo[0]
        self.parent = parent
        self.tamanho_total = 0
        self.tamanho_do_jogo = tamanho_do_jogo
        self.tamanho_computado = tamanho_do_jogo
        self.sistema_de_video = sistema_de_video
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
            self.form0.SetToolTipString(self.Tradutor.tradutor(u'Digite um código Válido'))
            self.form0.SetBackgroundColour(wx.RED)

        self.form1 = wx.TextCtrl(self, wx.ID_ANY, nome_do_jogo[0], (0, 0), (250, -1), style=wx.TE_RICH)
        self.Bind(wx.EVT_TEXT, self.MudarCodigoNome, self.form1)
        if not nome_do_jogo[0] == 'NOME_DO_JOGO':
            self.form1.SetToolTipString(self.Tradutor.tradutor(u'Digite um nome para o jogo'))
        if not self.status == 'OK':
            self.form1.SetBackgroundColour(wx.RED)
        codigo_e_nome_encontrado = '%s.%s' %(self.codigo_do_jogo, nome_do_jogo[0])
        self.organizando_dados_para_gravacao = [arquivo_do_jogo[0], tipo_pio, False, self.pastadefault, 0, codigo_e_nome_encontrado, fatiar, self.sistema_de_video]

        self.form2 = wx.TextCtrl(self, wx.ID_ANY, self.arquivo_do_jogo[0], (0, 0),(200,-1), style=wx.TE_RICH)
        self.form2.Enabled = False
        self.form2.SetToolTipString(self.arquivo_do_jogo[0])
        if not self.status == 'OK':
            self.form2.SetBackgroundColour(wx.RED)

        self.form3 = wx.TextCtrl(self, wx.ID_ANY, convert_tamanho(self.tamanho_do_jogo), (0, 0),(120,-1),style=wx.TE_RICH)
        self.form3.Enabled = False
        if not self.status == 'OK':
            self.form3.SetBackgroundColour(wx.RED)
        self.checkpadrao = wx.CheckBox(self, wx.ID_ANY,self.Tradutor.tradutor(u'Formato da cópia'),(0,0),(100,-1), style = wx.ALIGN_CENTER)
        self.checkselecionado = wx.CheckBox(self, wx.ID_ANY,self.Tradutor.tradutor('Selecionado'),(0,0),(100,-1), style = wx.ALIGN_CENTER)

        if fatiar == True:
           self.checkpadrao.SetValue(True)
        self.checkpadrao.SetToolTipString(self.Tradutor.tradutor(u'O ISO será convertivo para o formato UL se ativado, caso contrário, será no formato ISO'))

        if self.status == "OK":
            self.checkselecionado.SetValue(True)
            self.checkselecionado.SetToolTipString(self.Tradutor.tradutor(u'O jogo passou, desmarque se quer desistir de copiar'))
        else:
            self.checkselecionado.SetValue(False)
            self.checkselecionado.SetToolTipString(self.Tradutor.tradutor(u'Marque se tiver certeza que é um jogo válido'))

        self.Bind(wx.EVT_CHECKBOX, self.Selecionado, self.checkpadrao)
        self.Bind(wx.EVT_CHECKBOX, self.Selecionado, self.checkselecionado)

        self.form4 = wx.TextCtrl(self, wx.ID_ANY, self.status, (0, 0), (50, -1), style=wx.TE_RICH)
        self.form4.Enabled = False
        linha = wx.StaticLine(self, id=wx.ID_ANY, pos=(0, 0), size=(-1, -1),
                              style=wx.LI_HORIZONTAL | wx.BORDER_DOUBLE)

        self.MeuGridsizer = wx.GridBagSizer(0, 5)
        if self.Meu_ID == 1:
            pldj_texto_codigo= wx.StaticText(self, wx.ID_ANY, self.Tradutor.tradutor(u"Código"), (0, 0), (85, -1), style = wx.TE_RICH | wx.ALIGN_CENTER)
            pldj_texto_nome= wx.StaticText(self, wx.ID_ANY, self.Tradutor.tradutor(u"Nome"), (0, 0), (250,-1), style = wx.TE_RICH | wx.ALIGN_CENTER)
            pldj_texto_arquivo= wx.StaticText(self, wx.ID_ANY, self.Tradutor.tradutor("Arquivo"), (0, 0),(200,-1), style = wx.TE_RICH | wx.ALIGN_CENTER)
            pldj_texto_tamanho= wx.StaticText(self, wx.ID_ANY, self.Tradutor.tradutor("Tamanho"), (0, 0), (120,-1), style = wx.TE_RICH | wx.ALIGN_CENTER)
            pldj_texto_status= wx.StaticText(self, wx.ID_ANY, self.Tradutor.tradutor("Status"), (0, 0),(50,-1), style = wx.TE_RICH | wx.ALIGN_CENTER)
            self.MeuGridsizer.Add(pldj_texto_codigo,    (0,                                 0), (1, 1), wx.ALL | wx.EXPAND, 0)

        self.MeuGridsizer.Add(linha,                    (0 if not self.Meu_ID == 1 else 1, 0), (1, 8), wx.ALL | wx.EXPAND, 5)
        self.MeuGridsizer.Add(self.form0,               (1 if not self.Meu_ID == 1 else 2,  0), (1, 1), wx.ALL | wx.EXPAND, 0)
        if self.Meu_ID == 1:
            self.MeuGridsizer.Add(pldj_texto_nome,      (0, 1), (1, 1), wx.ALL | wx.EXPAND, 0)        
        self.MeuGridsizer.Add(self.form1,               (1 if not self.Meu_ID == 1 else 2,  1), (1, 1), wx.ALL | wx.EXPAND, 0)
        if self.Meu_ID == 1:
            self.MeuGridsizer.Add(pldj_texto_arquivo,   (0, 2), (1, 2), wx.ALL | wx.EXPAND, 0)        
        self.MeuGridsizer.Add(self.form2,               (1 if not self.Meu_ID == 1 else 2,  2), (1, 2), wx.ALL | wx.EXPAND, 0)
        if self.Meu_ID == 1:
            self.MeuGridsizer.Add(pldj_texto_tamanho,   (0, 4), (1, 1), wx.ALL | wx.EXPAND, 0)        
        self.MeuGridsizer.Add(self.form3,               (1 if not self.Meu_ID == 1 else 2,  4), (1, 1), wx.ALL | wx.EXPAND, 0)
        if self.Meu_ID == 1:
            self.MeuGridsizer.Add(pldj_texto_status,    (0, 5), (1, 1), wx.ALL | wx.EXPAND, 0)        
        self.MeuGridsizer.Add(self.form4,               (1 if not self.Meu_ID == 1 else 2,  5), (1, 1), wx.ALL | wx.EXPAND, 0)
        
        self.MeuGridsizer.Add(self.checkpadrao,         (1 if not self.Meu_ID == 1 else 2,  6), (1, 1), wx.ALL | wx.EXPAND|  wx.ALIGN_CENTER, 5)
        self.MeuGridsizer.Add(self.checkselecionado,    (1 if not self.Meu_ID == 1 else 2,  7), (1, 1), wx.ALL | wx.EXPAND|  wx.ALIGN_CENTER, 5)
        
        self.MeuGridsizer.AddGrowableCol(3)

        self.SetSizerAndFit(self.MeuGridsizer)
        if checkselecionado.GetValue() == True:
            memoria['selecionados_multiplos'][self.Meu_ID] = [self.organizando_dados_para_gravacao]
        else:
            memoria['selecionados_multiplos'][self.Meu_ID] = False
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

    def __init__(self, title):
        wx.Frame.__init__(self, None, wx.ID_ANY, title, (-1, -1), (400, 600),
                          style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.conf_prog = Configuracoes(memoria['arquivo_configuracao'])
        self.dicionario = memoria['configuracao']['DICIONARIO']
        self.Tradutor = Dicionario(self.dicionario)
        icone = wx.Icon(os.path.join(corrente, 'imagens', 'icon.ico'), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icone)
        painel_principal = wx.Panel(self, wx.ID_ANY)
        logo = wx.Image(os.path.join(corrente, 'imagens', 'conexaodidata.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        logocolocado = wx.StaticBitmap(painel_principal, wx.ID_ANY, logo, (0,0))
        

        if self.dicionario == "":

            self.codigo_html = u'''
            <html>
            <body bgcolor="#C7C7C7">
            <center><table bgcolor="#AAAAAA"  width="100%" cellspacing="0"
            cellpadding="0" border="1">
            <tr>
            <td align="center"><h2>PhanterPS2</h2></br><h5>versão 1.1</h5></td>
            </tr>
            </table>
            <br>
            <br>
            <b>acesse: http://www.conexaodidata.com.br/phanterps2</b>
            <br>
            </center>
            <p>O <b>PhanterPS2</b> foi desenvolvido por <b>PhanterJR</b>, sócio-proprietário da Conexão Didata.
            </p>
            <p>PhanterPS2: Copyright &copy; 2014 PhanterJR - Licença GPL2<br>
            https://github.com/PhanterJR/PhanterPS2</p>
            

            <p align="center"><b>CONTRIBUIÇÃO</b></p>
            <hr>
            <p><b>Junior Polegato</b><br>
            Módulo pycrc32<br>
            Copyright &copy; 2014 Junior Polegato<br>
            Licença LGPL<br>
            https://github.com/JuniorPolegato</p>
            <hr>
            <p><b>Barnaby Gale</b><br>
            Módulo iso9660<br>
            Copyright &copy; 2013-2014 Barnaby Gale<br>
            Licença BSD<br>
            https://github.com/barneygale
            </p>
            <hr>
            <p>
            <b>Python Software Foundation; All Rights Reserved</b><br>
            Linguagem Python2.7<br>
            Copyright &copy; 2001-2014 Python Software Foundation<br>
            Licença OSI<br>
            http://www.python.org
            </p>
            <hr>
            <p>
            <b>wxPython</b><br>
            wxWindows Library Licence, Versão 3.1<br>
            Copyright &copy; 1998-2005 Julian Smart, Robert Roebling et al<br>
            Licença LGPL<br>
            http://www.wxpython.org
            </p>        
            <hr>
            <p>
            <b>Pillow (PIL)</b><br>
            The Python Imaging Library (PIL)<br>
            Copyright © 1997-2011 by Secret Labs AB<br>
            Copyright © 1995-2011 by Fredrik Lundh<br>
            Licença LGPL<br>
            https://github.com/python-pillow
            </p>
            <hr>
            <p>
            <b>ExifRead</b><br>
            Modulo ExifRead<br>
            Copyright (c) 2002-2007 Gene Cash<br>
            Copyright (c) 2007-2013 Ianaré Sévi and contributors<br>
            Licença BSD<br>
            https://github.com/ianare/exif-py
            </p>
            </body>
            </html>'''
        else:
            self.codigo_html = u'''
            <html>
            <body bgcolor="#C7C7C7">
            <center><table bgcolor="#AAAAAA"  width="100%" cellspacing="0"
            cellpadding="0" border="1">
            <tr>
            <td align="center"><h2>PhanterPS2</h2></br><h5>version 1.1</h5></td>
            </tr>
            </table>
            <br>
            <br>
            <b>visit: http://www.conexaodidata.com.br/phanterps2</b>
            <br>
            </center>
            <p>The <b>PhanterPS2</b> was developed by <b>PhanterJR</b>, co-owner of Conexão Didata.
            </p>
            <p>PhanterPS2: Copyright &copy; 2014 PhanterJR - License GPL2<br>
            https://github.com/PhanterJR/PhanterPS2</p>
            

            <p align="center"><b>CONTRIBUTION</b></p>
            <hr>
            <p><b>Junior Polegato</b><br>
            Module pycrc32<br>
            Copyright &copy; 2014 Junior Polegato<br>
            License LGPL<br>
            https://github.com/JuniorPolegato</p>
            <hr>
            <p><b>Barnaby Gale</b><br>
            Module iso9660<br>
            Copyright &copy; 2013-2014 Barnaby Gale<br>
            License BSD<br>
            https://github.com/barneygale
            </p>
            <hr>
            <p>
            <b>Python Software Foundation; All Rights Reserved</b><br>
            Language Python2.7<br>
            Copyright &copy; 2001-2014 Python Software Foundation<br>
            License OSI<br>
            http://www.python.org
            </p>
            <hr>
            <p>
            <b>wxPython</b><br>
            wxWindows Library Licence, version 3.1<br>
            Copyright &copy; 1998-2005 Julian Smart, Robert Roebling et al<br>
            License LGPL<br>
            http://www.wxpython.org
            </p>        
            <hr>
            <p>
            <b>Pillow (PIL)</b><br>
            The Python Imaging Library (PIL)<br>
            Copyright © 1997-2011 by Secret Labs AB<br>
            Copyright © 1995-2011 by Fredrik Lundh<br>
            License LGPL<br>
            https://github.com/python-pillow
            </p>
            <hr>
            <p>
            <b>ExifRead</b><br>
            Module ExifRead<br>
            Copyright (c) 2002-2007 Gene Cash<br>
            Copyright (c) 2007-2013 Ianaré Sévi and contributors<br>
            License BSD<br>
            https://github.com/ianare/exif-py
            </p>  
            </body>
            </html>'''


        self.html = wx.html.HtmlWindow(painel_principal, style = wx.BORDER_DOUBLE)
        self.html.SetPage(self.codigo_html)
        button1 = wx.Button(painel_principal, wx.ID_OK, "OK")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(logocolocado, 0, wx.ALL| wx.ALIGN_CENTER, 10)
        sizer.Add(self.html, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(button1, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        painel_principal.SetSizer(sizer)

        self.Layout()
        self.Bind(wx.EVT_BUTTON, self.destruir, button1)
        self.CenterOnScreen()  # coloca no centro da tela

    def destruir(self, event):
        self.Destroy()


class FrameConfiguracao(wx.Frame):

    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.conf_prog = Configuracoes(memoria['arquivo_configuracao'])
        self.dicionario = memoria['configuracao']['DICIONARIO']
        if not os.path.exists(self.dicionario):
            self.dicionario=""
        self.dicqueestava = self.dicionario
        self.Tradutor = Dicionario(self.dicionario)
        self.parent = parent
        icone = wx.Icon(os.path.join(corrente, 'imagens', 'icon.ico'), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icone)
        painel = wx.Panel(self, wx.ID_ANY, (0, 0), (400, 300))
        config_pasta_jogos = memoria['configuracao']['PADRAO']
        self.estado = config_pasta_jogos

        text0 = wx.StaticText(painel, wx.ID_ANY,
                              self.Tradutor.tradutor(u"Pasta de jogos"), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)

        self.form0 = wx.TextCtrl(painel, wx.ID_ANY, config_pasta_jogos, (0, 0), (250, -1))
        self.form0.Enabled = False
        botao0 = wx.Button(painel, wx.ID_ANY, '...', (0, 0), (20, 20))
        botao0.SetToolTipString(self.Tradutor.tradutor(u'Selecione uma pasta padrão para ser armazenado os jogos de PS2'))
        self.Bind(wx.EVT_BUTTON, self.PegaPastaJogo, botao0)
        text1 = wx.StaticText(painel, wx.ID_ANY,
                              self.Tradutor.tradutor(u"Arquivos de Tradução"), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)
        self.form1 = wx.TextCtrl(painel, wx.ID_ANY, self.dicionario, (0, 0), (250, -1))
        self.form1.SetValue(self.dicionario)
        if not self.form1.GetValue() == '':
            self.form1.Enabled = True
        else:
            self.form1.Enabled = False
        botao1 = wx.Button(painel, wx.ID_ANY, '...', (0, 0), (20, 20))
        botao1.SetToolTipString(self.Tradutor.tradutor(u'Escolha um arquivo de tradução, para Português Brasil deixe vazio'))
        self.Bind(wx.EVT_BUTTON, self.PegaArquivoTradu, botao1)
        linha_horizontal = wx.StaticLine(painel, id=wx.ID_ANY, pos=(0, 0), size=(-1, -1),
                                         style=wx.LI_HORIZONTAL | wx.BORDER_DOUBLE, name='wx.StaticLineNameStr')
        text2 = wx.StaticText(painel, wx.ID_ANY,
                              self.Tradutor.tradutor(u"Pasta de DVD"), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)

        self.form2 = wx.TextCtrl(painel, wx.ID_ANY, os.path.join(config_pasta_jogos, 'DVD'), (0, 0), (250, -1))
        self.form2.Enabled = False
        text3 = wx.StaticText(painel, wx.ID_ANY,
                              self.Tradutor.tradutor(u"Pasta de CD"), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)
        self.form3 = wx.TextCtrl(painel, wx.ID_ANY, os.path.join(config_pasta_jogos, 'CD'), (0, 0), (250, -1))
        self.form3.Enabled = False
        text4 = wx.StaticText(painel, wx.ID_ANY,
                              self.Tradutor.tradutor(u"Pasta de capas"), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)
        self.form4 = wx.TextCtrl(painel, wx.ID_ANY, os.path.join(config_pasta_jogos, 'ART'), (0, 0), (250, -1))
        self.form4.Enabled = False
        text5 = wx.StaticText(painel, wx.ID_ANY,
                              self.Tradutor.tradutor(u"Pasta de configurações"), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)
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
        past_oui = memoria['configuracao']['PADRAO']
        dlg = wx.DirDialog(self, self.Tradutor.tradutor(u"Selecionando pasta de jogos..."), past_oui, style=wx.OPEN)
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

        self.wildcard2 = u"%s (*.lng)|*.lng" % (self.Tradutor.tradutor(u'Arquivo de Tradução'))
        dlg2 = wx.FileDialog(self, self.Tradutor.tradutor(u'Selecionando arquivo de tradução'), memoria['end_linguagem'], style=wx.OPEN,
                             wildcard=self.wildcard2)
        dlg2.CenterOnParent()
        if dlg2.ShowModal() == wx.ID_OK:
            valor_dialog = dlg2.GetPath()
            self.form1.Enabled = True
            self.form1.SetValue(valor_dialog)

    def Confirmar(self, event):
        self.muda_conf = Configuracoes(memoria['arquivo_configuracao'])
        confg1 = self.form0.GetValue()
        confg2 = self.form1.GetValue()
        self.muda_conf.mudar_configuracao('PADRAO', confg1)
        self.muda_conf.mudar_configuracao('DICIONARIO', confg2)
        self.DVD = self.form2.GetValue()
        self.CD = self.form3.GetValue()
        self.ART = self.form4.GetValue()
        self.CFG = self.form5.GetValue()
        memoria['configuracao'] = Configuracoes(memoria['arquivo_configuracao']).config

        lista_de_diretorios = [['DVD', self.DVD], ['CD', self.CD], ['ART', self.ART],
                               ['CFG', self.CFG]]
        for dirs in lista_de_diretorios:
            try:
                os.makedirs(dirs[1])
                self.muda_conf.mudar_configuracao(dirs[0], dirs[1])
            except:
                if os.path.exists(dirs[1]):
                    self.muda_conf.mudar_configuracao(dirs[0], dirs[1])
        memoria['configuracao'] = Configuracoes(memoria['arquivo_configuracao']).config
        if not self.dicqueestava == confg2:
            msg = wx.MessageDialog(self, u"The language file has changed, close and reopen PhanterPS2 to take effect", 'Information', wx.OK | wx.ICON_INFORMATION)
            msg.ShowModal()
        if not confg1 == self.estado:
            self.parent.apagar_checks_value()
            
            vlista_cover_ART = LocalizaArt(memoria['configuracao']['ART'])
            vlista_cover_ART.retirar_exitf_imagem(vlista_cover_ART.lista_conver)
            leinto_confi = Configuracoes(memoria['arquivo_imagemcheck'])
            for asjko in vlista_cover_ART.lista_conver:
                if not leinto_confi.leitor_configuracao(asjko) == 'OK':
                    leinto_confi.mudar_configuracao(asjko, 'OK')
            wx.PostEvent(self.parent, event)

        self.Destroy()


class FrameAdicionarIso(wx.Frame):

    def __init__(self, parent, ID, title, endereco=('', False), codigo_do_jogo=(False, False),
                 nome_do_jogo=('NOVO_JOGO', True), tamanho_do_jogo=0, sistema_de_video = '', lista_de_jogos=[]):
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.conf_prog = Configuracoes(memoria['arquivo_configuracao'])
        self.dicionario = memoria['configuracao']['DICIONARIO']
        self.Tradutor = Dicionario(self.dicionario)
        self.config_pasta_jogos = memoria['configuracao']['PADRAO']
        texto_adicional = '\n\n%s' % self.Tradutor.tradutor(u'OBSERVAÇÃO: Caso coloque um nome já usado o programa se encarregará de por um nome válido, Ex.:XXX_000.00.NOME_DO_ARQUIVO - 01')
        for procus in lista_de_jogos:
            if procus[1] == codigo_do_jogo[0]:
                texto_adicional = self.Tradutor.tradutor(u"Já existe um arquivo com esse mesmo código e nome, se continuar o programa irá adicionar números sequenciais afim de que evite que o arquivo existente seja sobrescrito. Ex.: XXX_000.00.NOME - 01")

        icone = wx.Icon(os.path.join(corrente, 'imagens', 'icon.ico'), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icone)
        self.parent = parent
        self.sistema_de_video = sistema_de_video

        self.endereco_do_jogo = endereco[0]
        self.codigo_do_jogo = codigo_do_jogo
        self.nome_do_jogo = nome_do_jogo[0]
        self.tamanho_do_jogo = convert_tamanho(tamanho_do_jogo)

        self.midia_origem = ['CD', 'DVD']
        self.padrao_destino = ['ISO', 'ul.cfg']

        if self.codigo_do_jogo[0] == False and self.codigo_do_jogo[1] == False:
            texto_info = self.Tradutor.tradutor(u"ATENÇÃO: O arquivo ISO selecionado não passou na checagem. Ao abrir o arquivo não foi encontrado o arquivo código característicos dos jogos de PS2. Isso pode ocorrer em jogos que possui alguma proteção.")
        elif not self.codigo_do_jogo[0] == False and self.codigo_do_jogo[1] == False:
            part_txt1 = self.Tradutor.tradutor(u"O arquivo ISO selecionado não passou no teste, ")
            part_txt2 = self.Tradutor.tradutor(u"Ao abrir o arquivo não foi encontrado o arquivo código característicos dos jogos de PS2. Porém no nome do ISO selecionado apresenta um código válido.")
            texto_info =  "%s %s" %(part_txt1, part_txt2)
            
        elif self.codigo_do_jogo[0] == False and self.codigo_do_jogo[1] == True:
            texto_info = self.Tradutor.tradutor(u"O arquivo ISO passou no teste. O código sugerido acima foi encontrado em seu interior.")
        else:
            texto_info = self.Tradutor.tradutor(u"A checagem do arquivo ISO ocorreu sem problemas. O código sugerido acima foi encontrado em seu interior.")
        texto_info += texto_adicional

        painel = wx.Panel(self, wx.ID_ANY, (0, 0), (400, 300))
        text0 = wx.StaticText(painel, wx.ID_ANY,
                              self.Tradutor.tradutor(u"Código do jogo"), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)
        self.form0 = wx.TextCtrl(painel, wx.ID_ANY,
                                 self.codigo_do_jogo[0] if not self.codigo_do_jogo[0] == False else '', (0, 0),
                                 (250, -1))
        self.form0.SetToolTipString(
            self.Tradutor.tradutor(u'Código do jogo, em caso de falha, coloque o código manualmente'))
        text1 = wx.StaticText(painel, wx.ID_ANY,
                              self.Tradutor.tradutor(u"Nome do jogo"), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)
        self.form1 = wx.TextCtrl(painel, wx.ID_ANY, self.nome_do_jogo, (0, 0), (250, -1))
        self.form1.SetToolTipString(self.Tradutor.tradutor(u'Adicionar nome do jogo'))
        text2 = wx.StaticText(painel, wx.ID_ANY,
                              self.Tradutor.tradutor(u"Tamanho do jogo"), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)
        self.form2 = wx.TextCtrl(painel, wx.ID_ANY, self.tamanho_do_jogo, (0, 0), (250, -1))
        self.form2.Enabled = False
        self.radius1 = wx.RadioBox(painel, wx.ID_ANY, self.Tradutor.tradutor(u"Mídia"), wx.DefaultPosition,
                                   wx.DefaultSize,
                                   self.midia_origem, 2, wx.RA_SPECIFY_ROWS)
        self.radius1.SetToolTipString(self.Tradutor.tradutor(u'Mídia detectada por tamanho, caso deseje escolha outro'))
        self.radius2 = wx.RadioBox(painel, wx.ID_ANY, self.Tradutor.tradutor(u'Formato'), wx.DefaultPosition,
                                   wx.DefaultSize,
                                   self.padrao_destino, 2, wx.RA_SPECIFY_ROWS)
        self.radius2.SetToolTipString(self.Tradutor.tradutor(u'UL divide em partes, ISO copia inteiro'))

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
        botaocancelar = wx.Button(painel, wx.ID_CANCEL, self.Tradutor.tradutor('CANCELAR'), (0, 0))
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
        valor_midia = self.radius1.GetSelection()
        valor_padrao = self.radius2.GetSelection()
        midia_temp = self.midia_origem[valor_midia]
        tipo = midia_temp
        checado = False
        destino = self.config_pasta_jogos
        tamanho = 0
        codigo = self.form0.GetValue()
        so_o_nome = self.form1.GetValue()
        nome = u"%s.%s" % (codigo, so_o_nome)
        nome_cfg = u"%s.cfg" % (codigo)
        if not os.path.exists(os.path.join(destino, "CFG", nome_cfg)):
            texto_cfg = "Title=%s\nRegion=%s\n" % (so_o_nome, self.sistema_de_video)
            with open(os.path.join(destino, "CFG", nome_cfg),'w') as grav_cfg:
                grav_cfg.write(texto_cfg.encode('utf-8'))
        else:
            Configuracoes(os.path.join(destino, "CFG", nome_cfg)).mudar_configuracao('Region', self.sistema_de_video)
            Configuracoes(os.path.join(destino, "CFG", nome_cfg)).mudar_configuracao('Title', so_o_nome)
        fatiar = True if valor_padrao == 1 else False

        mensagem = self.Tradutor.tradutor('Copiando')

        self.Progress = ProgressCopia(self, u'%s %s' % (mensagem, self.form1.GetValue()),
                                       [[origem, tipo, checado, destino, tamanho, nome, fatiar]],
                                       cancelar_ativo=True)
        self.Progress.Show()
        self.Progress.CenterOnParent()
        self.Progress.iniciarcopia()
        if not self.Progress.cancelado == False:
            deletararquivos(self.Progress.cancelado[0], self.Progress.cancelado[1])
        self.Destroy()
        self.parent.apagar_checks_value()
        wx.PostEvent(self.parent, event)


    def Cancelar(self, event):
        self.Destroy()


class CopiarPara(wx.Frame):

    def __init__(self, parent, ID, title, endereco_do_jogo, codigo_do_jogo, nome_do_jogo, tamanho_do_jogo=0,
                 imagem=False, cfg=False, tipo_origem='', tipo_destino=''):
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        icone = wx.Icon(os.path.join(corrente, 'imagens', 'icon.ico'), wx.BITMAP_TYPE_ICO)
        self.conf_prog = Configuracoes(memoria['arquivo_configuracao'])
        self.dicionario = memoria['configuracao']['DICIONARIO']
        self.Tradutor = Dicionario(self.dicionario)
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
                              self.Tradutor.tradutor(u"Destino"), (0, 0), style= wx.ALIGN_CENTER_VERTICAL)
        self.form0 = wx.TextCtrl(painel, wx.ID_ANY, '', (0, 0), (250, -1))
        self.form0.Enabled = False
        botao0 = wx.Button(painel, wx.ID_ANY, '...', (0, 0), (20, 20))
        botao0.SetToolTipString(self.Tradutor.tradutor(u'Escolha um drive ou pasta destino para o jogo'))
        self.Bind(wx.EVT_BUTTON, self.PegaPastaDestino, botao0)
        if tipo_origem == 'ul.cfg':
            texto1 = self.Tradutor.tradutor(u'Copiar no formato UL')
            texto2 = self.Tradutor.tradutor(u'Converter para o formato ISO')
        else:
            texto1 = self.Tradutor.tradutor(u'Converter para o formato UL')
            texto2 = self.Tradutor.tradutor(u'Copiar no formato ISO')
        self.midia = [texto1, texto2]

        self.radius1 = wx.RadioBox(painel, wx.ID_ANY, self.Tradutor.tradutor(u"Formato da cópia"), wx.DefaultPosition,
                                   wx.DefaultSize,
                                   self.midia, 2, wx.RA_SPECIFY_ROWS | wx.ALIGN_CENTER)
        self.check1 = wx.CheckBox(painel, wx.ID_ANY, self.Tradutor.tradutor("Copiar imagem de capa"))
        self.check2 = wx.CheckBox(painel, wx.ID_ANY, self.Tradutor.tradutor("Copiar arquivo cfg"))
        self.check3 = wx.CheckBox(painel, wx.ID_ANY, self.Tradutor.tradutor("Criar genericVMC vazio"))

        self.botaook = wx.Button(painel, wx.ID_OK, 'OK', (0, 0))
        self.botaook.Enabled = False
        self.Bind(wx.EVT_BUTTON, self.Confirmar, self.botaook)

        sizer = wx.GridBagSizer(0, 10)
        sizer2 = wx.GridBagSizer(0, 0)

        sizer.Add(text0, (1, 1), (1, 1), wx.ALIGN_RIGHT, 2)
        sizer.Add(self.form0, (1, 2), (1, 2), wx.ALL | wx.EXPAND, 2)
        sizer.Add(botao0, (1, 4), (1, 4), wx.ALL, 2)
        sizer.Add(self.radius1, (3, 1), (4, 2), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check1, (3, 3), (1, 2), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check2, (4, 3), (1, 2), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check3, (5, 3), (1, 2), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 2)
        sizer.Add(self.botaook, (8, 1), (2, 5), wx.ALL | wx.ALIGN_CENTER, 10)

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

        dlg = wx.DirDialog(self, self.Tradutor.tradutor(u"Selecionando pasta destino..."), corrente, style=wx.OPEN)
        dlg.CenterOnParent()
        if dlg.ShowModal() == wx.ID_OK:
            self.valor_dialog = dlg.GetPath()
            self.form0.SetValue(self.valor_dialog)
            self.check3.Enabled = True
            self.check3.SetToolTipString(self.Tradutor.tradutor(u'Adicionar um Virtual Memory Card vazio ao destino'))

            self.botaook.Enabled = True
            self.radius1.Enabled = True
            self.radius1.SetToolTipString(self.Tradutor.tradutor(u'UL divide em partes, ISO copia inteiro'))
            if not self.imagem == False:
                origem_imagem = self.imagem
                nome_imagemzd = False
                self.check1.Enabled = True
                self.check1.SetToolTipString(
                    self.Tradutor.tradutor(u'Uma imagem foi localizada, se marcado será adicionada'))
                self.check1.SetValue(True)
                if not eh_cover_art(self.imagem):
                    self.check1.SetToolTipString(
                        self.Tradutor.tradutor(u'Não foi localizado imagem, se marcado será adicionado a imagem padrão'))
                    self.check1.SetValue(False)
                    nome_imagemzd = "%s_COV" % self.codigo_do_jogo
                    origem_imagem = os.path.join(corrente, 'imagens', 'sample.png')

                self.copiar_imagemzd = [origem_imagem, 'ART', False, self.form0.GetValue(), 0, nome_imagemzd, False]
            if not self.cfg == False:
                self.check2.Enabled = True
                self.check2.SetToolTipString(
                    self.Tradutor.tradutor(u'Uma arquivo cfg foi localizado, se marcado será adicionado'))
                self.check2.SetValue(True)

                self.copiar_cfgzd = [self.cfg, 'CFG', False, self.form0.GetValue(), 0, False, False]


    def Confirmar(self, event):
        if self.form0.GetValue() == '':
            msgbox = wx.MessageDialog(self,
                                      self.Tradutor.tradutor(u'Escolhar um dispositivo ou pasta como destino da cópia.'),
                                      self.Tradutor.tradutor(u'Atenção'), wx.OK | wx.ICON_INFORMATION)
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
            mensagem = self.Tradutor.tradutor('Copiando')
            self.Progress = ProgressCopia(self, u'%s %s' % (mensagem, nome),
                                           self.lista_a_ser_copiada, cancelar_ativo=True)
            self.Progress.Show()
            self.Progress.CenterOnParent()
            self.Progress.iniciarcopia()
            if not self.Progress.cancelado == False:
                deletararquivos(self.Progress.cancelado[0], self.Progress.cancelado[1])
            self.Destroy()


class FrameConfiguracaoJogo(wx.Frame):
    def __init__(self, parent, ID, title, endereco_arquivo_cfg, nome_do_jogo):
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.parent = parent
        self.conf_prog = Configuracoes(memoria['arquivo_configuracao'])
        self.dicionario = memoria['configuracao']['DICIONARIO']
        self.Tradutor = Dicionario(self.dicionario)
        icone = wx.Icon(os.path.join(corrente, 'imagens', 'icon.ico'), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icone)
        self.endereco_arquivo_cfg = endereco_arquivo_cfg
        self.nome_do_jogo = nome_do_jogo
        self.fco_painel_principal = wx.Panel(self, wx.ID_ANY)
        self.manipula_cfg_jogo = ManipulaCfgJogo(endereco_arquivo_cfg)

        self.info_Nome_do_jogo = self.manipula_cfg_jogo.leitor_cfg('Title')
        self.info_sistema_de_video = self.manipula_cfg_jogo.leitor_cfg('Region')
        self.info_stilo_do_jogo = self.manipula_cfg_jogo.leitor_cfg('Genre')
        self.info_testado_em = self.manipula_cfg_jogo.leitor_cfg('Compatibility')

        self.info_descricao = self.manipula_cfg_jogo.leitor_cfg('Description')
        self.info_numero_jogadores = self.manipula_cfg_jogo.leitor_cfg('Players')

        self.info_avaliacao = self.manipula_cfg_jogo.leitor_cfg('Rating')
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

        self.painel = wx.Panel(self.fco_painel_principal, wx.ID_ANY, (0, 0), (-1, -1))

        self.text0 = wx.StaticText(self.painel, wx.ID_ANY, self.Tradutor.tradutor(u"Informações do jogo"), (0, 0),
                                   style=wx.TE_RICH)
        font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.text0.SetFont(font)

        self.text1 = wx.StaticText(self.painel, wx.ID_ANY,
                                   self.Tradutor.tradutor(u"Nome do jogo"), (0, 0),
                                   style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.form1 = wx.TextCtrl(self.painel, wx.ID_ANY, self.nome_do_jogo, (0, 0), (200, -1), style=wx.TE_RICH)
        self.form1.Enabled = False
        self.text2 = wx.StaticText(self.painel, wx.ID_ANY, self.Tradutor.tradutor(u"Descrição"), (0, 0),
                                   style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.form2 = wx.TextCtrl(self.painel, wx.ID_ANY, self.info_descricao, (0, 0), (200, 50),
                                 style=wx.TE_RICH| wx.TE_MULTILINE)

        self.form2.Enabled = True
        self.text3 = wx.StaticText(self.painel, wx.ID_ANY, self.Tradutor.tradutor(u"Sistema de imagem"), (0, 0),
                                   style=wx.TE_RICH)
        self.form3 = wx.TextCtrl(self.painel, wx.ID_ANY, self.info_sistema_de_video, (0, 0), (150, -1), style=wx.TE_RICH)
        self.form3.Enabled = False
        self.textgenero = wx.StaticText(self.painel, wx.ID_ANY,
                                        self.Tradutor.tradutor(u"Gênero"), (0, 0),
                                        style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.formgenero = wx.TextCtrl(self.painel, wx.ID_ANY, self.info_stilo_do_jogo, (0, 0), (150, -1), style=wx.TE_RICH)
        self.formgenero.Enabled = True
        self.formgenero.SetToolTipString(self.Tradutor.tradutor(u'Ex. Corrida, Luta, Aventura, FPS, etc.'))
        self.text4 = wx.StaticText(self.painel, wx.ID_ANY, self.Tradutor.tradutor(u"Numero de jogadores"), (0, 0),
                                   style=wx.TE_RICH)
        self.form4 = wx.TextCtrl(self.painel, wx.ID_ANY, self.info_numero_jogadores, (0, 0), (50, -1), style=wx.TE_RICH)
        self.form4.Enabled = True
        self.form4.SetToolTipString(self.Tradutor.tradutor(u'Quantidade de jogadores máximos no jogo'))
        self.text5 = wx.StaticText(self.painel, wx.ID_ANY, self.Tradutor.tradutor(u"Compatibilidade"), (0, 0), (-1, -1),
                                   style=wx.TE_RICH)
        self.form5 = wx.TextCtrl(self.painel, wx.ID_ANY, self.info_testado_em, (0, 0), (200, -1), style=wx.TE_RICH)
        self.form5.Enabled = True
        self.form5.SetToolTipString(
            self.Tradutor.tradutor(u'Lista dos dispositivos que o jogo funcionou Ex. REDE, USB, HD'))
        self.textrating = wx.StaticText(self.painel, wx.ID_ANY, self.Tradutor.tradutor(u"Avaliação"),
                                        (0, 0), (-1, -1), style=wx.TE_RICH)
        self.painel.avaliacao = 0
        painelavaliacao = PainelEstrelas(self.painel, wx.ID_ANY, (0, 0), (-1,-1), self.info_avaliacao, self.endereco_arquivo_cfg)
        painelavaliacao.SetToolTipString(self.Tradutor.tradutor(u'Clique nas estrelas para classificar'))

        self.textRelease = wx.StaticText(self.painel, wx.ID_ANY, self.Tradutor.tradutor(u"Lançamento"), (0, 0), (-1, -1),
                                         style=wx.TE_RICH)
        self.formRelease = wx.TextCtrl(self.painel, wx.ID_ANY, self.info_lancamento, (0, 0), (200, -1), style=wx.TE_RICH)
        self.formRelease.Enabled = True
        self.formRelease.SetToolTipString(self.Tradutor.tradutor(u'Ano de lançamento do jogo'))
        self.textScan = wx.StaticText(self.painel, wx.ID_ANY, self.Tradutor.tradutor(u"Tamanho da tela"), (0, 0),
                                      style=wx.TE_RICH)
        self.formScan = wx.TextCtrl(self.painel, wx.ID_ANY, self.info_tamvideo, (0, 0), (200, -1), style=wx.TE_RICH)
        self.formScan.Enabled = True
        self.formScan.SetToolTipString(self.Tradutor.tradutor(u'Dimensões da largura'))
        self.textEsrb = wx.StaticText(self.painel, wx.ID_ANY, self.Tradutor.tradutor(u"Classificação"), (0, 0),
                                      style=wx.TE_RICH)
        self.formEsrb = wx.TextCtrl(self.painel, wx.ID_ANY, self.info_classificacao, (0, 0), (200, -1), style=wx.TE_RICH)
        self.formEsrb.Enabled = True
        self.formEsrb.SetToolTipString(self.Tradutor.tradutor(u'Classificação indicativa, coloque a idade base'))
        self.textAspect = wx.StaticText(self.painel, wx.ID_ANY, self.Tradutor.tradutor(u"Formato da tela"), (0, 0), (-1, -1),
                                        style=wx.TE_RICH)
        self.formAspect = wx.TextCtrl(self.painel, wx.ID_ANY, self.info_proporcao_imagem, (0, 0), (200, -1),
                                      style=wx.TE_RICH)
        self.formAspect.Enabled = True
        self.formAspect.SetToolTipString(self.Tradutor.tradutor(u'Compatibilidade com telas Widescreen'))
        self.textDeveloper = wx.StaticText(self.painel, wx.ID_ANY, self.Tradutor.tradutor(u"Desenvolvedor"), (0, 0),
                                           style=wx.TE_RICH)
        self.formDeveloper = wx.TextCtrl(self.painel, wx.ID_ANY, self.info_desenvolvedor, (0, 0), (200, -1),
                                         style=wx.TE_RICH)
        self.formDeveloper.Enabled = True
        self.formDeveloper.SetToolTipString(self.Tradutor.tradutor(u'Desenvolvedor do jogo'))
        self.textcallbacktimer = wx.StaticText(self.painel, wx.ID_ANY, self.Tradutor.tradutor(u"Callback timer"), (0, 0),
                                               style=wx.TE_RICH)
        self.formcallbacktimer = wx.TextCtrl(self.painel, wx.ID_ANY, self.comp_callbacktimer, (0, 0), (200, -1),
                                             style=wx.TE_RICH)
        self.formcallbacktimer.Enabled = True
        self.formcallbacktimer.SetToolTipString(self.Tradutor.tradutor(u'Aplicar um atraso para as funções CDVD'))
        self.textAltStartup = wx.StaticText(self.painel, wx.ID_ANY, self.Tradutor.tradutor(u"Arquivo de arranque"), (0, 0),
                                            style=wx.TE_RICH)
        self.formAltStartup = wx.TextCtrl(self.painel, wx.ID_ANY, self.comp_AltStartup, (0, 0), (200, -1), style=wx.TE_RICH)
        self.formAltStartup.Enabled = True
        self.formAltStartup.SetToolTipString(self.Tradutor.tradutor(u'Apontar o arquivo ELF que inicia o jogo'))
        self.textdnas = wx.StaticText(self.painel, wx.ID_ANY, self.Tradutor.tradutor(u"ID DNA"), (0, 0),
                                      style=wx.TE_RICH | wx.ALIGN_CENTER_VERTICAL)
        self.formdnas = wx.TextCtrl(self.painel, wx.ID_ANY, self.comp_dnas, (0, 0), (200, -1), style=wx.TE_RICH)
        self.formdnas.SetToolTipString(self.Tradutor.tradutor(u'ID para jogar pela internet'))
        self.formdnas.Enabled = True

        linha_horizontal = wx.StaticLine(self.painel, id=wx.ID_ANY, pos=(0, 0), size=(-1, -1),
                                         style=wx.LI_HORIZONTAL | wx.BORDER_DOUBLE)
        self.text6 = wx.StaticText(self.painel, wx.ID_ANY,
                                   self.Tradutor.tradutor(u"Configurações de compatibilidade"), (0, 0))
        self.text6.SetFont(font)

        self.check1 = wx.CheckBox(self.painel, wx.ID_ANY, self.Tradutor.tradutor("Modo 1"))
        self.check1.SetToolTipString(self.Tradutor.tradutor(u'Ler core alternativo'))
        self.check2 = wx.CheckBox(self.painel, wx.ID_ANY, self.Tradutor.tradutor("Modo 2"))
        self.check2.SetToolTipString(self.Tradutor.tradutor(u'Método alternativo de leitura de dados'))
        self.check3 = wx.CheckBox(self.painel, wx.ID_ANY, self.Tradutor.tradutor("Modo 3"))
        self.check3.SetToolTipString(self.Tradutor.tradutor(u'Desprender chamadas do sistema'))
        self.check4 = wx.CheckBox(self.painel, wx.ID_ANY, self.Tradutor.tradutor("Modo 4"))
        self.check4.SetToolTipString(self.Tradutor.tradutor(u'Modo PPS 0'))
        self.check5 = wx.CheckBox(self.painel, wx.ID_ANY, self.Tradutor.tradutor("Modo 5"))
        self.check5.SetToolTipString(self.Tradutor.tradutor(u'Desabilitar DVD-DL'))
        self.check6 = wx.CheckBox(self.painel, wx.ID_ANY, self.Tradutor.tradutor("Modo 6"))
        self.check6.SetToolTipString(self.Tradutor.tradutor(u'Desabilitar IGR'))
        self.check7 = wx.CheckBox(self.painel, wx.ID_ANY, self.Tradutor.tradutor("Modo 7"))
        self.check7.SetToolTipString(self.Tradutor.tradutor(u'Usar hack IOP threading'))
        self.check8 = wx.CheckBox(self.painel, wx.ID_ANY, self.Tradutor.tradutor("Modo 8"))
        self.check8.SetToolTipString(self.Tradutor.tradutor(u'Esconder módulo dev9'))

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

        linha_horizontal2 = wx.StaticLine(self.painel, id=wx.ID_ANY, pos=(0, 0), size=(-1, -1),
                                          style=wx.LI_HORIZONTAL | wx.BORDER_DOUBLE)

        self.text7 = wx.StaticText(self.painel, wx.ID_ANY,
                                   self.Tradutor.tradutor(u"Configuração do Virtual Memory Card"), (0, 0),
                                   style= wx.ALIGN_CENTER_VERTICAL)
        self.text7.SetFont(font)
        self.text8 = wx.StaticText(self.painel, wx.ID_ANY,
                                   self.Tradutor.tradutor(u"VMC1"), (0, 0))
        self.form8 = wx.TextCtrl(self.painel, wx.ID_ANY, self.config_vmc0, (0, 0), (200, -1))
        self.form8.Enabled = False
        self.text9 = wx.StaticText(self.painel, wx.ID_ANY,
                                   self.Tradutor.tradutor(u"VMC2"), (0, 0),
                                   style= wx.ALIGN_CENTER_VERTICAL)
        self.form9 = wx.TextCtrl(self.painel, wx.ID_ANY, self.config_vmc1, (0, 0), (200, -1))
        self.form9.Enabled = False

        self.botaook = wx.Button(self.painel, wx.ID_OK, 'OK', (0, 0))
        self.Bind(wx.EVT_BUTTON, self.Confirmar, self.botaook)

        sizer = wx.GridBagSizer(0, 0)
        sizer2 = wx.GridBagSizer(0, 0)

        sizer.Add(self.text0,               (0, 0), (1, 6), wx.ALIGN_CENTER, 2)
        sizer.Add(self.text1,               (2, 0), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.form1,               (2, 1), (1, 3), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.text2,               (4, 0), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.form2,               (4, 1), (2, 3), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.text3,               (3, 0), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.form3,               (3, 1), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.textgenero,          (3, 2), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.formgenero,          (3, 3), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.text4,               (6, 0), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.form4,               (6, 1), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.text5,               (6, 2), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.form5,               (6, 3), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)

        sizer.Add(self.textDeveloper,       (7, 0), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.formDeveloper,       (7, 1), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)

        sizer.Add(self.textRelease,         (7, 2), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.formRelease,         (7, 3), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.textScan,            (8, 0), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.formScan,            (8, 1), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.textAspect,          (8, 2), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.formAspect,          (8, 3), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.textEsrb,            (9, 0), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.formEsrb,            (9, 1), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.textrating,          (9, 2), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(painelavaliacao,          (9, 3), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)

        sizer.Add(linha_horizontal,         (11, 0), (1, 6), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 2)
        sizer.Add(self.text6,               (12, 0), (1, 6), wx.ALIGN_CENTER, 2)

        sizer.Add(self.check1,              (14, 0), (1, 1), wx.ALL | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check2,              (14, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check3,              (15, 0), (1, 1), wx.ALL | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check4,              (15, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check5,              (16, 0), (1, 1), wx.ALL | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check6,              (16, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check7,              (17, 0), (1, 1), wx.ALL | wx.ALIGN_CENTER, 2)
        sizer.Add(self.check8,              (17, 1), (1, 1), wx.ALL | wx.ALIGN_CENTER, 2)
        sizer.Add(self.textcallbacktimer,   (14, 2), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.formcallbacktimer,   (14, 3), (1, 1), wx.ALL | wx.ALIGN_CENTER | wx.EXPAND, 2)
        sizer.Add(self.textAltStartup,      (15, 2), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.formAltStartup,      (15, 3), (1, 1), wx.ALL | wx.ALIGN_CENTER | wx.EXPAND, 2)
        sizer.Add(self.textdnas,            (17, 2), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.formdnas,            (17, 3), (1, 1), wx.ALL | wx.ALIGN_CENTER | wx.EXPAND, 2)

        sizer.Add(linha_horizontal2,        (19, 0), (1, 6), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 2)
        sizer.Add(self.text7,               (20, 0), (1, 6), wx.ALIGN_CENTER, 2)

        sizer.Add(self.text8,               (22, 0), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.form8,               (22, 1), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        sizer.Add(self.text9,               (22, 2), (1, 1), wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        sizer.Add(self.form9,               (22, 3), (1, 1), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)

        sizer.Add(self.botaook,             (24, 0), (2, 5), wx.ALL | wx.ALIGN_CENTER, 10)

        self.painel.SetSizerAndFit(sizer)
        sizer2.Add(self.painel,             (0, 0), (1, 1), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 10)

        self.fco_painel_principal.SetSizerAndFit(sizer2)
        self.Fit()
        self.Centre()


    def Confirmar(self, event):
        some = 0
        if self.painel.avaliacao == "1":
            self.parent.imagem_avaliacao.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'aval1.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())

        elif self.painel.avaliacao == "2":
            self.parent.imagem_avaliacao.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'aval2.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())

        elif self.painel.avaliacao == "3":
            self.parent.imagem_avaliacao.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'aval3.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())

        elif self.painel.avaliacao == "4":
            self.parent.imagem_avaliacao.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'aval4.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())

        elif self.painel.avaliacao == "5":
            self.parent.imagem_avaliacao.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'aval5.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())

        valor_esrb = self.formEsrb.GetValue()
        if not valor_esrb == "":
            try:
                valor_esrb = int(valor_esrb)
            except:
                valor_esrb = ""
        if valor_esrb == "":
            self.parent.pj_imagem_esrb.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'semesrb.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        elif valor_esrb < 10:
            self.parent.pj_imagem_esrb.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'esrb_livre.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        elif valor_esrb < 13:
            self.parent.pj_imagem_esrb.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'esrb_10.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        elif valor_esrb < 17:
            self.parent.pj_imagem_esrb.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'esrb_13.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        elif valor_esrb < 18:
            self.parent.pj_imagem_esrb.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'esrb_17.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        elif valor_esrb > 17:
            self.parent.pj_imagem_esrb.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'esrb_18.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        else:
            valor_esrb=""
            self.parent.pj_imagem_esrb.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'semesrb.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())

        num_de_players = self.form4.GetValue()
        if not num_de_players == "":
            try:
                num_de_players = int(num_de_players)
            except:
                num_de_players = ""

        if num_de_players == "":
            self.parent.pj_imagemplayers.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'quantosplayers.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        elif num_de_players == 1:
            num_de_players = "1"
            self.parent.pj_imagemplayers.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', '1P.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        elif num_de_players == 2:        
            num_de_players = "2"
            self.parent.pj_imagemplayers.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', '2P.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())


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
        self.manipula_cfg_jogo.mudar_dict_cfg('Rating', str(self.painel.avaliacao))
        self.manipula_cfg_jogo.mudar_dict_cfg('Compatibility', self.form5.GetValue())

        self.manipula_cfg_jogo.mudar_dict_cfg('Description', self.form2.GetValue())
        self.manipula_cfg_jogo.mudar_dict_cfg('Players', str(num_de_players))
        self.manipula_cfg_jogo.mudar_dict_cfg('Release', self.formRelease.GetValue())
        self.manipula_cfg_jogo.mudar_dict_cfg('Scan', self.formScan.GetValue())
        self.manipula_cfg_jogo.mudar_dict_cfg('Esrb', str(valor_esrb))
        self.manipula_cfg_jogo.mudar_dict_cfg('Aspect', self.formAspect.GetValue())

        self.manipula_cfg_jogo.mudar_dict_cfg('Developer', self.formDeveloper.GetValue())

        self.manipula_cfg_jogo.mudar_dict_cfg('$CallbackTimer', str(self.formcallbacktimer.GetValue()))
        self.manipula_cfg_jogo.mudar_dict_cfg('$AltStartup', self.formAltStartup.GetValue())
        self.manipula_cfg_jogo.mudar_dict_cfg("$Compatibility", str(some))
        self.manipula_cfg_jogo.mudar_dict_cfg("$DNAS", str(self.formdnas.GetValue()))
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
        self.conf_prog = Configuracoes(memoria['arquivo_configuracao'])
        self.dicionario = memoria['configuracao']['DICIONARIO']
        self.Tradutor = Dicionario(self.dicionario)
        self.dados_caso_cancelado = ""
        self.comandocancelar = True
        self.cancelado = False
        self.BUFFER = 1024*1024*2
        self.tamanho_maximo_fatia = 1073741824
        self.bytes_na_fatia = 1073741824
        self.tamanho_total = 0
        self.dados_gravados_total = 0
        self.quant = len(lista_de_arquivos)

        self.mensagem1 = self.Tradutor.tradutor('Copiando arquivo')
        self.mensagem2 = self.Tradutor.tradutor('de')
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
            self.cancel = wx.Button(self, wx.ID_CANCEL, self.Tradutor.tradutor("&Cancelar"))
            self.cancel.SetDefault()
            self.cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
            btnsizer = wx.StdDialogButtonSizer()
            btnsizer.AddButton(self.cancel)
            btnsizer.Realize()
            sizer.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
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
                self.bytes_na_fatia = self.tamanho_maximo_fatia
                fatias = 0
                with open(endereco_de_origem, 'rb') as origem_aberto:
                    bytes_no_total = tamanho
                    while self.comandocancelar:
                        self.arquivo_destino = os.path.join(destino, '%s.%02d' % (novo_nome, fatias))
                        self.destino_aberto = open(self.arquivo_destino, 'wb')
                        self.dados_gravados = 0
                        while self.comandocancelar:
                            pedaco_retirado = min(self.BUFFER, self.bytes_na_fatia)                                        # buffer = 50 | 50 | 50
                            datax = origem_aberto.read(pedaco_retirado)   # datax = 50 | 50 | 20

                            self.destino_aberto.write(datax)
                            self.dados_gravados += pedaco_retirado
                            self.dados_gravados_total += pedaco_retirado
                            self.progresso = int(
                                (float(self.dados_gravados_total) / float(self.tamanho_total)) * 100)
                            self.gauge.SetValue(self.progresso)
                            wx.Yield()
                            self.bytes_na_fatia -= pedaco_retirado
                            if self.bytes_na_fatia == 0 or self.bytes_na_fatia < 0:
                                break

                        bytes_no_total -= self.dados_gravados
                        if bytes_no_total == 0 or bytes_no_total < 0:
                            break
                        else:
                            self.bytes_na_fatia = self.tamanho_maximo_fatia 
                            fatias += 1
                    self.destino_aberto.close()
            else:
                self.tamanho_desse_arquivo = tamanho
                if fatiar == True and type(endereco_de_origem) == list:
                    contgh = 0
                    for g in endereco_de_origem:
                        s = os.stat(g)
                        self.tamanho_desse_arquivo = s.st_size

                        self.arquivo_destino = "%s.%02d" % (self.arquivo_destino, contgh)
                        with open(self.arquivo_destino, "wb") as self.destino_aberto:
                            with open(g, "rb") as origem_aberto:
                                while self.comandocancelar:
                                    y = origem_aberto.read(self.BUFFER)
                                    self.tamanho_desse_arquivo -= self.BUFFER
                                    self.dados_gravados_total += min(self.BUFFER, self.tamanho_desse_arquivo)
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
                                while self.comandocancelar:
                                    y = origem_aberto.read(self.BUFFER)
                                    self.tamanho_desse_arquivo -= self.BUFFER
                                    self.dados_gravados_total += min(self.BUFFER, self.tamanho_desse_arquivo)
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
            if nome is False:
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
                    self.dados_caso_cancelado = (os.path.join(destino, nome), nome)
                elif item[1] == 'CFG' or item[1] == 'ART':
                    if os.path.exists(os.path.join(destino, nome)):
                        os.remove(os.path.join(destino, nome))
                    item[5] = nome
                    self.dados_caso_cancelado = (os.path.join(destino, nome), nome)
                else:
                    while os.path.exists(os.path.join(destino, nome)):
                        cont += 1
                        nome = '%s - %02d.%s' % (nome_base, cont, extensao)
                    item[5] = nome
                    self.dados_caso_cancelado = (os.path.join(destino, nome), nome)
            else:
                nome_base = nome
                nome = "%s.%s" % (nome_base, extensao)
                cont = 0
                while os.path.exists(os.path.join(destino, nome)):
                    cont += 1
                    nome = '%s - %02d.%s' % (nome_base, cont, extensao)
                item[5] = nome
                self.dados_caso_cancelado = (os.path.join(destino, nome), nome)
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
                self.dados_caso_cancelado = (os.path.join(destino, nomeul_sem_extensao), novo_nome_ul)
            else:
                nome_base = nome
                nome = "%s.iso" % (nome_base)
                cont = 0
                while os.path.exists(os.path.join(destino, nome)):
                    cont += 1
                    nome = '%s - %02d.iso' % (nome_base, cont)
                item[5] = nome
                self.dados_caso_cancelado = (os.path.join(destino, nome), nome)


    def on_timer(self, event):
        if self.acabouse == True:
            self.timer.Stop()
            self.Destroy()

    def on_cancel(self, event):
        self.comandocancelar = False
        self.cancelado = self.dados_caso_cancelado
        self.Destroy()


class FrameLogin(wx.Dialog):


    def __init__(self, parent, title, nova_senha = False):

        wx.Dialog.__init__(self, parent, wx.ID_ANY, title, (-1,-1), (300,150))
        self.conf_prog = Configuracoes(memoria['arquivo_configuracao'])
        self.dicionario = memoria['configuracao']['DICIONARIO']
        self.Tradutor = Dicionario(self.dicionario)
        self.autorizado = False
        arquivo_de_senha = os.path.join(memoria['end_arquivo_senha'],'pwd')
        self.parent = parent

        painel = wx.Panel(self, wx.ID_ANY)
        self.nova_senha = nova_senha
        textnome = wx.StaticText(painel, label=self.Tradutor.tradutor("Nome:"),
                                 style = wx.TE_RICH | wx.ALIGN_RIGHT |wx.ALIGN_CENTER_VERTICAL)
        self.formnome = wx.TextCtrl(painel)
        if nova_senha == True:
            if os.path.exists(arquivo_de_senha):
                self.SetTitle(self.Tradutor.tradutor("Mudar senha"))
                textnome.SetLabel(self.Tradutor.tradutor("Novo nome"))
            else:
                self.SetTitle(self.Tradutor.tradutor("Criar senha"))
        textsenha = wx.StaticText(painel, label=self.Tradutor.tradutor("Senha:"),
                                  style = wx.TE_RICH | wx.ALIGN_RIGHT |wx.ALIGN_CENTER_VERTICAL)
        self.formsenha = wx.TextCtrl(painel, style=wx.TE_PASSWORD)


        textnovasenha = wx.StaticText(painel, label=self.Tradutor.tradutor("Nova Senha:"),
                                  style = wx.TE_RICH | wx.ALIGN_RIGHT |wx.ALIGN_CENTER_VERTICAL)
        self.formnovasenha = wx.TextCtrl(painel, style=wx.TE_PASSWORD)
        if nova_senha == False:
            self.formsenha.Bind(wx.EVT_KEY_UP, self.enter_pressionado)
        else:
            if os.path.exists(arquivo_de_senha):
                self.formnovasenha.Bind(wx.EVT_KEY_UP, self.enter_pressionado)
            else:
                self.formsenha.Bind(wx.EVT_KEY_UP, self.enter_pressionado)

        if not os.path.exists(arquivo_de_senha) and nova_senha == False:
            self.formnome.SetValue('admin')
            textnovasenha.Hide()
            self.formnome.Enabled = False
            self.formnovasenha.Hide()
        if not os.path.exists(arquivo_de_senha) and nova_senha == True:
            self.formnome.Enabled = True
            self.formnovasenha.Hide()
            textnovasenha.Hide()
        else:
            if nova_senha == True:
                textsenha.SetLabel(self.Tradutor.tradutor('Senha antiga'))
                self.SetSizeWH(300,170)
            else:
                self.formnovasenha.Hide()
                textnovasenha.Hide()
        painel_botoes = wx.Panel(painel, wx.ID_ANY)
        botaook = wx.Button(painel_botoes, wx.ID_ANY, "OK")
        botaocancelar = wx.Button(painel_botoes, wx.ID_CANCEL, self.Tradutor.tradutor('Cancelar'))
        sizerbotoes = wx.GridSizer(1, 2)
        sizerbotoes.Add(botaook, 0,  wx.ALIGN_CENTER|wx.ALL, 5)
        sizerbotoes.Add(botaocancelar,0,  wx.ALIGN_CENTER|wx.ALL, 5)
        painel_botoes.SetSizer(sizerbotoes)
        sizer = wx.GridBagSizer(0, 0)
        sizer.Add(textnome, (0, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL , 5)
        sizer.Add(self.formnome, (0, 1), (1, 1), wx.ALL | wx.EXPAND, 5)
        sizer.Add(textsenha, (1, 0), (1, 1), wx.ALIGN_RIGHT | wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.formsenha, (1, 1), (1, 1), wx.ALL | wx.EXPAND | wx.TE_PASSWORD, 5)
        sizer.Add(textnovasenha, (2, 0), (1, 1), wx.ALIGN_RIGHT | wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.formnovasenha, (2, 1), (1, 1), wx.ALL | wx.EXPAND | wx.TE_PASSWORD, 5)
        sizer.Add(painel_botoes, (3, 0), (1, 2), wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 0)
        sizer.AddGrowableCol(1)
        self.Bind(wx.EVT_BUTTON, self.Confirmar, botaook)
        painel.SetSizerAndFit(sizer)
        self.Fit()

    def Confirmar(self, event):
        self.acao()

    def enter_pressionado (self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN :
            self.acao()

    def acao(self):

        self.dicionario = memoria['configuracao']['DICIONARIO']
        arquivo_de_senha = os.path.join(memoria['end_arquivo_senha'],'pwd')
        login = self.formnome.GetValue()
        senha = self.formsenha.GetValue()
        senha_hash = hashlib.sha224(senha).hexdigest()
        if self.nova_senha == False:
            if os.path.exists(arquivo_de_senha):
                with open(arquivo_de_senha, 'r') as lendopass:
                    aberto = lendopass.read()
                    splitando = aberto.split(' = ')
                    if len(splitando) == 2:
                        login_no_arquivo = splitando[0]
                        if login == login_no_arquivo:
                            senha_no_arquivo = splitando[1].strip()
                            if senha_hash == senha_no_arquivo:
                                self.autorizado = True
                            else:
                                msgbox = wx.MessageDialog(self, self.Tradutor.tradutor(u'Não foi possivel completar a ação, login ou senha incorretos'),
                                                          self.Tradutor.tradutor(u'Atenção'),
                                                          wx.OK | wx.ICON_INFORMATION)
                                msgbox.ShowModal()
                        else:
                            msgbox = wx.MessageDialog(self, self.Tradutor.tradutor(u'Não foi possivel completar a ação, login ou senha incorretos'),
                                                          self.Tradutor.tradutor(u'Atenção'),
                                                          wx.OK | wx.ICON_INFORMATION)
                            msgbox.ShowModal()
            else:
                login_padrao = 'admin'
                senha_padrao = hashlib.sha224("admin").hexdigest()
                if senha_hash == senha_padrao:
                    self.autorizado = True

        else:
            if os.path.exists(arquivo_de_senha):
                with open(arquivo_de_senha, 'r') as lendopass:
                    aberto = lendopass.read()
                    splitando = aberto.split(' = ')
                    if len(splitando) == 2:
                        senha_no_arquivo = splitando[1].strip()
                        if senha_hash == senha_no_arquivo:
                            nova_senha = self.formnovasenha.GetValue()
                            nova_senha_hash = hashlib.sha224(nova_senha).hexdigest()
                            with open(arquivo_de_senha, 'w') as escrevendopass:
                                novo_texto = "%s = %s" %(login, nova_senha_hash)
                                escrevendopass.write(novo_texto)
                        else:
                            msgbox = wx.MessageDialog(self, self.Tradutor.tradutor(u'Não foi possivel completar a ação, login ou senha incorretos'),
                                                      self.Tradutor.tradutor(u'Atenção'),
                                                      wx.OK | wx.ICON_INFORMATION)
                            msgbox.ShowModal()
                    else:
                        texto_erro = self.Tradutor.tradutor(u'O arquivo de senha apresenta problema, apague-o para corrigir o problema e criar uma nova senha, ele se encontra em: ')
                        msgbox = wx.MessageDialog(self, "%s%s" % (texto_erro, os.path.join(memoria['end_arquivo_senha'], 'pwd')),
                                                  self.Tradutor.tradutor(u'Atenção'),
                                                  wx.OK | wx.ICON_INFORMATION)
                        msgbox.ShowModal()
            else:
                with open(arquivo_de_senha, 'w') as escrevendopass:
                    novo_texto = "%s = %s" %(login, senha_hash)
                    escrevendopass.write(novo_texto)
                texto1 = self.Tradutor.tradutor("Bem vindo")
                texto2 = self.Tradutor.tradutor('ao PhanterPS2')
                self.parent.SetStatusText("%s %s %s" % (texto1, login, texto2))

        self.Destroy()


class FrameClassificacao(wx.Dialog):


    def __init__(self, parent, title):

        wx.Dialog.__init__(self, parent, wx.ID_ANY, title, (0,0), (-1,-1))
        self.conf_prog = Configuracoes(memoria['arquivo_configuracao'])
        self.dicionario = memoria['configuracao']['DICIONARIO']
        self.fc_default_campo = self.conf_prog.leitor_configuracao('CLASSIFICACAO_CAMPO')
        self.fc_default_ordem = self.conf_prog.leitor_configuracao('CLASSIFICACAO_ORDEM')
        self.fc_default_default = self.conf_prog.leitor_configuracao('CLASSIFICACAO_DEFAULT')
        self.Tradutor = Dicionario(self.dicionario)
        self.parent = parent
        fc_opcoes_radio_nome = [self.Tradutor.tradutor('Nome'), 
                                self.Tradutor.tradutor(u'Código'), 
                                self.Tradutor.tradutor('Tamanho'), 
                                self.Tradutor.tradutor(u'Padrão')]
        fc_opcoes_radio_modo = [self.Tradutor.tradutor("Crescente"), 
                                self.Tradutor.tradutor("Decrescente")]
        self.fc_painel_principal = wx.Panel(self, wx.ID_ANY)
        self.fc_radio_campos = wx.RadioBox(self.fc_painel_principal, wx.ID_ANY, self.Tradutor.tradutor("Campos"),
                                        (0, 0), (-1,-1), fc_opcoes_radio_nome, 4, wx.RA_SPECIFY_COLS)
        self.fc_radio_modo = wx.RadioBox(self.fc_painel_principal, wx.ID_ANY, self.Tradutor.tradutor("Ordem"),
                                        (0, 0), (-1,-1), fc_opcoes_radio_modo, 2, wx.RA_SPECIFY_COLS)
        self.fc_check_box =  wx.CheckBox(self.fc_painel_principal, wx.ID_ANY, 
                                        self.Tradutor.tradutor(u'Padrão na inicialização?'),(0 ,0), style = wx.ALIGN_CENTER)
        
        self.fc_botao_ok = wx.Button (self.fc_painel_principal, wx.ID_ANY, 'OK')
        self.Bind(wx.EVT_BUTTON, self.confirmar, self.fc_botao_ok)
        fc_sizer_painel_principal = wx.BoxSizer(wx.VERTICAL)
        fc_sizer_painel_principal.Add(self.fc_radio_campos, 0, wx.ALL| wx.EXPAND| wx.ALIGN_CENTER,10)
        fc_sizer_painel_principal.Add(self.fc_radio_modo, 0, wx.ALL | wx.EXPAND|wx.ALIGN_CENTER, 10)
        fc_sizer_painel_principal.Add(self.fc_check_box, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        fc_sizer_painel_principal.Add(self.fc_botao_ok, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        if self.fc_default_default == "1" or self.fc_default_default == 1:

            self.fc_check_box.SetValue(True)
        if not self.fc_default_campo == "":
            if self.fc_default_campo == "2" or self.fc_default_campo == 2:
                self.fc_radio_campos.SetSelection(0)
            elif self.fc_default_campo == "1" or self.fc_default_campo == 1:
                self.fc_radio_campos.SetSelection(1)
            elif self.fc_default_campo == "3" or self.fc_default_campo == 3:
                self.fc_radio_campos.SetSelection(2)
            else:
                self.fc_radio_campos.SetSelection(3)
           
        if not self.fc_default_ordem == "":
            if self.fc_default_ordem == "crescente":
                self.fc_radio_modo.SetSelection(0)
            else:
                self.fc_radio_modo.SetSelection(1)

        self.fc_painel_principal.SetSizerAndFit(fc_sizer_painel_principal)
        self.Fit()
        self.Centre()

    def confirmar (self, event):

        classifica = self.fc_radio_campos.GetSelection()
        if classifica == 0:
            classificacao = 2
        elif classifica == 1:
            classificacao = 1
        elif classifica == 2:
            classificacao = 3
        elif classifica == 3:
            classificacao = False
        modo = self.fc_radio_modo.GetSelection()
        manu_cfg = Configuracoes(memoria['arquivo_configuracao'])
        if modo == 1:
            ordem = 'decrescente'
        else:
            ordem = 'crescente'
            
        if self.fc_check_box.GetValue() == True:
            manu_cfg.mudar_configuracao('CLASSIFICACAO_DEFAULT', "1")            
        else:
            manu_cfg.mudar_configuracao('CLASSIFICACAO_DEFAULT', "0")
        manu_cfg.mudar_configuracao('CLASSIFICACAO_CAMPO', "%s" % classificacao)
        manu_cfg.mudar_configuracao('CLASSIFICACAO_ORDEM', "%s" % ordem)

        self.Hide()
        
        self.parent.atualizaremanterchecks(refresh = True, classificacao = classificacao, modo = ordem)
        self.Destroy()


class PainelEstrelas(wx.Panel):
    def __init__(self, parent, ID, pos, size, info_avaliacao, endereco_arquivo_cfg):
        wx.Panel.__init__(self, parent, wx.ID_ANY, pos, size)
        self.parent = parent
        self.estrela = wx.Image(os.path.join(corrente, 'imagens', 'estrela.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.estrela_apagada = wx.Image(os.path.join(corrente, 'imagens', 'estrela_apagada.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.info_avaliacao = info_avaliacao
        if self.info_avaliacao == "1":
            self.botao_imagem1 = wx.BitmapButton(self, wx.ID_ANY, self.estrela, (0, 0))
            self.botao_imagem2 = wx.BitmapButton(self, wx.ID_ANY, self.estrela_apagada, (0, 0))
            self.botao_imagem3 = wx.BitmapButton(self, wx.ID_ANY, self.estrela_apagada, (0, 0))
            self.botao_imagem4 = wx.BitmapButton(self, wx.ID_ANY, self.estrela_apagada, (0, 0))
            self.botao_imagem5 = wx.BitmapButton(self, wx.ID_ANY, self.estrela_apagada, (0, 0))
        elif self.info_avaliacao == "2":
            self.botao_imagem1 = wx.BitmapButton(self, wx.ID_ANY, self.estrela, (0, 0))
            self.botao_imagem2 = wx.BitmapButton(self, wx.ID_ANY, self.estrela, (0, 0))
            self.botao_imagem3 = wx.BitmapButton(self, wx.ID_ANY, self.estrela_apagada, (0, 0))
            self.botao_imagem4 = wx.BitmapButton(self, wx.ID_ANY, self.estrela_apagada, (0, 0))
            self.botao_imagem5 = wx.BitmapButton(self, wx.ID_ANY, self.estrela_apagada, (0, 0))
        elif self.info_avaliacao == "3":
            self.botao_imagem1 = wx.BitmapButton(self, wx.ID_ANY, self.estrela, (0, 0))
            self.botao_imagem2 = wx.BitmapButton(self, wx.ID_ANY, self.estrela, (0, 0))
            self.botao_imagem3 = wx.BitmapButton(self, wx.ID_ANY, self.estrela, (0, 0))
            self.botao_imagem4 = wx.BitmapButton(self, wx.ID_ANY, self.estrela_apagada, (0, 0))
            self.botao_imagem5 = wx.BitmapButton(self, wx.ID_ANY, self.estrela_apagada, (0, 0))
        elif self.info_avaliacao == "4":
            self.botao_imagem1 = wx.BitmapButton(self, wx.ID_ANY, self.estrela, (0, 0))
            self.botao_imagem2 = wx.BitmapButton(self, wx.ID_ANY, self.estrela, (0, 0))
            self.botao_imagem3 = wx.BitmapButton(self, wx.ID_ANY, self.estrela, (0, 0))
            self.botao_imagem4 = wx.BitmapButton(self, wx.ID_ANY, self.estrela, (0, 0))
            self.botao_imagem5 = wx.BitmapButton(self, wx.ID_ANY, self.estrela_apagada, (0, 0))
        elif self.info_avaliacao == "5":
            self.botao_imagem1 = wx.BitmapButton(self, wx.ID_ANY, self.estrela, (0, 0))
            self.botao_imagem2 = wx.BitmapButton(self, wx.ID_ANY, self.estrela, (0, 0))
            self.botao_imagem3 = wx.BitmapButton(self, wx.ID_ANY, self.estrela, (0, 0))
            self.botao_imagem4 = wx.BitmapButton(self, wx.ID_ANY, self.estrela, (0, 0))
            self.botao_imagem5 = wx.BitmapButton(self, wx.ID_ANY, self.estrela, (0, 0))
        else:
            self.botao_imagem1 = wx.BitmapButton(self, wx.ID_ANY, self.estrela_apagada, (0, 0))
            self.botao_imagem2 = wx.BitmapButton(self, wx.ID_ANY, self.estrela_apagada, (0, 0))
            self.botao_imagem3 = wx.BitmapButton(self, wx.ID_ANY, self.estrela_apagada, (0, 0))
            self.botao_imagem4 = wx.BitmapButton(self, wx.ID_ANY, self.estrela_apagada, (0, 0))
            self.botao_imagem5 = wx.BitmapButton(self, wx.ID_ANY, self.estrela_apagada, (0, 0))
        self.Bind(wx.EVT_BUTTON, self.MudarImagem1, self.botao_imagem1)
        self.Bind(wx.EVT_BUTTON, self.MudarImagem2, self.botao_imagem2)
        self.Bind(wx.EVT_BUTTON, self.MudarImagem3, self.botao_imagem3)
        self.Bind(wx.EVT_BUTTON, self.MudarImagem4, self.botao_imagem4)
        self.Bind(wx.EVT_BUTTON, self.MudarImagem5, self.botao_imagem5)
        sizer_botoes = wx.BoxSizer(wx.HORIZONTAL)
        sizer_botoes.Add(self.botao_imagem1, 0, wx.ALL | wx.EXPAND, 0)
        sizer_botoes.Add(self.botao_imagem2, 0, wx.ALL | wx.EXPAND, 0)
        sizer_botoes.Add(self.botao_imagem3, 0, wx.ALL | wx.EXPAND, 0)
        sizer_botoes.Add(self.botao_imagem4, 0, wx.ALL | wx.EXPAND, 0)
        sizer_botoes.Add(self.botao_imagem5, 0, wx.ALL | wx.EXPAND, 0)
        self.SetSizer(sizer_botoes)
        
    def MudarImagem1(self, event):
        self.parent.avaliacao = "1"
        self.botao_imagem1.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem2.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela_apagada.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem3.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela_apagada.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem4.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela_apagada.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem5.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela_apagada.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())

    def MudarImagem2(self, event):
        self.parent.avaliacao = "2"
        self.botao_imagem1.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem2.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem3.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela_apagada.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem4.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela_apagada.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem5.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela_apagada.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())

    def MudarImagem3(self, event):
        self.parent.avaliacao = "3"
        self.botao_imagem1.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem2.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem3.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem4.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela_apagada.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem5.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela_apagada.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())

    def MudarImagem4(self, event):
        self.parent.avaliacao = "4"
        self.botao_imagem1.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem2.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem3.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem4.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem5.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela_apagada.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())

    def MudarImagem5(self, event):
        self.parent.avaliacao = "5"
        self.botao_imagem1.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem2.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem3.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem4.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        self.botao_imagem5.SetBitmap(wx.Image(os.path.join(corrente, 'imagens', 'estrela.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap())


class PopUp(wx.PopupTransientWindow):
    def __init__(self, parent, style):
        self.conf_prog = Configuracoes(memoria['arquivo_configuracao'])
        self.dicionario = memoria['configuracao']['DICIONARIO']
        self.Tradutor = Dicionario(self.dicionario)
        wx.PopupTransientWindow.__init__(self, parent, style)
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetBackgroundColour("#C7C7C7")
        texto1 = "\n%s\n" % self.Tradutor.tradutor("Clique para escolher")
        texto2 = "%s\n" % self.Tradutor.tradutor("uma pasta ou drive")
        texto3 = "%s\n" % self.Tradutor.tradutor("para copiar os jogos")
        texto4 = "%s\n" % self.Tradutor.tradutor("selecionados")
        texto = texto1 + texto2 + texto3 + texto4 
        st = wx.StaticText(panel, -1,texto, (0,0), (150,100), style = wx.ALIGN_CENTER)
        sizer.Add(st)
        panel.SetSizer(sizer)
        sizer.Fit(panel)
        sizer.Fit(self)
        self.Layout()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(2000)
    def on_timer(self, event):
        self.Destroy()
        del self       

if __name__ == '__main__':

    y = MeuPrograma()
    y.MainLoop()
