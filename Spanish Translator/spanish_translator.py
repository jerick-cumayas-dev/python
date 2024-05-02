from spanish_translator_functions import *

# program main function
# Sentences:
# 1. The girl's house is very big.
# 2. Jerick's house is very big and the boy's red car is very beautiful.
def main():
    sentence = ("Jerick's house is very big and the boy's red car is very beautiful.\n")

    print("\n[SPANISH TRANSLATOR]\nSentence:", sentence)

    if(checkWordsinDictionary(sentence)):
        chunked_posTags = getIOBTags(transformSentenceToWords(sentence))
        print("Chunked POS Tags:");
        for chunk in chunked_posTags:
            print(chunk)

        reconstructed = translateToPossession(chunked_posTags)
        print("\nStructure:", transformSentence(sentence, getWordsFromTuples(getTuplesFromPOSTags(reconstructed))))

        es_grammar = arrangeToSpanishGrammar(reconstructed)
        print("Adjectives:", transformSentence(sentence, getWordsFromTuples(getTuplesFromPOSTags(es_grammar))))

        es_translation = translateWordsToSpanish(es_grammar)
        print("Literal Translation:", transformSentence(sentence, getWordsFromTuples(getTuplesFromPOSTags(es_translation))))

        es_gender = applyGenderToSentence(es_grammar, es_translation)
        print("Gender:", transformSentence(sentence, getWordsFromTuples(es_gender)))

        final = finalizeSpanishTranslation(es_gender)
        print("Spanish Translation:", transformSentence(sentence, getWordsFromTuples(final)))
        
main()