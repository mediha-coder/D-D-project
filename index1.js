
const express = require('express');
const cors = require('cors');
const multer = require('multer');
const { exec } = require('child_process');

const app = express();
app.use(cors());
app.use(express.json());

const storage = multer.diskStorage({
  destination: function(req, file, cb) {
    cb(null, "C:/Users/chaie/OneDrive/Documents/Dell/OneDrive/Desktop/vs_code/reactapp/figma-project/src/assets");
  },
  filename: function (req, file, cb) {
    cb(null, "image.png"); // Nommez toujours le fichier "image.png"
  }
});

const upload = multer({storage});

app.post('/upload', upload.single('file'), (req, res) => {
  console.log(req.body);
  console.log(req.file);

  // Chemin vers le script Python à exécuter
  const scriptPath = 'C:/Users/chaie/OneDrive/Documents/Dell/OneDrive/Desktop/vs_code/reactapp/figma-project/src/script2.py';
  
  // Chemin vers l'image capturée à passer en paramètre
 
  
  // Commande à exécuter pour appeler le script Python avec l'image capturée en tant qu'argument
  const command = `python ${scriptPath} `;
  
  // Exécution de la commande
  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Erreur d'exécution du script Python: ${error.message}`);
      res.status(500).send(`Erreur d'exécution du script Python: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`Erreur du script Python: ${stderr}`);
      res.status(500).send(`Erreur du script Python: ${stderr}`);
      return;
    }
    console.log(` ${stdout}`);
   
    // Envoyer le résultat du script Python au client
    res.send(` ${stdout}`);
  });
}); 

app.listen(3002, () => {
  console.log("Server is running");
});