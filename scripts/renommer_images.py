import os

DOSSIER    = "raw_images/pizza"   
CLASS_NAME = "pizza"            
EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')

def renommer_images(dossier, class_name):
    fichiers = [
        f for f in os.listdir(dossier)
        if f.lower().endswith(EXTENSIONS)
    ]
    
    fichiers.sort()  

    print(f" Dossier    : {dossier}")
    print(f" Images     : {len(fichiers)} trouvées")

    temp_noms = []
    for i, fichier in enumerate(fichiers):
        ancien = os.path.join(dossier, fichier)
        temp   = os.path.join(dossier, f"__temp_{i:04d}.jpg")
        os.rename(ancien, temp)
        temp_noms.append(temp)

    for i, temp in enumerate(temp_noms):
        nouveau_nom  = f"{class_name}_{i+1:03d}.jpg"
        nouveau_path = os.path.join(dossier, nouveau_nom)
        os.rename(temp, nouveau_path)
        print(f"  ✓ {nouveau_nom}")

renommer_images(DOSSIER, CLASS_NAME)