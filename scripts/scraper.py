from bing_image_downloader import downloader

# On définit le terme de recherche
terme_recherche = "hotdog food" # "food" pour éviter les chiens "chiens-chauds"

# On lance le téléchargement
print(f"Début du téléchargement pour : {terme_recherche}")

downloader.download(
    terme_recherche, 
    limit=200,  # Le nombre d'images
    output_dir='dataset_repas',  # Le nom du dossier principal qui sera créé
    adult_filter_off=True, # filtre désactivé
    force_replace=False, # ne pas écraser si le dossier existe déjà
    timeout=60, # Temps d'attente maximum pour une image
    verbose=True # Affiche les détails dans la console
)

print("Téléchargement terminé !")
