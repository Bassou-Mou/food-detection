import os, shutil, random

SOURCE_DIR = "raw_images/pizza"   
OUTPUT_DIR = "dataset"            # dossier de sortie final
CLASS_NAME = "pizza"
TRAIN = 0.70   # 70% entraînement
VAL   = 0.15   # 15% validation
TEST  = 0.15   # 15% test

random.seed(42)

for split in ['train', 'val', 'test']:
    os.makedirs(f"{OUTPUT_DIR}/images/{split}", exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/labels/{split}", exist_ok=True)

images = []
for f in os.listdir(SOURCE_DIR):
    if f.lower().endswith(('.jpg', '.jpeg', '.png')):
        nom_base = os.path.splitext(f)[0]
        txt_path = os.path.join(SOURCE_DIR, nom_base + ".txt")
        if os.path.exists(txt_path):
            images.append(nom_base)
            

random.shuffle(images)
total = len(images)

n_train = int(total * TRAIN)
n_val   = int(total * VAL)

splits = {
    'train': images[:n_train],
    'val':   images[n_train:n_train + n_val],
    'test':  images[n_train + n_val:]
}

print(f"Total images annotées : {total}")
print(f"   Train : {len(splits['train'])} images")
print(f"   Val   : {len(splits['val'])} images")
print(f"   Test  : {len(splits['test'])} images\n")

for split, noms in splits.items():
    for nom in noms:
        for ext in ['.jpg', '.jpeg', '.png']:
            img_src = os.path.join(SOURCE_DIR, nom + ext)
            if os.path.exists(img_src):
                shutil.copy(img_src, f"{OUTPUT_DIR}/images/{split}/{nom}{ext}")
                break
        txt_src = os.path.join(SOURCE_DIR, nom + ".txt")
        shutil.copy(txt_src, f"{OUTPUT_DIR}/labels/{split}/{nom}.txt")
