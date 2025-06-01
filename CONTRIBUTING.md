# 🤝 Contribuer à MonAnalyserExif

Merci de ton intérêt pour ce projet ! Ce document t'explique comment contribuer efficacement au développement de **MonAnalyserExif**, une application Python permettant d'analyser les données EXIF de photos.

---

## ✅ Prérequis

Avant de contribuer :

- Avoir une connaissance de base de Python.
- Savoir utiliser Git et GitHub.
- Avoir installé les dépendances :

```bash
pip install -r requirements.txt
```

## Structure du projet
```bash
MonAnalyserExif/
│
├── main.py               # Script principal (Tkinter + matplotlib)
├── README.md             # Documentation du projet
├── CONTRIBUTING.md       # Ce fichier
├── requirements.txt      # Dépendances Python
└── screenshot.png        # Capture d'écran (facultatif)
```

## Tester
```bash
python main.py
```

## ✍️ Bonnes pratiques
- Suis le style du code existant.
- Ajoute des commentaires si ton code est complexe.
- Priorise la lisibilité plutôt que la concision.
- Les contributions sont petites, ciblées, et bien nommées.
- Ne supprime pas le code ou les fonctionnalités existantes sans discussion.

## 💡 Idées de contribution
- Tu ne sais pas par où commencer ? Voici quelques suggestions :
- Ajouter le support des fichiers .nef, .cr2, .arw, etc.
- Permettre d’exporter les données EXIF en .csv
- Ajouter des filtres supplémentaires (appareil photo, objectif, ISO max, etc.)
- Ajouter une mini-preview des images dans l’interface
- Améliorer le style visuel avec ttk ou customtkinter

