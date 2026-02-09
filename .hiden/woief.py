from PIL import Image

# Загрузи картинку (замени на свой файл)
img_path = 'nizanimlevel.png'  # PNG/JPG
img = Image.open(img_path).convert('L')  # В ч/б grayscale

# Масштабируем для консоли (ширина 80, высота пропорционально)
width, height = img.size
pixels = img.load()

# Печатаем матрицу
for y in range(height):
    row = ''
    for x in range(width):
        brightness = pixels[x, y]
        if brightness > 128:  # Порог: >128 белый, иначе чёрный
            row += '⬛'  # Белый квадрат
        else:
            row += '⬜'  # Чёрный (пробел)
    print(row)
