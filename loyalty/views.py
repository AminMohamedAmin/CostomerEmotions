from django.shortcuts import render, HttpResponse
from django.contrib import messages

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions, SentimentOptions

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

from .models import Files
from .forms import file_form
import os
from django.conf import settings

# Create your views here.
def home(request):
    try:
        authenticator = IAMAuthenticator('-GEDGacgnI36ctk77Aa4X5k3PAXBA_AaRQIxp6G71sOP')
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2019-07-12',
            authenticator=authenticator
        )
        natural_language_understanding.set_service_url(
            'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/b61e5fb9-726b-4cba-8b4b-12f1403ed4a1')

        # ii = "Hello, I'm having a problem with your service. Nothing is working well. The service here is very bad. I am really very upset. I was expecting better than that. And my service has been stopped since yesterday. I have been suffering from this problem for a long time and cannot find a solution. The service here is bad most of times. Why you do not solve these problems. Some had left your service for this reason. The network is weak all the time, and it stops at the call. why this happen!? I wait. I'm fed up with complaining from the service."
        # ii = "Hello, I need some help. I've subscribed to some news services and want to cancel them.They were not helpful with me plus they used a lot of balance. I feel bad because I used this service. Please remove it and try to improve these services. It has more harm than good. I hope to improve some services and offer some offers soon. I have another problem. My service has been disabled since yesterday. I have been suffering from this problem for a different times and cannot find a solution. It affects my work and communication in some important times."
        ii = request.POST['text']
        response1 = natural_language_understanding.analyze(
            text=ii,
            features=Features(emotion=EmotionOptions(targets=[ii.split()[1]]))).get_result()

        response2 = natural_language_understanding.analyze(
            text=ii,
            features=Features(sentiment=SentimentOptions(targets=[ii.split()[1]]))).get_result()
        global sad, joy, fear, disgust, anger, sentiment_label, sentiment
        sad = response1['emotion']['document']['emotion']['sadness']
        joy = response1['emotion']['document']['emotion']['joy']
        fear = response1['emotion']['document']['emotion']['fear']
        disgust = response1['emotion']['document']['emotion']['disgust']
        anger = response1['emotion']['document']['emotion']['anger']
        sentiment_label = response2['sentiment']['document']['label']
        sentiment = response2['sentiment']['document']['score']

        ####################################################################

        data = pd.read_csv("/Users/Ameen/Desktop/CV-projects/emotions/emotions/loyalty/dataset/final_dataset.csv")
        X_train, X_test, y_train, y_test = train_test_split(data[["sadness", "joy", "fear", "disgust", 'anger', 'score']],
                                                            data["label_state"], test_size=0.4)
        lsvm = LinearSVC()
        prid = lsvm.fit(X_train, y_train)
        accuracy = lsvm.score((X_test), y_test)
        # print(accuracy)
        out = lsvm.predict((X_test))
        from sklearn.metrics import classification_report
        # print(classification_report(out, y_test))
        lls = [sad, joy, fear, disgust, anger, sentiment]
        predict = lsvm.predict([lls])
        ss = predict
        if predict == [0]:
            predict = "leave"
        else:
            predict = "stay"

        form = file_form()
        context= {
            'sad':sad,
            'joy': joy,
            'fear': fear,
            'disgust': disgust,
            'anger': anger,
            'sentiment_label': sentiment_label,
            'sentiment': sentiment,
            'predict':predict,
            'form': form
        }
        return render(request, 'temp.html', context)
    except Exception as e:
        form = file_form()
        messages.error(request, e, extra_tags='error')
        return render(request, 'temp.html', {'form': form})

def temp(request):
    try:
        form = file_form()
        return render(request, 'temp.html', {'form': form})
    except Exception as e:
        form = file_form()
        messages.error(request, e, extra_tags='error')
        return render(request, 'temp.html', {'form': form})

def extract(request):
    try:
        ex = Files()
        form = file_form(request.POST, request.FILES)
        if form.is_valid():
            ex.file = form.cleaned_data['file']
            ex.save()
            e = ex.file.name
            p = 'media' + '/' + str(e)
            f = open(os.path.join(settings.BASE_DIR, p))
            data = f.read()
            ex.delete()
            return render(request, 'temp.html', {'data':data, 'form': form,})
        return render(request, 'temp.html', {'form': form})
    except Exception as e:
        form = file_form()
        messages.error(request, e, extra_tags='error')
        return render(request, 'temp.html', {'form': form})