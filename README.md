# Reconhecimento-Placa

Bem-vindo à documentação do software de detecção e leitura de placas de carro. Este documento fornecerá informações detalhadas sobre o funcionamento, recursos e uso do software.

## Visão Geral

O software de detecção e leitura de placas de carro é desenvolvido em Python e utiliza bibliotecas de visão computacional para identificar placas em vídeos, bem como ler os caracteres presentes nelas. Ele é projetado para auxiliar no processo de patrulha para detectar carros roubados ou suspeitos baseado na numeração da sua placa.

## Funcionamento

O software segue um fluxo básico para realizar a detecção e leitura de placas de carro:
1. Carregamento do vídeo: O software permite carregar vídeos para análise.
2. Detecção de placas: Utilizando algoritmos de visão computacional, o software identifica a região onde a placa está localizada no quadro do vídeo.
3. Pré-processamento da placa: A placa detectada é pré-processada para melhorar a qualidade da imagem e facilitar a leitura dos caracteres.
4. Reconhecimento de caracteres: O software aplica técnicas de processamento de imagem para ler os caracteres presentes na placa.
5. Saída dos resultados: Os caracteres lidos são comparados aos presentes numa lista de placas suspeitas e caso esteja presente será emitido um som de sirene de polícia.

## Requisitos de Instalação

Para utilizar o software de detecção e leitura de placas de carro, certifique-se de ter os seguintes requisitos instalados:
1. Python 3.11: https://www.python.org/downloads/
2. Bibliotecas Python:
  OpenCV: pip install opencv-python
  Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
                 pip install pytesseract
  Playsound: pip install playsound
  Numpy: pip install numpy
Certifique-se de instalar as versões mais recentes das bibliotecas Python para garantir a compatibilidade e o funcionamento adequado do software.
