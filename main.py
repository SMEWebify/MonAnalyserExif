import os
from tkinter import filedialog, Tk, messagebox, simpledialog
from PIL import Image
from PIL.ExifTags import TAGS
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from fractions import Fraction
import math

def get_exif_data(path):
    try:
        img = Image.open(path)
        exif_data = img._getexif()
        if not exif_data:
            return {}
        return {TAGS.get(tag): exif_data[tag] for tag in exif_data if tag in TAGS}
    except Exception as e:
        return {}

def extract_year(date_str):
    if date_str and isinstance(date_str, str):
        try:
            return int(date_str.split()[0].split(":")[0])
        except:
            return None
    return None

def choisir_annees(annees, root):
    from tkinter import Toplevel, Checkbutton, IntVar, Button

    top = Toplevel(root)
    top.title("Choisir les années à analyser")

    vars = {}
    for i, annee in enumerate(annees):
        var = IntVar()
        chk = Checkbutton(top, text=str(annee), variable=var)
        chk.grid(row=i+1, column=0, sticky="w")
        vars[annee] = var

    all_var = IntVar()

    def toggle_all():
        for var in vars.values():
            var.set(all_var.get())

    chk_all = Checkbutton(top, text="Tout sélectionner", variable=all_var, command=toggle_all)
    chk_all.grid(row=0, column=0, sticky="w")

    selected = []

    def valider():
        nonlocal selected
        selected = [a for a in vars if vars[a].get()]
        top.destroy()

    Button(top, text="Valider", command=valider).grid(row=len(annees) + 2, column=0)
    top.grab_set()  # bloque les interactions hors de cette fenêtre
    top.wait_window()  # attend la fermeture
    return selected


def to_float(value):
    try:
        return round(float(value), 6)
    except Exception as e:
        #print(f"Erreur to_float({value}) → {e}")
        return None

def scan_folder(folder):
    data = []
    for root_dir, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                path = os.path.join(root_dir, file)
                exif = get_exif_data(path)

                # DEBUG : afficher les champs trouvés
                # print(f"\n📸 {file} → {list(exif.keys())}")

                if exif:
                    #print(f"\n📸 {file}")
                    print(f"  FNumber brut     : {exif.get('FNumber')}")
                    #print(f"  ExposureTime brut: {exif.get('ExposureTime')}")
                    #print(f"  Iso: {exif.get('ISOSpeedRatings')}")
                    #print(f"  FocalLength brut : {exif.get('FocalLength')}")
                    
                    date_str = exif.get("DateTimeOriginal") or exif.get("DateTime")
                    ouverture = to_float(exif.get("FNumber"))
                    vitesse = to_float(exif.get("ExposureTime"))
                    focale = to_float(exif.get("FocalLength"))
                    iso = exif.get("ISOSpeedRatings")
                    annee = extract_year(date_str)

                    # DEBUG
                    print(f"  ➕ Données converties : Ouverture={ouverture}, Vitesse={vitesse}, Focale={focale}")

                    data.append({
                        "Nom": file,
                        "Ouverture": ouverture,
                        "Vitesse": vitesse,
                        "ISO": iso,
                        "Focale": focale,
                        "Année": annee,
                    })
        df = pd.DataFrame(data)

    # Forcer les colonnes numériques (float), ISO reste tel quel
    for col in ["Ouverture", "Vitesse", "Focale"]:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def vitesse_formatter(x, pos):
    try:
        if x <= 0 or math.isnan(x) or math.isinf(x):
            return ""
        if x >= 1:
            return f"{x:.1f}s"  # Pour les poses longues
        else:
            frac = Fraction(1 / x).limit_denominator(10000)
            return f"1/{frac.denominator}"
    except:
        return str(x)

def plot_stat_multi(df):
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))  # 1 ligne, 4 graphes

    columns = [
        ("ISO", "Distribution des ISO", ""),
        ("Vitesse", "Vitesse d’obturation", "s"),
        ("Ouverture", "Ouverture (FNumber)", ""),
        ("Focale", "Focale", "mm"),
    ]

    couleurs = plt.cm.get_cmap('tab10')  # Palette de 10 couleurs
    annees = sorted(df["Année"].dropna().unique())

    for ax, (col, title, unit) in zip(axes, columns):
        ax.set_title(title)
        ax.set_xlabel(f"{col} {unit}")
        ax.set_ylabel("Nombre de photos")

        for idx, annee in enumerate(annees):
            data_annee = df[df["Année"] == annee][col].dropna()

            if col == "Vitesse":
                data_annee = data_annee[data_annee > 0]  # 🔧 Évite division par 0

            if not data_annee.empty:
                ax.hist(
                    data_annee,
                    bins=20,
                    alpha=0.5,
                    color=couleurs(idx % 10),
                    label=str(int(annee))
                )

        if col == "Vitesse":
            #ax.set_yscale('log')
            ax.xaxis.set_major_formatter(ticker.FuncFormatter(vitesse_formatter))

        ax.legend()
        ax.grid(True)

    plt.tight_layout()
    plt.show()


def main():
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Choisis un dossier de photos", parent=root)
    if not folder:
        messagebox.showinfo("Info", "Aucun dossier sélectionné.")
        return

    df = scan_folder(folder)

    if df.empty:
        messagebox.showinfo("Info", "Aucune photo avec données EXIF trouvée.")
        return

    années_disponibles = sorted(df["Année"].dropna().unique())
    if not années_disponibles:
        messagebox.showinfo("Info", "Aucune année trouvée dans les métadonnées.")
        return

    annees_choisies = choisir_annees(années_disponibles, root)

    if not annees_choisies:
        messagebox.showinfo("Info", "Aucune année sélectionnée.")
        return

    df = df[df["Année"].isin(annees_choisies)]

    if df.empty:
        messagebox.showinfo("Info", "Aucune photo trouvée pour les années sélectionnées.")
        return

    print("\n📊 Résumé des données :")
    print(df[["Nom", "Ouverture", "Vitesse", "ISO", "Focale", "Année"]].to_string(index=False))

    plot_stat_multi(df)


if __name__ == "__main__":
    main()
