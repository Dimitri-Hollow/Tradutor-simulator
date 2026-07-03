import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random
import time

pontos = 0
duration = 5  # segundos de gravação
sample_rate = 44100
facil=['lápis','cachorro','chave','caneta',"Brasil"]
medio=['espanhol','teclado','almoço','estado','universidade']
dificil=['onomatopeia','pneumonia','anticonstitucional','traqueia','discordia']
dificuldades = {'fácil':facil, 
                'médio':medio, 
                'difícil':dificil}

print('-'*5,"<Tradutor simulator>",'-'*5)

while True:
    resposta1= input("Escolha sua dificuldade (fácil, médio, difícil): ")
    if resposta1== 'fácil' or resposta1=='médio':
        break
    elif resposta1== 'difícil':
        confirmação = input('Você tem certeza? (s/n): ')
        if confirmação== 's':
            break
    else:
        print("Dificuldade inválida. Tente novamente.")

print('Você escolheu a dificuldade:', '\n', resposta1)
print('Começando em 3 segundos...')
print('3')
time.sleep(1)
print('2')
time.sleep(1)
print('1')
time.sleep(1)
print('Começando!')

for i in range(5):
    palavra = random.choice((dificuldades[resposta1]))
    print('Escolhendo a palavra...')
    time.sleep(1)
    print('Traduza a palavra:', palavra)
    while True:   
        print("Fale agora...")
        recording = sd.rec(
        int(duration * sample_rate), # o número de amostras a serem registradas
        samplerate=sample_rate,      # taxa de amostras
        channels=1,                  # 1 significa gravação mono
        dtype="int16")               # tipo de dados para as amostras registradas
        sd.wait()  # aguardando o término da gravação

        wav.write("output.wav", sample_rate, recording)
        print("Gravação concluída, estou reconhecendo...")

        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            fala = recognizer.recognize_google(audio, language="en")
            print("Sua resposta:", fala)
            break
        except sr.UnknownValueError:             # - se o Google não conseguiu entender a fala devido a ruídos ou silêncio
            print("A fala não pôde ser reconhecida.")
        except sr.RequestError as e:             # - se não houver conexão com a Internet ou a API estiver indisponível
            print(f"Service error: {e}")
    translator = Translator()
    translated = translator.translate(palavra, dest='en')
    if fala.lower() == translated.text.lower():
        print("✅ Correto!")
        pontos += 1
    else:
        print("❌ Incorreto! A tradução correta é:", translated.text)
    (dificuldades[resposta1]).remove(palavra)
    
    
print("Sua pontuação final é", pontos, "de 5.")
