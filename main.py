#!/usr/bin/python

# Importação dos pacotes necessários
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import RPi.GPIO as GPIO


# Configuração dos GPIOs
entradaPosChave = 23  # GPIO para entrada do pós-chave
saidaBomba = 24       # GPIO para saída que liga a bomba de combustível
GPIO.setmode(GPIO.BCM)
GPIO.setup(saidaBomba, GPIO.OUT)
GPIO.setup(entradaPosChave, GPIO.IN)


# Inicializa 'currentname' para acionar apenas quando uma nova pessoa for identificada
currentname = "unknown"


# Carrega as faces conhecidas e codificações junto com o Haar cascade do OpenCV para detecção de faces
print("[INFO] carregando codificações + detector de faces...")
encodingsP = "encodings.pickle"
data = pickle.loads(open(encodingsP, "rb").read())


# Inicializa a captura de vídeo e permite que o sensor da câmera aqueça
vs = VideoStream(src=0, framerate=10).start()
time.sleep(2.0)


# Inicia o contador de FPS
fps = FPS().start()


# Loop sobre os frames do fluxo de vídeo
while True:
    # Captura o frame do fluxo de vídeo e redimensiona para 500px (para acelerar o processamento)
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    
    # Detecta as caixas de face
    boxes = face_recognition.face_locations(frame)
    # Calcula as codificações faciais para cada caixa delimitadora de face
    encodings = face_recognition.face_encodings(frame, boxes)
    names = []


    # Loop sobre as codificações faciais
    for encoding in encodings:
        # Tenta corresponder cada face na imagem de entrada às codificações conhecidas
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Intruso"  # Se a face não for reconhecida, atribui "Intruso"


        # Verifica se encontrou uma correspondência
        if True in matches:
            # Encontra os índices de todas as faces correspondentes e inicializa um dicionário para contar o número total de vezes que cada face foi correspondida
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}


            # Loop sobre os índices correspondentes e mantém uma contagem para cada face reconhecida
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1


            # Determina a face reconhecida com o maior número de votos
            name = max(counts, key=counts.get)


            # Se alguém no seu conjunto de dados for identificado, imprime o nome na tela
            if currentname != name:
                currentname = name
                print(currentname)
                # Ativa a saída para ligar a bomba de combustível
                GPIO.output(saidaBomba, True)
                time.sleep(1)  # Ajuste conforme necessário para manter o relé ligado
                GPIO.output(saidaBomba, False)
                
        # Atualiza a lista de nomes
        names.append(name)


    # Loop sobre as faces reconhecidas e desenha o nome da face prevista na imagem
    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)


    # Exibe a imagem na tela
    cv2.imshow("Reconhecimento Facial em Execução", frame)
    key = cv2.waitKey(1) & 0xFF


    # Sai do loop quando a tecla 'q' for pressionada
    if key == ord("q"):
        break


    # Reinicia o reconhecimento se o botão (entrada do pós-chave) for pressionado
    if GPIO.input(entradaPosChave):
        print("[INFO] Reiniciando reconhecimento...")
        currentname = "unknown"


    # Atualiza o contador de FPS
    fps.update()


# Para o cronômetro e exibe informações de FPS
fps.stop()
print("[INFO] tempo decorrido: {:.2f}".format(fps.elapsed()))
print("[INFO] FPS aproximado: {:.2f}".format(fps.fps()))


# Limpeza
cv2.destroyAllWindows()
vs.stop()
GPIO.cleanup()
