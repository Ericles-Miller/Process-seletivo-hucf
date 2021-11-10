from flask import Flask, blueprints 
from flask import render_template, blueprints,url_for,redirect
from flask.globals import request
from authlib.integrations.flask_client import OAuth
from auth import login, signup
from data_firebase import create_database,manda_gravar
#from config import oauth


app = Flask(__name__)
app.secret_key = 'adlo895020'
debug=True

#area reservada para config de authenticacao google facebook e twitter
oauth = OAuth(app)

app.config['SECRET_KEY']             = "adlo895020"
app.config['GOOGLE_CLIENT_ID']       = "<your google client id>"
app.config['GOOGLE_CLIENT_SECRET']   = "<your google client secret>"
app.config['TWITTER_CLIENT_ID']      = "<your twitter client id>"
app.config['TWITTER_CLIENT_SECRET']  = "<your twitter client secret>"
app.config['FACEBOOK_CLIENT_ID']     = "<your facebook client id>"
app.config['FACEBOOK_CLIENT_SECRET'] = "<your facebook client secret>"


#login google 
google = oauth.register(
    name               = 'google',
    client_id          = app.config["GOOGLE_CLIENT_ID"],
    client_secret      = app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url   = 'https://accounts.google.com/o/oauth2/token',
    access_token_params= None,
    authorize_url      = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params   = None,
    api_base_url       = 'https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint  = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs      = {'scope': 'openid email profile'},
)

#login twitter
twitter = oauth.register(
    name                =  'twitter',
    client_id           =  app.config['TWITTER_CLIENT_ID'],
    client_secret       =  app.config['TWITTER_CLIENT_SECRET'],
    request_token_url   =  None,
    request_token_params=  {'scope': 'email'},
    access_token_url    =  '/oauth/access_token',
    access_token_params =  None,
    authorize_url       =  'https://www.facebook.com/dialog/oauth',
    authorize_params    =  None,
    api_base_url        =  'https://api.twitter.com/1.1/',
    client_kwargs       =  None,
)


#login facebook 
facebook = oauth.register(
    name                = 'facebook',
    client_id           = app.config['FACEBOOK_CLIENT_ID'],
    client_secret       = app.config['FACEBOOK_CLIENT_SECRET'],
    request_token_url   = 'https://api.twitter.com/oauth/request_token',
    request_token_params= None,
    access_token_url    = 'https://api.twitter.com/oauth/access_token',
    access_token_params = None,
    authorize_url       = 'https://api.twitter.com/oauth/authenticate',
    authorize_params    = None,
    api_base_url        = 'https://api.twitter.com/1.1/',
    client_kwargs       = None,
)

#Rotas para acessar pags da API flask e python e firebase 

#rotas pertencentes ao menu
#pag inicial pertencente ao usuario
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST']) 
def index_post():
    email    = request.form.get('Email')
    password = request.form.get('pass')
    
    print(email, password)
    #fazer uma funcao que detecte se o email foi ou nao cadastrado 
    #chamo a funcao que grava o login atraves do emial comum
    #esse dado sera salvo via firebase
    login(email,password)

    #lembrando que tenho que retornar a pag que entrara diante do login 
    return 'foii '
    #return  redirect(url_for('nome_pag'))


#pag editais 
@app.route('/editais')
def editais():
    #return 'editais'
    return render_template('editais.html')


#rourte pertencente aos funcionarios que avaliaram os candidatos
@app.route('/institucional')
def institucional():
    return render_template('institucional.html')

@app.route('/institucional', methods=['POST'])
def institucional_post():
    email    = request.form.get('Email')
    password = request.form.get('pass')
    
    print(email,password)
    #fazer uma funcao de detectar email institucional 
    #fazer uma funcao que detecte se o email foi cadastrado
    
    

@app.route('/formulario')
def formulario():
    return render_template('form_cad.html')

@app.route('/formulario', methods=['POST'])
def formulario_post():
    database_users = list()
    data = dict()
    data['nome']          = request.form.get('Nome')
    data['cpf ']          = request.form.get('cpf')
    data['dt_nascimento'] = request.form.get('dtnasc')
    data['sexo']          = request.form.get('sexo')
    data['telefone_obr']  = request.form.get('tel1')
    data['telefone']      = request.form.get('tel2')
    data['email']         = request.form.get('email')
    data['cep']           = request.form.get('cep')
    data['rua']           = request.form.get('rua')
    data['numero']        = request.form.get('numero')
    data['bairro']        = request.form.get('bairro')
    data['cidade']        = request.form.get('cidade')
    data['estado']        = request.form.get('estado')
    data['filhos']        = request.form.get('filhos')
    data['qtd_filhos']    = request.form.get('filhos_qtd')
    data['hora_aula ']    = request.form.get('hora_aula')
    data['profissao ']    = request.form.get('profissao')
    #data['enc']           = request.form.get('enc')   #mudar o nome nesse campo
    data['aluno']         = request.form.get('aluno')
    data['curso']         = request.form.get('curso')
    data['desc']          = request.form.get('textinput')
    #data['historico']     = request.files.get('historico_escolar')
    arquivo = request.files.get('historico_escolar')
    print(type(arquivo))
    #salvo na lista com cada indice
    database_users.append(data)
    
    print(database_users)
    #chamo a funcao de mandar dados para o firebase
    manda_gravar(database_users)
    #create_database(data)

    return 'dados salvos com sucesso!'
#rotas do google ------------------------------

# Google login route
@app.route('/login/google')
def google_login():
    google       = oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


# Google authorize route
@app.route('/login/google/authorize')
def google_authorize():
    google = oauth.create_client('google')
    token  = google.authorize_access_token()
    resp   = google.get('userinfo').json()
    print(f"\n{resp}\n")
    return "You are successfully signed in using google"


#rotas do twitter  --------------------------

#twitter login toute 
@app.route('/login/twitter')
def twitter_login():
    twitter      = oauth.create_client('twitter')
    redirect_uri = 'https://example.com/authorize'
    return twitter.authorize_redirect(request, redirect_uri)

#twitter authorize route
@app.route('/login/twitter/authorize')
def twitter_authorize():
    twitter  = oauth.create_client('twitter')
    token    = twitter.authorize_access_token(request)
    resp     = twitter.get('account/verify_credentials.json')
    resp.raise_for_status()
    profile  = resp.json()   #alterar essa linha depois 
    # do something with the token and profile
    return 'You are successfully signed in using twitter'


#rotas do facebook --------------------------


#facebook login route 
@app.route('/login/facebook/')
def facebook_login():
    facebook     = oauth.create_client('facebook')
    redirect_uri = url_for('facebook_authorize', _external = True)
    return facebook.authorize_redirect(redirect_uri)

#facebook authorize route
@app.route('/login/facebook/authorize')
def facebook_authorize():
    facebook = oauth.create_client('facebook')
    token    = facebook.authoruze_access_token()
    resp     = facebook.get('userinfo').json()
    print(f'\n{resp}\n')
    return "You are successfully signed in using facebook"
    



if __name__ == '__main__':
    app.run()
    
