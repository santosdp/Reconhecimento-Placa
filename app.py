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


def main():
    source = "resource/carro3.png"
    not_authorized_plate = ['FUN-0972', 'BRA2E19',
                            'OJJ-3984', 'RTLOB27', 'NPA-6916']
    img = cv2.imread(source)
    cv2.imshow("Image", img)
    img_result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img_result = cv2.threshold(img_result, 90, 255, cv2.THRESH_BINARY)
    img_result = cv2.GaussianBlur(img_result, (5, 5), 0)
    contornos, hier = cv2.findContours(
        img_result, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for c in contornos:
        # perimetro do contorno, verifica se o contorno é fechado
        perimetro = cv2.arcLength(c, True)
        if perimetro > 150:
            # aproxima os contornos da forma correspondente
            approx = cv2.approxPolyDP(c, 0.03 * perimetro, True)
            # verifica se é um quadrado ou retangulo de acordo com a qtd de vertices
            if len(approx) == 4:
                # Contorna a placa atraves dos contornos encontrados
                (x, y, lar, alt) = cv2.boundingRect(c)
                cv2.rectangle(img, (x, y),
                              (x + lar, y + alt), (0, 255, 0), 2)
                # segmenta a placa da imagem
                roi = img[y:y + alt, x:x + lar]
                cv2.imshow("Teste", roi)
                plates_filter_applied = apply_filter(roi)
                plates_numbers = (scan_plate(plates_filter_applied)).split(' ')

                if plates_numbers:
                    for n in plates_numbers:
                        numbers = n.split()
                        if numbers:
                            print(numbers[0])
                            if numbers[0] in not_authorized_plate:
                                playsound("SIRENE.mp3")

                    print(plates_numbers[0])
    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()
