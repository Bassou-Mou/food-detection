import requests, os
from PIL import Image
from io import BytesIO

URLS_PIZZA = [

]


def download_images(urls, class_name, output_dir="raw_images"):
    folder = os.path.join(output_dir, class_name)
    os.makedirs(folder, exist_ok=True)

    saved = 0
    for i, url in enumerate(urls):
        try:
            r = requests.get(url, timeout=5, 
                           headers={"User-Agent": "Mozilla/5.0"})
            img = Image.open(BytesIO(r.content)).convert('RGB')
            
            # Filtre les images trop petites
            if img.size[0] >= 200 and img.size[1] >= 200:
                path = os.path.join(folder, f"{class_name}_{saved:03d}.jpg")
                img.save(path, "JPEG", quality=90)
                saved += 1
                print(f"  ✓ {class_name}_{saved:03d}.jpg")
        except Exception as e:
            print(f"  ✗ image {i} échouée : {e}")
    
    print(f">>> {class_name} : {saved} images sauvegardées\n")

# Lance le téléchargement
download_images(URLS_PIZZA, "pizza")
