from flask import render_template, request, url_for, redirect
from flask_login import login_user, logout_user, current_user
import werkzeug.exceptions
from app import app, lm, db
from app.models import User, Friend
from app.forms import LoginForm, RegisterForm, FriendForm
import json


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('register'))
    #Declaram forma pentru inregistrare
    msg = None
    form = RegisterForm(request.form)
    if request.method == 'GET':
        return render_template('layouts/default.html', content=render_template( 'pages/register.html', form=form, msg=msg ) )

    msg = 'V-ati inregistrat cu succes'
    # Verificam daca forma este valida
    if form.validate_on_submit():
        #Asignam forma datelor variabile
        name = request.form.get('name', '', type=str)
        lastn = request.form.get('lastn', '', type=str)
        username = request.form.get('username', '', type=str)
        email = request.form.get('email', '', type=str)
        password = request.form.get('password', '', type=str)
        #users = User.query.all()
        #server = Server.query.all()
        user1_mail = User.query.filter_by(email=email).first()
        user1_username = User.query.filter_by(username=username).first()
        #user1_passw = User.query.filter_by(password=password).first()
        if user1_mail:
            msg = 'Email-ul este ocupat, incercati din nou'
        if user1_username:
            msg = 'Numele de utilizator este ocupat, incercati din nou'

        pw_hash = password
        user = User(name, lastn, username, email, pw_hash)
        user.save()
    else:
        msg = 'Parola slaba. Introduceti o parola mai lunga (min. 6)'
    return render_template('layouts/default.html', content=render_template( 'pages/register.html', form=form, msg=msg) )

#ruta principala
@app.route('/', defaults={'path': 'user.html'}, methods=['GET', 'POST'])
@app.route('/<path>')
def userprofile(path):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    msg=None
    form = FriendForm(request.form)
    user = User.query.all()
    server = Friend.query.all()
    if request.method == 'GET':
        return render_template('layouts/default.html', content=render_template('pages/'+path, server=server, user=user, form=form, msg=msg))
    if form.validate_on_submit:
        try:
            username_friend = request.form.get('username_friend', '', type=str)
            username_fk = request.form.get('username_fk', '', type=str)
            server1 = Friend(username_friend, username_fk)
            server1.save1()

            userfr_nume = Friend.query.filter_by(username_friend=username_friend).first()

            if userfr_nume:
                if userfr_nume.username_friend == username_friend:
                    msg = "Numele pentru server este deja ocupat. Va rugam sa introduceti altul."

        except Exception:
            return render_template('layouts/default.html', content=render_template('pages/'+path, server=server, user=user, form=form, msg=msg))

    return render_template('layouts/default.html', content=render_template('pages/'+path, server=server, user=user, form=form, msg=msg))

@app.route('/home.html', methods=['GET', 'POST'])
def home():
    form = FriendForm(request.form)
    user = User.query.all() #se selecteaza toate datele despre utilizator
    server = Friend.query.all() #toate datele despre server, din baza
    msg = None
    if request.method == 'GET':
        return render_template('layouts/default.html', content=render_template('pages/home.html', server=server, user=user, form=form, msg=msg))
    if form.validate_on_submit:
        try:
            name_serv = request.form.get('name_serv', '', type=str)
            ip_serv = request.form.get('ip_serv', '', type=str)
            port_serv = request.form.get('port_serv', '', type=str)
            username_fk = request.form.get('username_fk', '', type=str)
        except Exception:
            return render_template('layouts/auth-default.html', content=render_template('pages/404.html'))
    return render_template('layouts/default.html', content=render_template('pages/home.html', server=server, user=user, form=form, msg=msg))

# Autentificare
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm(request.form)
    # Mesaje in cazuri de eroare
    msg = None
    # Verificam daca POST si forma sunt valide la submitere
    if request.method == 'GET':
        return render_template('layouts/default.html', content=render_template('pages/login.html', form=form, msg=msg))
    if form.validate_on_submit():
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str)
        user = User.query.filter_by(username=username).first() #preluam user-ul dupa username-ul sau
        if user:
            if user.password == password:
                login_user(user)
                return redirect(url_for('home'))
            else:
                msg = 'Parola gresita. Incercati din nou.'
        else:
            msg = "Nume de utilizator necunoscut. Va rugam sa incercati din nou sau sa va inregistrati."
    return render_template('layouts/default.html', content=render_template('pages/login.html', form=form, msg=msg, password=password)) #default distribuie roluri la pagini

@app.route('/server/check_selected', methods=['GET','POST']) #connect=False in html
def check_selected():
    global selected
    post = request.args.get('post', 0, type=int)
    return json.dumps({'selected post': str(post)});

@app.route('/server', methods=['GET', 'POST'])
def servere():
    global connected
    global inform
    global checkNotif
    if(connected==False):
        connected = True
    form = RegisterForm(request.form)
    if form.validate_on_submit:
        email = request.form.get('email', '', type=str)
    checkNotif = request.form.get('decizie')
    if request.form.get('decizie') != None:
        checkNotif = 1
    inform.request(email, checkNotif)
    server_name = request.args.get('name_svr')
    cpuTemp,memoryTemp,memoryUsage,fanSpeed,networkSpeedUpload,networkSpeedDownload,cpuAvgUsage = inform.getDataRepeat()
    memory, network, diskInfo, diskFreeSpace = inform.getDataOnce()
    check_selected()
    return render_template('layouts/default.html',
                           content=render_template('pages/home.html', cpuTemp=cpuTemp, memoryTemp=memoryTemp,
                                                   memoryUsage=memoryUsage, fanSpeed=fanSpeed,
                                                   networkSpeedUpload=networkSpeedUpload,
                                                   networkSpeedDownload=networkSpeedDownload,
                                                   cpuAvgUsage=cpuAvgUsage, memory=memory, network=network,
                                                   diskInfo=diskInfo, diskFreeSpace=diskFreeSpace,
                                                   server_name=server_name, connected=connected))


@app.route("/sters", methods=["POST"])
def delete():
    username_friend = request.form.get("username_friend")
    servdel = Friend.query.filter_by(username_friend=username_friend).first()
    db.session.delete(servdel)
    db.session.commit()
    return render_template('layouts/default.html', content=render_template('pages/home.html'))

@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_bad_request(e):
    return 'Ruta nu a putut fi gasita!', 404