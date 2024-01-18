from os import listdir, path, system
from re import search, IGNORECASE
from wx import App, FileDialog, DirDialog, FD_OPEN, FD_FILE_MUST_EXIST, ID_OK, DD_DEFAULT_STYLE, DD_DIR_MUST_EXIST 

total_files = []

def wx_filedialog(wildcard):
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

def wx_dirdialog():
    """Abre janela de dialogo para abrir pasta
    Returns:
        str: caminho da pasta
    """
    app = App(None)
    dialog = DirDialog (None, "Choose input directory", "", DD_DEFAULT_STYLE | DD_DIR_MUST_EXIST)
    if dialog.ShowModal() == ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

def listar_pasta(pasta):
    tot = []
    subpastas = list()
    if path.isdir(pasta):
        items = listdir(pasta)
        for item in items:
            if (not search('Recycle', item, IGNORECASE)) and (not search('System Volume Information', item, IGNORECASE)):
                novo_item = path.join(pasta,item)
                if path.isdir(novo_item):
                    subpastas.append(novo_item)
                    continue
                if item.endswith('.mpg') or item.endswith('.mkv') or item.endswith('.mp4') or item.endswith('.avi') or item.endswith('.ass') or item.endswith('.srt'):
                    tot.append(path.join(pasta, item))
        for subpasta in subpastas:
            if not search('Recycle', item, IGNORECASE):
                tot.extend(listar_pasta(subpasta))
    # arq.write("\n")
    return tot

if __name__ == '__main__':
    path_files = wx_dirdialog()
    total_files.extend(listar_pasta(path_files))
    # chdir(path_files)
    # files_path = [x for x in listdir(path_files) if x.endswith('.mkv') or x.endswith('.mp4') or x.endswith('.avi') or x.endswith('.ass') or x.endswith('.srt')]
    files_path = [path.join(path_files, x) for x in listdir(path_files) if x.endswith('.mkv') or x.endswith('.mpg') or x.endswith('.mp4') or x.endswith('.avi') or x.endswith('.ass') or x.endswith('.srt')]
    index = 0
    for item in total_files:
        if item.endswith('.mkv'):
            new_item = item.split('.mkv')[0]
        elif item.endswith('.mpg'):
            new_item = item.split('.mpg')[0]
        elif item.endswith('.mp4'):
            new_item = item.split('.mp4')[0]
        elif item.endswith('.avi'):
            new_item = item.split('.avi')[0]
        elif item.endswith('.ass'):
            new_item = item.split('.ass')[0]
        elif item.endswith('.srt'):
            new_item = item.split('.srt')[0]
        else:
            print(f"Arquivo {item} com formato nao suportado")
        print(f"Gerando legenda para {new_item}")
        try:
            system(f'translatesubs "{item}" "{new_item}.PT.ass" --to_lang pt')
        except:
            system(f'translatesubs "{item}" "item_{index+1}.PT.ass" --to_lang pt')
        index += 1
