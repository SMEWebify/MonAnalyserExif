
# 📸 MonAnalyserExif

**MonAnalyserExif** est une application Python avec interface graphique (Tkinter) qui scanne les photos d’un dossier, extrait les métadonnées EXIF, et affiche des statistiques visuelles sur les réglages utilisés (ISO, ouverture, vitesse d’obturation, focale), avec filtrage par année.

---

## ✨ Fonctionnalités

- 📂 Sélection d’un dossier contenant des photos `.jpg` ou `.jpeg`
- 🏷️ Extraction des données EXIF : ISO, ouverture (FNumber), vitesse (ExposureTime), focale, date
- 📅 Sélection des années à inclure via des cases à cocher
- 📊 Affichage de 4 histogrammes sur une seule fenêtre :
  - ISO
  - Vitesse d’obturation (en `1/xxx`)
  - Ouverture (F-number)
  - Focale (en mm)
- 🌈 Couleurs différenciées par année
- 🔍 Échelle logarithmique pour la vitesse (facultative mais utile)

---

## 🖼️ Aperçu

![WhatsApp Image 2025-06-01 à 00 34 36_a5fd2f02](https://github.com/user-attachments/assets/5a8afd40-b510-46c3-a68a-bd738931f93e)

---

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone https://github.com/ton-utilisateur/MonAnalyserExif.git
cd MonAnalyserExif
