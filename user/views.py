from django.shortcuts import render, redirect
import pyrebase
from .models import Contactus
import requests
import json
from firebase_admin import credentials,firestore, messaging
import firebase_admin



cred = credentials.Certificate("./star.json")
app = firebase_admin.initialize_app(cred)
store = firestore.client()
query = store.collection(u'users').where(u'userAuthId', u'==','rish1234')
doc_ref = query.stream()
currUser = 0

docId = ""
docToken = ""
for doc in doc_ref:
    print(doc)
    currUser = doc
    docId = doc.id
    data = doc.to_dict()
    docToken = data['userToken']
    print(data['userName'])




url = 'http://127.0.0.1:5000/files'

firebaseConfig = {
    'apiKey': "AIzaSyBc9d3c5edVlscSWzrTnMW54gI6qlI_oYA",
    'authDomain': "star-bugs.firebaseapp.com",
    'databaseURL': "https://star-bugs.firebaseio.com",
    'projectId': "star-bugs",
    'storageBucket': "star-bugs.appspot.com",
    'messagingSenderId': "450899693729",
    'appId': "1:450899693729:web:24eeb110b85b1ceaede0e0",
    'measurementId': "G-NE8B9E9EDC"
}
firebase = pyrebase.initialize_app(firebaseConfig)

authe = firebase.auth()


def index(request):
    if request.method == 'POST':
        your_name = request.POST['your_name']
        your_email = request.POST['your_email']
        your_message = request.POST['your_message']

        contact = Contactus(your_name= your_name, your_email=your_email, your_message= your_message)
        contact.save()
        return render(request,'index.html', {'message':'Your response has been recorded'})
    else:
        return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = authe.sign_in_with_email_and_password(email, password)
            session_id = user['idToken']
            request.session['uid'] = str(session_id)
            return redirect('profile')


        except:
            message = 'Invalid login details'
            context = {
                'message': message
            }
            return render(request, 'login.html', context)


    else:
        return render(request, 'login.html')


def profile(request):
    try:

        data=[]
        time = []
        url_route =[]
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        b = a.get('users')

        response = requests.get(url)
        json_response = response.json()

        l = len(json_response)


        cols = store.collection(u'users').document(docId).collection(u'notifications').stream()


        for doc in cols:

            data.append(doc.to_dict())

        for i in data:
            st='%.2s' % i.get('eventStartTime')
            et = '%.2s' % i.get('eventEndTime')
            time.append(st+'sec - '+et+'sec')
            loc = i.get('eventGifUrl')
            loca = loc.replace('http://192.168.137.1:5000','http://127.0.0.1:5000')
            url_route.append(loca)


        print(url_route)



        return render(request, 'profile.html',{'gif':url_route,'loacation':'ABESIT College of Engineering','length':l,'time':time})
    except KeyError:
        message = 'you must login first'
        return render(request,'login.html',{'message':message})



def history(request):
    try:
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        return render(request, 'history.html')
    except KeyError:
        message = 'you must login first'
        return render(request,'login.html',{'message':message})


def signout(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
    return redirect('login')

