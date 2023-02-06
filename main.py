import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import jsonify

app = Flask(__name__)


@app.route('/ping', methods=['GET', 'POST'])
def parse_news(link):
    print(f"https://rusdisinfo.voxukraine.org{link}")
    resp = requests.get(f"https://rusdisinfo.voxukraine.org{link}")
    if resp.status_code == 200:
        sp = BeautifulSoup(resp.content, "lxml")
        narratives_links = [i.text for i in sp.find_all("h3", class_="Narrative_fakeLink___YbTe")]
        countries = [i.text for i in sp.find_all("div", class_="Narrative_country__RtYzo")]
        media = [i.text for i in sp.find_all("div", class_="Narrative_media__B2gNZ  ")]
        return narratives_links, countries, media


@app.route('/', methods=['GET', 'POST'])
def parser():
    url = "https://rusdisinfo.voxukraine.org/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "lxml")
        home_container = soup.find("div", class_="Home_container__bCOhY").find_all("a")
        data = list()
        narratives = [i.text for i in home_container]
        for i in home_container:
            data += parse_news(i.get("href"))
        return narratives, data


app.run(host='0.0.0.0', port=5001)
