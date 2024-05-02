import string
from spanish_translator_modules import *

# Sentences are transformed into lower cases
# returned as a list
def transformSentenceToWords(sentence):
    exclude = set(string.punctuation) - {"'"}
    translate_table = str.maketrans('', '', ''.join(exclude))

    # remove punctuation except for apostrophes
    clean_sentence = sentence.lower().translate(translate_table)

    # split the sentence into a list of words
    words = clean_sentence.split()

    # print the list of words
    return words

def checkWordsinDictionary(sentence):
    words = transformSentenceToWords(sentence)
    length = len(words)
    num = 0

    for word in words:
        found = 0
        for pos in parts_of_speech.keys():
            if word in parts_of_speech[pos]:
                num = num + 1
                found = 1
                break
        if found != 1:
            print(f"[{word}] not in English dictionary.")

    if(num == len(words)):
        return True

    return False

# words are grouped into tuples with IOB tags, Pos Tags, and the word itself
# used chunking to be used in determining and changing the gender of words
# (IOB Tag, Pos Tag, 'word) ex. ('B', 'NNS', 'cat')
def getIOBTags(words):
    iobTagged = []
    temp = []
    num = 0

    for word in words:
        for pos in parts_of_speech.keys():
            if word in parts_of_speech[pos]:
                if word not in verbs and word not in conjunctions and word not in linking_verbs:
                    if num == 0:
                        temp.append(('B', pos, word))
                        num = num + 1
                    else:
                        temp.append(('I', pos, word))
                        num = num + 1
                else: 
                    if (len(temp) == 0):
                        temp.append(('O', pos, word))
                        iobTagged.append(temp)
                        temp = []
                        num = 0
                    else:
                        iobTagged.append(temp)
                        temp = []
                        temp.append(('O', pos, word))
                        iobTagged.append(temp)
                        temp = []
                        num = 0

    iobTagged.append(temp)

    return iobTagged

def hasNounPhrase(chunk):
    for tupl in chunk:
        if tupl[1] == 'NOUN' or tupl[1] == 'PROPER NOUN' or tupl[1] == 'PRONOUN':
            return True
    return False

def getIndexOfTuple(search, chunk):
    for tupl in chunk:
        if tupl[1] == search:
            return chunk.index(tupl)

def getGender(noun):
    for ending, gender in gender_endings.items():
        if noun.endswith(ending):
            return gender
    return 'unknown'

def checkNounSingularPlural(noun):
    print("Hello world")

def arrangeToSpanishGrammar(chunked_posTags):
    temp = []
    adjs = []
    reconstructed = []
    num = 0
    for chunk in chunked_posTags:
        if hasNounPhrase(chunk) == True:
            for tupl in chunk:
                if tupl[1] == "ADJ":
                    adjs.append(tupl)
                else:
                    if tupl[1] == "CONJ":
                        if len(temp) == 0:
                            temp.append(tupl)
                        else:
                            adjs.append(tupl)
                    elif tupl[1] == "NOUN" or tupl[1] == "PROPER NOUN" or tupl[1] == "PRONOUN":
                        temp.append(tupl)
                        temp.extend(adjs)
                        reconstructed.append(temp)
                        temp = []
                        adjs = []
                    else: 
                        temp.append(tupl)
                num = num + 1
            temp = []
            adjs = []
        else:
            reconstructed.append(chunk)

    return reconstructed

def translateToPossession(es_grammar):
    sentence = getWordsFromTuples(getTuplesFromPOSTags(es_grammar))

    for chunk in es_grammar:
        if hasNounPhrase:
            for index, tupl in enumerate(chunk):
                if tupl[1] == "NOUN" or tupl[1] == "PROPER NOUN":
                    try:
                        if tupl[1] == "NOUN":
                            if "\'s" in tupl[2] and chunk[index + 1][1] == "NOUN":
                                phrase = tupl[2] + " " + chunk[index + 1][2]
                                new_phrase = chunk[index + 1][2] + " " + "of the " + tupl[2].replace('\'s', "")
                                
                            elif "\'s" in tupl[2] and chunk[index + 1][1] == "ADJ":
                                if chunk[index + 2][1] == "NOUN":
                                    phrase = tupl[2] + " " + chunk[index + 1][2] + " " + chunk[index + 2][2]
                                    new_phrase = chunk[index + 1][2] + " " + chunk[index + 2][2] + " " + "of the " + tupl[2].replace('\'s', "")
                        elif tupl[1] == "PROPER NOUN":
                            if "\'s" in tupl[2] and chunk[index + 1][1] == "NOUN":
                                phrase = tupl[2] + " " + chunk[index + 1][2]
                                new_phrase = "the " + chunk[index + 1][2] + " " + "of " + tupl[2].replace('\'s', "")

                        sentence = sentence.replace(phrase, new_phrase)

                    except Exception:
                        print("")

    return getIOBTags(transformSentenceToWords(sentence))
    
def translateWordsToSpanish(es_grammar):
    translation = [] 
    temp = []
    proper = []
    num = 0

    for chunk in es_grammar:
        for tupl in chunk:
            for key, value in spanish_dictionary.items():
                if (tupl[2] in value):
                    if tupl[1] != "VERB" and tupl[1] != "LINKING_VERB":
                        if num == 0:
                            temp.append((tupl[0], tupl[1], key))
                            num = num + 1
                        else:
                            temp.append((tupl[0], tupl[1], key))
                            num = num + 1
                    else: 
                        if (len(temp) == 0):
                            temp.append((tupl[0], tupl[1], key))
                            translation.append(temp)
                            temp = []
                            num = 0
                        else:
                            translation.append(temp)
                            temp = []
                            temp.append((tupl[0], tupl[1], key))
                            translation.append(temp)
                            temp = []
                            num = 0
                    # translation.append((tupl[0], tupl[1], key))
            if tupl[1] == "PROPER NOUN":
                temp.append((tupl[0], tupl[1], tupl[2]))
    if len(temp) != 0:            
        translation.append(temp)   

    return translation

def applyGenderToSentence(es_grammar, es_translation):
    appliedNounGender = []
    for chunk in es_translation:
        if hasNounPhrase(chunk):
            for tupl in chunk:
                if tupl[1] == "NOUN" or tupl[1] == "PRONOUN":
                    if getGender(tupl[2]) == 'masculine':
                        if tupl[2] not in singular_words:
                            try:
                                if chunk[chunk.index(tupl) - 1][1] == "DET" and chunk[chunk.index(tupl) - 1][2] == "el":
                                    temp = chunk[chunk.index(tupl) - 1]
                                    chunk[chunk.index(tupl) - 1] = (temp[0], temp[1], 'los')
                            except Exception:
                                    print("")
                        else:
                            try:
                                if chunk[chunk.index(tupl) - 1][1] == "DET" and chunk[chunk.index(tupl) - 1][2] == "el":
                                    temp = chunk[chunk.index(tupl) - 1]
                                    chunk[chunk.index(tupl) - 1] = (temp[0], temp[1], 'el')
                                elif chunk[chunk.index(tupl) - 1][1] == "DET" and chunk[chunk.index(tupl) - 1][2] == "a":
                                    temp = chunk[chunk.index(tupl) - 1]
                                    chunk[chunk.index(tupl) - 1] = (temp[0], temp[1], 'un')
                            except Exception:
                                    print("")
                    else:
                        if tupl[2] not in singular_words:
                            try:
                                if chunk[chunk.index(tupl) - 1][1] == "DET" and chunk[chunk.index(tupl) - 1][2] == "la":
                                    temp = chunk[chunk.index(tupl) - 1]
                                    chunk[chunk.index(tupl) - 1] = (temp[0], temp[1], 'las')
                            except Exception:
                                    print("")
                        else:
                            try:
                                if chunk[chunk.index(tupl) - 1][1] == "DET" and chunk[chunk.index(tupl) - 1][2] == "el":
                                    temp = chunk[chunk.index(tupl) - 1]
                                    chunk[chunk.index(tupl) - 1] = (temp[0], temp[1], 'la')
                                elif chunk[chunk.index(tupl) - 1][1] == "DET" and chunk[chunk.index(tupl) - 1][2] == "a":
                                    temp = chunk[chunk.index(tupl) - 1]
                                    chunk[chunk.index(tupl) - 1] = (temp[0], temp[1], 'una')
                            except Exception:
                                    print("")
    return capitalizedProperNouns(es_translation)

def finalizeSpanishTranslation(tags):
    for index,tupl in enumerate(tags):
        if tupl[2] == "de" and index + 1 < len(tags) and tags[index + 1][2] == "el":
            tags[index] = ((tupl[0], tupl[1], "del"))
            tags.remove(tags[index + 1])
        
    return tags

def capitalizedProperNouns(tags):
    capitalized = []
    for chunk in tags:
        for tupl in chunk:
            if tupl[1] != "PROPER NOUN":
                capitalized.append(tupl)
            else:
                capitalized.append((tupl[0], tupl[1], tupl[2].capitalize()))
    return capitalized

def transformSentence(sentence, es_translation):
    if sentence[-1] != ".":
        return es_translation[0].capitalize() + es_translation[1:] + "."
    else:
        return es_translation[0].capitalize() + es_translation[1:] + sentence[len(sentence) - 1]

def getTuplesFromPOSTags(tags):
    tagged = []
    for chunk in tags:
        for taggedWord in chunk:
            tagged.append(taggedWord)
    return tagged

def getWordsFromTuples(tags):
    sentence = []
    for tupl in tags:
        sentence.append(tupl[2])
    return " ".join(sentence)

def minimum_edit_distance(first_string, second_string):
    row = len(first_string)
    col = len(second_string)
    distance_matrix = [[0 for j in range(col + 1)] for i in range(row + 1)]
    
    first_word = list(first_string)
    second_word = list(second_string)

    for i in range(row + 1):
        distance_matrix[i][0] = i
    for j in range(col + 1):
        distance_matrix[0][j] = j
        
    for row in range(1, row + 1):
        for col in range(1, col + 1):
            left = distance_matrix[row][col - 1] + 1
            down = distance_matrix[row - 1][col] + 1
            diagonal = distance_matrix[row - 1][col - 1] + ( 0 if (first_word[(row - 1) - 1] == second_word[(col - 1) - 1]) else 2)
            distance_matrix[row][col] = min(left, down, diagonal)

    return distance_matrix[row][col]