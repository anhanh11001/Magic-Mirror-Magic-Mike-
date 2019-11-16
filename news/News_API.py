import requests
import json

class News:
    def __init__(self):
        #self.dummyData = dummyData
        self.news = []
        API_key = 'b735516e12d7494ead5916850f4a6851'
        response = requests.get('https://newsapi.org/v2/top-headlines?country=nl&apiKey=' + API_key)
        geladen = response.json()['articles']

        for d in geladen:
                article = []
                title = d['title']
                description = d['description']
                url = d['url']
                article.append(title)
                article.append(description)
                #article.append(url)
                self.news.append(article)

    def get_news(self):
            return self.news

if __name__ == '__main__':
    print(News().get_news())
