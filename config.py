import pyrebase as pb

#area reservada para config firebase
def firebase_function():
  firebaseConfig = {
    'apiKey'           : "AIzaSyDYlqHS3MamsIsfmdai9LbkVDwdfBpe-f4",
    'authDomain'       : "processo-seletivo-estagiario.firebaseapp.com",
    'projectId'        : "processo-seletivo-estagiario",
    'databaseURL'      : 'https://processo-seletivo-estagiario-default-rtdb.firebaseio.com/',
    'storageBucket'    : "processo-seletivo-estagiario.appspot.com",
    'messagingSenderId': "379647248745", 
    'appId'            : "1:379647248745:web:e7c7c68d949494e7b995f8",
    'measurementId'    : "G-HT16M6NT0Y",
    'serviceAccount'   : 'serviceAccountKey.json'
  }  
  firebase = pb.initialize_app(firebaseConfig)
  
  #db = firebase.database()
  
  return firebase #verificar


