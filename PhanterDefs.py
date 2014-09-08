# -*- coding: utf-8 -*- 
import logging
import os
import re
from contrib import iso9660
from contrib import pycrc32
import string
#from ctypes import windll
import glob
from PIL import Image

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

corrente = os.getcwd()

procura_cod_e_nome = re.compile(r'([a-zA-Z]{4}_[0-9]{3}\.[0-9]{2}\..*\.[iI][sS][oO])$')
procura_nome_e_cod_no_ul = re.compile(r'([ a-zA-Z0-9]*.*ul\.[ a-zA-Z0-9]{4}_[0-9]{3}\.[0-9]{2})')
procura_apenas_cod = re.compile(r'^/([a-zA-Z]{4}_[0-9]{3}\.[0-9]{2})')
procura_apenas_cod2 = re.compile(r'^([a-zA-Z]{4}_[0-9]{3}\.[0-9]{2})')
procura_coverart = re.compile(r'(.*_COV\.[jJpP][pPnN][gG])$')

class configuracoes():
	def __init__ (self, nome_do_arquivo='phanterps2.cfg'):
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
		except IOError :
			with open(os.path.join(corrente, nome_do_arquivo), 'w') as arquivo_cfg:
				padrao = ""
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
			return dado if not dado == '\r' else ''

	def mudar_configuracao (self, chave, nova_configuracao):
		if chave=='':
			pass
		else:
			
			self.config[chave] = nova_configuracao+'\n'
			
			with open(os.path.join(corrente, self.nome_do_arquivo), 'w') as arquivo_cfg:
				new_config=''
				for x in self.config:
					new_config += "%s = %s" %(x, self.config[x])
				
				arquivo_cfg.write(new_config)

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
		logger.info("Iniciando classe Varifica_jogo(): %s" %(arquivoiso))
		logger.info("Verificando se %s existe" %(arquivoiso))
		if os.path.exists(arquivoiso):
			nome_do_arquivo=[]
			nome_do_arquivo = procura_cod_e_nome.findall(arquivoiso)
			logger.debug('O nome do arquivo é: %s' %(nome_do_arquivo))
			self.end_jogo = arquivoiso, True

			self.codigo_do_jogo1=False
			self.nome_do_jogo1=''

			if not nome_do_arquivo == []:
				self.codigo_do_jogo1 = nome_do_arquivo[0][:11]
				self.nome_do_jogo1 = nome_do_arquivo[0][12:-4]

			self.procura_cod_in_iso(arquivoiso)


			self.nome_do_jogo2 = "NOME_DO_JOGO"
			self.codigo_do_jogo = self.codigo_do_jogo1 if self.codigo_encontrado==False else self.codigo_encontrado, True if not self.codigo_encontrado==False else False
			self.nome_do_jogo = self.nome_do_jogo1 or self.nome_do_jogo2, True

			s = os.stat(arquivoiso)
			tamanho = s.st_size

			self.resultado_final = [self.end_jogo, self.codigo_do_jogo, self.nome_do_jogo, tamanho]
			logger.debug('resultado final da verificação: %s' %self.resultado_final)
		else:
			logger.info("O iso do jogo %s não existe em %s" %(self.nome_do_jogo, arquivoiso))

	def procura_cod_in_iso(self, endereco):
		logger.debug(u'Iniciando Funcao procura_cod_in_iso: procurando código em %s' %endereco)
		
		try:
			x = iso9660.ISO9660(endereco)
		except:
			x=False
			print "Erro na checagem"
		self.codigo_encontrado=False
		if x:
			for y in x.tree():
				if procura_apenas_cod.match(y):
					p = procura_apenas_cod.findall(y)
					self.codigo_encontrado = p[0]
					logger.debug(u'Código encontrado: %s' %self.codigo_encontrado)
				else:
					logger.debug('código não encontrado, retornando False')
		logger.debug(u'resultado da procura do código: %s' %self.codigo_encontrado)

class imagens_jogos():
	def __init__ (self, pasta_das_imagens):
		logger.info('Iniciando a Classe localiza_imagem_jogo')

		self.pasta_das_imagens=pasta_das_imagens
		self.cove = [os.path.join(corrente, 'imagens'),'sample.jpg']
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
				self.cove = [os.path.join(corrente,'imagens'), covex]
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

		self.extrai_ul = manipula_ul()

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
			logger.info('Localizando os jogos na pasta DVD')
			lDVD = os.listdir(os.path.join(pasta_de_jogos, 'DVD'))
			logger.debug('localizados: %s' %lDVD)
			for x in lDVD:
				if procura_cod_e_nome.match(x):
					logger.debug('Verificando o tamanho do arquivo %s' %x)
					self.quant_de_jogos+=1
					s = os.stat(os.path.join(pasta_de_jogos, 'DVD', u'%s.%s.iso' %(x[:11], x[12:-4])))
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

		self.lista_total_de_jogos = self.lista_ul+self.lista_DVD+self.lista_CD
		self.jogos_e_info = [self.lista_total_de_jogos, self.quant_de_jogos, self.tamanho_total]

class manipula_ul():
	def __init__ (self):
		self.progresso=0
		pass

	def __call__ (self, endereco_do_arquivo):
		self.extrai_ul(endereco_do_arquivo)
		return self.jogos_e_info_ul
				
	def criar_nome_ul (self, codigo_do_jogo, nome_do_jogo):
		cod = 'ul.%s' %(codigo_do_jogo)
		codigo_hex = cod.encode('hex')
		codigo_completo_hex = '%s000014000000000800000000000000000000' %(codigo_hex)
		nome_hex = nome_do_jogo.encode('hex')
		numnome = len(nome_hex)
		if numnome > 60:
			nome_hex = nome_hex[0:60]
			numnome = len(nome_hex)
		faltantenome = 64 - numnome
		nome_completo_hex = '%s%s' %(nome_hex, '0'*faltantenome)
		results = '%s%s' %(nome_completo_hex.decode('hex'), codigo_completo_hex.decode('hex'))
		return results

	def criar_nome_base_arquivo(self, codigo_do_jogo, nome_do_jogo):
		crc = pycrc32.crc32(nome_do_jogo)
		nomebase ='ul.%08X.%s' %(crc, codigo_do_jogo)
		return nomebase

	def extrai_ul(self, endereco_do_arquivo, renomear=False, novo_nome=''):
		logger.info(u'função extrair_ul:Examinando %s'%endereco_do_arquivo)
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
							patern = 'ul.%08X.*' %(crc)
							if re.match(patern, j):

								partes.append(j)
						tamtot = 0
						for tt in partes:
							pp=os.stat(os.path.join(endereco_do_arquivo[0:-7], tt))
							tama = pp.st_size
							tamtot += tama
						self.tamanho_total_ul += tamtot
						self.jogos_ul_encontrados.append([endereco_do_arquivo, cod1, nom1, tamtot])
					logger.info('Encontrado %s jogos no ul.cfg' %(len(self.jogos_ul_encontrados)))
		except IOError:
			logger.info(u'Arquivo cfg.ul não encontrado em %s' %(endereco_do_arquivo))
			pass
		ct = 0
		self.jogos_e_info_ul = [self.jogos_ul_encontrados, self.tamanho_total_ul]
		return self.jogos_e_info_ul

	def juntar_arquivos (self, arquivos, destino='', nome='NOVO_NOME.iso'):
		if not arquivos == list():
			self.zarquivos = [arquivos]
		else:
			self.zarquivos = arquivos
		self.progresso=0
		gravados = 0
		BUFFER = 1024
		destino = os.path.join(destino, nome)
		with open(destino, "wb") as arquico_alvo:
			tamanho_total=0
			for f in self.zarquivos:
				print f
				vv = os.stat(f)

				tamanho_parcial = vv.st_size
				tamanho_total += tamanho_parcial
			for f in self.zarquivos:
				with open(f, "rb") as arquivo_in:
					x = os.stat(f)
					tam = x.st_size
					while True:
						y = arquivo_in.read(BUFFER)
						tam-=BUFFER
						gravados +=BUFFER
						self.progresso = int((float(gravados)/float(tamanho_total))*100)

						arquico_alvo.write(y)
						if not tam > 0:
							break


	def cortar_aquivos(self, endereco_do_jogo, codigo_do_jogo, nome_do_jogo, destino='', BUFFER = 1024, tamanho_maximo_fatia = 1073741824):

		self.endereco_do_jogo = endereco_do_jogo
		self.codigo_do_jogo = codigo_do_jogo
		self.nome_do_jogo = nome_do_jogo
		self.tamanho_maximo_fatia  = tamanho_maximo_fatia # 1GB  - tamanho_maximo_fatia chapter size
		self.BUFFER  = BUFFER 
		fatias = 0
		codigo_crc = "%08X" %(self.nome_do_jogo)

		ARQUIVO = self.endereco_do_jogo
		contador_de_bytes_gravados=0
		fim=False
		with open(ARQUIVO, 'rb') as arquivo_in:
			while True:
				arquivo_alvo = open('%sul.%s.%s.%02d' %(destino, codigo_crc, self.codigo_do_jogo, fatias), 'wb')
				bytes_escritos = 0
				while bytes_escritos < self.tamanho_maximo_fatia:

					datax = arquivo_in.read(self.BUFFER)
					if datax:
						arquivo_alvo.write(datax)
						bytes_escritos += self.BUFFER
					else:
						fim = True
						break
				fatias+=1
				if datax:
					pass
				else:
					break
	def renomear_jogo_ul (self, pasta_do_arquivo, antigo_nome, novo_nome):
		jog = self.extrai_ul(os.path.join(pasta_do_arquivo,'ul.cfg'))
		
		jogos_existentes = jog[0]

		nomes_jogos_existentes = []
		for jjj in jogos_existentes:
			n = jjj[2]
			nomes_jogos_existentes.append(n)
		cocount = 0
		nome_base = novo_nome
		while novo_nome in nomes_jogos_existentes:
				cocount+=1
				novo_nome = '%s - %02d' %(nome_base, cocount)

		crc_antigo_nome = '%08X' %pycrc32.crc32(antigo_nome)

		crc_novo_nome = '%08X' %pycrc32.crc32(novo_nome)

		lista_glob = glob.glob(os.path.join(pasta_do_arquivo, 'ul.%s*' %crc_antigo_nome))

		# renomeados = {}
		# for x in lista_glob:
		# 	renomeados[x] = x.replace(crc_antigo_nome, crc_novo_nome)
		for x in lista_glob:
			os.rename(x, x.replace(crc_antigo_nome, crc_novo_nome))
		with open(os.path.join(pasta_do_arquivo, 'ul.cfg'), 'r') as aberto:
			lido =  aberto.read()

			convertido_hex = lido.encode('hex')
			antigo_nome_hex = antigo_nome.encode('hex')
			novo_nome_hex = novo_nome.encode('hex')

			intes= max(len(antigo_nome_hex), len(novo_nome_hex))
			falta = intes - min(len(antigo_nome_hex), len(novo_nome_hex))
			acres = '0'*falta
			if max(len(antigo_nome_hex), len(novo_nome_hex)) == len(antigo_nome_hex):
				pass
			else:
				antigo_nome_hex +=acres
			if max(len(antigo_nome_hex), len(novo_nome_hex)) == len(novo_nome_hex):
				pass
			else:
				novo_nome_hex +=acres	


			mudado_hex = convertido_hex.replace(antigo_nome_hex, novo_nome_hex)

			mudado = mudado_hex.decode('hex')

		aberto.close()
		with open(os.path.join(pasta_do_arquivo, 'ul.cfg'), 'w') as escrever:
			escrever.write(mudado)
		return novo_nome

	def deletar_jogo_ul (self, endereco_pasta, nome_do_jogo):
		jog = self.extrai_ul(os.path.join(endereco_pasta,'ul.cfg'))
		
		jogos_existentes = jog[0]

		nomes_jogos_existentes = []
		for jjj in jogos_existentes:
			n = jjj[2]
			nomes_jogos_existentes.append(n)

		crc_nome_do_jogo = '%08X' %pycrc32.crc32(nome_do_jogo)

		lista_glob = glob.glob(os.path.join(endereco_pasta, 'ul.%s*' %crc_nome_do_jogo))

		for x in lista_glob:
			os.remove(x)
			print 'removendo arquivo %s' %x

		with open(os.path.join(endereco_pasta, 'ul.cfg'), 'r') as aberto:
			lido =  aberto.read()
			convertido_hex = lido.encode('hex')
			nome_do_jogo_hex = nome_do_jogo.encode('hex')
			posicao_var = convertido_hex.find(nome_do_jogo_hex)
			print posicao_var
			pedaco = convertido_hex[posicao_var:posicao_var+128]
			print pedaco.decode('hex')

			mudado_hex = convertido_hex.replace(pedaco, '')

			mudado = mudado_hex.decode('hex')
			print mudado

		aberto.close()
		with open(os.path.join(endereco_pasta, 'ul.cfg'), 'w') as escrever:
			escrever.write(mudado)


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

# def drivers_do_windows():
# 	drives = []
# 	bitmask = windll.kernel32.GetLogicalDrives()
# 	print bitmask
# 	for letter in string.uppercase:
# 		if bitmask & 1:
# 			drives.append(letter)
# 		bitmask >>= 1

# 	return drives

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

def retirar_exitf_imagem(lista_de_imagens):
	arquivos = glob.glob(os.path.join('D:\\','PS2','ART','*.png'))
	if not lista_de_imagens == list():
		lista = []
		lista.append(lista_de_imagens)
		lista_de_imagens = lista 

	for path in lista_de_imagens:
		image = Image.open(path)

		data = list(image.getdata())
		image_without_exif = Image.new(image.mode, image.size)
		image_without_exif.putdata(data)
		filename = os.path.basename(path).replace('-','_')

		image_without_exif.save(path)

def muda_nome_jogo(endereco_do_jogo, novo_nome):
	nome_antigo = os.path.basename(endereco_do_jogo)
	nome_do_arquivo = os.path.basename(endereco_do_jogo)
	endereco = os.path.dirname(endereco_do_jogo)
	codigo_do_jogo=''
	if procura_apenas_cod2.match(nome_antigo):
		codigo_do_jogo=procura_apenas_cod2.findall(nome_antigo)[0]
		apenas_nome = nome_do_arquivo.split('.')[-2]
	else:
		apenas_nome = nome_do_arquivo.split('.')[-2]

	cont = 0
	nome_bade = novo_nome
	while os.path.exists(os.path.join(endereco, u"%s.%s.iso" %(codigo_do_jogo, novo_nome))):
		cont += 1
		novo_nome = u"%s - %02d" %(nome_bade, cont)
	os.rename(endereco_do_jogo, os.path.join(endereco, u"%s.%s.iso" %(codigo_do_jogo, novo_nome)))
	resultado = [os.path.join(endereco, u"%s.%s.iso" %(codigo_do_jogo, novo_nome)), codigo_do_jogo , novo_nome]
	return resultado


if __name__ == '__main__':
	x = manipula_ul()
	y = x.criar_nome_ul('SLPM_234.23', 'Vai_cagar')
	print y
