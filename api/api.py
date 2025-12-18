from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import sys

sys.path.append('../correct')

from correct import MalagasySpellChecker

app = FastAPI(title="API TSIPeLINA")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation du correcteur
correcteur = None

with open("../data/malagasy.json", "r", encoding="utf-8") as f:
    dico = json.load(f)

# Initialiser le correcteur
try:
    correcteur = MalagasySpellChecker("../correct/lista_teny_malagasy.txt")
    print("✅ Correcteur orthographique malgache initialisé avec succès")
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation du correcteur: {e}")
    correcteur = None

@app.get("/")
def read_root():
    return {"message": "Bienvenue"}

# Endpoint pour récupérer tout le dictionnaire
@app.get("/dico")
def get_dico():
    return JSONResponse(content=dico)

# Endpoint pour récupérer un mot du dico
@app.get("/dico/{word}")
def get_dico_word(word: str):
    results = [
        entry for entry in dico
        if word.lower() in entry["teny"].lower()
    ]
    if results:
        return JSONResponse(content={"resultats": results})
    return JSONResponse(content={"message": "Aucun mot trouvé."}, status_code=404)

# SEUL NOUVEL ENDPOINT AJOUTÉ - JUSTE LA CORRECTION
@app.post("/corriger")
async def corriger_texte(texte: dict):
    """
    Corrige l'orthographe d'un texte malgache avec détection précise des fautes
    """
    if not correcteur:
        return JSONResponse(
            content={"error": "Correcteur non initialisé"}, 
            status_code=503
        )
    
    if "texte" not in texte:
        return JSONResponse(
            content={"error": "Clé 'texte' manquante"}, 
            status_code=400
        )
    
    try:
        texte_original = texte["texte"]
        texte_corrige = correcteur.correct_text(texte_original)
        
        # Détection précise des fautes
        import re
        
        # Séparation des mots en gardant la ponctuation
        mots_originaux = re.findall(r"[\w']+|[^\w\s]", texte_original)
        mots_corriges = re.findall(r"[\w']+|[^\w\s]", texte_corrige)
        
        nombre_fautes = 0
        corrections_detail = []
        
        # Comparaison mot à mot
        min_length = min(len(mots_originaux), len(mots_corriges))
        
        for i in range(min_length):
            mot_orig = mots_originaux[i]
            mot_corr = mots_corriges[i]
            
            # Ne compter que les mots (pas la ponctuation) qui ont changé
            if mot_orig.isalpha() and mot_orig != mot_corr:
                nombre_fautes += 1
                corrections_detail.append({
                    "mot_original": mot_orig,
                    "mot_corrige": mot_corr,
                    "position": i
                })
        
        return {
            #"original": texte_original,
            "corrige": texte_corrige,
            "nombre_fautes": nombre_fautes,
            #"corrections_detail": corrections_detail
        }
    except Exception as e:
        return JSONResponse(
            content={"error": f"Erreur lors de la correction: {str(e)}"}, 
            status_code=500
        )

# Lancement de l'api
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
