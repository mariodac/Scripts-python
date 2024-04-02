from google.cloud import speech_v1p1beta1 as speech
# from google.cloud import speech_v1p1beta1.types

import io
import fleep
from wx import App, FileDialog, DirDialog, FD_OPEN, FD_FILE_MUST_EXIST, ID_OK, DD_DEFAULT_STYLE, DD_DIR_MUST_EXIST 

# Configure as credenciais do Google Cloud
# Certifique-se de ter as credenciais JSON do serviço configuradas como variável de ambiente


def wx_filedialog( wildcard):
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
    dialog = DirDialog (None, "Escolha o diretório", "", DD_DEFAULT_STYLE | DD_DIR_MUST_EXIST)
    if dialog.ShowModal() == ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    app.Destroy()
    return path

def transcrever_audio(arquivo_audio):
    client = speech.SpeechClient()

    with io.open(arquivo_audio, "rb") as audio_file:
        content_audio = audio_file.read()

    """ audio = speech.RecognitionAudio(content=content_audio)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="pt-BR",  # Idioma do áudio (por exemplo, pt-BR para português)
    )

    response = client.recognize(config=config, audio=audio) """

    language_code = "pt-BR"
    sample_rate_hertz = 16000
    encoding = speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
    config = {
        "encoding": encoding,
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
    }
    audio = {"content": content_audio}
    response = client.recognize(request={"config": config, "audio": audio})

    # Exibindo as transcrições
    for result in response.results:
        print(f"Transcrição: {result.alternatives[0].transcript}")

if __name__ == "__main__":
    arquivo_audio = wx_filedialog('')
    with open(arquivo_audio, 'rb') as file:
        info = fleep.get(file.read(128))
    # print(info.extension)
    print(list(set(info.extension + [x.split('/')[1] for x in info.mime])))
    # transcrever_audio(arquivo_audio)