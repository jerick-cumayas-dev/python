determiners = ["the", "a", "an"]
nouns = ["cat", "house",  "car", "man", "woman", "cats", 
"song", "songs", "fish", "dog", "fox", "i", "boy's", "boy", "girl's", "girl", "man's", "man"]
proper_nouns = ["jerick's", "jerick", "royce", "cumayas", "princess", "ericka", 'philippines']
pronouns = ["he", "she"]
adjectives = ["red", "blue", "country", "quick", "brown", "lazy", "important", "big", "beautiful"]
linking_verbs = ["is"]
verbs = ["go", "ate", "jumps", "am", "speak", "have"]
conjunctions = ["and", "but", "so"]
prepositions = ["over", "in", "to", "from", "of"]
continuous = ["barking", "working", "practicing", "eating", "sleeping", "uploading", '`', '`']
past_LV = ["was", "were", '`', '`']
adverbs = ["very","gracefully", "extremely", "very","now", "then", "soon", "early", "late", "never", "always", "often", "sometimes", "rarely", "mostly", "maybe", "perhaps", "here", "there", "anywhere", "everywhere", "nowhere", "well", "quickly", "slowly", "fast", "loudly", "quietly", "hard", "easily"]
numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty']

parts_of_speech = dict()
parts_of_speech["DET"] = determiners
parts_of_speech["NOUN"] = nouns
parts_of_speech["PROPER NOUN"] = proper_nouns
parts_of_speech["PRONOUN"] = pronouns
parts_of_speech["ADJ"] = adjectives
parts_of_speech["CONJ"] = conjunctions
parts_of_speech["VERB"] = verbs
parts_of_speech["PREP"] = prepositions
parts_of_speech["LINKING_VERB"] = linking_verbs
parts_of_speech["ADVERB"] = adverbs

singular_words = ['gato', 'perro', 'casa', 'coche', 'mesa', 'silla', 'manzana', 
                    'pelota', 'lápiz', 'libro', 'cama', 'flor', 'árbol', 'reloj', 
                    'sol', 'luna', 'puerta', 'ventana', 'taza', 'zapato', 'canción', 
                    'mujer', 'zorra', 'hombre', 'nina']

spanish_verbs_base = { 
    'hablar': 'to speak',
    'comer': 'to eat',
    'beber': 'to drink',
    'vivir': 'to live',
    'trabajar': 'to work',
    'estudiar': 'to study',
    'amar': 'to love',
    'querer': 'to want',
    'tener': 'to have',
    'necesitar': 'to need',
    'poder': 'to be able to',
    'ir': 'to go',
    'venir': 'to come',
    'saber': 'to know',
    'conocer': 'to know',
    'dar': 'to give',
    'poner': 'to put',
    'decir': 'to say',
    'ver': 'to see',
    'hacer': 'to make',
    'sentir': 'to feel',
    'caminar': 'to walk',
    'correr': 'to run',
    'saltar': 'to jump',
    'bailar': 'to dance'
}

spanish_dictionary = {
    "muy": ['very'],
    "tengo" : ['have'],
    "grande" : ['big'],
    "es" : ['is'],
    "un" : ['a'],
    "en": ["in"],
    "de" : ['from', 'of'],
    "soy" : ['am'],
    "yo" : ['i'],
    "rapido" : ['quick'],
    "perezoso" : ['lazy'],
    "perro" : ['dog'],
    "encima" : ['encima'],
    "salta" : ['jumps'],
    "marron" : ['brown'],
    "zorra" : ['fox'],
    "perro": ['dog'],
    "hermosa" : ['beautiful'],
    "pescado" : ['fish'],
    "canción": ['song'],
    "cansiones" : ['songs'],
    "un" : ['a'],
    "el" : ['the', 'he'],
    "and" : ['y'],
    "comió" : ['ate'],
    "gato" : ['cat'],
    "gatos" : ['cats'],
    "rojo" : ['red'],
    "azul" : ['blue'],
    "casa" : ['house'],
    "perro" : ['dog'],
    "niño" : ['boy'],
    "nina" : ['girl'],
    "hombre" : ['man'],
    "mujer" : ['woman'],
    "comida" : ['food'],
    "agua" : ['water'],
    "familia" : ['family'],
    "amigo" : ['friend'],
    "trabajo" : ['work'],
    "escuela" : ['school'],
    "coche" : ['car'],
    "calle" : ['street'],
    "ciudad" : ['city'],
    "país" : ['country'],
    # "bueno" : 'good',
    # "malo" : 'bad',
    # "grande" : 'big',
    # "pequeño" : 'small',
    # "nuevo" : 'new',
    # "viejo" : 'old',
    # "primero" : 'first',
    # "último" : 'last',
    # "verdad" : 'truth',
    # "mentira" : 'lie',
    # "importante" : 'important',
    # "interesante" : 'interesting',
    # "difícil" : 'difficult',
    # "fácil" : 'easy',
    # "contento" : 'happy',
    # "triste" : 'sad',
    # "enfermo" : 'sick',
    # "saludable" : 'healthy',
    # "abierto" : 'open',
    # "cerrado" : 'closed',
    # "dentro" : 'inside',
    # "fuera" : 'outside',
    # "ahora" : 'now',
    # "después" : 'after',
    # "antes" : 'before',
    # "siempre" : 'always',
    # "nunca" : 'never',
    # "quizás" : 'maybe',
    # "tal vez" : 'perhaps',
    # "porque" : 'because',
    "pero" : ['but'],
    "y" : ['and'],
    "o" : ['or'],
    "con" : ['with'],
    "sin" : ['without'],
    "para" : ['for'],
    "en" : ['in'],
    "sobre" : ['on'],
    "bajo" : ['under'],
}

gender_endings = {
        'coche':'masculine',
        'nina' : 'feminine',
        'gato': 'masculine',
        'casa': 'feminine',
        'ción': 'feminine',
        'dad': 'feminine',
        'tad': 'feminine',
        'sión': 'feminine',
        'tud': 'feminine',
        'umbre': 'feminine',
        'eza': 'feminine',
        'itis': 'feminine',
        'ie': 'feminine',
        'cia': 'feminine',
        'sis': 'feminine',
        'za': 'feminine',
        'ga': 'feminine',
        'ora': 'feminine',
        'uda': 'feminine',
        'isa': 'feminine',
        'nza': 'feminine',
        'tura': 'feminine',
        'ía': 'feminine',
        'ó': 'masculine',
        'or': 'masculine',
        'aje': 'masculine',
        'ambre': 'masculine',
        'en': 'masculine',
        'án': 'masculine',
        'ín': 'masculine',
        'il': 'masculine',
        'ón': 'masculine',
        'ma': 'masculine',
        'man:' : 'masculine',
        'hombre' : 'masculine'
    }

spanish_words_plural = {
    "rojos" : 'rojo',
    "los" : 'el',
    "las" : 'la',
    "unos" : 'un',
    "unas" : 'una'
}

spanish_grammar = [
    ["DET", "NNS", "ADJ"], 
    ["DET", "NNP", "ADJ"],
    ["DET", "NNS", "ADJ", "CONJ", "DET", "NNS", "ADJ"]
]