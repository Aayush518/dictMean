import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import time

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
    part_of_speech = soup.find('div', class_="posgram dpos-g hdib lmr-5")
    meanings = soup.find_all('div', class_='ddef_h')

    word_result = {
        'word': wd.text.strip(),
        'part_of_speech': part_of_speech.text.strip(),
        'meanings': [meaning.text.strip() for meaning in meanings]
    }

    return word_result, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    word = request.form['word']
    result, error = get_dictionary_results(word)

    if error:
        return render_template('index.html', error=error)

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
