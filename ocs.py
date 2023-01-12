
#Desenvolvido por Mario Cabral em 27/10/2021
#Atualização: 07/01/2022.
#Loga no OCS INVENTORY e faz o merge de duplicatas de hostname

import selenium.webdriver.chrome.options as chromeOptions
import getpass, re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from os import path
from time import sleep

def optionsChrome(headless=False):
    """ Configura opções para chrome """
    chrome_options = chromeOptions.Options()
    print('Configurando navegador Chrome ...')
    if(headless):
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    return chrome_options

def open_ocs(url):
    s = Service(ChromeDriverManager().install())
    with webdriver.Chrome(service=s, options=optionsChrome(True)) as driver:
        driver.get(url)
        alert = 'alerta'
        while alert:
            user = input('User: ')
            password = getpass.getpass('Password: ')
            login_element = driver.find_element(By.ID, 'LOGIN')
            password_element = driver.find_element(By.ID, 'PASSWD')
            login_element.send_keys(user)
            password_element.send_keys(password)
            btn_login = driver.find_element(By.ID, 'btn-logon')
            btn_login.click()
            sleep(2)
            try:
                alert = driver.find_element(By.ID, 'my-alert-')
            except:
                alert = None
            if alert:
                print('Login falhou!')
                print(alert.text)
                login_element = driver.find_element(By.ID, 'LOGIN')
                password_element = driver.find_element(By.ID, 'PASSWD')
                login_element.clear()
                password_element.clear()
        # navbar = driver.find_elements_by_css_selector('.nav.navbar-nav')
        elemento = driver.find_element(By.CSS_SELECTOR, '.nav.navbar-nav')
        links = elemento.find_elements(By.TAG_NAME, 'li')
        filtro = [x for x in links if re.search('manage', x.text, re.IGNORECASE)]
        if filtro:
            elemento = filtro[0]
        elemento.click()
        sleep(2)
        elementos = driver.find_elements(By.CSS_SELECTOR, '.dropdown-menu')
        filtro = [x for x in elementos if re.search('duplicates', x.text, re.IGNORECASE)]
        if filtro:
            elemento = filtro[0]
        links = elemento.find_elements(By.TAG_NAME, 'li')
        filtro = [x for x in links if re.search('duplicates', x.text, re.IGNORECASE)]
        if filtro:
            elemento = filtro[0]
        elemento.click()
        elementos = driver.find_elements(By.CLASS_NAME, 'row')
        filtro = [x for x in elementos if re.search('hostname only',x.text,re.IGNORECASE)]
        if filtro:
            elemento = filtro[0]
        link = elemento.find_element(By.TAG_NAME, 'a')
        link.click()
        elementos = driver.find_elements(By.ID, 'selected_grp_dupli')
        for e in elementos:
            e.click()
            sleep(5)
        elemento = driver.find_element(By.NAME, 'FUSION')
        elemento.click()
        sleep(60)
        elementos = driver.find_elements(By.TAG_NAME, 'center')
        merge = ['{}\n'.format(x.text) for x in elementos]
    arquivo = open(path.join(path.dirname(path.realpath(__file__)), 'logs.txt'), 'w')
    arquivo.writelines(merge)
    arquivo.close()

open_ocs('http://192.168.1.26/ocsreports/')