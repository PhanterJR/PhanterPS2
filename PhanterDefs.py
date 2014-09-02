# -*- coding: utf-8 -*- 
import logging
import os
import re
from contrib import iso9660
from contrib import pycrc32
import string
from ctypes import windll

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

corrente = os.getcwd()


procura_cod_e_nome = re.compile(r'([a-zA-Z]{4}_[0-9]{3}\.[0-9]{2}\..*\.[iI][sS][oO])')
procura_nome_e_cod_no_ul = re.compile(r'([ a-zA-Z0-9]*.*ul\.[ a-zA-Z0-9]{4}_[0-9]{3}\.[0-9]{2})')
procura_apenas_cod = re.compile(r'^/([a-zA-Z]{4}_[0-9]{3}\.[0-9]{2})')
procura_coverart = re.compile(r'(.*_COV\.[jJpP][pPnN][gG])')

class configuracoes():
	def __init__ (self):
		self.configuracoes = ''
		self.config = {}
		try:
			with open(os.path.join(corrente,'phanterps2.cfg'), 'r') as arquivo_cfg:
				self.configuracoes = arquivo_cfg.readlines()
				
				for x in self.configuracoes:
					y = x.split(' = ')
					if len(y) == 1:
						pass
					else:
						self.config[y[0]] = y[1]
			
		except IOError :
			with open(os.path.join(corrente,'phanterps2.cfg'), 'w') as arquivo_cfg:
				padrao = """pasta_destino_jogos = \npasta_cover_art = \ndicionario = \n"""
				arquivo_cfg.write(padrao)
				arquivo_cfg.close()
		self.pasta_padrao_jogos = self.leitor_configuracao('pasta_destino_jogos')
		

	def leitor_configuracao(self, chave=''):
		if chave=='':
			dado = ''
		else:
			try:
				dado = self.config[chave][:-1]
			except KeyError:
				logger.info("configuração não encontrada")
				dado = ''
			return dado

	def mudar_configuracao (self, chave, nova_configuracao):
		if chave=='':
			pass
		else:
			
			self.config[chave] = nova_configuracao+'\n'
			
			with open(os.path.join(corrente,'phanterps2.cfg'), 'w') as arquivo_cfg:
				new_config=''
				for x in self.config:
					new_config += "%s = %s" %(x, self.config[x])
				
				arquivo_cfg.write(new_config)
				arquivo_cfg.close()

def Tradutor (palavra, dicionario = '', isunicode=True):
	"""

	"""
	if isunicode==False:
		pass
	else:
		palavra = palavra.encode('utf-8')
	palavra2 = palavra

	caracteres_para_escape = ['/', '.', '*', '+', '?', '|','(', ')', '[', ']', '{', '}', '\\']

	palavra_em_escape = ''
	for g in palavra2:
		achei = 0
		for f in caracteres_para_escape:
			if g == f:
				achei=1
			else:
				pass
		if achei:
			palavra_em_escape += "\\"+g
		else:
			palavra_em_escape+=g

	if dicionario=='':
		traducao = palavra
		texto_lido=''
		try:
			with open(os.path.join(corrente, 'language', 'sample.lng'), 'r') as palavraprocurada:
				texto = palavraprocurada.read()

				patern = '(%s =.*)' %(palavra_em_escape)
				x = re.findall(patern, texto)

				if not x == []:
					pass
				else:
					texto_lido = texto
					palavraprocurada.close()

					with open(os.path.join(corrente, 'language', 'sample.lng'), 'w') as palavraprocurada:
						escrever = texto_lido+'%s = %s\n' %(palavra,palavra)
						palavraprocurada.write(escrever)
		except IOError:

			with open(os.path.join(corrente, 'language', 'sample.lng'), 'w') as palavraprocurada:
				palavraprocurada.write('%s = %s\n' %(palavra,palavra))
	else:
		with open(dicionario, 'r') as palavraprocurada:
			texto = palavraprocurada.read()

			patern = '(%s =.*)' %(palavra_em_escape)

			x = re.findall(patern, texto)

			if x==[]:
				traducao = palavra
			else:
				y = x[0].find(' = ')
				traducao = x[0][y+3:]
	if isunicode:
		traducao = traducao.decode('utf-8')
	return traducao 

class verifica_jogo():
	def __init__ (self, arquivoiso):
		"""verifica se o arquivo existe. 
		Verifica se o jogo já se encontra com a nomeclatura do OPL (XXX_999.99.NOME_DO_JOGO.iso)
		Abre o arquivo iso para verificar a existência do arquivo launch do jogo (XXX_999.99)
		Se os 3 testes passarem será criado uma lista com tuplas com endereço, código e nome do jogo seguido dos respectivos estados.
		Ex.: [('C:\XXX_999.99.NOME_DO_JOGO.iso', True), ('XXX_999.99',True), ('NOME_DO_JOGO', True)]
		Se não passar a lista será como o exemplo seguinte.
		Ex.: [('C:\COD_INVALIDO.NOME_QUALQUER_DE_JOGO.iso', True), ('', False), ('NOME_DO_JOGO', False)]
		"""
		self.resultado_final = False
		nome_do_arquivo=''
		logger.info("Iniciando classe Varifica_jogo(): %s" %(os.path.exists(endereco_do_jogo)))
		logger.info("Verificando se %s existe" %(os.path.exists(endereco_do_jogo)))
		if os.path.exists(endereco_do_jogo):
			nome_do_arquivo=[]
			nome_do_arquivo = procura_cod_e_nome.findall(endereco_do_jogo)
			self.end_jogo = endereco_do_jogo, True
			self.codigo_do_jogo2 = []
			self.codigo_do_jogo1=''
			self.nome_do_jogo1=''

			if nome_do_arquivo:
				self.codigo_do_jogo1 = nome_do_arquivo[0][:11]
				self.nome_do_jogo1 = nome_do_arquivo[0][12:-4]

			x = self.procura_cod_in_iso(endereco_do_jogo)
			self.codigo_do_jogo2 = x.condigo_encontrado

			self.nome_do_jogo2 = "NOME_DO_JOGO"

			if self.codigo_do_jogo2 == False and nome_do_arquivo == []:
				self.codigo_do_jogo = '', False
				self.nome_do_jogo = '', False
			elif self.codigo_do_jogo2 == False and not nome_do_arquivo ==[]:
				self.codigo_do_jogo = self.codigo_do_jogo1, False
				self.nome_do_jogo = self.nome_do_jogo1, True
			else:
				self.self.codigo_do_jogo = codigo_do_jogo2 or self.codigo_do_jogo1, True
				self.nome_do_jogo = nome_do_jogo1 or nome_do_jogo2, True

			self.resultado_final = [self.end_jogo, self.codigo_do_jogo, self.nome_do_jogo]
		else:
			logger.info("O iso do jogo %s não existe em %s" %(self.nome_do_jogo ,endereco_do_jogo))

	def procura_cod_in_iso(self, endereco):
		x = iso9660.ISO9660(endereco)
		for y in x.tree():
			if procura_apenas_cod.match(y):
				p = procura_apenas_cod.findall(y)
				self.codigo_encontrado = p[0]
			else:
				self.condigo_encontrado=False

class imagens_jogos():
	def __init__ (self, pasta_das_imagens):
		logger.info('Iniciando a Classe localiza_imagem_jogo')

		self.pasta_das_imagens=pasta_das_imagens
		self.cove = [corrente,'sample.jpg']
		self.cover_encontrados = {}
		logger.info('Verificando se "%s" existe' %self.pasta_das_imagens)
		if os.path.exists(self.pasta_das_imagens):
			self.lista = os.listdir(self.pasta_das_imagens)
			logger.debug('lista de arquivos encontrados:%s'%self.lista)
			logger.debug('Criando dicionário com códigos relacionados aos nomes das imagens')
			for x in self.lista:
				if procura_coverart.match(x):
					self.cover_encontrados[x] = x
			logger.debug('dicionario construido: %s' %self.cover_encontrados)			

	def localiza_cover_art (self, codigo_do_jogo=''):
		logger.info('Função localiza_cover_art(): Localizando imagem com o nome "%s_COV"' %(codigo_do_jogo))
		self.cove=[]
		logger.info('Examinando a pasta %s' %(self.pasta_das_imagens))

		try:
			covex = self.cover_encontrados[codigo_do_jogo+'_COV.png']
			self.cove = [self.pasta_das_imagens, covex]
			logger.info(self.cove)
			
		except KeyError:
			try: 
				covex = self.cover_encontrados[codigo_do_jogo+'_COV.jpg']
				self.cove = [self.pasta_das_imagens, covex]
				logger.info(self.cove)
			except KeyError:
				covex = 'sample.jpg'
				self.cove = [corrente, covex]
				logger.info(self.cove)


		logger.info('localizado %s em %s' %(self.cove[1],self.cove[0]))
		return self.cove

class lista_de_jogos ():
	def __init__ (self, pasta_de_jogos):
		logger.info('Função lista_de_jogos(): Examinando pasta %s'%pasta_de_jogos)
		self.lista_ul=[]
		self.lista_DVD=[]
		self.lista_CD=[]
		self.tamanho_total = 0
		self.quant_de_jogos = 0

		logger.info('verificando se %s existe' %(os.path.join(pasta_de_jogos, 'ul.cfg')))
		if os.path.exists(os.path.join(pasta_de_jogos, 'ul.cfg')):
			lista_parcial = self.extrai_ul(os.path.join(pasta_de_jogos, 'ul.cfg'))
			self.lista_ul = lista_parcial[0]
			self.tamanho_total = lista_parcial[1]
			self.quant_de_jogos=len(self.lista_ul)
			logger.info('Adicionando jogos do ul, encontrado(s) %s jogos' %(self.quant_de_jogos))
		else:
			logger.info('Arquivo "%s" não existe' %os.path.join(pasta_de_jogos, 'ul.cfg'))

		logger.info('verificando se "%s" existe' %(os.path.join(pasta_de_jogos, 'DVD')))

		if os.path.exists(os.path.join(pasta_de_jogos, 'DVD')):
	 		lDVD = os.listdir(os.path.join(pasta_de_jogos, 'DVD'))
			for x in lDVD:
				if procura_cod_e_nome.match(x):
					self.quant_de_jogos+=1
					s = os.stat(os.path.join(pasta_de_jogos, 'DVD', '%s.%s.iso' %(x[:11], x[12:-4])))
					tamanho = s.st_size
					self.lista_DVD.append([os.path.join(pasta_de_jogos, 'DVD', '%s.%s.iso' %(x[:11], x[12:-4])), x[:11], x[12:-4], tamanho])
					self.tamanho_total+=tamanho
			logger.info('Adicionando jogos da pasta DVD, encontrado(s) %s jogos' %(len(self.lista_DVD)))
		else:
			logger.info('A pasta "%s" não existe' %os.path.join(pasta_de_jogos, 'DVD'))

		logger.info('verificando se "%s" existe' %(os.path.join(pasta_de_jogos, 'CD')))
		if os.path.exists(os.path.join(pasta_de_jogos, 'CD')):
			lCD = os.listdir(os.path.join(pasta_de_jogos, 'CD'))
			for x in lCD:
				if procura_cod_e_nome.match(x):
					self.quant_de_jogos+=1
					t = os.stat(os.path.join(pasta_de_jogos, 'CD', '%s.%s.iso' %(x[:11], x[12:-4])))
					tamanho = t.st_size
					self.lista_CD.append([os.path.join(pasta_de_jogos, 'CD', '%s.%s.iso' %(x[:11], x[12:-4])), x[:11], x[12:-4], tamanho])
					self.tamanho_total+=tamanho
			logger.info('Adicionando jogos da pasta CD, encontrado(s) %s jogos' %(len(self.lista_CD)))
		else:
			logger.info('A pasta "%s" não existe' %os.path.join(pasta_de_jogos, 'CD'))

		c = self.lista_ul+self.lista_DVD+self.lista_CD
		self.jogos_e_info = [c, self.quant_de_jogos, self.tamanho_total]

	def extrai_ul(self, endereco_do_arquivo):
		logger.info('função extrair_ul:Examinando %s'%endereco_do_arquivo)
		self.jogos_ul_encontrados = []
		self.tamanho_total_ul=0
		try:
			logger.debug('Tentando abrir %s' %endereco_do_arquivo)
			with open(endereco_do_arquivo, 'r') as dados:
				dados = dados.read()
				if dados =='':
					pass
				else:
					dados = dados.encode('hex')
					LUL = os.listdir(endereco_do_arquivo[0:-7])

					conter=0
					for x in range(len(dados)/128):
						y = dados[0+conter:conter+128]
						conter += 128
						cod, nom = y[70:92], y[0:64]
						p = nom.find('00')
						nom = nom[:p]
						cod1=cod.decode('hex')
						nom1=nom.decode('hex')
						crc = pycrc32.crc32(nom1)

						partes = []
						for j in LUL:
							patern = 'ul.%X.*' %(crc)
							if re.match(patern, j):

								partes.append(j)
						tamtot = 0
						for tt in partes:
							pp=os.stat(os.path.join(endereco_do_arquivo[0:-7], tt))
							tama = pp.st_size
							tamtot += tama
						self.tamanho_total_ul += tamtot
						self.jogos_ul_encontrados.append([endereco_do_arquivo, cod1, nom1, tamtot])
					logger.info('Encontrado no %s jogos no ul.cfg' %(len(self.jogos_ul_encontrados)))
		except IOError:
			logger.info('Arquivo cfg.ul não encontrado em %s' %(endereco_do_arquivo))
			pass
		ct = 0
		self.jogos_e_info_ul = [self.jogos_ul_encontrados, self.tamanho_total_ul]
		return self.jogos_e_info_ul


def convert_tamanho(valor=''):
	logger.info('Função convert_tamanho: Convertendo %s' %(valor))
	if valor =='':
		tamanho = "Problema ao calcular"
	else:
		valor= long(valor)
		KB = 1024
		MB = 1024*1024
		GB = 1024*1024*1024
		if valor < MB:
			t = valor/KB
			tamanho = "%s KB" %(t)
		elif valor < GB:
			t = valor/MB
			tamanho = "%s MB" %(t)	
	
		else:
			t = valor/MB
			t2 = float(valor)/GB
			tamanho = "%s MB ou %.1f GB" %(t, t2)

	return tamanho

def drivers_do_windows():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    print bitmask
    for letter in string.uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives


