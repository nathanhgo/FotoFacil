# FotoFácil (Legacy v1) 📸

> An intelligent image processing web app built with Python and OpenCV, featuring automated face detection and smart cropping for social media formats.

![Project Banner](https://via.placeholder.com/1000x300?text=FotoFacil+Project+Banner)
### 💡 About the Project
**FotoFácil** was my first venture into Computer Vision and Image Processing. It started as an undergraduate project to solve a common problem: resizing images for social media without losing the main subject.

Unlike simple cropping tools, FotoFácil uses **OpenCV** to detect faces and automatically center the crop around the person, ensuring the subject is never cut off. It also features advanced color correction algorithms.

*> Note: This project is the predecessor to my current research on node-based image processing pipelines.*

### 🛠️ Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)

### ✨ Key Features

#### 🧠 Smart Cropping (Face Detection)
- Uses **Haar Cascades** to detect faces in the uploaded image.
- Automatically calculates the center of the face to define the crop area, ensuring perfectly framed portraits for Instagram/LinkedIn.
- **Manual Mode:** Allows users to click on a point of interest if no face is detected.

#### 🎨 Image Enhancement
- **Histogram Equalization:** Converts images to YCrCb color space to equalize luminance, improving contrast in lighting-challenged photos.
- **Channel Filtering:** Ability to isolate specific RGB channels (Red, Green, Blue) or convert to Grayscale.

#### 📐 Social Media Ready
- Preset aspect ratios for major platforms:
  - **Instagram Feed** (4:5)
  - **Stories** (9:16)
  - **LinkedIn Profile** (1:1)
  - **Full HD** (16:9)
- **High-Quality Upscaling:** Uses **Lanczos** and **Bicubic** interpolation to resize images while preserving sharpness.

### 🚀 How to Run

1. **Clone the repository**
   ```bash
   git clone [https://github.com/nathanhgo/fotofacil.git](https://github.com/nathanhgo/fotofacil.git)
   cd fotofacil
   ```

2. Install Dependencies It is recommended to use a virtual environment.

```bash
pip install -r requirements.txt
```

3. Run the Server

```bash
python app.py
```

Access at http://localhost:5000

<BR>

📂 Project Structure
app.py: Flask entry point and route handling.

editor.py: Core class containing static methods for OpenCV manipulations (Crop, Filter, Detect).

haarcascade_frontalface_default.xml: Pre-trained model for face detection.

Developed by @nathanhgo.
