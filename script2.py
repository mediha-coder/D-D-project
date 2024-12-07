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
image_path = r"C:/Users/chaie/OneDrive/Documents/Dell/OneDrive/Desktop/vs_code/reactapp/figma-project/src/assets/image.png"
image = cv2.imread(image_path)

start_time = time.time()
# Détecter les visages avec MTCNN
faces, _ = mtcnn(image, return_prob=True)
authorized = False
# Vérifier si des visages ont été détectés
if faces is not None:
    faces = faces.clone().detach()
    # Ajouter une dimension de lot (batch dimension)
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
            embedding = np.array(list(map(float,row[0].split(','))))
            label = row[1]
            database_embeddings.append(embedding)
            database_labels.append(label)
    
    def cosine_similarity(a, b):
     a = a.squeeze()
     dot_product = np.dot(a, b)
     norm_a = np.linalg.norm(a)
     norm_b = np.linalg.norm(b)
     return dot_product / (norm_a * norm_b)
    # Comparaison les embeddings avec la base de données
    
    for embedding in embeddings:
    # Calculer la similarité cosinus 
     similarities = [cosine_similarity(embedding.detach().cpu().numpy(), emb) for emb in database_embeddings]
    
    # Seuil de correspondance
     threshold = 0.5
    
    # Vérifier si une correspondance est trouvée
     if max(similarities) >= threshold:
        idx = similarities.index(max(similarities))
        class_name = database_labels[idx]
        print("Match found with:", class_name)
       
        authorized = True
        break

# Obtenir l'heure de début 
start_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))

if not authorized:
    print("No matches found.")
print(start_time_str)
elapsed_time = time.time() - start_time
elapsed_time_rounded = round(elapsed_time, 3)  
print(elapsed_time_rounded, "seconds")
