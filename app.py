#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash, Response
import cv2
import os
import base64
import numpy as np
import subprocess


# Inicializa a aplicação Flask
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Chave secreta para gerenciamento de sessões


# Inicializa a câmera
camera = cv2.VideoCapture(0)


# Função para gerar frames da câmera para a transmissão em tempo real
def gen_frames():
    while True:
        success, frame = camera.read()  # Captura frame da câmera
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# Rota para a página de login
@app.route('/')
def login():
    return render_template('login.html')


# Rota para processar o login
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'admin':  # Verifica credenciais
        return redirect(url_for('capture'))  # Redireciona para a página de captura
    else:
        flash('Credenciais incorretas. Tente novamente.')  # Mensagem de erro
        return redirect(url_for('login'))


# Rota para a página de captura
@app.route('/capture')
def capture():
    return render_template('capture.html')


# Rota para fornecer o feed de vídeo
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Rota para salvar as imagens capturadas
@app.route('/save_images', methods=['POST'])
def save_images():
    name = request.form['name']
    directory = 'dataset/{}'.format(name)
    if not os.path.exists(directory):
        os.makedirs(directory)  # Cria diretório para salvar imagens


    # Salva as 5 imagens capturadas
    for i in range(5):
        image_data = request.form['image_{}'.format(i)]
        img_data = base64.b64decode(image_data.split(',')[1])
        np_img = np.frombuffer(img_data, dtype=np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        cv2.imwrite('{}/image_{}.jpg'.format(directory, i), img)
    
    # Executa o script de treinamento em segundo plano
    subprocess.Popen(['python', 'trainModelRpi4.py'])
    
    return redirect(url_for('login'))


# Inicializa a aplicação Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
