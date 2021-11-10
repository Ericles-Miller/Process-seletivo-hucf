from flask import render_template, Blueprint, url_for, request, redirect
'''auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
    return "pagina que render login de authentication"

@auth.route('/login')
def login():
    return 'tora destinada a pagina de login do user'''


#function referente a mandar dados para o firebase
from pyrebase import pyrebase as pb
from config import firebase_function

#esta funcionando com o envio para o email. nao apague 
def signup(email,password):
    auth = firebase_function()
    
    #criando o comando para passar o email e a senha pra o firebase
    try:
        user = auth.create_user_with_email_and_password(email,password)
        #mandar emial de confirmacao de conta 
        
    except:
        print('\nEmail ja cadastrodo!\n Tente outro email ou entre em contato com servidor')
        #tenho que criar uma forma de renderizar uima pag com um alert dizendo que a conta ja existe
        
    
    #user = auth.create_user_with_
    print('Dados cadastrados com sucesso!')

def login(email,password):
    auth = firebase_function() 
    
    #criando excecao caso a senha do usuario esteja errada 
    try:
        login = auth.sign_with_email_and_password(email,password)
        print("sucess logged!") 
        return 1
    except:
        print('Invalid email or password!')
        #criar uma funcao que renderize e mostre que a senha esta errada
        return 0
        

