import pyrebase as pb , json, os
from config import firebase_function

# -- variaveis globais de aplicacao 

diretorio = 'C:\\Users\\server\\Desktop\\proj_seletivo'

def download_pdf(lista):
    # -- salvando pdf no diretorio
    arquivo = lista[0]['historico']
    print(arquivo)
    nome_arq_pdf = arquivo.filename
    arquivo.save(os.path.join(diretorio,nome_arq_pdf))
    
    return nome_arq_pdf


def create_database(lista):
    #chamo a funcao que comunica com o firebase 
    firebase = firebase_function()

    #-- chamo a funcao de firebase que conecta com storage
    storage = firebase.storage()
    
    # -- inicializo comandos para upload dos dados para o firebase
    path_on_cloud = 'candidato/{}/lista/candidatos.json'.format(lista[0]['nome']) # -- defino o nome da pasta 
    path_local    = 'lista_candidatos.json'
    # -- realizando upload
    storage.child(path_on_cloud).put(path_local)
    
    # -- funcao download pdf 
    
    nome_arq_pdf = download_pdf(lista)
    
    # -- enviando dado pdf
    storage2 = firebase.storage()
    path_on_cloud_2 = 'candidato/{}/pdfs/arq.pdf'.format(lista[0]['nome']) # -- defino o nome da pasta 
    path_local2     = nome_arq_pdf # -- verificar se o esse paramentro funciona   
    # -- realizando upload
    storage2.child(path_on_cloud_2).put(path_local2)
    
    
    #db.child("Users").child(lista[0]['nome']).set(nome_arq)

def manda_gravar(lista):
    print(lista)
    arquivo = 'lista_candidatos.json'
    grava_em_arquivo(arquivo,lista)


def grava_em_arquivo(nome_arq,lista):
    with open(nome_arq, 'w', encoding='utf8') as f:
        json.dump(lista,f,ensure_ascii=False,sort_keys=True ,indent=4, separators=(',', ':'))
    create_database(lista)