from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from utils.auth import IGNORED_EXCEPTIONS, login

import time
import os
import argparse
import re

parser = argparse.ArgumentParser(description='Escolha o navegador para executar.')

group = parser.add_mutually_exclusive_group(required=False)
group.add_argument('--firefox', action='store_true', help='Executa com o Firefox')
group.add_argument('--chrome', action='store_true', help='Executa com o Chrome')

args = parser.parse_args()

if args.chrome:
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
else:
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

driver.maximize_window()
driver.get("https://sigaa.ufpb.br/sigaa/public/home.jsf")

time.sleep(3)
acessar_tela = WebDriverWait(driver, 20, ignored_exceptions=IGNORED_EXCEPTIONS).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@title="Acessar o SIGAA"]'))
)

acessar_tela.click()
time.sleep(2)

with open(os.path.join("data", "login.txt")) as file:
    lines = file.read().splitlines()
    users = []
    passwords = []
    for line in lines:
        users.append(line.split(" ")[0])
        passwords.append(line.split(" ")[1])

for user, password in zip(users, passwords):
    login(driver, user, password, exit=False)

    tabela_turmas = WebDriverWait(driver, 20, ignored_exceptions=IGNORED_EXCEPTIONS).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'minhas-turmas'))  # Substitua pelo nome correto da classe
    )

    linhas_turmas = tabela_turmas.find_elements(By.XPATH, './/tbody//tr')

    matriculas = []
    nomes = []
    usernames = []

    for i in range(len(linhas_turmas)):
        turma = linhas_turmas[i].find_element(By.XPATH, './/td/strong/a')  # Busca a primeira célula da linha
        WebDriverWait(driver, 20, ignored_exceptions=IGNORED_EXCEPTIONS).until(
            EC.element_to_be_clickable(turma)  # Espera que o elemento esteja clicável
        )
        
        turma.click()

        participantes = WebDriverWait(driver, 20, ignored_exceptions=IGNORED_EXCEPTIONS).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'rich-panelbar-content-exterior')]//table//tbody/tr//a[4]"))
        )

        participantes.click()

        nome_turma = WebDriverWait(driver, 20, ignored_exceptions=IGNORED_EXCEPTIONS).until(
            EC.presence_of_element_located((By.ID, "linkNomeTurma"))
        )
        print("\n\n", nome_turma.text, "\n")

        emails_alunos = WebDriverWait(driver, 20, ignored_exceptions=IGNORED_EXCEPTIONS).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='emailsAlunos']"))
        )
        emails = emails_alunos.get_attribute('value')
        print(emails)

        matricula_alunos = driver.find_elements('xpath', "//td[@valign='top']//text()[contains(., 'Matrícula:')]/following::em[1]")
        matriculas = [matricula.text for matricula in matricula_alunos]
        print(matriculas)

        nomes_alunos = driver.find_elements('xpath', "//td[@valign='top']//strong")
        nomes = [nome.text for nome in nomes_alunos]
        print(nomes)

        pattern = re.compile(r"Mensagem\.show\(\d+, '([^']+)'\)")
        alunos = driver.find_elements('xpath', "//a[@class='naoImprimir'][@href='javascript://nop/']")
        usernames = [
            pattern.search(aluno.get_attribute('onclick')).group(1)
            for aluno in alunos
            if pattern.search(aluno.get_attribute('onclick'))
        ]
        print(usernames)
        
        try:
            with open('banco_alunos_sigaa.txt', '+r', encoding="utf-8") as file:
                linhas_existentes = {linha.strip() for linha in file}
        except FileNotFoundError:
            linhas_existentes = set()

        with open('banco_alunos_sigaa.txt', '+a', encoding='utf-8') as file:
            qtd_alunos = len(usernames)
            for matricula, nome, username in zip(matriculas[-qtd_alunos:], nomes[-qtd_alunos:], usernames):
                linha = f"{matricula} {nome} {username}"
                if linha not in linhas_existentes:
                    file.write(linha + '\n')
                    linhas_existentes.add(linha)

        driver.back()

        driver.back()

        tabela_turmas = WebDriverWait(driver, 20, ignored_exceptions=IGNORED_EXCEPTIONS).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'minhas-turmas'))  # Substitua pelo nome correto da classe
        )

        linhas_turmas = tabela_turmas.find_elements(By.XPATH, './/tbody//tr')

    sair = WebDriverWait(driver, 20, ignored_exceptions=IGNORED_EXCEPTIONS).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@class= "icone-sair"]'))
    )
    sair.click()
