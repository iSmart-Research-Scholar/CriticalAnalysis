from django.shortcuts import render
import requests
from CriticalAnalysis import CriticalAnalysis
from django.http import HttpResponse, JsonResponse
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

# Create your views here.

def HomeRoute(request):
    query = request.GET['query']
    tokens = query.split(" ")
    tokenString = '+'.join(tokens)
    URL = "https://api.semanticscholar.org/graph/v1/paper/search?query=" + tokenString + "&offset=30&limit=30&fields=title,abstract,url"
    papers = ((requests.get(url = URL )).json()['data'])
    scores = CriticalAnalysis.CriticalAnalysis.Score(papers)
    topParams = scores['queryparams']
    papersAre = []
    for paperindex, paper in enumerate(papers):
        url = paper["url"]
        title = paper["title"]
        print(title)
        values = [0]*10
        if paper["abstract"] != None:
            word_tokens = paper["abstract"].split(' ')
            stop_words = set(stopwords.words('english'))
            filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
            text = ' '.join(filtered_sentence)
            text = text.lower()
            text = text.replace('-', '')
            text = text.replace('.', '')
            text = text.replace(',', '')
            for index, param in enumerate(topParams):
                if param in text:
                    values[index] = 1
                if param in title:
                    values[index] = 1
            if paperindex == 0:
                print(title)
                print(topParams)
        papersAre.append({"url": url, "title": title, "values": values})
    return JsonResponse({"params": topParams, "papers": papersAre})
    
    