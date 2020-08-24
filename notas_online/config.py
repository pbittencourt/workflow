#!/usr/bin/env python3
"""
CONFIGURAÇÕES GLOBAIS
Módulo contendo funções comuns a todos os
scripts do 'notas_online', bem como variáveis
do professor, tais como turmas, disciplinas, etc.

Autor: Pedro P. Bittencourt
Contato: contato@pedrobittencourt.com.br
Site: pedrobittencourt.com.br
"""

from selenium import webdriver
import logging
import os
import sys


def login(username: str, password: str) -> None:
    """
    Recebe username e password do usuário e utiliza essas credenciais
    para tentar fazer login no sistema do notas online. Após a
    submissão do formulário, veriica se o conteúdo exibido corresponde
    à página inicial do sistema, retornando True ou False.
    """

    # inicializa driver
    driver = webdriver.Chrome(executable_path=os.getcwd() + r'/../drivers/chromedriver')

    # abre página de login
    driver.get('https://www.notasonline.com/pages/nol_logon.asp')

    # preenche credenciais do usuário
    driver.find_element_by_id('txtLogin').send_keys(username)
    driver.find_element_by_id('txtPassword').send_keys(password)
    driver.find_element_by_id('frmForm').submit()

    # verifica se o login foi efetuado, através da url atual
    if driver.current_url == 'https://www.notasonline.com/pages/home_teacher.asp':
        return driver
    else:
        errorquit('Não foi possível logar no sistema. Você digitou as credenciais corretas?')
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

##############################
# SETUP LOGGING
##############################

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s %(levelname)s %(message)s',
                   datefmt='%d-%b-%Y %H:%M:%S',
                   filename='notasonline.log',
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

##############################
# END OF SETUP LOGGING
##############################


diarios = {
    '6ADG': '591D1214-CEC7-4511-B99D-38B64C224704',
    '6BDG': '2C350D3D-560B-4FE3-A6B8-9C3B4C1D7BB2',
    '7ADG': '860B570A-9F38-4384-93BA-8905AE76B98C',
    '8ADG': '570678BF-C4FD-4E26-BB11-9C19AA9BB457',
    '8AFIS': '6CDA5EAA-BB3C-4029-8F27-674B385E4689',
    '9ADG': 'C35A5E17-0299-4E6F-86A5-3BFCEAE34E87',
    '9AFIS': 'D61E769F-C1BF-4720-9F0F-28DB24889C73',
    '1AFIS': '993A3639-2A70-4748-8BB9-CF4BF24131FE',
    '1AGMT': '80A71A6F-1ED2-4267-8E93-FD74B5B77EA4',
    '2AFIS': '88A1A059-12DE-4676-9A28-E07EB47DE913',
    '2AGMT': 'E12A8904-21D6-4E1B-A1DA-99A66EAF400F',
    '3AFIS': '930B8C3A-450A-405D-A1ED-725FD1FC19E8',
    '3AGMT': 'E08722EA-267E-42DE-875E-35944FA616D9',
}
disciplinas = {
    'DG': 'Desenho Geométrico / Pedro Pompermayer Bittencourt',
    'FIS': 'Física / Pedro Pompermayer Bittencourt',
    'GMT': 'Geometria / Pedro Pompermayer Bittencourt',
}
turmas = {
    '6A': 'Sexto Ano / 1M6A / Manhã',
    '6B': 'Sexto Ano / 1M6B / Manhã',
    '7A': 'Sétimo Ano / 1M7A / Manhã',
    '8A': 'Oitavo Ano / 1M8A / Manhã',
    '9A': 'Nono Ano / 1M9A / Manhã',
    '1A': 'Primeira Série / 2M1A / Manhã',
    '2A': 'Segunda Série / 2M2A / Manhã',
    '3A': 'Terceira Série / 2M3A / Manhã',
}
ocorrencias = {
    'A': ['C6AE796F-E4BA-47C2-A725-98C36CD12E11', 'Não apresentou a lição de casa'],
    'B': ['AE890406-F8E3-442D-BF98-44498DC1F517', 'Lição de casa incompleta'],
    'C': ['743091FC-5899-477C-8C68-35A55343B70F', 'Não entregou trabalho (1a data)'],
    'D': ['733DA849-6942-44C4-B170-F3B7A97F518A', 'Não entregou trabalho (2a data)'],
    'E': ['E6F973C7-8146-450F-AE4F-02D2C2D451D1', 'Trabalho fora das especificações solicitadas.'],
    'F': ['7A80526B-387F-4743-87AF-DB2666CE6639', 'Não trouxe material'],
    'G': ['80860D8F-1152-43BE-ABE3-FCE16987F413', 'Atraso'],
    'H': ['3F67CD55-86B0-4C5F-9502-83F04CF3EE5A', 'Não fez atividades em classe'],
    'I': ['4B55A896-FDA8-484C-81C5-882E140C290E', 'Sem uniforme (Educação Física)'],
    'J': ['31F0C7AE-8528-463E-81E0-EF4B4F9A65C7', 'Outras ocorrências'],
    'K': ['40A94F21-D8A3-408F-AA30-10BE6F7BCE49', 'Não compareceu ao plantão.'],
    'L': ['B43C3E32-2BDC-47C3-90A3-B7004920E0CC', 'Não compareceu à aula - período intensivo de estudos'],
    'M': ['E8E54836-8579-49CC-B66A-57D7AC7D67C4', 'Não compareceu para a prova de recuperação.'],
    'N': ['4342E427-808E-4BE7-AF73-8E2540FA84C9', 'Não compareceu ao Exame.'],
    'O': ['BDD11FB6-BF3F-42C2-B7DB-B81D1CE2AE5E', 'Não realizou as atividades no Plurall.'],
    'P': ['8C8A120C-755E-4650-883B-1EB8D033513C', 'Não assistiu a aula síncrona (ao vivo).'],
    'Q': ['E07BC23B-5247-4494-9C95-9E7DB46A84E2', 'Não visualizou as atividades enviadas no PLURALL.'],
    'R': ['90D4F55A-B000-46BB-B90B-99D205911188', 'Não participou da avaliação síncrona.'],
}