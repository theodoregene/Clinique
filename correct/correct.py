# correcteur_malgache_grammatical.py

import re
import json
from collections import defaultdict

class MalagasyLexicon:
    def __init__(self):
        self.words = set()
        self.word_freq = defaultdict(int)
        self.by_length = defaultdict(list)
        self.by_prefix = defaultdict(list)
        self.by_suffix = defaultdict(list)
        
    def load_from_file(self, filename, min_word_length=2):
        """Charge et structure le lexique depuis votre fichier"""
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if len(word) >= min_word_length:
                    clean_word = word.lower().strip()
                    if clean_word and clean_word.isalpha():
                        self.words.add(clean_word)
                        self.word_freq[clean_word] += 1
                        
        self._build_indexes()
        print(f"✅ Lexique chargé : {len(self.words)} mots")
        
    def _build_indexes(self):
        """Construit des index pour accélérer la recherche"""
        for word in self.words:
            self.by_length[len(word)].append(word)
            
            if len(word) >= 2:
                prefix = word[:2]
                self.by_prefix[prefix].append(word)
                
            if len(word) >= 2:
                suffix = word[-2:]
                self.by_suffix[suffix].append(word)

def damerau_levenshtein_optimized(s1, s2):
    """Version améliorée de Damerau-Levenshtein"""
    if s1 == s2:
        return 0
        
    len1, len2 = len(s1), len(s2)
    
    if abs(len1 - len2) > 3:
        return 999
    
    max_dist = len1 + len2
    char_dict = {}
    
    H = {(-1, -1): max_dist}
    for i in range(0, len1 + 1):
        H[(i, -1)] = max_dist
        H[(i, 0)] = i
    for j in range(0, len2 + 1):
        H[(-1, j)] = max_dist
        H[(0, j)] = j

    for i in range(0, len1):
        char_dict[s1[i]] = 0
                
    for i in range(0, len1):
        DB = 0
        for j in range(0, len2):
            i1 = char_dict.get(s2[j], -1)
            j1 = DB
            cost = 1
            if s1[i] == s2[j]:
                cost = 0
                DB = j + 1
                    
            H[(i+1, j+1)] = min(
                H[(i, j)] + cost,
                H[(i+1, j)] + 1,
                H[(i, j+1)] + 1,
                H[(i1, j1)] + (i - i1 - 1) + 1 + (j - j1 - 1)
            )
        char_dict[s1[i]] = i + 1

    return H[(len1, len2)]

class MalagasySpellChecker:
    def __init__(self, lexicon_file):
        self.lexicon = MalagasyLexicon()
        self.lexicon.load_from_file(lexicon_file)
        self.max_distance = 2
        self.max_suggestions = 5
        self.suggestion_cache = {}
        
        self.malagasy_rules = [
            (r'u$', 'o'),
            (r'à$', 'a'),
            (r'ì$', 'y'),
            (r'^rr', 'r'),
            (r'^tt', 't'),
            (r'^mm', 'm'),
            (r'^mpa', 'ma'),
            (r'^mpti', 'mi'),
            (r'^nts', 'ts'),
        ]
        
    def is_correct(self, word):
        return word.lower() in self.lexicon.words
    
    def apply_malagasy_rules(self, word):
        variations = [word]
        
        for pattern, replacement in self.malagasy_rules:
            new_word = re.sub(pattern, replacement, word)
            if new_word != word and len(new_word) >= 2:
                variations.append(new_word)
                
            inverse_word = re.sub(replacement, pattern, word)
            if inverse_word != word and len(inverse_word) >= 2:
                variations.append(inverse_word)
        
        return list(set(variations))
    
    def calculate_similarity_score(self, original, candidate, distance):
        """Calcule un score de similarité qui favorise le même début"""
        base_score = distance
        
        if candidate.startswith(original[0]):
            base_score -= 0.5
            
        if len(original) >= 2 and len(candidate) >= 2:
            if candidate.startswith(original[:2]):
                base_score -= 1.0
                
            if candidate.startswith(original[:3]):
                base_score -= 1.5
        
        length_diff = abs(len(original) - len(candidate))
        if length_diff <= 1:
            base_score -= 0.3
        
        freq = self.lexicon.word_freq.get(candidate, 1)
        base_score -= (freq * 0.001)
        
        return base_score
    
    def get_candidate_words(self, word):
        """Retourne des candidats en priorisant ceux qui commencent pareil"""
        word_lower = word.lower()
        candidates = set()
        
        prefix_lengths = [3, 2, 1]
        
        for prefix_len in prefix_lengths:
            if len(word_lower) >= prefix_len:
                prefix = word_lower[:prefix_len]
                if prefix_len == 1:
                    for key in self.lexicon.by_prefix.keys():
                        if key.startswith(prefix):
                            candidates.update(self.lexicon.by_prefix[key])
                else:
                    if prefix in self.lexicon.by_prefix:
                        candidates.update(self.lexicon.by_prefix[prefix])
        
        length = len(word_lower)
        for l in range(max(2, length-1), length+2):
            if l in self.lexicon.by_length:
                candidates.update(self.lexicon.by_length[l])
        
        if len(word_lower) >= 2:
            suffix = word_lower[-2:]
            if suffix in self.lexicon.by_suffix:
                candidates.update(self.lexicon.by_suffix[suffix])
        
        variations = self.apply_malagasy_rules(word_lower)
        for variation in variations:
            if variation in self.lexicon.words:
                candidates.add(variation)
        
        return list(candidates)
    
    def get_suggestions(self, word):
        """Retourne les suggestions de correction avec priorité au même début"""
        word_lower = word.lower()
        
        if word_lower in self.suggestion_cache:
            return self.suggestion_cache[word_lower]
        
        if self.is_correct(word_lower):
            self.suggestion_cache[word_lower] = [word_lower]
            return [word_lower]
        
        candidates = self.get_candidate_words(word_lower)
        suggestions = []
        
        for candidate in candidates:
            distance = damerau_levenshtein_optimized(word_lower, candidate)
            if distance <= self.max_distance:
                score = self.calculate_similarity_score(word_lower, candidate, distance)
                suggestions.append((score, distance, candidate))
        
        suggestions.sort(key=lambda x: (x[0], x[1]))
        result = [s[2] for s in suggestions[:self.max_suggestions]]
        
        if not result or (result and damerau_levenshtein_optimized(word_lower, result[0]) > 1):
            length = len(word_lower)
            fallback_candidates = []
            for l in range(max(2, length-2), length+3):
                if l in self.lexicon.by_length:
                    for candidate in self.lexicon.by_length[l]:
                        distance = damerau_levenshtein_optimized(word_lower, candidate)
                        if distance <= min(3, self.max_distance + 1):
                            score = self.calculate_similarity_score(word_lower, candidate, distance)
                            fallback_candidates.append((score, distance, candidate))
            
            fallback_candidates.sort(key=lambda x: (x[0], x[1]))
            fallback_result = [s[2] for s in fallback_candidates[:self.max_suggestions]]
            
            combined = list(dict.fromkeys(result + fallback_result))
            result = combined[:self.max_suggestions]
        
        self.suggestion_cache[word_lower] = result
        return result

    def apply_grammar_rules(self, text):
        """Applique les règles grammaticales de majusculation"""
        if not text:
            return text
        
        # Séparer le texte en phrases (délimitées par . ! ?)
        sentences = re.split(r'([.!?]+\s*)', text)
        result_sentences = []
        
        capitalize_next = True  # Première phrase doit avoir une majuscule
        
        for i, sentence in enumerate(sentences):
            if not sentence.strip():
                result_sentences.append(sentence)
                continue
                
            # Si c'est un délimiteur de phrase (. ! ?)
            if re.match(r'[.!?]+\s*$', sentence):
                result_sentences.append(sentence)
                capitalize_next = True
                continue
            
            # Appliquer la majuscule si nécessaire
            if capitalize_next:
                # Trouver le premier caractère alphabétique
                for j, char in enumerate(sentence):
                    if char.isalpha():
                        sentence = sentence[:j] + char.upper() + sentence[j+1:]
                        break
                capitalize_next = False
            
            result_sentences.append(sentence)
        
        return ''.join(result_sentences)
    
    def correct_text(self, text):
        """Corrige un texte complet avec règles grammaticales"""
        if not text.strip():
            return text
        
        # Étape 1: Correction orthographique
        words_and_spaces = re.findall(r"[\w']+|[^\w\s]|\s+", text)
        corrected_parts = []
        
        for part in words_and_spaces:
            if not part.strip():
                corrected_parts.append(part)
            elif not part.isalpha():
                corrected_parts.append(part)
            else:
                if self.is_correct(part):
                    corrected_parts.append(part)
                else:
                    suggestions = self.get_suggestions(part)
                    if suggestions:
                        correction = suggestions[0]
                        if part.istitle():
                            corrected_parts.append(correction.title())
                        elif part.isupper():
                            corrected_parts.append(correction.upper())
                        else:
                            corrected_parts.append(correction)
                    else:
                        corrected_parts.append(part)
        
        text_corrige = ''.join(corrected_parts)
        
        # Étape 2: Application des règles grammaticales
        text_avec_grammaire = self.apply_grammar_rules(text_corrige)
        
        return text_avec_grammaire

def test_grammaire_et_correction():
    """Test des règles grammaticales et de correction"""
    correcteur = MalagasySpellChecker('lista_teny_malagasy.txt')
    
    print("🎯 TEST CORRECTION + GRAMMAIRE")
    print("=" * 45)
    
    tests = [
        # Test majuscule début de texte
        "manao ahoana ry zanako. tia anao aho. veloma.",
        
        # Test après point
        "mangatsiaka androany. tsy mivoaka aho. mbola marary ihany.",
        
        # Test avec points d'exclamation et interrogation
        "inona no vaovao? tsy mahalala aho. eny tokoa!",
        
        # Test avec fautes + grammaire
        "oluna malalako. manao ahona. tia anao aho.",
        
        # Début sans majuscule
        "maharitra ve ianao? azafady, omeo rano aho.",
    ]
    
    for i, test in enumerate(tests, 1):
        corrige = correcteur.correct_text(test)
        print(f"\nTest {i}:")
        print(f"Original: {test}")
        print(f"Corrigé : {corrige}")
        print("-" * 50)

def test_interactif_complet():
    """Mode interactif avec correction complète"""
    correcteur = MalagasySpellChecker('lista_teny_malagasy.txt')
    
    print("💬 CORRECTEUR MALGACHE - MODE INTERACTIF COMPLET")
    print("Correction orthographique + Règles grammaticales")
    print("Tapez 'quit' pour quitter")
    print("=" * 55)
    
    while True:
        texte = input("\nEntrez un texte à corriger: ").strip()
        
        if texte.lower() == 'quit':
            break
        
        if not texte:
            continue
            
        # Correction complète
        texte_corrige = correcteur.correct_text(texte)
        
        print(f"\n📝 RÉSULTAT:")
        print(f"Original: {texte}")
        print(f"Corrigé : {texte_corrige}")
        
        # Afficher aussi les suggestions si c'est un mot unique
        if ' ' not in texte.strip():
            suggestions = correcteur.get_suggestions(texte)
            est_correct = correcteur.is_correct(texte)
            statut = "✅ CORRECT" if est_correct else "❌ FAUX"
            print(f"Orthographe: {statut}")
            if suggestions and not est_correct:
                print(f"Suggestions: {suggestions}")

if __name__ == "__main__":
    # Test des fonctionnalités grammaticales
    test_grammaire_et_correction()
    
    # Lancer le mode interactif
    test_interactif_complet()