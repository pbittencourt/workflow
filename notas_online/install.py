#!/usr/bin/env python3
"""
INSTALAÇÃO
Raspa os dados de notas online, buscando chaves
necessárias para automatização de registros.

Autor: Pedro P. Bittencourt
Email: contato@pedrobittencourt.com.br
Site: pedrobittencourt.com.br
"""


from bs4 import BeautifulSoup as bs
from selenium import webdriver
from time import sleep
import getpass
import logging
import os


def login(username: str, password: str) -> None:
    """
    Recebe username e password do usuário e utiliza essas credenciais
    para tentar fazer login no sistema do notas online. Após a
    submissão do formulário, verifica se o conteúdo exibido corresponde
    à página inicial do sistema, retornando True ou False.
    """

    # abre página de login
    driver.get('https://www.notasonline.com/pages/nol_logon.asp')
    logger.info(f'ACESSO À PÁGINA EFETUADO POR {username}!')
    sleep(1)

    # preenche credenciais do usuário
    driver.find_element_by_id('txtLogin').send_keys(username)
    driver.find_element_by_id('txtPassword').send_keys(password)
    driver.find_element_by_id('frmForm').submit()

    # verifica se o login foi efetuado, através da url atual
    if driver.current_url == 'https://www.notasonline.com/pages/home_teacher.asp':
        logger.info('Logou com sucesso!')
        return True
    else:
        logger.error('Não foi possível logar no sistema. Você digitou as credenciais corretas?')
        return False


def errorquit(msg: str = 'ERRO NÃO ESPECIFICADO') -> str:
    """
    Quando falhar numa requisição importante, exibe
    mensagem de erro, registra no log, fecha o driver
    e encerra o programa.
    """
    logger.error(f'Não foi possível continuar devido ao seguinte problema: {msg}.')
    logger.info('O programa será encerrado agora. Verifique o registro para detalhes!')
    driver.quit()
    sys.exit(1)


###############
# SETUP LOGGING
###############

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s %(levelname)s %(message)s',
                   datefmt='%d-%b-%Y %H:%M:%S',
                   filename='install.log',
                   filemode='a')
# create logger object
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# handle which writes INFO messages to stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# format for console
formatter = logging.Formatter('%(levelname)-8s %(message)s')
console.setFormatter(formatter)

# add console handler to logger
logger.addHandler(console)

######################
# END OF SETUP LOGGING
######################

# credenciais do usuário
username = str(input('Usuário: _ '))
password = getpass.getpass('Senha: _ ')

# inicializa driver
driver = webdriver.Chrome(executable_path=os.getcwd() + r'/../drivers/chromedriver')

if login(username, password):
    
    # para 'codificar' os nomes das disciplinas
    # (pode ser necessário alterar para outros casos)
    disc = {
        'D': 'DG',
        'F': 'FIS',
        'G': 'GMT',
        'Q': 'QUI',
        'C': 'CIE'
    }

    # acessa página de diários de classe
    try:
        url = 'https://www.notasonline.com/pages/admin_divisions_diaries_fill_in.asp?default_year=2020'
        page = driver.get(url)
        logger.info('Página com diários de classe acessada.')
    except:
        errorquit(f'não foi possível acessar página com os diários de classe, url {url}')

    try:
        objid = 'seldivisions_teachers_subjects'
        html = driver.find_element_by_id(objid).get_attribute('innerHTML')
        soup = bs(html, 'html.parser')
        options = soup.find_all('option')
        logger.info(f'Objeto {objid} localizado com sucesso.')
    except:
        errorquit(f'não foi possível localizar objeto {objid}')

    # insere dict 'diarios' e 'disciplinas' no arquivo
    with open('config.py', 'a') as f:
        print('diarios = {', file=f)
        for option in options:
            line = option.get_text().strip().split(' / ')
            if len(line) > 1:
                code = option.get('value')
                turma, codigo, periodo, disciplina, professor = line
                text = f"    '{codigo[2:]}{disc[disciplina[:1]]}': '{code}',"
                print(text, file=f)
        print('}', file=f)
        logger.info('Instalação dos diários de classe concluída!')

        store = []
        print('disciplinas = {', file=f)
        for option in options:
            line = option.get_text().strip().split(' / ')
            if len(line) > 1:
                turma, codigo, periodo, disciplina, professor = line
                text = f"    '{disc[disciplina[:1]]}': '{disciplina} / {professor}',"
                if text not in store:
                    store.append(text)
                    print(text, file=f)
        print('}', file=f)
        logger.info('Instalação das disciplinas concluída!')

    # acessa página de ocorrências
    try:
        url = 'https://www.notasonline.com/pages/user_occurrence.asp'
        page = driver.get(url)
        logger.info('Página de ocorrências acessada.')
    except:
        errorquit(f'não foi possível acessar página de ocorrências, url {url}')

    # localiza turmas e ocorrências
    try:
        objid = 'selDivisions'
        html = driver.find_element_by_id(objid).get_attribute('innerHTML')
        soup = bs(html, 'html.parser')
        turmas = soup.find_all('option')
        logger.info(f'Objeto {objid} localizado com sucesso.')
    except:
        errorquit(f'não foi possível localizar objeto {objid}')
    try:
        objid = 'selOccurrences_codes'
        html = driver.find_element_by_id(objid).get_attribute('innerHTML')
        soup = bs(html, 'html.parser')
        ocorrencias = soup.find_all('option')
        logger.info(f'Objeto {objid} localizado com sucesso.')
    except:
        errorquit(f'não foi possível localizar objeto {objid}')

    # insere dict 'turmas' e 'ocorrencias' no arquivo
    with open('config.py', 'a') as f:
        print('turmas = {', file=f)
        for option in turmas:
            line = option.get_text().strip().split('/')
            if len(line) > 1:
                turma = line[1].strip()
                text = f"    '{turma[2:]}': '{option.get_text().strip()}',"
                print(text, file=f)
        print('}', file=f)
        logger.info('Instalação das turmas concluída!')

        print('ocorrencias = {', file=f)
        for option in ocorrencias:
            code = option.get('value')
            line = option.get_text().strip().split(' - ')
            if len(line) == 2:
                occ, desc = line
                text = f"    '{occ[1]}': ['{code}', '{desc}'],"
                print(text, file=f)
            elif len(line) == 3:
                occ, desc1, desc2 = line
                text = f"    '{occ[1]}': ['{code}', '{desc1} - {desc2}'],"
                print(text, file=f)
        print('}', file=f)
        logger.info('Instalação das ocorrências concluída!')

# encerra driver
driver.quit()
