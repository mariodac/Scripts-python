import openai
import PySimpleGUI as sg

# código gerado pelo chatgpt

# Insira aqui sua chave da API do OpenAI
openai.api_key = "chave"

# Defina o layout da interface gráfica
layout = [[sg.Text("Faça sua pergunta:"), sg.Input(key="-PERGUNTA-")],
          [sg.Button("Enviar"), sg.Button("Sair")]]

# Crie a janela com o layout definido
janela = sg.Window("ChatGPT").Layout(layout)

# Loop principal do programa
while True:
    # Leia os eventos da janela
    evento, valores = janela.Read()

    # Se o evento for o botão "Sair", feche a janela e encerre o programa
    if evento == sg.WINDOW_CLOSED or evento == "Sair":
        break

    # Se o evento for o botão "Enviar", faça a pergunta para o ChatGPT
    if evento == "Enviar":
        pergunta = valores["-PERGUNTA-"]
        resposta = openai.Completion.create(
            engine="davinci",
            prompt=pergunta,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5
        ).choices[0].text

        # Mostre a resposta em uma nova janela
        sg.Popup("Resposta:", resposta)

# Feche a janela e encerre o programa
janela.Close()