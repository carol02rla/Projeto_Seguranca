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

        tabela_participantes = WebDriverWait(driver, 20, ignored_exceptions=IGNORED_EXCEPTIONS).until(
            EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'participantes')]/following-sibling::*[1]//table[contains(@class, 'participantes')]"))
        )

        linhas_participantes = tabela_participantes.find_elements(By.XPATH, './/tbody/tr')

        for i in range(len(linhas_participantes)):
            tds_valing_top = linhas_participantes[i].find_elements(By.XPATH, './/td[@valign="top"]')
            for j in range(len(tds_valing_top)):
                link_to_info = tds_valing_top[j].find_element(By.XPATH, './/strong/a')

                WebDriverWait(driver, 20, ignored_exceptions=IGNORED_EXCEPTIONS).until(
                    EC.element_to_be_clickable(link_to_info)
                )
                time.sleep(2)
                link_to_info.click()

                info_table = WebDriverWait(driver, 20, ignored_exceptions=IGNORED_EXCEPTIONS).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'j_id_jsp_1900130699_17')]//span/span/div/table/tbody/tr/td[2]"))
                )
                nome = info_table.find_element(By.XPATH, ".//span[1]").text
                matricula = info_table.find_element(By.XPATH, ".//strong[contains(text(), 'Matrícula')]/following-sibling::em[1]").text
                usuario = info_table.find_element(By.XPATH, ".//strong[contains(text(), 'Usuário')]/following-sibling::em[1]").text

                print(nome, matricula, usuario)

                close_button = WebDriverWait(driver, 3, ignored_exceptions=IGNORED_EXCEPTIONS).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(@id, 'ui-dialog-title-j_id_jsp_1900130699_17')]/following-sibling::a[1]"))
                )

                actions = ActionChains(driver)
                actions.move_to_element(close_button).click().perform()

                # close_button.click()
                # driver.execute_script("arguments[0].click();", close_button)
                # time.sleep(2)

                tabela_participantes = WebDriverWait(driver, 20, ignored_exceptions=IGNORED_EXCEPTIONS).until(
                    EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'participantes')]/following-sibling::*[1]//table[contains(@class, 'participantes')]"))
                )

                linhas_participantes = tabela_participantes.find_elements(By.XPATH, './/tbody/tr')


        driver.back()

        driver.back()

        tabela_turmas = WebDriverWait(driver, 20, ignored_exceptions=IGNORED_EXCEPTIONS).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'minhas-turmas'))  # Substitua pelo nome correto da classe
        )

        linhas_turmas = tabela_turmas.find_elements(By.XPATH, './/tbody//tr')


    # sair = WebDriverWait(driver, 20, ignored_exceptions=IGNORED_EXCEPTIONS).until(
    #     EC.element_to_be_clickable((By.XPATH, '//*[@class= "icone-sair"]'))
    # )
    # sair.click()

