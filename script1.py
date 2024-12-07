from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import numpy as np
import cv2
import csv
import sys

def extract_and_save_features(image_path, person_name):
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
    mtcnn = MTCNN(
        image_size=160, margin=0, min_face_size=20,
        thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True,
        device=device
    )

    # Charger l'image avec OpenCV
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)


    # Détecter les visages avec MTCNN
    faces, _ = mtcnn(image, return_prob=True)

    # Vérifier si des visages ont été détectés
    if faces is not None:
        # Pour chaque visage détecté
        for face in faces:
            face = face.clone().detach()
            # Calculer les embeddings pour chaque visage détecté
            face = face.unsqueeze(0).to(device)  # Ajouter une dimension de lot (batch dimension)
            embeddings = resnet(face)
            
            # Convertir l'embedding en liste pour le sauvegarder dans un fichier CSV
            embedding_list = embeddings.cpu().detach().numpy().tolist()

            # Enregistrer les caractéristiques dans un fichier CSV
            with open('C:/Users/chaie/OneDrive/Documents/Dell/OneDrive/Desktop/vs_code/reactapp/figma-project/src/embedding1.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([','.join(map(str, embedding_list)), person_name])

if __name__ == "__main__":
    image_path = sys.argv[1]
    person_name = sys.argv[2]
    extract_and_save_features(image_path, person_name)
