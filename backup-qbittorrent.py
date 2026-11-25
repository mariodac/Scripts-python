from os import environ, path
from shutil import copytree
from tkinter import Tk
import tkinter.filedialog

def select_backup_directory():
    # Seleciona o diretório onde será o caminho do backup
    Tk().withdraw()
    path_backup = tkinter.filedialog.askdirectory(title="Selecione a pasta do diretório")
    Tk().destroy()

    if not path_backup:
        raise SystemExit("Nenhum diretório selecionado. O programa será encerrado.")
    return path_backup

def make_backup():
    try:
        path_backup = select_backup_directory()

        print(f"O caminho selecionado foi: {path_backup}")

        localappdata = path.join(environ.get("LOCALAPPDATA"), "qBittorrent")
        appdata = path.join(environ.get("APPDATA"), "qBittorrent")

        localappdata_backup = path.join(path_backup, 'localappdata', path.basename(localappdata))
        appdata_backup = path.join(path_backup, 'roamingappdata', path.basename(appdata))

        copytree(localappdata, localappdata_backup)
        copytree(appdata, appdata_backup)

        print("Backup realizado com sucesso!")
    except Exception as e:
        print(f"Erro ao realizar backup: {e}")

def restore_backup():
    try:
        path_backup = select_backup_directory()

        print(f"O caminho selecionado foi: {path_backup}")

        localappdata_backup = path.join(path_backup, 'localappdata', "qBittorrent")
        appdata_backup = path.join(path_backup, 'roamingappdata', "qBittorrent")

        localappdata = path.join(environ.get("LOCALAPPDATA"), "qBittorrent")
        appdata = path.join(environ.get("APPDATA"), "qBittorrent")

        copytree(localappdata_backup, localappdata)
        copytree(appdata_backup, appdata)

        print("Backup Restaurado com sucesso!")
    except Exception as e:
        print(f"Erro ao restaura backup: {e}")


if __name__ == "__main__":

    while True:
        print("1 - Fazer backup\n2 - Restaurar backup")
        choice = input("Escolha => ")
        if choice == "1":
            make_backup()
        elif choice == "2":
            restore_backup()
        else:
            break

