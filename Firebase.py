import pyrebase

config = {
    "apiKey": "AIzaSyAVscr9cvbOXD-AtB4vt9tzwBDjj0v7e48",
    "authDomain": "python-rpg-mirumee-starter.firebaseapp.com",
    "databaseURL": "https://python-rpg-mirumee-starter-default-rtdb.europe-west1.firebasedatabase.app/",
    "storageBucket": "python-rpg-mirumee-starter.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()
