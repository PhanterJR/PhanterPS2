# -*- coding: utf-8 -*-
# Copyright &copy; 2014 Junior Polegato
# https://github.com/JuniorPolegato
# Licença LGPL
 
def crc32(string):
 
	crctab = []
	 
	for table in range(256):
		crc = table << 24
		 
		for count in range(8):
			# Em Python o inteiro não tem limite de bits e a sinalização
			# é aparte do número
			# Em C está com limite de 32 bits sendo que o bit mais
			# significativo é a sinalização
			# Então precisa fazer "& 0xFFFFFFFF" em Python para 32 bits
			# e negativo com "crc >> 31 == 1"
			if crc >> 31 == 1:
				crc = (crc << 1) & 0xFFFFFFFF
			else:
				crc = ((crc << 1) & 0xFFFFFFFF) ^ 0x04C11DB7
		crctab.append(crc)
	 
	# O preencimento de crctab foi de 0 a 255, mas em C está invertido,
	# portanto vamos inverter aqui. Observo que, se crctab fosse
	# dicionário, então seguiria o mesmo princípio em C de posições
	# nomeadas por um inteiro (hash).
	crctab = crctab[::-1]
	 
	# String em C é ponteiro de char, e char em C são inteiros
	# sinalizados de 8 bits, e é terminada por zero
	# Em Python não existe esse conceito, então tem que converter
	# a string em lista de inteiros de 8 bits, utilizando completo de 2
	# no caso de números, e terminada por 0
	string = [ord(c) for c in string ]
	string.append(0)
	 
	for byte in string:
		crc = crctab[byte ^ ((crc >> 24) & 0xFF)] ^ ((crc << 8) & 0xFFFFFF00);
	 
	return crc
