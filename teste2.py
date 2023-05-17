#######################################################
#     Detecção de Placas atraves de contornos  HD     #
#                       by AY7                        #
#######################################################

import pytesseract
import cv2
from playsound import playsound
from lib.filters import get_grayscale, thresholding, pytesseract


def apply_filter(plate):
    gray = get_grayscale(plate)
    thresh = thresholding(gray)
    return thresh


def scan_plate(image):
    custom_config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789- --psm 6'
    plate_number = (pytesseract.image_to_string(image, config=custom_config))
    return plate_number


def desenhaContornos(contornos, imagem, plates):
    for c in contornos:
        # perimetro do contorno, verifica se o contorno é fechado
        perimetro = cv2.arcLength(c, True)
        if perimetro > 120:
            # aproxima os contornos da forma correspondente
            approx = cv2.approxPolyDP(c, 0.03 * perimetro, True)
            # verifica se é um quadrado ou retangulo de acordo com a qtd de vertices
            if len(approx) == 4:
                # Contorna a placa atraves dos contornos encontrados
                (x, y, lar, alt) = cv2.boundingRect(c)
                cv2.rectangle(imagem, (x, y),
                              (x + lar, y + alt), (0, 255, 0), 2)
                # segmenta a placa da imagem
                roi = imagem[y:y + alt, x:x + lar]
                plates_filter_applied = apply_filter(roi)
                plates_numbers = (scan_plate(plates_filter_applied)).split(' ')
                if plates_numbers:
                    for n in plates_numbers:
                        numbers = n.split()
                        if numbers:
                            print(numbers[0])
                            if numbers[0] in plates:
                                playsound("SIRENE.mp3")
                                return True


def buscaRetanguloPlaca(source, plates):
    # Captura ou Video
    video = cv2.VideoCapture(source)
    cont = 0
    while video.isOpened():
        if cont % 1 == 0:
            ret, frame = video.read()

            if (ret == False):
                break

            # area de localização u 720p
            area = frame[200:, 200:600]

            # area de localização 480p
            # area = frame[350:, 220:500]

            # escala de cinza
            img_result = cv2.cvtColor(area, cv2.COLOR_BGR2GRAY)

            # limiarização
            ret, img_result = cv2.threshold(
                img_result, 90, 255, cv2.THRESH_BINARY)

            # desfoque
            img_result = cv2.GaussianBlur(img_result, (5, 5), 0)

            # lista os contornos
            contornos, hier = cv2.findContours(
                img_result, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            cv2.imshow('FRAME', frame)

            if (desenhaContornos(contornos, area, plates)) == True:
                break

            cv2.imshow('RES', area)

            if cv2.waitKey(1) & 0xff == ord('q'):
                break

    video.release()
    cv2.destroyAllWindows()
    cont = cont + 1


if __name__ == "__main__":
    source = "resource/video2.mp4"
    not_authorized_plate = ['FUN-0972', 'BRA2E19',
                            'OJJ-3984', 'RTLOB27', 'NPA-6916']
    buscaRetanguloPlaca(source, not_authorized_plate)
