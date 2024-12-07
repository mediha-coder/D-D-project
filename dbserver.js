const express = require('express');
const multer = require('multer');
const { exec } = require('child_process');
const path = require('path');

const app = express();
const port = 8000;

app.use(express.json());

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'C:/Users/chaie/OneDrive/Documents/Dell/OneDrive/Desktop/vs_code/reactapp/figma-project/src/assets/');
    },
    filename: (req, file, cb) => {
        cb(null, 'image1.png');
    }
});

const upload = multer({ storage });

app.post('/api/upload', upload.single('image'), (req, res) => {
    const imagePath = req.file.path;
    const personName = req.body.personName;
    const scriptPath = path.join(__dirname, 'script1.py'); // Full path to the Python script

    // Execute the Python script to detect face and extract features
    exec(`python "${scriptPath}" "${imagePath}" "${personName}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error}`);
            console.error(stderr);
            return res.status(500).send('Error processing image.');
        }

        console.log(stdout);
        res.status(200).send({ message: 'Image uploaded and features extracted successfully.' });
    });
});

app.listen(port, () => {
    console.log(`Server started at http://localhost:${port}`);
});

