import requests
import pandas as pd
from os import path, mkdir, listdir
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

def webScrape(url:str):
    """Realiza requisição na URL informada e obtem dados do site da url"""
    # realiza requisição na URL informada
    req = requests.get(url)
    # obtem dados do site da requisição realizada
    site = BeautifulSoup(req.content, features="lxml")
    return site

def criarPasta(nome, dir_nome):
    """ Cria uma pasta com nome e caminho especificado na função """
    try:
        # remove caractere problematico no windows
        nome = nome.replace(':', ' - ')
        # lista itens do diretorio informado
        directory = listdir(dir_nome)
        # realiza junção do nome com o diretorio
        complete = path.join(dir_nome, nome)
        # verifica se não existe o diretorio com o nome informado, se existir apenas retorna o caminho completo da url
        if(nome not in directory):
            # verifica se não existe o diretorio com o nome informado se sim cria pasta, senão apenas retorna o caminho completo
            if not path.isdir(complete):
                mkdir(complete)
                return complete
            return complete
        else:
            # print('Diretório {} existente'.format(complete))
            return complete
    except Exception as err:
        print('ERROR (criarPasta): {0}'.format(err))

def downloadArchive(url, path_archive, nome_arquivo=None):  
    try:
        # realiza requisição no arquivo
        response = requests.get(url, stream=True)
        # obtem nome do arquivo da url
        name_file_url = path.basename(response.url.split("/")[-1])
        if nome_arquivo:
            # obtem extensão do arquivo
            extension = name_file_url.split(".")[-1]
            path_archiveName = path.join(path_archive, '{}.{}'.format(nome_arquivo, extension))
        else:
            # define o caminho do arquivo a ser salvo
            path_archiveName = path.join(path_archive, path.basename(response.url.split("/")[-1]))
        # verifica codigo de status da requisição
        if response.status_code == requests.codes.OK: #pylint: disable=no-member
            # abre o arquivo e inicia a escrita
            with open(path_archiveName, "wb") as f:
                for chunk in response:
                    f.write(chunk)
            # print("Download finalizado. Arquivo salvo em: {}".format(path_archiveName))
        else:
            response.raise_for_status()
    except Exception as err:
        if('520 Server Error' in str(err) or '522 Server Error' in str(err) or '404 Client Error' in str(err)):
            print('ERROR (downloadArchive): {0}'.format(err))
            pass
        else:
            print('ERROR (downloadArchive): {0}'.format(err))

if __name__ == '__main__':
    pokemons_info = {'NOME': [], 'ID': [], 'TIPOS': [], 'DESCRICAO': [],'GIF': []}
    site = webScrape('https://pokemondb.net/pokedex/national')
    gen = site.find('h2', id='gen-1')
    # gen = site.find('h2', id='gen-2')
    # gen = site.find('h2', id='gen-3')
    # gen = site.find('h2', id='gen-4')
    # gen = site.find('h2', id='gen-5')
    # gen = site.find('h2', id='gen-6')
    # gen = site.find('h2', id='gen-7')
    # gen = site.find('h2', id='gen-8')
    # gen = site.find('h2', id='gen-9')
    pokemons = gen.parent.find('div', class_='infocard-list').find_all('div', class_='infocard')
    path_images = criarPasta(nome='gifs', dir_nome=path.dirname(path.realpath(__file__)))
    for x in pokemons:
        url_gif = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/'
        name = x.find('a', class_='ent-name')
        site = webScrape('https://pokemondb.net'+name.get('href'))
        # obtem a descrição, estou utilzando a descrição de firered
        descricao = site.find('span', class_='igame firered').parent.parent.td.text
        # traduzindo a descrição
        descricao = (GoogleTranslator(source='auto', target='pt').translate(descricao))
        # obtem o id e os tipos
        id, tipos = x.find_all('small')
        # remove # e realiza a conversão para inteiro
        id = int(id.text.replace('#', ''))
        # monta a url do gif
        new_url_gif = '{}{}.gif'.format(url_gif, id)
        # realiza o download do gif
        # downloadArchive(url=new_url_gif, path_archive=path_images, nome_arquivo=name.text.lower())
        tipos = tipos.text.replace(' · ', '/')
        tipos = (GoogleTranslator(source='auto', target='pt').translate(tipos))
        # atualizando valores de cada chave do dicionario
        pokemons_info.get('NOME').append(name.text)
        pokemons_info.get('ID').append(id)
        pokemons_info.get('TIPOS').append(tipos)
        pokemons_info.get('DESCRICAO').append(descricao)
        pokemons_info.get('GIF').append('{}{}.gif'.format(url_gif, id))
    # transforma dicionario para o formata do pandas
    df = pd.DataFrame.from_dict(pokemons_info)
    # defino caminho para arquivo csv
    file_path = path.join((path.dirname(path.realpath(__file__))), 'pokemons.csv')
    # salva o csv
    df.to_csv(file_path, index=False)