import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("/firebase.json")
firebase_admin.initialize_app(cred)

dbRef = db.reference("/")