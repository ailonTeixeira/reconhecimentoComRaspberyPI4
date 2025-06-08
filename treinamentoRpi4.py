#! /usr/bin/python
# -*- coding: utf-8 -*-


# Importa os pacotes necessários
from imutils import paths
import face_recognition
import pickle
import cv2
import os


# Mensagem inicial indicando o início do processamento das faces
print("[INFO] Iniciando o processamento de faces...")
print("[INFO] Acessando faces capturadas e salvas no sistema de arquivos...")


# Lista todos os caminhos das imagens no diretório 'dataset'
imagePaths = list(paths.list_images("dataset"))


# Inicializa as listas para armazenar as codificações e nomes conhecidos
knownEncodings = []
knownNames = []


# Loop sobre os caminhos das imagens
for (i, imagePath) in enumerate(imagePaths):
    # Extrai o nome da pessoa a partir do caminho da imagem
    print("[INFO] Processando imagens {}/{}".format(i + 1, len(imagePaths)))
    name = imagePath.split(os.path.sep)[-2]


    # Carrega a imagem de entrada e converte de BGR (ordem do OpenCV) para RGB (ordem do dlib)
    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


    # Detecta as coordenadas (x, y) das caixas delimitadoras correspondentes a cada face na imagem de entrada
    boxes = face_recognition.face_locations(rgb, model="hog")


    # Calcula a codificação facial para a face
    encodings = face_recognition.face_encodings(rgb, boxes)


    # Loop sobre as codificações
    for encoding in encodings:
        # Adiciona cada codificação e nome ao conjunto de nomes e codificações conhecidos
        knownEncodings.append(encoding)
        knownNames.append(name)


# Serializa as codificações faciais e nomes para o disco
print("[INFO] Serializando codificações...")
print("[INFO] Arquivo encodings.pickle atualizado.")
data = {"encodings": knownEncodings, "names": knownNames}
with open("encodings.pickle", "wb") as f:
    f.write(pickle.dumps(data))
