from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import numpy as np
import cv2
import csv
import time
import os
import matplotlib.pyplot as plt
workers = 0 if os.name == 'nt' else 4
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
mtcnn = MTCNN(
    image_size=160, margin=0, min_face_size=20,
    thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True,
    device=device
)
# Charger l'image avec OpenCV
image_path = r"C:/Users/chaie/OneDrive/Documents/Dell/OneDrive/Desktop/vs_code/reactapp/figma-project/src/assets/image.png"
image = cv2.imread(image_path)

start_time = time.time()
# Détecter les visages avec MTCNN
faces, _ = mtcnn(image, return_prob=True)

# Définir la variable authorized
authorized = False

# Vérifier si des visages ont été détectés
if faces is not None:
    faces = faces.unsqueeze(0)
    # Calculer les embeddings pour chaque visage détecté
    embeddings = resnet(faces)
    
    # Charger les embeddings de la base de données depuis le fichier CSV
    database_embeddings = []
    database_labels = []
    with open('C:/Users/chaie/OneDrive/Documents/Dell/OneDrive/Desktop/vs_code/reactapp/figma-project/src/embeddings.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            embedding = np.array(list(map(float, row[0].split(','))))
            label = row[1]
            database_embeddings.append(embedding)
            database_labels.append(label)
    
    # Comparer les embeddings avec la base de données
    for embedding in embeddings:
        # Calculer la distance euclidienne entre l'embedding de l'image et chaque embedding de la base de données
        distances = [np.linalg.norm(embedding.detach().cpu().numpy() - emb) for emb in database_embeddings]
        
        # Seuil de correspondance
        threshold = 0.8  # À ajuster selon votre application
        
        # Vérifier si une correspondance est trouvée
        if min(distances) < threshold:
            idx = distances.index(min(distances))
            class_name = database_labels[idx]
            print("Correspondance trouvée avec:", class_name)
            authorized = True
            break

# Obtenir l'heure de début de l'opération
start_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))

if not authorized:
    print("Aucune correspondance trouvée. Personne non autorisée.")
    print("Heure de début de l'opération:", start_time_str)
    # Afficher l'image avec un message indiquant que la personne n'est pas autorisée
    cv2.imshow('Personne non autorisée', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
print("Heure de début de l'opération:", start_time_str)
print("Temps d'exécution de l'algorithme pour la détection des visages:", time.time() - start_time, "seconds")
