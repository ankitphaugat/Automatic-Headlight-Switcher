# 🚗 Automatic Headlight Beam Controller using OpenCV

This project uses a webcam and computer vision techniques to **automatically switch between high and low beam headlights** based on real-time detection of oncoming light sources. It's designed to reduce glare for other drivers during night driving and enhance road safety.

---

## 🎯 Features

- 🔦 **Bright Light Detection:** Detects intense light sources (like oncoming headlights) and switches to low beam automatically.
- 🚫 **Red Light Filtering:** Ignores rear vehicle tail lights using color masking.
- 🧠 **Region-Based Analysis:** Focuses on lower half of the frame to detect distant vehicles more accurately.
- ⏱️ **Time-based Decision Reset:** If no light is detected for a certain time, system reverts to high beam.
- 🔍 **Debug Mode:** Toggle visualizations like grayscale, red mask, thresholds, and overlays for analysis.

---

## 📸 Demo / Screenshots
- **High Intensity Light** is detected from each frame

<img width="795" height="633" alt="Screenshot (148)" src="https://github.com/user-attachments/assets/3f52a4ba-21a8-460a-8884-d039936227dc" />

- Image is coverted to **grayscale** and then high intensity points are recognized and the beam is signalled to change

  <img width="967" height="751" alt="Screenshot (150)" src="https://github.com/user-attachments/assets/96c74d6e-f5a3-463e-b94e-f3ebfc6a8b71" />

  
---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- OpenCV
- NumPy

### Installation

```bash
git clone https://github.com/rishabhgaur22/Automatic-headlight-switcher.git
cd Automatic-headlight-switcher
pip install -r requirements.txt 
python new.py
