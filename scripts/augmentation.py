import os
import cv2
import albumentations as A
import re # pour vérifier les noms de fichiers avec une précision absolue

# UNIQUEMENT le dossier train
dossier_base = "/home/fdiwa/Desktop/Projet app/food-detection/dataset"
dossier_images_train = os.path.join(dossier_base, "images", "train", "hotdog")
dossier_labels_train = os.path.join(dossier_base, "labels", "train", "hotdog")

# les transformations (YOLO)
params_bbox = A.BboxParams(format='yolo', min_visibility=0.3)

transformations = [
    A.Compose([A.HorizontalFlip(p=1.0)], bbox_params=params_bbox), # _1 : Miroir
    A.Compose([A.RandomBrightnessContrast(p=1.0)], bbox_params=params_bbox), # _2 : Luminosité
    A.Compose([A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.1, rotate_limit=10, p=1.0)], bbox_params=params_bbox) # _3 : Zoom/Rotation
]

print("Début de l'augmentation sur le dossier TRAIN...")
images_traitees = 0
images_generees = 0

# On définit le modèle strict d'une image originale : "hotdog_" suivi de chiffres uniquement
pattern_original = re.compile(r"^hotdog_\d+$")

# On parcourt le dossier train
for nom_image in os.listdir(dossier_images_train):
    if not nom_image.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue

    # On récupère le nom sans l'extension (ex: "hotdog_1")
    nom_base = os.path.splitext(nom_image)[0]

    # VÉRIFICATION SÉCURISÉE : Si le nom ne correspond pas exactement à "hotdog_numero", on passe !
    # Ainsi, "hotdog_1_1" ou "hotdog_12_3" seront ignorés.
    if not pattern_original.match(nom_base):
        continue

    chemin_img = os.path.join(dossier_images_train, nom_image)
    chemin_txt = os.path.join(dossier_labels_train, nom_base + ".txt")

    if not os.path.exists(chemin_txt):
        continue

    # Lecture de l'image
    image = cv2.imread(chemin_img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Lecture des annotations
    bboxes = []
    with open(chemin_txt, 'r') as f:
        for ligne in f:
            elements = ligne.strip().split()
            if len(elements) == 5:
                class_id = int(elements[0])
                x, y, w, h = map(float, elements[1:])
                bboxes.append([x, y, w, h, class_id])

    if not bboxes:
        continue

    images_traitees += 1

    # Application des transformations
    for i, transform in enumerate(transformations):
        try:
            transformed = transform(image=image, bboxes=bboxes)
            img_aug = transformed['image']
            bboxes_aug = transformed['bboxes']

            nouveau_nom_img = f"{nom_base}_{i+1}.jpg"
            nouveau_nom_txt = f"{nom_base}_{i+1}.txt"

            img_aug_bgr = cv2.cvtColor(img_aug, cv2.COLOR_RGB2BGR)
            cv2.imwrite(os.path.join(dossier_images_train, nouveau_nom_img), img_aug_bgr)

            with open(os.path.join(dossier_labels_train, nouveau_nom_txt), 'w') as f:
                for bbox in bboxes_aug:
                    x, y, w, h, class_id = bbox
                    f.write(f"{class_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")
            
            images_generees += 1
        except Exception as e:
            pass

print(f"\n Terminé ! {images_traitees} images originales ont été augmentées.")
print(f" {images_generees} nouvelles images ont été ajoutées au dossier d'entraînement !")
