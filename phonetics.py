# phonetics.py
import nltk
from nltk.corpus import cmudict

nltk.download('cmudict')

def text_to_ipa(text):
    words = nltk.word_tokenize(text.lower())
    pronunciation_dict = cmudict.dict()

    ipa_transcription = []
    for word in words:
        if word in pronunciation_dict:
            ipa_transcription.append(' '.join(pronunciation_dict[word][0]))
        else:
            ipa_transcription.append(word)

    return ' '.join(ipa_transcription)
