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

#   apiKey: "AIzaSyAVscr9cvbOXD-AtB4vt9tzwBDjj0v7e48",
#   authDomain: "python-rpg-mirumee-starter.firebaseapp.com",
#   databaseURL: "https://python-rpg-mirumee-starter-default-rtdb.europe-west1.firebasedatabase.app",
#   projectId: "python-rpg-mirumee-starter",
#   storageBucket: "python-rpg-mirumee-starter.appspot.com",
#   messagingSenderId: "644731220342",
#   appId: "1:644731220342:web:53b89284341b8d10a50a57"
