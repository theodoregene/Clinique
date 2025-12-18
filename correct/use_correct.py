# debut_rapide.py

from correct import MalagasySpellChecker

# Utilisation la plus simple
def exemple_simple():
    # 1. Créer le correcteur (remplacez par le chemin de votre fichier)
    correcteur = MalagasySpellChecker('lista_teny_malagasy.txt')
    
    # 2. Vérifier un mot
    mot = "oluna"
    if correcteur.is_correct(mot):
        print(f"✅ '{mot}' est correct")
    else:
        suggestions = correcteur.get_suggestions(mot)
        print(f"❌ '{mot}' → Suggestions: {suggestions}")
    
    # 3. Corriger une phrase
    phrase = "Manao ahoana ry zanako"
    corrige = correcteur.correct_text(phrase)
    print(f"Phrase: {phrase}")
    print(f"Corrigé: {corrige}")

# Test interactif
def mode_interactif():
    correcteur = MalagasySpellChecker('lista_teny_malagasy.txt')
    
    print("💬 Correcteur Malgache - Mode Interactif")
    print("Tapez 'quit' pour quitter")
    print("-" * 40)
    
    while True:
        texte = input("\nEntrez un mot ou une phrase: ").strip()
        
        if texte.lower() == 'quit':
            break
            
        if ' ' in texte:
            # C'est une phrase
            corrige = correcteur.correct_text(texte)
            print(f"🔧 Correction: {corrige}")
        else:
            # C'est un mot unique
            if correcteur.is_correct(texte):
                print(f"✅ '{texte}' est correct")
            else:
                suggestions = correcteur.get_suggestions(texte)
                print(f"❌ Suggestions pour '{texte}': {suggestions}")

if __name__ == "__main__":
    # Choisissez l'exemple que vous voulez exécuter :
    
    # Exemple simple
    #exemple_simple()
    
    # Ou mode interactif
    mode_interactif()