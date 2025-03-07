from bs4 import BeautifulSoup
import requests
import os
import ntpath
import sys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.core.os_manager import ChromeType
import re
from wx import App, FileDialog, DirDialog, FD_OPEN, FD_FILE_MUST_EXIST, ID_OK, DD_DEFAULT_STYLE, DD_DIR_MUST_EXIST

class Utils:
    def __init__(self):
        pass

    def check_internet()-> bool:
        """Simples requisição no site do google se não houver resposta no dentro timeout definido, implica que há um erro na conexão
        """
        timeout = 10
        try:
            # requisição com tempo limite de 10 segundos
            requests.get('https://www.google.com', timeout=timeout)
            return True
        except ConnectionError:
            print('Sem conexão')
            return False
    
    def web_scrape(self, url:str=None, markup:str=None)-> BeautifulSoup:
        """Realiza requisição na URL informada e obtem dados do site da url"""
        if markup is not None:
            html_markup = markup
        if url is not None:
            # realiza requisição na URL informada
            req = requests.get(url)
            html_markup = req.content
        # obtem dados do site do html informado
        site = BeautifulSoup(html_markup, features="html.parser")
        return site
    
    def init_webdriver(self, default=True, headless=False, output:str=None):
        """Inicia navegador automatizado google chrome

        Args:
            default (bool, optional): Define se navegador será aberto com opções padrão. Defaults to True.
            headless (bool, optional): Define se navegador abrirá com interface. Defaults to False.
            saida (str, optional): Diretório para downloads. Defaults to None.

        Returns:
            webdriver: navegador automatizado google chrome configurado
        """
        try:
            print('Iniciando navegador automatizado google chrome')
            s=ChromeService(ChromeDriverManager().install())
            if default:
                if headless:
                    driver = webdriver.Chrome(service=s, options=self.options_chrome(headless=True, download_output=output))
                else:
                    driver = webdriver.Chrome(service=s, options=self.options_chrome(headless=False, download_output=output))
                    # driver = webdriver.Chrome(service=s, options=self.options_chrome(headless=False, download_output=output))
            else:
                # caminho das extensões
                extension_path = os.path.join(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0], 'extensions')
                extensions = [os.path.join(extension_path, 'popup_blocker.crx'), os.path.join(extension_path, 'enable_right_click.crx')]
                # extension = [os.path.join(extension_path, 'adblock.crx'), os.path.join(extension_path, 'enable_right_click.crx')]
                # extension = [os.path.join(extension_path, 'enable_right_click.crx')]
                try:
                    if headless:
                        driver = webdriver.Chrome(service=s, options=self.options_chrome(headless=True, download_output=output, crx_extension=extensions))
                    else:
                        driver = webdriver.Chrome(service=s, options=self.options_chrome(headless=False, download_output=output, crx_extension=extensions))
                except:
                    if headless:
                        driver = webdriver.Chrome(service=s, options=self.options_chrome(headless=True, download_output=output))
                    else:
                        driver = webdriver.Chrome(service=s, options=self.options_chrome(headless=False, download_output=output))
            return driver
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO NA FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.init_webdriver.__name__,exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace('\n', '')))
            sys.exit()

    def options_chrome(self, headless=False, download_output=None, crx_extension:list=None):
        """Configura opções do navegador chrome

        Args:
            headless (bool, optional): Define se navegador irá iniciar sem interface. Defaults to False.
            download_output (str, optional): Define diretorio para downloads. Defaults to None.
            crx_extension (list, optional): Listas de extensões para instalar no navegador. Defaults to None.

        Returns:
            Options: objeto contendo todas as opções configuradas do navegador
        """
        # Criar uma instância dr opções Chrome e devolvê-lo. Esta é a primeira chamada que você quer executar
        try:
            chrome_options = Options()
            if(headless):
                chrome_options.add_argument("--headless")
            prefs = {}
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-logging")
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--ignore-ssl-errors")
            # chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0")
            binary_location = self.verify_chrome()
            chrome_options.binary_location = binary_location
            if download_output:
                download_output = os.path.normpath(download_output)
                download_output = download_output.replace('/',ntpath.sep)
                prefs.update({"download.default_directory" : download_output})
            if crx_extension:
                for extension in crx_extension:
                    chrome_options.add_extension(extension)
            chrome_options.add_experimental_option('prefs', prefs)
            return chrome_options
            
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERRO DURANTE EXECUÇÃO {}: \nTIPO - {}\nARQUIVO - {}\nLINHA - {}\nMESSAGE:{}'.format(self.options_chrome.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__))
        
    def verify_chrome(self):
        """Verifica se existe navegador chrome instalado e retorna o binario do navegador

        Returns:
            str: caminho do binário do navegador chrome
        """
        # Retorna o caminho para o executável mais recente do Chrome x32 ou X86. Isso é baseado na presença de um arquivo
        results_32 = [x for x in os.listdir(os.environ['PROGRAMFILES']) if re.search(r'(google)', x, re.IGNORECASE)]
        results_64 = [x for x in os.listdir(os.environ['PROGRAMFILES(X86)']) if re.search(r'(google)', x, re.IGNORECASE)]
        # Retorna o navegador da base de dados.
        if results_32:
            chrome_path = os.path.join(os.environ['PROGRAMFILES'], results_32[0], 'Chrome', 'Application')
            files = [x for x in os.listdir(chrome_path) if re.search(r'.exe$', x)]
            # Retorna o primeiro arquivo na lista de arquivos.
            if len(files) == 1:
                file = files[0]
            else:
                file = [x for x in files if re.search(r'chrome.exe', x)][0]
            
            browser_path = os.path.join(chrome_path,file)
            return browser_path
        elif results_64:
            chrome_path = os.path.join(os.environ['PROGRAMFILES(X86)'], results_64[0], 'Chrome', 'Application')
            files = [x for x in os.listdir(chrome_path) if re.search(r'.exe$', x)]
            # Retorna o primeiro arquivo na lista de arquivos.
            if len(files) == 1:
                file = files[0]
            else:
                file = [x for x in files if re.search(r'chrome.exe', x)][0]
            browser_path = os.path.join(chrome_path, file)
            return browser_path
        else:
            print("Navegador não instalado")
            return None
        
    def wx_filedialog(self, wildcard):
        """Abre janela de dialogo para abrir arquivo
        Args:
            wildcard (str): filtro de arquivos
        Returns:
            str: caminho do arquivo
            """
        app = App(None) # type: ignore
        style = FD_OPEN | FD_FILE_MUST_EXIST
        dialog = FileDialog(None, 'Selecione o arquivo', wildcard=wildcard, style=style)
        if dialog.ShowModal() == ID_OK:
            path = dialog.GetPath()
            dialog.Destroy()
            app.Destroy()
            return path
        else:
            path = ""
            dialog.Destroy()
            app.Destroy()
            return path

    def wx_dirdialog(self):
        """Abre janela de dialogo para abrir pasta
        Returns:
            str: caminho da pasta
        """
        app = App(None)
        dialog = DirDialog (None, "Escolha o diretório", "", DD_DEFAULT_STYLE | DD_DIR_MUST_EXIST)
        if dialog.ShowModal() == ID_OK:
            path = dialog.GetPath()
        else:
            path = None
        dialog.Destroy()
        return path