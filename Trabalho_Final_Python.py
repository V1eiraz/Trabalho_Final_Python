
#	Linha = modelo fixo
#	OnibusDia = instância real do ônibus naquele dia

import os
import numpy as np
from colorama import init, Fore, Back, Style
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date, time, timedelta
from pathlib import Path
#=================================== TRATAMENTO DE ERROS ==========================================
erro_nao_inteiro = (Fore.RED+"||	  Apenas Numeros inteiros sao permitidos"+Style.RESET_ALL)
opcao_invalida = (Fore.RED+"||	Opção invalida!! Escolha novamente."+Style.RESET_ALL)

#=======================================	CLASSES		===========================================

class Cidade:
	def __init__(self, nome):
		self.nome = nome

	def __repr__ (self):
		return f"{self.nome}"

CIDADES = [
	
]


class OnibusDia:						#Uma linha de ônibus existe todos os dias, mas a reserva de assentos é diferente em cada data.
	def __init__ (self, linha:"LinhaOnibus", data: date):
		self.linha = linha				# a rota que o onibus vai fazer
		self.data  	= data				# o dia da viagem
		self.assentos = [False] * 20 	# situação dos 20 assentos // False = Livre || True = Ocupado
		self.vendas =[]					# armazena as vendas feitas
	
	def reservar(self, n, comprador="manual"):				# Tenta receber algum assento , retorna true, msg) se der certo, ou (false, msg) se falhar.
		if n < 1 or n > 20:
			return False, "Assento inválido"
		if self.assentos[n-1]:
			return False, "Assento ocupado"
		self.assentos [n-1] = True		#reservando o assento
		self.vendas.append((n, self.linha.valor, datetime.now(),comprador))
		return True, "Reserva ok"
	
	def assentos_disponiveis(self):		#Lista quais assentos estão disponiveis
		return [i+1 for i, ocupado in enumerate(self.assentos) if not ocupado]

class LinhaOnibus: # a rota dos onibus
	def __init__(self, origem:Cidade, destino:Cidade, horario, valor):
	#	Objetos:
		self.origem = origem		#Objeto Cidade
		self.destino = destino
		try: #valida o horário
			h, m = map(int, horario.split(':'))
			self.horario = time(h, m)
		except Exception:
			raise ValueError("Formato de horário inválido , esperando (HH:MM)")
		self.valor= float(valor)
		self.onibus_por_data = {}
	
	def cria_onibus_por_data(self, data: date):	#Cria um ônibus (OnibusDia) para a data se ainda não existir
		if data not in self.onibus_por_data:
			self.onibus_por_data[data] = OnibusDia(self, data)
	
	def get_onibus(self, data:date):	#Retorna o OnibusDia de uma data, ou None se não existir
		return self.onibus_por_data.get(data, None)
	
class SistemaPassagens:
	def __init__ (self):
		self.cidades = CIDADES[:] #copia as cidades ja criadas
		self.linhas  = []	#lista de linhas cadastradas
		self.reservas_negadas= []	#historico de tentativas de reserva negadas
		self.reservas = []  # Adicionado para armazenar reservas bem-sucedidas (origem, destino, horario(time), data(date), assento, valor, datetime_venda)

	def adicionar_cidades(self, nome):				#usada quando o usuário digita uma cidade nova que não existia.
		cidade = Cidade(nome)
		self.cidades.append(cidade)
		return cidade
	
	def buscar_cidade(self, nome):					# Usada pra saber se a cidade já existe na base do sistema.
		for c in self.cidades:
			if c.nome.lower() == nome.lower():
				return c 
		return None
	
	def obter_criar_cidade(self, nome):				#procura uma cidade, se não existir ela cria
		cidade = self.buscar_cidade(nome)
		if cidade is None:
			cidade = self.adicionar_cidades(nome)
			print(Fore.GREEN+f"||	Cidade {cidade} foi cadastrada !"+Style.RESET_ALL)
		return cidade

	def exibirTabela(self): #função para exbiir as linhas e todos os respectivos 30 dias futuros dessas linhas com a quantidade de assentos disponiveis 
		print("="*65)
		print(Fore.GREEN + "||		  TABELA DE HORARIOS ÔNIBUS"+Fore.WHITE)
		print("||","-"*62)
		
		if not self.linhas:
			print(Fore.RED+"||		Não há linhas cadastradas ainda."+Style.RESET_ALL)
			return

		for i, linha in enumerate(self.linhas, start= 1):
			print(f"||	{i}. {linha.origem.nome} --> {linha.destino.nome}")#exibir a linha
			print(f"||	Horario : {linha.horario}")	#o horario da linha
			print(f"|| 	Valor : R${linha.valor:.2f}")	#o valor da linha

			if linha.onibus_por_data:
				print("||  Datas com ônibus criados:")
				for data, onibus in linha.onibus_por_data.items():#os proximos 30 dias disponiveis com reservas livres
					livres = len(onibus.assentos_disponiveis())
					print("||	Assentos livres ",Fore.YELLOW+f"[{data}]"+Style.RESET_ALL, f": {livres}/20")
			else:
				print(Fore.RED+"||		Nenhum ônibus criado ainda."+Style.RESET_ALL)
    
	def cadastrar_linha(self): #menu para cadastrar uma nova linha no sistema
		print("||")
		print(Fore.BLUE+"||			CADASTRAR NOVA LINHA	"+Style.RESET_ALL)
		origem_nome = input("||	Insira o nome da Cidade de Origem: ").strip()
		destino_nome =input("||	Insira o nome da Cidade de Destino: ").strip()

		origem = self.obter_criar_cidade(origem_nome)
		destino = self.obter_criar_cidade(destino_nome)
		
		while True: #vai receber o horario
			horario =input("||	Insira o horario de partida do onibus (HH:MM): ")
			try:
				h, m = map(int, horario.split(':'))
				_ = time(h, m)  # validação
				break
			except Exception:
				print(Fore.RED + "|| Formato Inválido!! Use (HH:MM)" + Style.RESET_ALL)
				
		while True:	
			try:
				valor =float(input(f"||	Insira o valor da passagem {origem.nome}  -->  {destino.nome}: R$ "))
				break
			except ValueError:
				print(erro_nao_inteiro)
				
		nova = LinhaOnibus(origem, destino, horario, valor) #criando a linha
		self.linhas.append(nova)
  
		hoje = date.today() #criando onibus para os proximos 30 dias
		for i in range(30):
			data_futura = hoje + timedelta(days=i)
			nova.cria_onibus_por_data(data_futura)
   
		print(Fore.GREEN+"|| 	Linha cadastrada com sucesso !"+Style.RESET_ALL)
		print(Fore.GREEN+"|| 	Ônibus criado para os próximos 30 dias !"+Style.RESET_ALL)

	def consultar_passagens_cidade(self):	#menu para consultar se existe uma linha na cidade fornecida
		cidade_nome = input("|| Insira o nome da cidade para consultar horários: ")
		cidade = self.buscar_cidade(cidade_nome)
		if not cidade:
			print(Fore.RED+"|| Cidade não encontrada."+Style.RESET_ALL)
			return
		print(f"|| Horários disponíveis para {cidade}:")
		encontrado = False
		for linha in self.linhas:
			if linha.origem == cidade or linha.destino == cidade:
				print(f"|| {linha.origem} --> {linha.destino} | Horário: {linha.horario} | Valor: R${linha.valor:.2f}")
				encontrado = True
		if not encontrado:
			print(Fore.RED+"|| Nenhum horário encontrado."+Style.RESET_ALL)

	def consultar_assentos_disponiveis(self): #menu para consultar quais assentos estão disponiveis e fazer a reserva de assentos
		print("||")
		print(Fore.BLUE+"||		CONSULTAR ASSENTOS DISPONÍVEIS	"+Style.RESET_ALL)
		destino_nome = input("|| Insira a cidade de destino: ").strip()
		horario = input("|| Insira o horário (hh:mm): ").strip()
		data = input("|| Insira a data (dd/mm/aaaa): ").strip()
		
		# Valida e converte a data
		try:
			data = datetime.strptime(data, "%d/%m/%Y").date()
			data_atual = datetime.now().date()
			if (data - data_atual).days >= 30 or data < data_atual:
				print("|| Data inválida: deve ser inferior a 30 dias e futura.")
				return
		except ValueError:
			print(Fore.RED+"|| Formato de data inválido."+Style.RESET_ALL)
			return
		
		#busca a linha com as informaçoes recebidas
		linha_encontrada = None
		for linha in self.linhas:
			if linha.destino.nome.lower() == destino_nome.lower() and linha.horario == time(*map(int, horario.split(':'))):
				linha_encontrada = linha
				break
		if not linha_encontrada:
			print(Fore.RED+"|| Linha não encontrada para o destino e horário especificados."+Style.RESET_ALL)
			return
		
		onibus = linha_encontrada.get_onibus(data)
		
		# Verificar se já partiu
		try:
			hora_partida = time(*map(int, horario.split(':')))
			data_hora_partida = datetime.combine(data, hora_partida)
			if data_hora_partida <= datetime.now():
				print("||	Ônibus já partiu.")
				return
		except ValueError:
			print(Fore.RED+"||	Formato de horário inválido."+Style.RESET_ALL)
			return
		
		# Mostrar assentos disponíveis
		disp = onibus.assentos_disponiveis()
		if not disp:
			print(Fore.RED+"||		Nenhum assento disponível."+Style.RESET_ALL)
			return
		print(f"||	 Assentos disponíveis: {disp}")
		print("||	Assentos ímpares são nas janelas.")
		
		# Perguntar se quer fazer a reserva 
		resp = input("||	Deseja reservar um assento? (s/n): ").lower()
		if resp == 's':
			try:
				assento = int(input("||		Escolha o assento: "))
				sucesso, msg= onibus.reservar(assento)#se estiver desocupado faz a reserva senao avisa que esta ocupado
				if sucesso:
					self.reservas.append((linha_encontrada.origem.nome, linha_encontrada.destino.nome, horario, data, assento, linha_encontrada.valor, datetime.now()))
					print(Fore.RED+f"||		Assento {assento} reservado com sucesso. Valor: R$ {linha_encontrada.valor:.2f}"+Style.RESET_ALL)
				else:
					print(Fore.RED+ f"|| 	{msg}"+Style.RESET_ALL)
					self.reservas_negadas.append((linha_encontrada.origem.nome,linha_encontrada.destino.nome, horario, data, assento, msg))
			except ValueError:
				print(Fore.RED+"||	Entrada inválida para assento."+Style.RESET_ALL)
				self.reservas_negadas.append((destino_nome, horario, data, "N/A", "Entrada inválida"))

	def alterar_linha(self):	#menu para alterar as informaçoes da linha (horario, valor, destino, origem)
			print("||")
			print(Fore.BLUE + "||			ALTERAR LINHA" + Style.RESET_ALL)
			if not self.linhas: #confere se existem linhas
				print(Fore.RED + "||	Não há linhas cadastradas para alterar." + Style.RESET_ALL)
				return
			
			# printa a tabela de linhas com as linhas disponiveis e todos os 30 dias futuros com as reservas
			self.exibirTabela()
			
			try:
				escolha = int(input("||	Escolha o número da linha a alterar: ")) - 1 #vai verificar qual linha voce quer alterar e se ela existe
				if escolha < 0 or escolha >= len(self.linhas):
					print(opcao_invalida)
					return
				linha = self.linhas[escolha]
			except ValueError:
				print(erro_nao_inteiro)
				return
			
			print(f"||	Linha selecionada: {linha.origem.nome} --> {linha.destino.nome} | Horário: {linha.horario} | Valor: R${linha.valor:.2f}")
			
			# menu para alterar a linha 
			while True:
				print("||	O que deseja alterar?")
				print("||	1 - Origem")
				print("||	2 - Destino")
				print("||	3 - Horário")
				print("||	4 - Valor")
				print("||	0 - Voltar")
				try:
					opcao = int(input("||	Escolha uma opção: "))
					if opcao == 0:
						break
					elif opcao == 1:
						novo_origem_nome = input("||	Novo nome da cidade de origem: ").strip()	#vai mudar a origem da linha
						novo_origem = self.obter_criar_cidade(novo_origem_nome)
						linha.origem = novo_origem
						print(Fore.GREEN + "||	Origem alterada com sucesso!" + Style.RESET_ALL)
					elif opcao == 2:
						novo_destino_nome = input("||	Novo nome da cidade de destino: ").strip()	#vai mudar o destino
						novo_destino = self.obter_criar_cidade(novo_destino_nome)
						linha.destino = novo_destino
						print(Fore.GREEN + "||	Destino alterado com sucesso!" + Style.RESET_ALL)
					elif opcao == 3:
						while True:
							novo_horario = input("||	Novo horário (HH:MM): ").strip()	#vai verificar se voce inseriu o horario de maneira correta e ira fazer a alteração
							try:
								h, m = map(int, novo_horario.split(':'))
								linha.horario = time(h, m)
								print(Fore.GREEN + "||	Horário alterado com sucesso!" + Style.RESET_ALL)
								break
							except Exception:
								print(Fore.RED + "||	Formato inválido! Use (HH:MM)" + Style.RESET_ALL)
					elif opcao == 4:	
						while True:	#vai veridicar se voce inseriu um valor inteiro e alterará o valor da passagem
							try:
								novo_valor = float(input("||	Novo valor: R$ "))
								linha.valor = novo_valor
								print(Fore.GREEN + "||	Valor alterado com sucesso!" + Style.RESET_ALL)
								break
							except ValueError:
								print(erro_nao_inteiro)
					else:
						print(opcao_invalida)
				except ValueError:
					print(erro_nao_inteiro)
		
	def remover_linha(self):
		print("||")
		print(Fore.BLUE + "||			REMOVER LINHA" + Style.RESET_ALL)
		if not self.linhas:
			print(Fore.RED + "||	Não há linhas cadastradas para remover." + Style.RESET_ALL)
			return
		
		# printa a tabela de linhas com as linhas disponiveis e todos os 30 dias futuros com as reservas
		self.exibirTabela()
		
		try:
			escolha = int(input("||	Escolha o número da linha a remover: ")) - 1#vai verificar qual linha voce quer excluir e se ela existe
			if escolha < 0 or escolha >= len(self.linhas):
				print(opcao_invalida)
				return
			linha = self.linhas[escolha]
		except ValueError:
			print(erro_nao_inteiro)
			return
		
		# verifica se há reservas ativas
		tem_reservas = any(sum(onibus.assentos) > 0 for onibus in linha.onibus_por_data.values())
		if tem_reservas:
			confirmar = input("||	Atenção: Esta linha possui reservas ativas. Deseja remover mesmo assim? (s/n): ").lower()
			if confirmar != 's':
				print("||	Remoção cancelada.")
				return
		
		del self.linhas[escolha]	#removendo a linha
		print(Fore.GREEN + "||	Linha removida com sucesso!" + Style.RESET_ALL)
		
	def ler_reservas_arquivos(self, nome_arquivo="Reservas.txt"):

			try:
				# Abre o arquivo e lê todas as linhas
				with open(nome_arquivo, "r", encoding="utf-8") as arq:
					linhas = arq.readlines()
				
				#tratamento de arquivo vazio
				for linha in linhas:
					linha = linha.strip()
					if not linha or ";" not in linha:
						continue

					try:
						origem_nome, destino_nome, data_str, horario_str, assento_str = linha.split(";")

						#Converte strings para objetos
						data_obj = datetime.strptime(data_str.strip(), "%d/%m/%Y").date()
						horario_obj = time(*map(int, horario_str.strip().split(':')))
						assento_int = int(assento_str.strip())

						#Encontra a LinhaOnibus
						linha_encontrada = None
						for linha_onibus in self.linhas:
							if (linha_onibus.origem.nome.lower() == origem_nome.strip().lower() and
								linha_onibus.destino.nome.lower() == destino_nome.strip().lower() and
								linha_onibus.horario == horario_obj):
								linha_encontrada = linha_onibus
								break

						if not linha_encontrada:
							print(Fore.YELLOW + f"|| Aviso: Linha {origem_nome} -> {destino_nome} {horario_str} não encontrada." + Style.RESET_ALL)
							continue
						onibus_dia = linha_encontrada.get_onibus(data_obj)

						if not onibus_dia:
							print(Fore.YELLOW + f"|| Aviso: Ônibus não encontrado para a linha {linha_encontrada} na data {data_str}." + Style.RESET_ALL)
							continue
						# 4. Chamar o método reservar()
						sucesso, msg = onibus_dia.reservar(assento_int, comprador="arquivo")
						
						if sucesso:
							# Se a reserva for bem sucedida, adiciona à lista de reservas
							self.reservas.append((origem_nome.strip(), destino_nome.strip(), horario_str.strip(), data_obj, assento_int, linha_encontrada.valor, datetime.now()))
							print(Fore.GREEN + f"|| Reserva do assento {assento_int} na data {data_str} carregada com sucesso!" + Style.RESET_ALL)
						else:
							# Se a reserva falhar (assento ocupado, inválido), adiciona a reservas negadas
							self.reservas_negadas.append((origem_nome.strip(), destino_nome.strip(), data_obj, horario_str.strip(), assento_int, msg))
							print(Fore.YELLOW + f"|| Reserva {assento_int} de {data_str} negada: {msg}" + Style.RESET_ALL)


					except Exception as erro:
						# Caso alguma linha esteja mal formatada, mostra erro mas continua lendo
						print(Fore.RED + f"|| Erro ao ler linha: {linha}" + Style.RESET_ALL)
						print(Fore.RED + f"|| Motivo: {erro}" + Style.RESET_ALL)

				# Confirma ao usuário que as reservas foram carregadas
				print(Fore.GREEN + "||  Processamento de reservas finalizado!" + Style.RESET_ALL)
			except Exception as erro: #Tratamento de Arquivo
            	# Erro ao tentar abrir ou ler o arquivo
				print(Fore.RED + "||  Erro ao abrir ou ler o arquivo!" + Style.RESET_ALL)
				print(Fore.RED + f"||  Detalhes: {erro}" + Style.RESET_ALL)
		
	def gerar_relatorios(self): #menu para gerar o faturamento mensal
		mes_atual = datetime.now().month
		ano_atual = datetime.now().year
		arrecadacao = {}
  
		for linha in self.linhas:
			chave = (linha.origem, linha.destino, linha.horario)
			total = 0
			
			for data, onibus in linha.onibus_por_data.items():
				data_objeto = data

				if data_objeto.month == mes_atual and data_objeto.year == ano_atual:
					assentos_ocupados = sum(onibus.assentos) 			# Conta os assentos ocupados
					total += assentos_ocupados * linha.valor 			# Soma ao total da linha
			arrecadacao[chave] =total
		texto_relatorio = "||		RELATORIO DE ARRECADAÇÃO DO MÊS ATUAL\n\n"
		for chave, total in arrecadacao.items():
			origem, destino, horario = chave
			texto_relatorio +=(
				f"||	Linha {origem} -> {destino}	|	Horario:	({horario})	\n"	
				f"||	Total arrecadado: R$ {total:.2f}\n"
			)
   
		print(Fore.BLUE+"||			GERAR RELATORIOS"+Style.RESET_ALL)
		try:
			relatorio_opcao = int(input("||	1 - Exibir na tela\n||	2 - Gerar arquivo .txt\n||	0 - Voltar\n||	Escolha alguma oção:"))
			match relatorio_opcao:
				case 1:
					print(texto_relatorio)
				case 2:
					with open("Relatorio_Arrecadacao.txt", "w", encoding="utf-8") as arq:
						arq.write(texto_relatorio)
				case 0:
					print("voltando")
				case _: 
					print(opcao_invalida)
		except ValueError:
				print(erro_nao_inteiro)
    

	def gerar_arquivo_reservas_negadas(self):
	#Gera um arquivo .txt contendo todas as reservas negadas no sistema.Inclui informações como origem, destino, data, horário, assento e motivo.
		if not self.reservas_negadas:	# Verifica se a lista de reservas negadas está vazia
			print(Fore.RED + "||  Não há reservas negadas registradas." + Style.RESET_ALL)

				# Mesmo sem registros, ainda assim cria um arquivo informativo
			with open("Reservas_Negadas.txt", "w", encoding="utf-8") as arq:
					arq.write("NÃO HÁ RESERVAS NEGADAS REGISTRADAS.")
			return  # Sai da função porque não há nada para listar

		# Cabeçalho do relatório
		texto = ""
		texto += "="*65 + "\n"
		texto += "||        RELATÓRIO DE RESERVAS NEGADAS\n"
		texto += "="*65 + "\n\n"

		# Percorre todas as reservas negadas registradas no sistema
		for reserva in self.reservas_negadas:
			# Obtém as informações armazenadas no dicionário da reserva
			origem = reserva[0]
			destino = reserva[1]
			data = reserva[2]
			horario = reserva[3]
			assento = reserva[4]
			motivo = reserva[5]

			# Adiciona as informações formatadas ao texto do relatório
			texto += (
				f"|| Linha: {origem} -> {destino}\n"
				f"|| Data: {data}   |   Horário: {horario}\n"
				f"|| Assento solicitado: {assento}\n"
				f"|| Motivo: {motivo}\n"
				f"||\n"
				+ "-"*65 + "\n")

			# Cria e grava o arquivo .txt contendo todas as reservas negadas
			with open("Reservas_Negadas.txt", "w", encoding="utf-8") as arq:
				arq.write(texto)

			# Mensagem final confirmando a geração do arquivo
			print(Fore.GREEN + "|| Arquivo 'Reservas_Negadas.txt' gerado com sucesso!" + Style.RESET_ALL)



#======================================================= Menu =======================================
sistema = SistemaPassagens()
print("="*65)
print(" 	SISTEMA DE UMA EMPRESA DE TRANSPORTE DE PASSAGEIROS.")
while True:
	print("="*65)
	try:
		opcao_menu = int(input("||			OPÇÕES\n||	1 - Exibir Tabela de Horários \n||	2 - Cadastrar nova Linha\n||	3 - Consultar passagens para determinada cidade\n||	4 - Consultar assentos disponíveis\n||	5 - Alterar linha \n||	6 - Remover linha \n||	7 - Ler reservas de arquivo\n||	8 - Gerar relatórios\n||	9 - Gerar arquivo de reservas negadas\n||	0 - Sair\n||\n|| Escolha alguma opção :"))
		match opcao_menu:
			case 1:
				sistema.exibirTabela()
			
			case 2:
				sistema.cadastrar_linha()
			
			case 3:
				sistema.consultar_passagens_cidade()
    
			case 4:
				sistema.consultar_assentos_disponiveis()
    
			case 5:
				sistema.alterar_linha()
    
			case 6:
				sistema.remover_linha()
    
			case 7:
				sistema.ler_reservas_arquivos()
    
			case 8:
				sistema.gerar_relatorios()
    
			case 9:
				sistema. gerar_arquivo_reservas_negadas()
    
			case 0:
				print("Finalizando sistema...")
				quit()
			case _: 
				print(opcao_invalida)
	except ValueError:
		print(erro_nao_inteiro)