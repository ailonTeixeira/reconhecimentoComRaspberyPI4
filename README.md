🚗 Sistema de Segurança Veicular com Reconhecimento Facial embarcado em Raspberry Pi

![alt text](https://img.shields.io/badge/status-protótipo%20funcional-brightgreen)


![alt text](https://img.shields.io/badge/tecnologia-Python%20%7C%20Flask%20%7C%20RPi-blue)

Protótipo de um dispositivo de segurança veicular que utiliza inteligência artificial e reconhecimento facial para prevenir roubos e furtos. O sistema autoriza o funcionamento do veículo apenas para motoristas cadastrados, controlando a ativação da bomba de combustível.
📖 Sumário

    Sobre o Projeto

    🚀 Funcionalidades

    ⚙️ Arquitetura e Funcionamento

    🛠️ Componentes e Tecnologias

    ▶️ Processo de Utilização

    📊 Resultados

📝 Sobre o Projeto

Este trabalho apresenta o desenvolvimento de um protótipo de dispositivo de segurança automotiva baseado em reconhecimento facial. O núcleo do sistema é uma inteligência artificial que realiza a identificação em tempo real do rosto do condutor.

Caso o sistema não reconheça a pessoa, ele atua diretamente no sistema de ignição, desligando a bomba de combustível e impedindo o funcionamento do motor. Se o motorista for reconhecido, o veículo opera normalmente. O projeto foi desenvolvido sobre um microcomputador Raspberry Pi 4 e conta com uma interface web para o cadastro de novos motoristas.
🚀 Funcionalidades

    Cadastro de Usuários via Interface Web: Uma aplicação web amigável para cadastrar novos motoristas autorizados.

    Captura Guiada de Imagens: O sistema instrui o usuário a posicionar o rosto em diferentes ângulos para um cadastro mais robusto.

    Treinamento Automático do Modelo: A IA é retreinada automaticamente após cada novo cadastro.

    Reconhecimento Facial em Tempo Real: Identifica o motorista assim que ele entra no veículo.

    Controle da Bomba de Combustível: Interage com um relé para habilitar ou desabilitar a alimentação da bomba de combustível.

⚙️ Arquitetura e Funcionamento

O sistema é dividido em dois componentes principais:

    Aplicação de Cadastro (Web App):

        Um servidor Flask (app.py) fornece uma interface web (login.html, capture.html).

        O administrador acessa a página, faz login (admin/admin).

        Ele digita o nome do novo motorista e a interface guia o usuário na captura de 5 fotos do rosto.

        As imagens são salvas no diretório dataset/ e o script de treinamento (trainModelRpi4.py) é executado em segundo plano para atualizar o modelo de reconhecimento (encodings.pickle).

    Serviço de Reconhecimento (Script Principal):

        O script faciarecognition.py é executado continuamente no Raspberry Pi.

        Ele utiliza a câmera para monitorar quem está no banco do motorista.

        Quando um rosto é detectado, ele o compara com a base de dados de rostos autorizados (encodings.pickle).

        ✅ Rosto Reconhecido: O script envia um sinal GPIO (saidaBomba) para acionar o relé que liga a bomba de combustível.

        ❌ Rosto Não Reconhecido ("Intruso"): O relé permanece desativado, impedindo a partida do veículo.

🛠️ Componentes e Tecnologias
Hardware

    Microcomputador Raspberry Pi 4

    Módulo de Câmera ou Câmera USB

    Módulo Relé de 1 canal

Software e Bibliotecas

    Linguagem: Python 3

    Interface Web: Flask

    Visão Computacional: OpenCV, face_recognition

    Utilitários: imutils, numpy, pickle

    Controle de Hardware: RPi.GPIO

Para que o protótipo funcione, o ambiente de software requer a linguagem Python e as bibliotecas essenciais listadas acima. A configuração do hardware envolve conectar a câmera e o módulo relé ao Raspberry Pi. O relé é o componente chave que se integra ao sistema elétrico do veículo para controlar a bomba de combustível, uma etapa que exige cuidado técnico para garantir a segurança.
▶️ Processo de Utilização

O uso do sistema é dividido em duas etapas operacionais distintas:
Etapa 1: Cadastro de Novos Motoristas

Para cadastrar um novo motorista, a aplicação web do sistema é ativada. Através de um navegador, o administrador acessa uma página de login segura. Após a autenticação, ele insere o nome do novo usuário. A interface então guia o motorista por um processo de captura de cinco imagens do seu rosto em diferentes ângulos ("olhe para a câmera", "vire para a esquerda", etc.) para garantir um reconhecimento mais preciso.

Ao final da captura, essas imagens são enviadas ao sistema, que automaticamente inicia o processo de treinamento do modelo de inteligência artificial, atualizando sua base de dados de rostos autorizados sem necessidade de intervenção manual.
Etapa 2: Operação do Sistema de Segurança

Com os motoristas já cadastrados, o sistema de segurança principal é ativado no veículo. Este módulo opera em modo de vigilância contínua. Ao tentar ligar o carro, a câmera captura o rosto do condutor. O software de reconhecimento facial analisa a imagem em tempo real.

Se o rosto corresponder a um motorista autorizado na base de dados, o sistema envia um sinal para o relé, liberando o funcionamento da bomba de combustível e permitindo que o carro seja ligado. Caso contrário, se o rosto for desconhecido ("Intruso") ou não for detectado, o relé permanece desativado, impedindo a partida do veículo e frustrando a tentativa de furto.
📊 Resultados

Os experimentos realizados demonstraram que o dispositivo atende aos requisitos propostos. O protótipo foi capaz de detectar e reconhecer com sucesso a face de uma pessoa, enviando o comando correto para o relé da bomba de combustível e validando a eficácia do conceito para a prevenção de furtos.
