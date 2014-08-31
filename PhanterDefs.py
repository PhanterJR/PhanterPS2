# -*- coding: utf-8 -*- 
import os
import re
from contrib import iso9660
from contrib import pycrc32

corrente = os.getcwd()


procura_cod_e_nome = re.compile(r'([a-zA-Z]{4}_[0-9]{3}\.[0-9]{2}\..*\.[iI][sS][oO])')
procura_nome_e_cod_no_ul = re.compile(r'([ a-zA-Z0-9]*.*ul\.[ a-zA-Z0-9]{4}_[0-9]{3}\.[0-9]{2})')
procura_apenas_cod = re.compile(r'^/([a-zA-Z]{4}_[0-9]{3}\.[0-9]{2})')
procura_coverart = re.compile(r'(.*_COV\.[jJpP][pPnN][gG])')

def leitor_configuracao(chave=''):
	config = {}
	try:
		with open('phanterps2.cfg', 'r') as arquivo_cfg:
			configuracoes = arquivo_cfg.readlines()
			for x in configuracoes:
				y = x.split(' = ')
				config[y[0]] = y[1]

	except IOError :
		with open('phanterps2.cfg', 'w') as arquivo_cfg:
			arquivo_cfg.close()

	if chave=='':
		dado = ''
	else:
		try:
			dado = config[chave]
		except KeyError:
			print "A chave %s não foi encontrada nas configurações" %chave
			dado = ''
		return dado


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
			with open(corrente +'\language\sample.lng', 'r') as palavraprocurada:
				texto = palavraprocurada.read()

				patern = '(%s =.*)' %(palavra_em_escape)
				x = re.findall(patern, texto)

				if not x == []:
					pass
				else:
					texto_lido = texto
					palavraprocurada.close()

					with open(corrente +'\language\sample.lng', 'w') as palavraprocurada:
						escrever = texto_lido+'%s = %s\n' %(palavra,palavra)
						palavraprocurada.write(escrever)
		except IOError:

			with open(corrente +'\language\sample.lng', 'w') as palavraprocurada:
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

def localiza_cover_art (pasta_de_jogos, codigo_do_jogo=''):
	if os.path.exists(pasta_de_jogos+'\ART'):
		lista = os.listdir(pasta_de_jogos+'\ART')
		cover_encontrados = {}
		for x in lista:
			if procura_coverart.match(x):
				cover_encontrados[x] = x
		if codigo_do_jogo=='':
			cove = []
			for x in cover_encontrados:
				cove.append(cover_encontrados[x])
		else:
			try:
				covex = cover_encontrados[codigo_do_jogo+'_COV.png']
				
			except KeyError:
				try: 
					covex = cover_encontrados[codigo_do_jogo+'_COV.jpg']
				except KeyError:
					covex = 'sample.jpg'
					
			cove = [pasta_de_jogos+'\ART', covex]


	return cove



def extrai_ul(endereco_do_arquivo):
	jogos_encontrados = []
	try:
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
						pp=os.stat(endereco_do_arquivo[0:-7]+'\\'+tt)
						tama = pp.st_size
						tamtot += tama
					

					jogos_encontrados.append([endereco_do_arquivo, cod1, nom1, tamtot])
	except IOError:
		print 'Arquivo cfg.ul não encontrado em %s' %(endereco_do_arquivo)
		pass
	ct = 0


	return jogos_encontrados

extrai_ul('D:\PS2\ul.cfg')

def lista_de_jogos (pasta_de_jogos):
	lista_ul=[]
	lista_DVD=[]
	lista_CD=[]

	if os.path.exists(pasta_de_jogos+'\ul.cfg'):
		lista_ul = extrai_ul(pasta_de_jogos+'\ul.cfg')

	if os.path.exists(pasta_de_jogos+'\DVD'):
 
		lDVD = os.listdir(pasta_de_jogos+'\DVD')
		for x in lDVD:
			if procura_cod_e_nome.match(x):
				s = os.stat(pasta_de_jogos+'\DVD\%s.%s.iso' %(x[:11], x[12:-4]))
				tamanho = s.st_size
				lista_DVD.append([pasta_de_jogos+'\DVD\%s.%s.iso' %(x[:11], x[12:-4]), x[:11], x[12:-4], tamanho])

	if os.path.exists(pasta_de_jogos+'\CD'):

		lCD = os.listdir(pasta_de_jogos+'\CD')
		for x in lCD:
			if procura_cod_e_nome.match(x):
				t = os.stat(pasta_de_jogos+'\CD\%s.%s.iso' %(x[:11], x[12:-4]))
				tamanho = t.st_size
				lista_CD.append([pasta_de_jogos+'\CD\%s.%s.iso' %(x[:11], x[12:-4]), x[:11], x[12:-4], tamanho])

	c = lista_ul+lista_DVD+lista_CD
	return c

def convert_tamanho(valor=''):
	if valor =='':
		tamanho = "Problema ao calcular"
	else:
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



