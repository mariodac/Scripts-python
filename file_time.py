#!/usr/bin/python3

# -*- coding: utf-8 -*-

#Desenvolvido  em 04/01/2022
#Atualização: 24/06/2022.
#Verificar ultima modificação de arquivo e exclui arquivo +1 dia.

import os, time, shutil, stat, socket,logging
from datetime import date, datetime

path_user = "/home/user"
# lista de itens no diretorio
home_dir_itens = os.listdir(path_user)
exclude_itens = []
# tempo atual em segundos
time_now = time.time()
# hostname da máquina que executa o script
hostname = socket.gethostname()
# formato do log
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#define o nome do modulo para o log
logger = logging.getLogger(__name__)
# configura nivel de log
logger.setLevel('DEBUG')
try:
	# verifica se existe o diretorio de log se não existir faz a criação
	new_path = os.path.join('/var/log/', 'exclude_itens')
	if not os.path.isdir(new_path):
		os.mkdir(new_path)
except Exception as err:
	logger.debug(err)
path_hostname = os.path.join(new_path, hostname)
file_handler = logging.FileHandler("{}.log".format(path_hostname))
# aplica formato 
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def get_time_file(path_item: str):
	try:
		# ultima modificação do arquivo em segundos
		time_mod = os.path.getmtime(path_item)
		# tempo  em dias do arquivo
		time_diff = int((time_now - time_mod)/86400)
		return time_diff
	except Exception as err:
		logger.debug(err)
try:
	# obtem caminhos dos itens contidos na lista home_dir_files
	for item in home_dir_itens:
		# exclude_item = os.path.join(path_user, item)
		path_item = os.path.join(path_user, item)
		# ignora itens ocultos
		if item.startswith('.'):
			continue
		# ignora itens link simbolico
		if os.path.islink(path_item):
			continue
		# verifica se item é diretorio ou arquivo
		if os.path.isdir(path_item):
			# lista arquivos de diretorio 
			list_path_item = os.listdir(path_item)
			for item_list_path_item in list_path_item:
				#caminho do item atual
				exclude_item = os.path.join(path_item, item_list_path_item)
				# ignora item com .desktop
				if item_list_path_item.endswith('.desktop'):
					continue
				# ignora item que são atalho
				if os.path.islink(exclude_item):
					continue
				# pega tempo da ultima modificação
				time_diff = get_time_file(exclude_item)
				# verifica se arquivo tem mais de um dia
				if time_diff > 1:
					logger.info("Item {} modificado há {} dias".format(exclude_item, time_diff))
					exclude_itens.append(exclude_item)
		else:
			exclude_item = path_item
			# ignora item que são atalho
			if os.path.islink(exclude_item):
				continue
			# pega tempo da ultima modificação
			time_diff = get_time_file(exclude_item)
			# verifica se arquivo tem mais de um dia e adiciona na lista
			if time_diff > 1:
				logger.info("Item {} modificado há {} dias".format(exclude_item, time_diff))
				exclude_itens.append(exclude_item)
except Exception as err:
	logger.debug(err)

for item in exclude_itens:
	try:
		# verifica permissão
		if not os.access(item, os.W_OK):
			logger.info("Item {} sem permissão, alterando permissão ...".format(item))
			# modifica permisão do item
			os.chmod(item, stat.S_IWOTH)
		# verifica se é arquivo se não será um diretorio e realiza exclusão
		if os.path.isfile(item):
			# exclusão de arquivo
			os.remove(item)
			logger.info("Arquivo {} excluído".format(item))
		else:
			# exclusão de diretorio
			shutil.rmtree(item)
			logger.info("Diretorio {} excluído".format(item))
	except Exception as err:
		logger.debug(err)
