from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC

import logging

IGNORED_EXCEPTIONS = (NoSuchElementException,StaleElementReferenceException)

def login(driver, usuario, senha, exit=True):
    logging.info(f"Login for {usuario} user with {senha} password")
    usuario_field = driver.find_element(By.XPATH, '//*[@name="form:login"]')
    usuario_field.clear()
    usuario_field.send_keys(usuario)
    senha_field = driver.find_element(By.XPATH, '//*[@name="form:senha"]')
    senha_field.clear()
    senha_field.send_keys(senha)
    driver.find_element(By.XPATH, '//*[@id="form:entrar"]').click()

    try:
        driver.find_element(By.XPATH,'//div[contains(text(), "Usuário e/ou senha inválidos")]')
    except NoSuchElementException:
        portal_discente = WebDriverWait(driver, 10, ignored_exceptions=IGNORED_EXCEPTIONS).until(
            EC.presence_of_element_located((By.XPATH, '//*[@title="SIGAA"]//following::span//a'))
        )
        assert portal_discente.text.strip() == "Portal do Discente", f"Erro ao acessar o sistema.\n"
        logging.info("Sucesso na autenticacao.")

        if exit:
            sair = WebDriverWait(driver, 20, ignored_exceptions=IGNORED_EXCEPTIONS).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@class= "icone-sair"]'))
            )
            sair.click()
            acessar_tela = WebDriverWait(driver, 20, ignored_exceptions=IGNORED_EXCEPTIONS).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@title="Acessar o SIGAA"]'))
            )
            acessar_tela.click()
    else:
        logging.info("Usuario e/ou senha invalidos.")