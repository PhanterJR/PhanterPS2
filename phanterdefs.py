# -*- coding: utf-8 -*- 
# Copyright (c) 2014 PhanterJR
# https://github.com/PhanterJR
# Licença LGPL

import logging
import os
import re
from contrib import iso9660
from contrib import pycrc32
import glob
from PIL import Image
from itertools import combinations

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

corrente = os.getcwd()

procura_cod_e_nome = re.compile(r'([a-zA-Z]{4}_[0-9]{3}\.[0-9]{2}\..*\.[iI][sS][oO])$')
procura_nome_e_cod_no_ul = re.compile(r'([ a-zA-Z0-9]*.*ul\.[ a-zA-Z0-9]{4}_[0-9]{3}\.[0-9]{2})')
procura_apenas_cod = re.compile(r'^/([a-zA-Z]{4}_[0-9]{3}\.[0-9]{2})')
procura_apenas_cod2 = re.compile(r'^([a-zA-Z]{4}_[0-9]{3}\.[0-9]{2})')
procura_apenas_cod3 = re.compile(r'([a-zA-Z]{4}_[0-9]{3}\.[0-9]{2})')
procura_coverart = re.compile(r'(.*_COV\.[pP][Nn][Gg])|(.*_COV\.[Jj][Pp][Gg])$')
procura_systema_de_video = re.compile(r'NTSC|PAL')


class Configuracoes():
    """

    Ler arquivos de configurações
    """

    def __init__(self, nome_do_arquivo='phanterps2.cfg'):
        """

        se o nome do arquivo não for pahnterps2, será criado um arquivo vazio, senão será criado um arquivo padrão
        """
        self.nome_do_arquivo = nome_do_arquivo
        self.configuracoes = ''
        self.config = {}
        try:
            with open(os.path.join(corrente, nome_do_arquivo), 'r') as arquivo_cfg:
                self.configuracoes = arquivo_cfg.readlines()
                for x in self.configuracoes:
                    y = x.split(' = ')
                    if len(y) == 1:
                        pass
                    else:
                        self.config[y[0]] = y[1]

        except IOError:

            if nome_do_arquivo == "phanterps2.cfg":
                with open(os.path.join(corrente, nome_do_arquivo), 'w') as arquivo_cfg:
                    padrao = "DVD = %s\DVD\n" \
                             "CFG = %s\CFG\n" \
                             "DICIONARIO = \n" \
                             "ART = %s\ART\n" \
                             "PADRAO = %s\n" \
                             "CD = %s\CD\n" % (corrente, corrente, corrente, corrente, corrente)
                    arquivo_cfg.write(padrao)
                    arquivo_cfg.close()
            else:
                with open(os.path.join(corrente, nome_do_arquivo), 'w') as arquivo_cfg:
                    padrao = ""
                    arquivo_cfg.write(padrao)
                    arquivo_cfg.close()

    def leitor_configuracao(self, chave=''):
        if chave == "":
            dado = ''
        else:
            try:
                dado = self.config[chave][:-1]
            except KeyError:
                dado = ''
        return dado if not dado == '\r' else ''

    def mudar_configuracao(self, chave, nova_configuracao):
        if chave == '':
            pass
        else:

            self.config[chave] = nova_configuracao + '\n'

            with open(os.path.join(corrente, self.nome_do_arquivo), 'w') as arquivo_cfg:
                new_config = ''
                for x in self.config:
                    new_config += "%s = %s" % (x, self.config[x])

                arquivo_cfg.write(new_config)


class VerificaJogo():

    def __init__(self, arquivoiso):
        """

        Verifica se o jogo já se encontra com a nomeclatura do OPL (XXX_999.99.NOME_DO_JOGO.iso)
        Abre o arquivo iso para verificar a existência do arquivo launch do jogo (XXX_999.99)
        Se os 3 testes passarem será criado uma lista com tuplas com endereço,
        código e nome do jogo seguido dos respectivos estados.
        Ex.: [('C:\XXX_999.99.NOME_DO_JOGO.iso', True), ('XXX_999.99',True), ('NOME_DO_JOGO', True)]
        Se não passar a lista será como o exemplo seguinte.
        Ex.: [('C:\COD_INVALIDO.NOME_QUALQUER_DE_JOGO.iso', True), ('', False), ('NOME_DO_JOGO', False)]
        @param arquivoiso: Endereco do arquivo ISO
        """
        self.resultado_final = False
        self.codigo_encontrado = ""
        self.sistema_de_video = ""
        self.arquivoiso = arquivoiso

        if os.path.exists(arquivoiso):
            nome_do_arquivo = procura_cod_e_nome.findall(arquivoiso)
            self.end_jogo = (self.arquivoiso, True)
            self.codigo_do_jogo1 = False
            self.nome_do_jogo1 = ""

            if not nome_do_arquivo == []:
                self.codigo_do_jogo1 = nome_do_arquivo[0][:11]
                self.nome_do_jogo1 = nome_do_arquivo[0][12:-4]

            self.procura_cod_in_iso(arquivoiso)
            self.nome_do_jogo2 = "NOME_DO_JOGO"
            self.codigo_do_jogo = (self.codigo_do_jogo1 if self.codigo_encontrado is False else self.codigo_encontrado,
                                   True if not self.codigo_encontrado is False else False)

            self.nome_do_jogo = (self.nome_do_jogo1 or self.nome_do_jogo2, True)

            stam = os.stat(arquivoiso)
            tamanho = stam.st_size
            self.resultado_final = [self.end_jogo, self.codigo_do_jogo,
                                    self.nome_do_jogo, tamanho, self.sistema_de_video]
        else:
            pass

    def procura_cod_in_iso(self, endereco=""):
        if endereco == "":
            endereco = self.arquivoiso
        self.codigo_encontrado = False

        try:
            x = iso9660.ISO9660(endereco)
            systemcnfx = x.get_file('/SYSTEM.CNF')
            systemcnf = procura_apenas_cod3.findall(systemcnfx)[0]
            sysvideo = procura_systema_de_video.findall(systemcnfx)[0]
            self.codigo_encontrado = systemcnf
            self.sistema_de_video = sysvideo
        except:
            x = False

        return x

    def pega_sistema_de_video(self):
        tt = self.procura_cod_in_iso()
        if tt is False:
            return ""
        else:
            return self.sistema_de_video


class ManipulaCfgJogo():

    def __init__(self, endereco_cfg, lista=(1, 2, 4, 8, 16, 32, 64, 128)):
        """

        @param endereco_cfg: Endereço do arquivo de configuraçao
        @param lista: Lista padrão usado para mapear as diferentes configurações do modo de compatibilidade
        """
        self.endereco_cfg = endereco_cfg

        if os.path.exists(endereco_cfg):
            self.endereco_cfg = endereco_cfg
            self.dicionario_cfg = {}
            with open(endereco_cfg, 'r') as config:
                conteudo = config.readlines()
                for x in conteudo:
                    x = x
                    partido = x.split('=')
                    par = partido[1].split('\n')
                    if type(par) == list:
                        par = par[0]

                    self.dicionario_cfg[partido[0]] = par

        else:
            with open(endereco_cfg, 'w') as configzsh:
                configzsh.write('')
            self.dicionario_cfg = {}

        self.dicionario_compatibilidade = {}
        quant = len(lista)
        y = 0
        for x in range(quant):
            y += 1
            z = combinations(lista, y)
            for i in z:
                soma = 0
                for s in i:
                    soma += s
                self.dicionario_compatibilidade[soma] = i

    def leitor_cfg(self, chave):

        try:
            resultado = self.dicionario_cfg[chave]
            if resultado == '\n' or resultado == '':
                resultado = ''
            else:
                resultado = resultado.split('\n')[0]
                if type(resultado) == list:
                    resultado = resultado[0]
        except KeyError:
            resultado = ''
        return resultado.decode('utf-8')

    def leitor_compatibilidade(self, chave):

        try:
            resultado = self.dicionario_compatibilidade[chave]
        except KeyError:
            resultado = ''
        return resultado

    def mudar_dict_cfg(self, chave, resultado):
        self.dicionario_cfg[chave] = resultado.encode('utf-8')

    def gravar_em_arquivo(self):
        texto = ''
        ordem_gravacao_comp = ['$VMC_1', '$VMC_0', '$Compatibility', '$DNAS', '$CallbackTimer', '$AltStartup']
        ordem_gravacao_info = ['Title', 'Region', 'Genre', 'Description', 'Players', 'Scan', 'Esrb', 'Aspect', 'Rating',
                               'Compatibility', 'Developer', 'Release']
        for x in ordem_gravacao_comp:
            y = self.leitor_cfg(x)
            if not y == '':
                texto += u'%s=%s\n' % (x, y)

        for x in ordem_gravacao_info:
            y = self.leitor_cfg(x)
            if not y == '':
                texto += u'%s=%s\n' % (x, y)
        texto = texto
        with open(self.endereco_cfg, 'w') as aberto:
            aberto.write(texto.encode('utf-8'))


class LocalizaArt():
    def __init__(self, pasta_das_imagens):

        self.pasta_das_imagens = pasta_das_imagens
        self.cove = [os.path.join(corrente, 'imagens'), 'sample.png']
        self.cover_encontrados = {}
        if os.path.exists(self.pasta_das_imagens):
            self.lista = os.listdir(self.pasta_das_imagens)
            for x in self.lista:
                if procura_coverart.match(x):
                    self.cover_encontrados[x] = x

    def localiza_cover_art(self, codigo_do_jogo=''):
        self.cove = []

        try:
            covex = self.cover_encontrados[codigo_do_jogo + '_COV.png']
            self.cove = [self.pasta_das_imagens, covex]

        except KeyError:
            try:
                covex = self.cover_encontrados[codigo_do_jogo + '_COV.jpg']
                self.cove = [self.pasta_das_imagens, covex]
            except KeyError:
                covex = 'sample.png'
                self.cove = [os.path.join(corrente, 'imagens'), covex]

        return self.cove


class LocalizaJogos():
    def __init__(self, pasta_de_jogos):
        self.lista_ul = []
        self.lista_DVD = []
        self.lista_CD = []
        self.tamanho_total = 0
        self.quant_de_jogos = 0

        self.extrai_ul = ManipulaUl()

        if os.path.exists(os.path.join(pasta_de_jogos, 'ul.cfg')):
            lista_parcial = self.extrai_ul(os.path.join(pasta_de_jogos, 'ul.cfg'))

            self.lista_ul = lista_parcial[0]
            self.tamanho_total = lista_parcial[1]
            self.quant_de_jogos = len(self.lista_ul)
        else:
            pass

        if os.path.exists(os.path.join(pasta_de_jogos, 'DVD')):
            ldvd = os.listdir(os.path.join(pasta_de_jogos, 'DVD'))
            for x in ldvd:
                if procura_cod_e_nome.match(x):
                    self.quant_de_jogos += 1
                    cod_kjh = x[:11]

                    nom_kjh = x[12:-4].decode('latin-1')

                    s = os.stat(os.path.join(pasta_de_jogos, 'DVD', '%s.%s.iso' % (cod_kjh, nom_kjh)))
                    tamanho = s.st_size
                    self.lista_DVD.append(
                        [os.path.join(pasta_de_jogos, 'DVD', '%s.%s.iso' % (x[:11], nom_kjh)), x[:11], x[12:-4],
                         tamanho, '1', '14'])
                    self.tamanho_total += tamanho
        else:
            pass

        if os.path.exists(os.path.join(pasta_de_jogos, 'CD')):
            lcd = os.listdir(os.path.join(pasta_de_jogos, 'CD'))
            for x in lcd:
                if procura_cod_e_nome.match(x):
                    self.quant_de_jogos += 1
                    nomefsd = x[12:-4].decode('latin-1')

                    t = os.stat(os.path.join(pasta_de_jogos, 'CD', '%s.%s.iso' % (x[:11], nomefsd)))
                    tamanho = t.st_size
                    self.lista_CD.append(
                        [os.path.join(pasta_de_jogos, 'CD', '%s.%s.iso' % (x[:11], nomefsd)), x[:11], nomefsd,
                         tamanho, '1', '12'])
                    self.tamanho_total += tamanho
        else:
            pass

        self.lista_total_de_jogos = self.lista_ul + self.lista_DVD + self.lista_CD

        self.jogos_e_info = [self.lista_total_de_jogos, self.quant_de_jogos, self.tamanho_total]
       
    def ordem_alfabetica(self, coluna=False, modo='crescente'):
        """
        coloca a lista de jogos, SELF.JOGOS_E_INFO, em ordem alfabetica sendo:
            @param coluna:
                False, coloca em ordem de codigo, porem ul vem primeiro, depois DVD depois CD
                0, coloca a coluna arquivo em ordem
                1, coloca o codigo
                2, coloca o nome
                3, coloca em ordem de tamanho
            @param modo:
                Coloca em ordem crescente ou decrescente
                @value modo: ['crescente', 'decrescente']
        """

        possiveis = [0, 1, 2, 3, 4, 5, 6]

        if coluna is False:
            if modo == 'decrescente':
                lista_reves = self.jogos_e_info[0]
                lista_reves = lista_reves[::-1]
                self.jogos_e_info = [lista_reves, self.quant_de_jogos, self.tamanho_total]
                return self.jogos_e_info

            return self.jogos_e_info

        elif not coluna in possiveis:
            if modo == 'decrescente':
                lista_reves = self.jogos_e_info[0]
                lista_reves = lista_reves[::-1]
                self.jogos_e_info = [lista_reves, self.quant_de_jogos, self.tamanho_total]
                return self.jogos_e_info

            return self.jogos_e_info
        else:
            organizador = {}
            lista_indice = []
            for x in self.jogos_e_info[0]:
                if coluna == 3:
                    cocoa = "%012d" % x[coluna]
                    novo_indice = "%s%s%s" % (cocoa, str(x[0]), x[1])
                else:
                    novo_indice = "%s%s%s" % (x[coluna], str(x[0]), x[1])
                lista_indice.append(novo_indice)
                organizador[novo_indice] = x
            lista_organizada = []
            lista_indice.sort()
            if modo == 'decrescente':
                lista_indice = lista_indice[::-1]
                
            for x in lista_indice:
                lista_organizada.append(organizador[x])
            self.jogos_e_info = [lista_organizada, self.quant_de_jogos, self.tamanho_total]
            return [lista_organizada, self.quant_de_jogos, self.tamanho_total]            


class ManipulaUl():

    def __init__(self):
        self.progresso = 0
        self.jogos_e_info_ul = ""
        self.zarquivos = ""
        self.tamanho_maximo_fatia = 0
        self.endereco_do_jogo = ""
        self.codigo_do_jogo = 'XXX_000.00'
        self.nome_do_jogo = 'NOME DO JOGO'

    def __call__(self, endereco_do_arquivo):
        self.extrai_ul(endereco_do_arquivo)
        return self.jogos_e_info_ul

    @staticmethod
    def criar_nome_ul(codigo_do_jogo, nome_do_jogo, midia='DVD', quant_de_partes=5):
        cod = 'ul.%s' % codigo_do_jogo
        if midia == 'CD':
            tipo_id = 12
        else:
            tipo_id = 14
        codigo_hex = cod.encode('hex')
        codigo_completo_hex = '%s000%s%s000000000800000000000000000000' % (codigo_hex, quant_de_partes, tipo_id)
        nome_hex = nome_do_jogo.encode('utf-8').encode('hex')
        numnome = len(nome_hex)
        if numnome > 60:
            nome_hex = nome_hex[0:60]
            numnome = len(nome_hex)
        faltantenome = 64 - numnome
        nome_completo_hex = '%s%s' % (nome_hex, '0' * faltantenome)
        results = '%s%s' % (nome_completo_hex.decode('hex'), codigo_completo_hex.decode('hex'))
        results = results.decode('utf-8')
        return results

    @staticmethod
    def criar_nome_base_arquivo(codigo_do_jogo, nome_do_jogo):
        crc = pycrc32.crc32(nome_do_jogo)
        nomebase = 'ul.%08X.%s' % (crc, codigo_do_jogo)
        return nomebase

    def extrai_ul(self, endereco_do_arquivo):
        with open(endereco_do_arquivo, 'r') as arquivo_lido:

            conteudo = arquivo_lido.read()
            conteudo = conteudo.decode('utf-8')

        endereco_base = os.path.dirname(endereco_do_arquivo)
        conteudo_hex = conteudo.encode('utf-8').encode('hex')

        quantidade_de_jogos_no_ul = len(conteudo_hex) / 128
        jogos_separados = []
        inicont = 0
        tamanho_totaldf = 0
        for x in range(quantidade_de_jogos_no_ul):
            pedaco_nome_jogo = conteudo_hex[inicont:inicont + 64]
            pedaco_codigo = conteudo_hex[inicont + 70:inicont + 92]
            pedaco_quant_partes = conteudo_hex[inicont + 95:inicont + 96]
            pedaco_tipo = conteudo_hex[inicont + 96:inicont + 98]
            procs = pedaco_nome_jogo.find('000')
            pedaco_so_o_nome = conteudo_hex[inicont:inicont + procs]
            if len(pedaco_so_o_nome) % 2 == 1:
                pedaco_so_o_nome = "%s0" % pedaco_so_o_nome
            pedaco_codigo_nrm = pedaco_codigo.decode('hex')

            pedaco_so_o_nome_nrm = pedaco_so_o_nome.decode('hex')

            inicont += 128
            nome_base_pedaco = "ul.%08X.%s" % (pycrc32.crc32(pedaco_so_o_nome_nrm.decode('utf-8')), pedaco_codigo_nrm)
            pedacos_encontrados = glob.glob(os.path.join(endereco_base, "%s.*" % nome_base_pedaco))
            tamanhossssd = 0
            for hj in pedacos_encontrados:
                inforhj = os.stat(hj)
                tamtam = inforhj.st_size
                tamanhossssd += tamtam
            tamanho_totaldf += tamanhossssd
            jogos_separados.append(
                [endereco_do_arquivo, pedaco_codigo_nrm, pedaco_so_o_nome_nrm.decode('utf-8'),
                 tamanhossssd, pedaco_quant_partes, pedaco_tipo])
        self.jogos_e_info_ul = [jogos_separados, tamanho_totaldf]

        return self.jogos_e_info_ul

    def juntar_arquivos(self, arquivos, destino='', nome='NOVO_NOME.iso'):
        if not arquivos == list:
            self.zarquivos = [arquivos]
        else:
            self.zarquivos = arquivos
        self.progresso = 0
        gravados = 0
        buffer_local = 1024
        destino = os.path.join(destino, nome)
        with open(destino, "wb") as arquico_alvo:
            tamanho_total = 0
            for f in self.zarquivos:
                vv = os.stat(f)

                tamanho_parcial = vv.st_size
                tamanho_total += tamanho_parcial
            for f in self.zarquivos:
                with open(f, "rb") as arquivo_in:
                    x = os.stat(f)
                    tam = x.st_size
                    while True:
                        y = arquivo_in.read(buffer_local)
                        tam -= buffer_local
                        gravados += buffer_local
                        self.progresso = int((float(gravados) / float(tamanho_total)) * 100)

                        arquico_alvo.write(y)
                        if not tam > 0:
                            break

    def cortar_aquivos(self, endereco_do_jogo, codigo_do_jogo, nome_do_jogo, destino='', buffer_local=1024,
                       tamanho_maximo_fatia=1073741824):

        self.endereco_do_jogo = endereco_do_jogo
        self.codigo_do_jogo = codigo_do_jogo
        self.nome_do_jogo = nome_do_jogo
        self.tamanho_maximo_fatia = tamanho_maximo_fatia  # 1gb  - tamanho_maximo_fatia chapter size
        buffer_local = buffer_local
        fatias = 0
        codigo_crc = "%08X" % self.nome_do_jogo

        endereco_arquivo = self.endereco_do_jogo
        datax = 0
        with open(endereco_arquivo, 'rb') as arquivo_in:
            while True:
                arquivo_alvo = open('%sul.%s.%s.%02d' % (destino, codigo_crc, self.codigo_do_jogo, fatias), 'wb')
                bytes_escritos = 0
                while bytes_escritos < self.tamanho_maximo_fatia:

                    datax = arquivo_in.read(buffer_local)
                    if datax:
                        arquivo_alvo.write(datax)
                        bytes_escritos += buffer_local
                    else:
                        break
                fatias += 1
                if datax:
                    pass
                else:
                    break

    def renomear_jogo_ul(self, pasta_do_arquivo, antigo_nome, novo_nome):
        jog = self.extrai_ul(os.path.join(pasta_do_arquivo, 'ul.cfg'))

        jogos_existentes = jog[0]

        nomes_jogos_existentes = []
        for jjj in jogos_existentes:
            n = jjj[2]
            nomes_jogos_existentes.append(n)
        cocount = 0
        nome_base = novo_nome
        while novo_nome in nomes_jogos_existentes:
            cocount += 1
            novo_nome = '%s - %02d' % (nome_base, cocount)

        crc_antigo_nome = '%08X' % pycrc32.crc32(antigo_nome)

        crc_novo_nome = '%08X' % pycrc32.crc32(novo_nome)

        lista_glob = glob.glob(os.path.join(pasta_do_arquivo, 'ul.%s*' % crc_antigo_nome))

        # renomeados = {}
        # for x in lista_glob:
        # renomeados[x] = x.replace(crc_antigo_nome, crc_novo_nome)
        for x in lista_glob:
            os.rename(x, x.replace(crc_antigo_nome, crc_novo_nome))

        with open(os.path.join(pasta_do_arquivo, 'ul.cfg'), 'r') as aberto:
            lido = aberto.read()

            convertido_hex = lido.encode('hex')
            antigo_nome_hex = antigo_nome.encode('utf-8').encode('hex')
            novo_nome_hex = novo_nome.encode('utf-8').encode('hex')

            intes = max(len(antigo_nome_hex), len(novo_nome_hex))
            falta = intes - min(len(antigo_nome_hex), len(novo_nome_hex))
            acres = '0' * falta
            if max(len(antigo_nome_hex), len(novo_nome_hex)) == len(antigo_nome_hex):
                pass
            else:
                antigo_nome_hex += acres
            if max(len(antigo_nome_hex), len(novo_nome_hex)) == len(novo_nome_hex):
                pass
            else:
                novo_nome_hex += acres

            mudado_hex = convertido_hex.replace(antigo_nome_hex, novo_nome_hex)

            texto_mudado = mudado_hex.decode('hex')

            with open(os.path.join(pasta_do_arquivo, 'ul.cfg'), 'w') as escrever:
                escrever.write(texto_mudado)

        return novo_nome

    def deletar_jogo_ul(self, endereco_pasta, nome_do_jogo):
        jog = self.extrai_ul(os.path.join(endereco_pasta, 'ul.cfg'))

        jogos_existentes = jog[0]

        nomes_jogos_existentes = []
        for jjj in jogos_existentes:
            n = jjj[2]
            nomes_jogos_existentes.append(n)

        crc_nome_do_jogo = '%08X' % pycrc32.crc32(nome_do_jogo)

        lista_glob = glob.glob(os.path.join(endereco_pasta, 'ul.%s*' % crc_nome_do_jogo))

        for x in lista_glob:
            print x
            os.remove(x)

        with open(os.path.join(endereco_pasta, 'ul.cfg'), 'r') as aberto:
            lido = aberto.read()
            lido = lido.decode('utf-8')
            convertido_hex = lido.encode('utf-8').encode('hex')
            nome_do_jogo_hex = nome_do_jogo.encode('utf-8').encode('hex')
            posicao_var = convertido_hex.find(nome_do_jogo_hex)

            pedaco = convertido_hex[posicao_var:posicao_var + 128]

            mudado_hex = convertido_hex.replace(pedaco, '')

            mudado = mudado_hex.decode('hex')

        aberto.close()
        with open(os.path.join(endereco_pasta, 'ul.cfg'), 'w') as escrever:
            escrever.write(mudado)


class Dicionario():

    def __init__(self, dicionario=''):
        self.keys = ""
        self.comp = ""
        if dicionario == "":
            pass
        else:
            self.dicionario_traduzido = {}
            with open(dicionario,  'r') as aberto:
                self.dicionario_traduzido = aberto.readlines()

    def tradutor(self, palavra, dicionario=""):
        """

        """
        traducao = palavra
        if not dicionario == "":
            for x in self.dicionario_traduzido:
                
                if len(x.split(" = ")) == 2:
                    y = x.split(" = ")
                    key = y[0]
                    
                    if key == palavra.encode('utf-8'):
                        traducao = y[1].strip().encode('utf-8').decode('utf-8')
                       
                        break
                    else:
                        traducao = palavra
        return traducao

    def criar_sample(self):
        with open(os.path.join(corrente, 'phanterps2.py'), 'r') as abe:
            f = abe.read()
        achei = re.findall(r'Tradutor\.tradut.*["\'](.*)["\'].*dicionario', f)
        texto = ""
        keys = ""
        comp = []
        for x in achei:
            if not x in comp:
                texto += x + " = " + x + '\n'
                keys += x+'\n'
                comp.append(x)
        with open(os.path.join(corrente, 'language', 'sample.lng'), 'w') as cop:
            cop.write(texto)
        self.keys = keys
        self.comp = comp

    def criar_keys(self):
        self.criar_sample()
        with open(os.path.join(corrente, 'language', 'keys.lng'), 'w') as cop:
            cop.write(self.keys)

    def criar_nova_linguage(self, endereco_traduzido, nome_da_linguagem):
        with open(endereco_traduzido, 'r') as abe:
            f = abe.readlines()
        ct = 0
        df = ""
        for z in self.comp:
            df += z + " = " + f[ct]
            ct += 1
        with open(os.path.join(nome_da_linguagem), 'w') as pis:
            pis.write(df)


def convert_tamanho(valor=''):
    if valor == '':
        tamanho = "Problema ao calcular"
    else:
        valor = long(valor)
        kb = 1024
        mb = 1024 * 1024
        gb = 1024 * 1024 * 1024
        if valor < mb:
            t = valor / kb
            tamanho = "%s KB" % t
        elif valor < gb:
            t = valor / mb
            tamanho = "%s MB" % t

        else:
            t = valor / mb
            t2 = float(valor) / gb
            tamanho = "%s MB ou %.1f GB" % (t, t2)

    return tamanho


def eh_cover_art(endereco_da_imagem):
    if os.path.exists(endereco_da_imagem):
        nome = os.path.basename(endereco_da_imagem)
        if procura_coverart.match(nome):
            return True


def retirar_exitf_imagem(lista_de_imagens):
    if not type(lista_de_imagens) == list:
        lista_de_imagens = [lista_de_imagens]

    for path in lista_de_imagens:
        image = Image.open(path)

        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)

        image_without_exif.save(path)


def muda_nome_jogo(endereco_do_jogo, novo_nome):
    nome_antigo = os.path.basename(endereco_do_jogo)
    endereco = os.path.dirname(endereco_do_jogo)
    codigo_do_jogo = ''
    if procura_apenas_cod2.match(nome_antigo):
        codigo_do_jogo = procura_apenas_cod2.findall(nome_antigo)[0]

    cont = 0
    nome_bade = novo_nome
    while os.path.exists(os.path.join(endereco, u"%s.%s.iso" % (codigo_do_jogo, novo_nome))):
        cont += 1
        novo_nome = u"%s - %02d" % (nome_bade, cont)
    os.rename(endereco_do_jogo, os.path.join(endereco, u"%s.%s.iso" % (codigo_do_jogo, novo_nome)))
    resultado = [os.path.join(endereco, u"%s.%s.iso" % (codigo_do_jogo, novo_nome)), codigo_do_jogo, novo_nome]
    return resultado

#Ferramentas de desenvolvimento
def lista_imagem():

    """
    lista de todas as imagens
    @return: nadica
    """
    extencoes = ['png', 'jpg']
    for z in extencoes:
        x = glob.glob(os.path.join(corrente, 'imagens', '*.%s' % z))
        for y in x:
            retirar_exitf_imagem(y)


def deletararquivos(endereco_arquivo, nome):

    nome_base = os.path.basename(endereco_arquivo)
    if nome_base[:3] == "ul.":
        dir_base = os.path.dirname(endereco_arquivo)
        tool_ul = ManipulaUl()
        tool_ul.deletar_jogo_ul(dir_base, nome)
    else:
        os.remove(endereco_arquivo)


def propagacao ():
    
    programa = (os.path.join(corrente),['py', 'bin'],"")
    imagens = (os.path.join(corrente, 'imagens'),['jpg', 'png', 'ico'],'imagens')
    language = (os.path.join(corrente, 'language'), ['lng'],'language')
    propagar = ['Y:\PhanterPS2', 'Z:\PhanterPS2']

    lista = [programa, imagens, language]
    for x in lista:
        alvo = x[1]
        for y in alvo:
            glo = glob.glob(os.path.join(x[0], '*.%s' % y))
            for z in glo:
                if x[2] == 'imagens':
                    for pro in propagar:
                        print pro
                        with open(z, 'rb') as lendo:
                            lido = lendo.read()
                        with open(os.path.join(pro, 'imagens', os.path.basename(z)), 'wb') as lendo_w:
                            lendo_w.write(lido)
                if x[2] == 'language':
                    for pro in propagar:
                        with open(z, 'rb') as lendo:
                            lido = lendo.read()
                        with open(os.path.join(pro, 'language', os.path.basename(z)), 'wb') as lendo_w:
                            lendo_w.write(lido)
                if x[2] == '':
                    for pro in propagar:
                        with open(z, 'rb') as lendo:
                            lido = lendo.read()
                        with open(os.path.join(pro, os.path.basename(z)), 'wb') as lendo_w:
                            lendo_w.write(lido)

if __name__ == '__main__':
    propagacao()









