# app.py
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from phonetics import text_to_ipa  # Import the text_to_ipa function
import nltk
from nltk.corpus import wordnet

app = Flask(__name__)

def get_dictionary_results(word):
    url = 'https://dictionary.cambridge.org/dictionary/english/' + word
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        return None, str(e)

    html = r.text
    soup = BeautifulSoup(html, 'html.parser')

    wd = soup.find('div', class_="di-title")
    if wd is None:
        suggestion_elements = soup.select('.suggestions-list .suggestion-link')
        suggested_words = [suggestion.text.strip() for suggestion in suggestion_elements]
        if suggested_words:
            return None, f"No results found for '{word}'. Did you mean: {', '.join(suggested_words)}?"
        return None, f"No results found for '{word}'."

    part_of_speech = soup.find('div', class_="posgram dpos-g hdib lmr-5")
    meanings = soup.find_all('div', class_='ddef_h')

    word_result = {
        'word': wd.text.strip(),
        'part_of_speech': part_of_speech.text.strip(),
        'meanings': [meaning.text.strip() for meaning in meanings]
    }

    return word_result, None

def get_synonyms(word):
    synonyms = []
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            synonyms.append(lemma.name())
    return list(set(synonyms))

def get_antonyms(word):
    antonyms = []
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            if lemma.antonyms():
                antonyms.append(lemma.antonyms()[0].name())
    return list(set(antonyms))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    word = request.form['word']
    result, error = get_dictionary_results(word)

    if error:
        return render_template('index.html', error=error)

    if result is None:
        return render_template('index.html', suggestion=error)

    synonyms = get_synonyms(word)
    antonyms = get_antonyms(word)

    # Add IPA transcription to the result
    ipa_transcription = text_to_ipa(word)

    return render_template('result.html', result=result, word=word, synonyms=synonyms, antonyms=antonyms, ipa_transcription=ipa_transcription)

if __name__ == '__main__':
    app.run(debug=True)
