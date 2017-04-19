import requests
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import html5lib
import pprint
from bottle import route, run, template, request
from bottle import redirect
from sqlalchemy.ext.declarative import declarative_base
import nltk
import pickle
from collections import defaultdict
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from math import log

Base = declarative_base()

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key = True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

def get_news(query):
    page = BeautifulSoup(query, 'html5lib')
    news_table = page.find('table', class_='itemlist')
    links_list = news_table.find_all('a', class_='storylink')
    info_list = news_table.find_all('td', class_='subtext')
    news_list = []
    for link, info in zip(links_list, info_list):
        author = info.find('a', class_='hnuser').text
        comments = info.find_all('a')
        comments = comments[-1].text
        if comments == 'discuss':
            comments = 0
        else:
            comments = int(comments.replace('comment', '').replace('s', ''))
        points = info.find('span', class_='score').text
        points = int(points.replace('point', '').replace('s', ''))
        title = link.text
        # title = title.replace('\u2013', '-').replace('\u2019', "'")
        # title = title.replace('\u201c', '"').replace('\u201d', '"')
        url = link['href']
        article = dict(title=title, author=author, \
            points=points, comments=comments, url=url)
        news_list.append(article)
    return news_list


@route('/')
@route('/news')
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    fl = open('dicslabel.py', 'rb')
    data_label = pickle.load(fl)
    fw = open('dicsword.py', 'rb')
    data_word = pickle.load(fw)
    fa = open('dicsauthor.py', 'rb')
    data_author = pickle.load(fa)
    fu = open('dicsurl.py', 'rb')
    data_url = pickle.load(fu)
    new_rows = []
    k = 0.000000001
    for r in rows:
        freq = defaultdict(int, {'good': 0, 'maybe': 0, 'never': 0})
        author = r.author
        url = r.url
        title_split = r.title.split()
        for word in title_split:
            word = word.strip().lower()
            if word not in stw:
                freq['never'] += log(data_word[word, 'never'] + k)
                freq['maybe'] += log(data_word[word, 'maybe'] + k)
                freq['good'] += log(data_word[word, 'good'] + k)
        freq['never'] += log(data_author[author, 'never'] + k)
        freq['maybe'] += log(data_author[author, 'maybe'] + k)
        freq['good'] += log(data_author[author, 'good'] + k)
        freq['never'] += log(data_url[url, 'never'] + k)
        freq['maybe'] += log(data_url[url, 'maybe'] + k)
        freq['good'] += log(data_url[url, 'good'] + k)
        probability = max(data_label.keys(), key = lambda label: (log(data_label[label]) + freq[label]))
        if probability == 'good':
            color = '#adff2f'
        else:
            if probability == 'maybe':
                color = '#81B8D9'
            else:
                color = '#929BAA'
        new_rows.append((probability, color, r))
    new_rows.sort(key=lambda i: i[0])
    fl.close()
    fw.close()
    fa.close()
    fu.close()
    return template('news_template', rows=new_rows)

@route('/add_label/', method='GET') 
def add_label(): 
    label = request.GET.get('label').strip() 
    idd = request.GET.get('id').strip()
    s = session()
    record = s.query(News).filter(News.id == idd)
    rec = record[0]
    rec.label = label
    s.commit()
    redirect('/news')

@route('/update_news')
def update_news():
    r = requests.get("https://news.ycombinator.com/newest")
    news_list = get_news(r.text)
    s = session()
    for n in news_list:
        rows = s.query(News).filter(News.author == n['author']).filter(News.title == n['title']).all()
        if rows == []:
            news = News(**n)
            s.add(news)
            s.commit()
    redirect('/news')

if __name__ == "__main__":
    stw = set(stopwords.words('english'))
    st = LancasterStemmer()
    '''prob_labels = {'good': 0, 'maybe': 0, 'never': 0}
    prob_words_labels = prob_urls_labels = prob_authors_labels = defaultdict(int)
    count_authors = count_words = count_urls = defaultdict(int)
    news_for_class = s.query(News).filter(News.label != None).all()
    for n in news_for_class:
        label = n.label
        author = n.author
        url = n.url
        prob_labels[label] += 1
        title_split = n.title.split()
        for word in title_split:
            if word not in stw:
                word = st.stem(word)
                word = word.strip().lower()
                count_words[word] += 1
                prob_words_labels[word, label] += 1
        count_authors[author] += 1
        prob_authors_labels[author, label] += 1
        count_urls[url] += 1
        prob_urls_labels[url, label] += 1     
    for label in prob_labels:
        prob_labels[label] /= len(news_for_class)
    for word, label in prob_words_labels:
        prob_words_labels[word, label] /= count_words[word]
    for author, label in prob_authors_labels:
        prob_authors_labels[author, label] /= count_authors[author]
    for url, label in prob_urls_labels:
        prob_urls_labels[url, label] /= count_urls[url]

    fl = open('dicslabel.py', 'wb')
    pickle.dump(prob_labels, fl)
    fl.close()
    fw = open('dicsword.py', 'wb')
    pickle.dump(prob_words_labels, fw)
    fw.close()
    fa = open('dicsauthor.py', 'wb')
    pickle.dump(prob_authors_labels, fa)
    fa.close()
    fu = open('dicsurl.py', 'wb')
    pickle.dump(prob_urls_labels, fu)
    fu.close()'''
    r = requests.get("https://news.ycombinator.com/newest")
    news_list = get_news(r.text)
    engine = create_engine("sqlite:///news.db")
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)
    s = session()
    '''for n in news_list:
    news = News(title=n['title'], author=n['author'], url=n['url'], comments=n['comments'], points=n['points'])
    s.add(news)
    s.commit()'''
    
    run(host='localhost', port=8080)
