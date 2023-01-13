#Desenvolvido em 09/09/2022
#Atualização: 29/10/2022.
#Configuração automatizada de roteadores

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions as selenium_exceptions
import time, sys, requests, logging, os, wx
import pandas as pd
from bs4 import BeautifulSoup

SEM_CABECA = False
# configuração logger
# formato do log
logger = logging.getLogger('config_router')
# configura nivel de log
logger.setLevel('DEBUG')
# verificação de SO
try:
    # verifica sistema operacional
    if os.name == 'nt':
        # caminho do log
        path_log = os.environ['TEMP']
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        # aplica formato 
        formatter = logging.Formatter(log_format)
    else:
        # caminho do log
        path_log = environ['HOME']
        # formato do log
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_format)
except Exception as err:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print('ERRO: TIPO {} - ARQUIVO {} - LINHA {} - MESSAGE:{}'.format(exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
    print('\a')
file_handler = logging.FileHandler("{}.log".format(os.path.join(path_log, '.config_router')))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def check_internet():
    """Simples requisição no site do google se não houver resposta no dentro timeout definido, implica que há um erro na conexão
    """
    timeout = 10
    try:
        # requisição com tempo limite de 10 segundos
        requests.get('https://www.google.com', timeout=timeout)
        return True
    except ConnectionError:
        logger.error('Sem conexão')
        return False

def browser_is_closed(driver:webdriver.Chrome):
    """Verifica se navegador esta aberto

    Args:
        driver (webdriver.Chrome): Navegador automatizado chrome

    Returns:
        bool: Falso para navegador fechado ou headless ou True para navegador fechado
    """
    try: 
        if SEM_CABECA:
            # verifica se há janela aberta
            if driver.window_handles:
                return False
        else:
            return False
    except:
        logger.error('Browser fechado')
        return True
    
def init_selenium(headless=False):
    """Inicia navegador automatizado

    Args:
        headless (bool, optional): Navegador com ou sem interface. Defaults to False.

    Returns:
        webdriver.Chrome: Navegador automatizado Chrome
    """
    try:
        options = Options()
        # define se webdriver será com ou sem interface
        if headless:
            options.add_argument('headless')
        # desativa log do webdriver no terminal
        options.add_argument('--disable-logging')
        options.add_argument('--log-level=3')
        # ignore erros de certificados de segurança
        options.add_argument('--ignore-certificate-errors')
        # seleciona o webdriver correto para cada sistema
        if os.name == 'nt':
            service = ChromeService(executable_path=ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())
        else:
            service = ChromeService(executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        try:
            driver = webdriver.Chrome(service=service, options=options)
        except:
            options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
            driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error('FUNÇÃO {} - TIPO {} - ARQUIVO {} - LINHA {} - MESSAGE:{}'.format(init_selenium.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))

def login_TL_WR841HP(driver:webdriver.Chrome, roteadores:pd.DataFrame, index:int):
    """Realiza login no roteador WR841HP

    Args:
        driver (webdriver.Chrome): Navegador automatizado Chrome
        roteadores (pd.DataFrame): Planilha contendo informações dos roteadores
        index (int): index do roteador a ser logado

    Raises:
        selenium_exceptions.WebDriverException: Caso webdriver seja fechado durante execução
    """
    # verifica se webdriver está com ou sem interface
    if not browser_is_closed(driver):
        try:
            while True:
                # obtem usuario e senha da planilha
                user, pswd = roteadores['Senha'].to_list()[index].split(' / ')
                try:
                    # busca campo de usário
                    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'userName')))
                except:
                    element = None
                if element:
                    # preenche campo de usuário
                    element.send_keys(user)
                else:
                    continue
                try:
                    # busca campo de senha
                    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'pcPassword')))
                except:
                    element = None
                if element:
                    # preenche campo de senha
                    element.send_keys(pswd)
                else:
                    continue
                try:
                    # busca botão de login
                    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'loginBtn')))
                except:
                    element = None
                if element:
                    # clica no botão de login
                    element.click()
                else:
                    continue
                try:
                    # verifica se há elemento indicando erro no login
                    nota = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'tip')))
                except:
                    nota = None
                    print
                    break
                if nota:
                    logger.warning("Erro ao logar no roteador {} - {}".format(roteadores['SSID'].to_list()[index], nota.text))
                    print(nota.text)
                    continue
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error('FUNÇÃO {} - TIPO {} - ARQUIVO {} - LINHA {} - MESSAGE:{}'.format(login_TL_WR841HP.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
    else:
        raise selenium_exceptions.WebDriverException("webdriver foi fechado")

def restart_TL_WR841HP(roteadores:pd.DataFrame, index:int):
    """Reinicia roteador WR841HP

    Args:
        roteadores (pd.DataFrame): Planilha contendo informações dos roteadores
        index (int): index do roteador a ser reiniciado

    Raises:
        selenium_exceptions.WebDriverException: Caso o webbdriver seja fechado durante a execução
    """
    try:
        driver = init_selenium(SEM_CABECA)
        i = 1
        driver.get(roteadores['Acesso'].to_list()[index])
        login_TL_WR841HP(driver, roteadores, index)
        if not browser_is_closed(driver):
            while True:
                i += 1
                ActionChains(driver).send_keys(Keys.TAB).perform()
                if i >= 19:
                    break 
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            i = 1
            while True:
                i += 1
                ActionChains(driver).send_keys(Keys.TAB).perform()
                if i >= 5:
                    break 
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            time.sleep(5)
            
            driver.find_elements(By.ID, 'frame2')[0].send_keys(Keys.TAB)
            driver.find_elements(By.ID, 'frame2')[0].send_keys(Keys.ENTER)
            time.sleep(1)
            alert = Alert(driver)
            alert.accept()
            logger.info('Reinicialização {} iniciada'.format(roteadores['SSID'].to_list()[index]))
            print('Roteador', roteadores['SSID'].to_list()[index], 'reinicializando, aguarde 1 minuto para término do processo')
            time.sleep(60)
            logger.info('Reinicialização {} concluída'.format(roteadores['SSID'].to_list()[index]))
        else:
            raise selenium_exceptions.WebDriverException("webdriver foi fechado")
    except Exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error('FUNÇÃO {} - TIPO {} - ARQUIVO {} - LINHA {} - MESSAGE:{}'.format(restart_TL_WR841HP.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
    finally:
        driver.quit()

def login_AC1200_ARCHER_C6(driver:webdriver.Chrome, roteadores:pd.DataFrame, index:int):
    """Realiza login no roteador C6

    Args:
        driver (webdriver.Chrome): Navegador automatizado Chrome webdriver
        roteadores (pd.DataFrame): Planilha contendo informações dos roteadores
        index (int): index do roteador a ser reiniciado

    Raises:
        selenium_exceptions.WebDriverException: Caso o webbdriver seja fechado durante a execução

    Returns:
        bool: Checagem se houve sucesso em logar no roteador
    """
    try:
        # variavel para retorno se houve sucesso para logar no roteador
        logged = False
        # verifica se webdriver está com ou sem cabeça
        if not browser_is_closed(driver):
            time.sleep(5)
            while True:
                # obtem senha do planilha
                pswd = roteadores['Senha'].to_list()[index]
                try:
                    # procura elemento form
                    form = driver.find_element(By.ID, 'form-login')
                except:
                    form = None
                if form:
                    try:
                        # busca campo de senha
                        element = form.find_element(By.TAG_NAME, 'input')
                    except:
                        element = None
                else:
                    continue
                if element:
                    # preencha campo de senha
                    element.send_keys(pswd)
                else:
                    continue
                try:
                    # busca botão de login
                    element = form.find_element(By.ID, 'login-btn')
                except:
                    element = None
                if element:
                    # clica no botão de login
                    element.click()
                else:
                    continue
                # verificação se houve no login
                try:
                    banner = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'menu-basic')))
                except:
                    banner = None
                if banner:
                    logged = True
                    break
                else:
                    try:
                        conflict = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'user-conflict-msg-container')))
                    except:
                        conflict = None
                        continue
                    if conflict:
                        try:
                            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.button-button.btn-msg.btn-msg-ok.btn-prompt')))
                        except:
                            element = None
                        if element:
                            element.click()
                            logged = True
                            break
                        else:
                            logger.error('Erro de conflito de login')
        else:
            raise selenium_exceptions.WebDriverException("webdriver foi fechado")
        return logged
    except Exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error('FUNÇÃO {} - TIPO {} - ARQUIVO {} - LINHA {} - MESSAGE:{}'.format(login_AC1200_ARCHER_C6.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))

def restart_AC1200_ARCHER_C6(roteadores:pd.DataFrame, index:int):
    """Reinicia roteador C6

    Args:
        roteadores (pd.DataFrame): Planilha contendo informações dos roteadores
        index (int): index do roteador a ser reiniciado

    Raises:
        selenium_exceptions.WebDriverException: Caso o webbdriver seja fechado durante a execução
    """
    try:
        driver = init_selenium(SEM_CABECA)
        if not browser_is_closed(driver):
            driver.get((roteadores['Acesso'].to_list()[index]))
            if login_AC1200_ARCHER_C6(driver, roteadores, index):
                try:
                    # busca botão de Reboot
                    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'top-control-reboot')))
                except:
                    element = None
                if element:
                    driver.execute_script("arguments[0].scrollIntoView();", element)
                    # se encontrado clica
                    element.click()
                    time.sleep(5)
                else:
                    logger.error("Elemento não encontrado")
                try:
                    # busca mensagem de confirmação de reboot
                    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-msg-ok')))
                except:
                    element = None
                if element:
                    element.click()
                else:
                    logger.error("Elemento não encontrado")
                logger.info('Reinicialização {} iniciada'.format(roteadores['SSID'].to_list()[index]))
                print('Roteador', roteadores['SSID'].to_list()[index], 'reinicializando, aguarde 2 minutos para término do processo')
                time.sleep(120)
                logger.info('Reinicialização {} concluída'.format(roteadores['SSID'].to_list()[index]))
            else:
                logger.error('Erro ao logar no roteador {}'.format(roteadores['SSID'].to_list()[index]))
        else:
            raise selenium_exceptions.WebDriverException("webdriver foi fechado")
    except Exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error('FUNÇÃO {} - TIPO {} - ARQUIVO {} - LINHA {} - MESSAGE:{}'.format(restart_AC1200_ARCHER_C6.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
    finally:
        driver.quit()

def login_AC1200_ARCHER_C5(driver:webdriver.Chrome, roteadores:pd.DataFrame, index:int):
    """Realiza login no roteador C5

    Args:
        driver (webdriver.Chrome): Navegador automatizado Chrome webdriver
        roteadores (pd.DataFrame): Planilha contendo informações dos roteadores
        index (int): index do roteador a ser reiniciado

    Raises:
        selenium_exceptions.WebDriverException: Caso o webbdriver seja fechado durante a execução

    Returns:
        bool: Checagem se houve sucesso em logar no roteador
    """
    try:
        # variavel para retorno se houve sucesso para logar no roteador
        logged = False
        # verifica se webdriver está com ou sem cabeça
        if not browser_is_closed(driver):
            time.sleep(5)
            while True:
                # obtem senha do planilha
                pswd = roteadores['Senha'].to_list()[index]
                try:
                    # procura campo de senha
                    element = driver.find_element(By.ID, 'pc-login-password')
                except:
                    element = None
                if element:
                    try:
                        # busca campo de senha
                        element.send_keys(pswd)
                    except:
                        element = None
                else:
                    # verificação se houve no login
                    try:
                        menuTree = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'menuTree')))
                    except:
                        menuTree = None
                    if menuTree:
                        logged = True
                        break
                    else:
                        logger.warning('Erro ao logar no roteador {}'.format(roteadores['SSID'].to_list()[index]))
                        continue
                try:
                    # busca botão de login
                    element = driver.find_element(By.ID, 'pc-login-btn')
                except:
                    element = None
                if element:
                    # clica no botão de login
                    element.click()
                else:
                    continue
                # verificação se houve no login
                time.sleep(5)
                try:
                    menuTree = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'menuTree')))
                except:
                    menuTree = None
                if menuTree:
                    logged = True
                    break
                else:
                    logger.warning('Erro ao logar no roteador {}'.format(roteadores['SSID'].to_list()[index]))
                    continue
        else:
            raise selenium_exceptions.WebDriverException("webdriver foi fechado")
        return logged
    except Exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error('FUNÇÃO {} - TIPO {} - ARQUIVO {} - LINHA {} - MESSAGE:{}'.format(login_AC1200_ARCHER_C5.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))

def restart_AC1200_ARCHER_C5(roteadores:pd.DataFrame, index:int):
    """Reinicia roteador C5

    Args:
        roteadores (pd.DataFrame): Planilha contendo informações dos roteadores
        index (int): index do roteador a ser reiniciado

    Raises:
        selenium_exceptions.WebDriverException: Caso o webbdriver seja fechado durante a execução
    """
    try:
        driver = init_selenium(SEM_CABECA)
        if not browser_is_closed(driver):
            driver.get((roteadores['Acesso'].to_list()[index]))
            if login_AC1200_ARCHER_C5(driver, roteadores, index):
                try:
                    # busca botão de Reboot
                    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'topReboot')))
                except:
                    element = None
                if element:
                    # se encontrado clica
                    element.click()
                else:
                    logger.error("Elemento não encontrado")
                try:
                    # busca mensagem de confirmação de reboot
                    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-msg-ok')))
                except:
                    element = None
                if element:
                    element.click()
                else:
                    logger.error("Elemento não encontrado")
                logger.info('Reinicialização {} iniciada'.format(roteadores['SSID'].to_list()[index]))
                print('Roteador', roteadores['SSID'].to_list()[index], 'reinicializando, aguarde 1 minuto para término do processo')
                time.sleep(60)
                logger.info('Reinicialização {} concluída'.format(roteadores['SSID'].to_list()[index]))
            else:
                logger.error('Erro ao logar no roteador {}'.format(roteadores['SSID'].to_list()[index]))
        else:
            raise selenium_exceptions.WebDriverException("webdriver foi fechado")
    except Exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error('FUNÇÃO {} - TIPO {} - ARQUIVO {} - LINHA {} - MESSAGE:{}'.format(restart_AC1200_ARCHER_C5.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
    finally:
        driver.quit()
    
def get_roteadores():
    """Obtem informações dos roteadores contidas na planilha google

    Raises:
        ConnectionError: Caso não tenha conexão com rede

    Returns:
        pd.DataFrame: Planilha pandas contendo as informações
    """
    if check_internet():
        try:
            # id da planilha no google
            sheet_id = '1OnhWA98xNmpbPT2XFaJto4_gf8FoscAjUgYXAv9Bsf4'
            # nome da aba
            sheet_name = 'ROTEADORES'
            # formando a url para exportação do csv
            url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
            # lendo csv da url
            df = pd.read_csv(url, skiprows=[0,2,3,4,6,10,13,14,15,16,17,18]) 
            # filtrando apenas o conteúdo necessário
            new_df = df[['Acesso','SSID','Senha']]
            return new_df
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error('FUNÇÃO {} - TIPO {} - ARQUIVO {} - LINHA {} - MESSAGE:{}'.format(get_roteadores.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
    else:
        raise ConnectionError("Internet fora do ar!")

def add_device_whitelist_TL_WR841HP(devices:dict, roteadores:pd.DataFrame, index:int):
    """Adiciona dispositivo no controle de acesso dos roteadores wr841hp

    Args:
        devices (dict): dicionario com nome e mac dos dispositos a serem adicionados
        roteadores (pd.DataFrame): planilha com dados do roteador
        index (int): index do roteador a ser acessado

    Raises:
        selenium_exceptions.WebDriverException: caso o webdriver seja fechado
    """
    try:
        driver = init_selenium(SEM_CABECA)
        if not browser_is_closed(driver):
            i = 1
            driver.get(roteadores['Acesso'].to_list()[index])
            login_TL_WR841HP(driver, roteadores, index)
            # frame1 =  driver.find_element(By.ID, 'frame1')
            # Navega até opção "Wireless" no menu lateral
            while True:
                i += 1
                ActionChains(driver).send_keys(Keys.TAB).perform()
                # frame1.send_keys(Keys.TAB)
                if i >= 7:
                    break 
            # entra na opção "Wireless" no menu lateral
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            time.sleep(5)
            i = 1
            # Navega até subopção do "Filtro de MAC Wireless"
            while True:
                i += 1
                ActionChains(driver).send_keys(Keys.TAB).perform()
                if i >= 5:
                    break 
            # entra na subopção "Filtro de MAC Wireless"
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            time.sleep(5)
            for device_name, mac in devices.items():
                # frame2 = driver.find_element(By.ID, 'frame2')
                try:
                    frame2 = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'frame2')))
                except:
                    frame2 = None
                if frame2:
                    # vai até o botão de "Adicionar Novo"
                    frame2.send_keys(Keys.TAB)
                    frame2.send_keys(Keys.TAB)
                    frame2.send_keys(Keys.ENTER)
                    time.sleep(5)
                    # vai até o campo "Endereço MAC"
                    frame2.send_keys(Keys.TAB)
                    frame2.send_keys(mac)
                    time.sleep(5)
                    # vai até o campo "Descrição"
                    frame2.send_keys(Keys.TAB)
                    frame2.send_keys(device_name)
                    time.sleep(5)
                    # vai até o botão "Salvar"
                    frame2.send_keys(Keys.TAB)
                    frame2.send_keys(Keys.TAB)
                    frame2.send_keys(Keys.ENTER)
                    # busca alerta
                    try:
                        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                    except:
                        alert = None
                    if alert:
                        logger.error("{}Dispositivo {} com MAC {} não adicionado".format(alert.text, device_name, mac))
                        # clica no "Ok" do alerta
                        alert = Alert(driver)
                        alert.accept()
                        # vai até botão de voltar
                        frame2.send_keys(Keys.TAB)
                        frame2.send_keys(Keys.TAB)
                        frame2.send_keys(Keys.TAB)
                        frame2.send_keys(Keys.TAB)
                        frame2.send_keys(Keys.ENTER)
                    else:
                        logger.info('Dispositivo {} com MAC {} adicionado com sucesso'.format(device_name, mac))
                else:
                    logger.error('Erro ao buscar o elemento frame2')
        else:
            raise selenium_exceptions.WebDriverException("webdriver foi fechado")
    except:
        if driver:
            driver.quit()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error('ERRO DURANTE EXECUÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(add_device_whitelist_TL_WR841HP.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))

def add_device_whitelist_archer_c6(devices:dict, roteadores:pd.DataFrame, index:int):
    """Adiciona dispositivo no controle de acesso dos roteadores c6

    Args:
        devices (dict): dicionario com nome e mac dos dispositos a serem adicionados
        roteadores (pd.DataFrame): planilha com dados do roteador
        index (int): index do roteador a ser acessado

    Raises:
        selenium_exceptions.WebDriverException: caso o webdriver seja fechado
    """
    try:
        driver = init_selenium(SEM_CABECA)
        if not browser_is_closed(driver):
            try:
                driver.get(roteadores['Acesso'].to_list()[index])
                if login_AC1200_ARCHER_C6(driver, roteadores, index):
                    time.sleep(5)
                    try:
                        # busca aba "Advanced" 
                        element = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.NAME, 'advanced')))
                    except:
                        element = None
                    # verifica se elemento foi encontrado e clica nele
                    if element is not None:
                        element.click()
                        time.sleep(5)
                        try:
                            # busca opção "Security" no menu lateral
                            element = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.NAME, 'security')))
                        except:
                            element = None
                        # verifica se elemento foi encontrado e clica nele
                        if element is not None:
                            element.click()
                            time.sleep(5)
                            try:
                                # # busca subopção "Acess Control" no menu lateral
                                element = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.NAME, 'access-control')))
                            except:
                                element = None
                            # verifica se elemento foi encontrado e clica nele
                            if element is not None:
                                element.click()
                                # percorre dicionario com os dispositivos e macs
                                for device, mac in devices.items():
                                    time.sleep(5)
                                    try:
                                        # busca botão "+Add"
                                        add = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='operation-btn btn-add  ']")))
                                    except:
                                        add = None
                                    # verifica se elemento foi encontrado e clica nele
                                    if add is not None:
                                        driver.execute_script("arguments[0].scrollIntoView();", add[-1])
                                        add[-1].click()
                                        time.sleep(5)
                                        try:
                                            # busca formulário para preencher dispositivo e mac
                                            element = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//tr[@class='editor-container container widget-container']")))
                                        except:
                                            element = None
                                        # verifica se elemento foi encontrado e clica nele
                                        if element is not None:
                                            form = element.find_element(By.TAG_NAME, 'form')
                                            if form:
                                                # busca os campos a ser preenchido
                                                input_name = form.find_element(By.NAME, 'name')
                                                input_mac = form.find_element(By.NAME, 'mac')
                                                # rola até o elemento
                                                driver.execute_script("arguments[0].scrollIntoView();", input_mac)
                                                try:
                                                    # preenche os campos
                                                    input_name.send_keys(device)
                                                    input_mac.send_keys(mac)
                                                except:
                                                    input_name.send_keys(device)
                                                    input_mac.send_keys(mac)
                                                # procura o botão de "Save" e clica nele
                                                button = form.find_element(By.XPATH, "//button[@class='editor-btn btn-submit button-button']")
                                                button.click()
                                                try:
                                                    # busca elemento indicando erro ao adicionar dispositivo
                                                    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//span[@class="form-error-tips"]')))
                                                except:
                                                    element = None
                                                #  se existir elemento houve ao adicionar o elemento
                                                if element:
                                                    logger.error(element.text)
                                                    logger.error('Dispositivo {} com MAC {} não foi adicionado'.format(device, mac))
                                                    try:
                                                        # busca elemento botão "Cancel"
                                                        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".editor-btn.btn-cancel.button-button")))
                                                    except:
                                                        element = None
                                                    if element:
                                                        element.click()
                                                    else:
                                                        logger.error('Erro ao clicar no botão "Cancel"')
                                                else:
                                                    logger.info('Dispositivo {} com MAC {} adicionado com sucesso'.format(device, mac))
                                    else:
                                        logger.error("Erro ao clicar no botão 'Add'")
                            else:
                                logger.error("Erro ao clicar na seção 'Acess Control'")
                        else:
                            logger.error("Erro ao clicar na seção 'Security'")            
                    else:
                        logger.error("Erro ao clicar na aba 'Advanced'")        
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                logger.error('ERRO DURANTE EXECUÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(add_device_whitelist_TL_WR841HP.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))

        else:
            raise selenium_exceptions.WebDriverException("webdriver foi fechado")
    except:
        if driver:
            driver.quit()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error('ERRO DURANTE EXECUÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(add_device_whitelist_archer_c6.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))

def add_device_whitelist_archer_c5(devices:dict, roteadores:pd.DataFrame, index:int):
    """Adicione dispositivo na white list do roteador c5

    Args:
        devices (dict): Dicionario com os dispositivos a serem adicionados
        roteadores (pd.DataFrame): matriz com as informações dos roteadores
        index (int): index do roteador a ser utilizado

    Raises:
        selenium_exceptions.WebDriverException: Erro ao fechar o webdriver durante execução
    """
    try:
        driver = init_selenium(SEM_CABECA)
        if not browser_is_closed(driver):
            try:
                driver.get(roteadores['Acesso'].to_list()[index])
                if login_AC1200_ARCHER_C5(driver, roteadores, index):
                    try:
                        # busca aba "Avançado"
                        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "advanced")))
                    except:
                        element = None
                    # se encontrar o elemento clica nele
                    if element:
                        element.click()
                        try:
                            # busca opção "Segurança"
                            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@url="ddos.htm"]')))
                        except:
                            element = None
                        # se encontrar o elemento clica nele
                        if element:
                            element.click()
                            try:
                                # buscar subopção "Controle de acesso"
                                element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@url="accessControl.htm"]')))
                            except:
                                element = None
                            # se encontrar o elemento clica nele
                            if element:
                                time.sleep(2)
                                element.click()
                            else:
                                logger.error('Erro ao acessar subopção "Controle de acesso"')
                            for device_name, mac in devices.items():
                                try:
                                    # buscar botão "Adicionar"
                                    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'addWhiteListIcon')))
                                except:
                                    element = None
                                # se encontrar elemento clica nele
                                if element:
                                    element.click()
                                    try:
                                        # busca tabela para adicionar dispositivo
                                        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'editContainerDevicesInWhiteList')))
                                    except:
                                        element = None
                                    if element:
                                        try:
                                            input_name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'whiteDevName')))
                                            input_name.send_keys(device_name)
                                            input_mac = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.tpAddress-cell-input.tp-input-text.whiteMacAddr-address-cell')))
                                            # percorre os input do mac e preenche
                                            for element in input_mac:
                                                # busca o index do elemento atual
                                                index_mac = input_mac.index(element)
                                                element.send_keys(mac.split('-')[index_mac].lower())
                                            save_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'whiteListEditOk')))
                                            save_button.click()
                                            try:
                                                # busca se houve erro ao adicionar dispositivo
                                                element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.msg-container-wrapper')))
                                            except:
                                                element = None
                                            if element:
                                                try:
                                                    # busca mensagem de erro
                                                    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.msg-wrap')))
                                                except:
                                                    element = None
                                                if element:
                                                    logger.error(element.text.replace('\n', ' '))
                                                    logger.error('Dispositivo {} com MAC {} não foi adicionado'.format(device_name, mac))
                                                    try:
                                                        # busca butão "OK" da mensagem de erro
                                                        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.button-button.green.pure-button.btn-msg.btn-msg-ok.btn-confirm')))
                                                    except:
                                                        element = None
                                                    # se encontrar o elemento clica nele
                                                    if element:
                                                        element.click()
                                                        try:
                                                            # busca botão "Cancelar" 
                                                            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'whiteListEditCancel'))).click()
                                                        except:
                                                            element = None
                                                        if element:
                                                            # se encontrar elemento clica nele
                                                            element.click()
                                                        else:
                                                            logger.error('Erro ao clicar no botão "Cancelar"')

                                                    else:
                                                        logger.error('Erro ao clicar no botão "OK" da mensagem de erro')
                                                else:
                                                    logger.info('Dispositivo {} com MAC {} adicionado com sucesso'.format(device_name, mac))
                                            else:
                                                logger.info('Dispositivo {} com MAC {} adicionado com sucesso'.format(device_name, mac))
                                        except:
                                            logger.error()
                                else:
                                    logger.error('Erro ao acessar botão "Adicionar"')
                        else:
                            logger.error('Erro ao acessar opção "Segurança"')
                    else:
                        logger.error('Erro ao acessar ')
                else:
                    logger.error('Erro ao logar no roteador {}'.format(roteadores['SSID'].to_list()[index]))
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                logger.error('ERRO DURANTE EXECUÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(add_device_whitelist_TL_WR841HP.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
        else:
            raise selenium_exceptions.WebDriverException("webdriver foi fechado")
    except:
        if driver:
            driver.quit()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error('ERRO DURANTE EXECUÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(add_device_whitelist_archer_c5.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))

def get_acess_control_c5(roteadores:pd.DataFrame, index:int):
    try:
        driver = init_selenium(SEM_CABECA)
        if not browser_is_closed(driver):
            driver.get(roteadores['Acesso'].to_list()[index])
            if login_AC1200_ARCHER_C5(driver, roteadores, index):
                try:
                    # busca aba "Avançado"
                    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "advanced")))
                except:
                    element = None
                # se encontrar o elemento clica nele
                if element:
                    element.click()
                    try:
                        # busca opção "Segurança"
                        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@url="ddos.htm"]')))
                    except:
                        element = None
                    # se encontrar o elemento clica nele
                    if element:
                        element.click()
                        try:
                            # buscar subopção "Controle de acesso"
                            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@url="accessControl.htm"]')))
                        except:
                            element = None
                        # se encontrar o elemento clica nele
                        if element:
                            time.sleep(2)
                            element.click()
                        else:
                            logger.error('Erro ao acessar subopção "Controle de acesso"')
                        # buscar tabela de controle de acesso

                    else:
                        logger.error('Erro ao acessar opção "Segurança"')
                else:
                    logger.error('Erro ao acessar{}'.format(roteadores['SSID'].to_list()[index]))
            else:
                logger.error('Erro ao logar no roteador {}'.format(roteadores['SSID'].to_list()[index]))
    except:
        if driver:
            driver.quit()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error('ERRO DURANTE EXECUÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(get_acess_control_c5.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))

def get_acess_control_c6(roteadores:pd.DataFrame, index:int):
    try:
        driver = init_selenium(SEM_CABECA)
        if not browser_is_closed(driver):
            driver.get(roteadores['Acesso'].to_list()[index])
            if login_AC1200_ARCHER_C6(driver):
                time.sleep(5)
                try:
                    # busca aba "Advanced" 
                    element = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.NAME, 'advanced')))
                except:
                    element = None
                # verifica se elemento foi encontrado e clica nele
                if element is not None:
                    element.click()
                    time.sleep(5)
                    try:
                        # busca opção "Security" no menu lateral
                        element = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.NAME, 'security')))
                    except:
                        element = None
                    # verifica se elemento foi encontrado e clica nele
                    if element is not None:
                        element.click()
                        time.sleep(5)
                        try:
                            # # busca subopção "Acess Control" no menu lateral
                            element = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.NAME, 'access-control')))
                        except:
                            element = None
                        # verifica se elemento foi encontrado e clica nele
                        if element is not None:
                            element.click()
                            # buscar elemento da tabela de controle de acesso
                        else:
                            logger.error("Erro ao clicar na seção 'Acess Control'")
                    else:
                        logger.error("Erro ao clicar na seção 'Security'")            
                else:
                    logger.error("Erro ao clicar na aba 'Advanced'")        

        else:
            raise selenium_exceptions.WebDriverException("webdriver foi fechado")
    except:
        if driver:
            driver.quit()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error('ERRO DURANTE EXECUÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(get_acess_control_c6.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))

def get_path_file(wildcard):
    """Abre janela de dialogo para abrir arquivo

    Args:
        wildcard (str): filtro de arquivos

    Returns:
        str: caminho do arquivo
    """
    try:
        app = wx.App(None)
        style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        dialog = wx.FileDialog(None, 'Selecione o arquivo CSV', wildcard=wildcard, style=style)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
        else:
            path = None
        dialog.Destroy()
        return path
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error('ERRO DURANTE EXECUÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(get_path_file.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))

def get_csv():
    """Abre janela para selecionar arquivo csv e realiza a leitura

    Returns:
        pd.DataFrame: planilha do csv
    """
    try:
        csv_path = None
        while csv_path is None:
            # filtro apenas arquivos csv
            csv_path = get_path_file("*.csv")
        # realiza leitura do csv
        df = pd.read_csv(csv_path)
        return df
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error('ERRO DURANTE EXECUÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(get_csv.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))

def reinicia_roteadores(op:int):   
    if op == 0:
        restart_AC1200_ARCHER_C6(roteadores, op)
    elif op == 1:
        restart_AC1200_ARCHER_C6(roteadores, op)
    elif op == 2:
        restart_AC1200_ARCHER_C5(roteadores, op)
    elif op == 3:
        restart_AC1200_ARCHER_C6(roteadores, op)
    elif op == 4:
        restart_TL_WR841HP(roteadores, op)
    elif op == 5:
        restart_TL_WR841HP(roteadores, op)

def adicione_controle_acesso(op:int):
    csv_device = get_csv()
    if op == 0:
        devices_dic = {y[0].split(";")[0]:y[0].split(";")[1].replace(":", "-") for y in [x for x in csv_device._values]}
        add_device_whitelist_archer_c6(devices_dic, roteadores, op)
    elif op == 1:
        devices_dic = {y[0].split(";")[0]:y[0].split(";")[1].replace(":", "-") for y in [x for x in csv_device._values]}
        add_device_whitelist_archer_c6(devices_dic, roteadores, op)
    elif op == 2:
        devices_dic = {y[0].split(";")[0]:y[0].split(";")[1].replace(":", "-") for y in [x for x in csv_device._values]}
        add_device_whitelist_archer_c5(roteadores, op)
    elif op == 3:
        devices_dic = {y[0].split(";")[0]:y[0].split(";")[1].replace(":", "-") for y in [x for x in csv_device._values]}
        add_device_whitelist_archer_c6(roteadores, op)
    elif op == 4:
        devices_dic = {y[0].split(";")[0]:y[0].split(";")[1].replace("-", ":") for y in [x for x in csv_device._values]}
        add_device_whitelist_TL_WR841HP(devices_dic, roteadores, op)
    elif op == 5:
        devices_dic = {y[0].split(";")[0]:y[0].split(";")[1].replace("-", ":") for y in [x for x in csv_device._values]}
        add_device_whitelist_TL_WR841HP(devices_dic, roteadores, op)
    else:
        print("Opção inválida ou inexistente!")

def selecione_roteador(roteadores):
    for index,item in enumerate(roteadores['SSID'].to_list()):
        print("{} - {}".format(index, item))
    choice = ""
    while type(choice) != int:
        try:
            choice = int(input('Digite o numero do roteador e aperte ENTER-> '))
        except:
            continue
    return choice

if __name__ == "__main__":
    if check_internet():
        while True:
            roteadores = get_roteadores()
            print("CONTROLE AUTOMÁTICO DE ROTEADORES")
            print("1 - reinicia roteadores\n2 - adicionar dispositivo na white list")
            choice = ''
            while type(choice) != int:
                try:
                    choice = int(input('Digite o numero da opção desejada e aperte ENTER-> '))
                except:
                    print("Deve digitar um número")
                    continue
                if choice == 1:
                    op = selecione_roteador(roteadores)
                    reinicia_roteadores(op)
                elif choice == 2:
                    op = selecione_roteador(roteadores)
                    adicione_controle_acesso(op)
                else:
                    print("Opção inválida ou inexistente!")
    else:
        print("Internet fora do ar!")
