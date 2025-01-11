import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyB9gewo5hZO4JBRMmVIxw4cjS7gBwkg124",
  "authDomain": "fbla2025-cf1b8.firebaseapp.com",
  "projectId": "fbla2025-cf1b8",
  "storageBucket": "fbla2025-cf1b8.firebasestorage.app",
  "messagingSenderId": "305951395537",
  "appId": "1:305951395537:web:b6e250c6e147e04d047ff0"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
auth = firebase.auth()