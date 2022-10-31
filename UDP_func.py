def complemento(n, tamanho):
    comp = n ^ ((1 << tamanho) - 1)
    return '0b{0:0{1}b}'.format(comp, tamanho)

def checksum(portaorigem,portadestino,comprimento):
	primeirasoma = bin(portaorigem+portadestino)[2:].zfill(16)
	if (len(primeirasoma)>16):
		primeirasoma = primeirasoma[1:17]
		primeirasoma = bin(int(primeirasoma,2) + 1)[2:].zfill(16)
	segundasoma = bin(int(primeirasoma,2)+comprimento)[2:].zfill(16)
	if (len(segundasoma)>16):
		segundasoma = segundasoma[1:17]
		segundasoma = bin(int(segundasoma,2) + 1)[2:].zfill(16)
	checksum = complemento(int(segundasoma,2),16)[2:]
	return int(checksum,2)

def cria_pacote_cliente(portaorigem,portadestino,comprimento,seq,dado):
    soma = checksum(portaorigem,portadestino,comprimento)

    if type(dado) == str:
        dado = dado.encode()

    pacote = f"{portaorigem}".encode().zfill(16)+ \
        f"{portadestino}".encode().zfill(16)+ \
        f'{comprimento}'.encode().zfill(16)+ \
        f'{soma}'.encode().zfill(16)+ \
        f'{seq}'.encode().zfill(1)+ \
        dado
        
    return pacote

def cria_pacote_servidor(portaorigem,portadestino,comprimento,ack,seq):
	soma = checksum(portaorigem,portadestino,comprimento)

	pacote = f'{portaorigem}'.encode().zfill(16)+ \
    f'{portadestino}'.encode().zfill(16)+ \
    f'{comprimento}'.encode().zfill(16)+ \
    f'{ack}'.encode().zfill(1)+ \
    f'{seq}'.encode().zfill(1)+ \
    f'{soma}'.encode().zfill(16)

	return pacote