# 💻Fake-card-detection
This project is an analyzer that detects whether an uploaded ID card image is real or fake using image analysis techniques.  


It is a simple web application (Deployed on Render) that calculates the Structural Similarity Index Measure (SSIM) between a reference image (assumed to be from a trusted database but we upload a sample one) and another uploaded ID card image to determine whether the two images are the same.       




## 📁Project Structure
```
fake-id-card-detection/
│
├── fakecard.png              # sample image for analysis
├── image analysis.ipynb      # to see image preprocessing methods and how project works(not used in the app creation)
├── realcard.png             
│
└── App/
    ├── app.py                # Main Flask application file
    ├── Procfile              # Procfile for deployment in Render
    ├── requirements.txt      # Required libraries
    ├── runtime.txt           # Python version
    │
    ├── static/          
    │   └── style.css
    │
    └── templates/       
        └── index.html
```
## 🌐 Live Demo
You can check the live web app here:
