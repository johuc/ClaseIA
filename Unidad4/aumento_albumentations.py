import cv2
import pandas as pd
import albumentations as A
import os

# Ruta donde están tus imágenes originales
carpeta_imagenes = r"C:\Users\jlcb_\OneDrive\Escritorio\imagenes"

# Carpeta para guardar imágenes aumentadas
output_dir = 'aumentadas'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Lee tu CSV
df = pd.read_csv(r"C:\Users\jlcb_\OneDrive\Escritorio\TAVan\inteligArt\labels_database_2025-05-24-09-00-16.csv")

# Definir transformaciones (ejemplo)


transform = A.Compose([
    A.HorizontalFlip(p=0.5),               # Volteo horizontal aleatorio
    A.RandomBrightnessContrast(p=0.3),    # Ajuste aleatorio de brillo y contraste
    A.ShiftScaleRotate(                    # Mover, escalar y rotar la imagen
        shift_limit=0.05, scale_limit=0.1, rotate_limit=15, p=0.5
    ),
    A.GaussNoise(p=0.2),                   # Ruido gaussiano
    A.Blur(blur_limit=3, p=0.1),           # Desenfoque
    A.HueSaturationValue(p=0.3),           # Cambiar matiz, saturación y valor (color)
    A.CoarseDropout(max_holes=8, max_height=20, max_width=20, p=0.3)
])

for idx, row in df.iterrows():
    image_path = os.path.join(carpeta_imagenes, row['image_name'])

    if not os.path.exists(image_path):
        print(f"No se encontró la imagen: {image_path}")
        continue

    image = cv2.imread(image_path)
    image = cv2.resize(image, (224, 224))

    for i in range(5):
        augmented = transform(image=image)['image']
        base_name = os.path.splitext(row['image_name'])[0]
        output_path = os.path.join(output_dir, f"{base_name}_aug_{i}.jpg")
        cv2.imwrite(output_path, augmented)
        print(f"Guardada imagen aumentada: {output_path}")

print("✅ Aumento de datos completado.")
