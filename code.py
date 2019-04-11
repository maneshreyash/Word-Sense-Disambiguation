# Using WordNet Library API to access the WordNet dictionary, implement the
# SIMPLIFIED LESK algorithm to disambiguate the word bank in the sentence. Your
# output should show the word overlap for each sense of the word bank in WordNet
# and the final chosen sense.
#
# @author: Shreyash Sanjay Mane


from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
import itertools


# Helper method to get the definition and examples of a sense and convert all of the words in it to token format.
# @param:   sense - the sense for which the retrieval is to be done from word net.
# @return:  merged - the list of tokens from definition and examples merged together as one.
def get_glossary(sense):

    # get definition of sense
    definition = wn.synset(sense).definition()

    # get examples of sense
    examples = wn.synset(sense).examples()

    glossary = []

    # tokenize the words from definition
    glossary.append(word_tokenize(definition))
    for example in examples:

        # consider every example and tokenize the words to add to the glossary
        glossary.append(word_tokenize(example))

    # combine the list of lists to form one
    merged = list(itertools.chain(*glossary))
    return merged


# Compute the overlap between words from the retrieved glossary and the input sentence
# @param:   glossary - The set of tokens for a sense from word net
#           sentence - The set of tokens of input sentence
# @return:  overlap_count - The total number of words that match in glossary and sentence
#           overlap_words - The words that have matched between glossary and sentence
def compute_overlap(glossary, sentence):

    # perform intersection on the sets of glossary and sentence
    overlap_count = len(set(glossary).intersection(set(sentence)))
    overlap_words = set(glossary).intersection(sentence)
    return overlap_count, overlap_words


# The simplified Lesk algorithm
# @param:   word - The input word whose sense is to be determined
#           sentence - The input sentence which should have the input word
# @return:  best_sense - The sense that is most likely for the given word in context of the given sentence
def simplified_lesk(word, sentence):

    # retrieve the senses for word from word net
    senses = wn.synsets(word)
    best_sense = senses[0]
    max_overlap = 0

    # tokenize the input sentence
    context = word_tokenize(sentence)
    print "\n"
    for i in range(0, len(senses)):

        # method call to get the glossary of the senses from the syn sets
        signature = get_glossary(senses[i].name())

        #  method call to compute the overlaps from the glossary and sentence
        overlap_count, overlap_words = compute_overlap(signature, context)

        # print the sense, the words that overlap, and the total count of overlaps
        print (senses[i].name(), overlap_words, overlap_count)

        # set the max_overlap to determine in choosing of the best possible sense
        if overlap_count > max_overlap:
            max_overlap = overlap_count
            best_sense = senses[i]

    return best_sense


if __name__ == "__main__":
    input_sentence = "The bank can guarantee deposits will eventually cover future tuition costs " \
                     "because it invests in adjustable-rate mortgage securities."
    word_sense = "bank"
    lesk = simplified_lesk(word_sense, input_sentence)
    print("\nFinal best sense calculated: ")
    print ("Sense: " + lesk.name())
