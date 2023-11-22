import wx, os

def wx_filedialog(wildcard):
    """Abre janela de dialogo para abrir arquivo
    Args:
        wildcard (str): filtro de arquivos
    Returns:
        str: caminho do arquivo
        """
    app = wx.App(None) # type: ignore
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Selecione o arquivo', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
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
    app = wx.App(None)
    dialog = wx.DirDialog (None, "Choose input directory", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

if __name__ == '__main__':
    path_files = wx_dirdialog()
    os.chdir(path_files)
    files_path = [x for x in os.listdir(path_files) if x.endswith('.mkv') or x.endswith('.mkv') ]
    for item in files_path:
        new_item = item.split('.mkv')[0]
        print(f"Gerando legenda para {new_item}")
        os.system(f'translatesubs "{item}" "{new_item}_PT-BR.ass" --to_lang pt')
