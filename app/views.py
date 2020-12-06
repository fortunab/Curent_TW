from datetime import datetime

from flask import render_template, request, url_for, redirect, g, abort, jsonify, send_from_directory, send_file
from flask_login import login_user, logout_user, current_user
import werkzeug.exceptions
from app import app, lm, db
from app.models import User, Friend, Chat, Message, FileContinut
from app.forms import LoginForm, RegisterForm, FriendForm, ConnectChatForm, MessageForm
import json

from flask_socketio import SocketIO, send, emit, disconnect
from erudit import manipulareYaml, functii, chatterREF

from werkzeug.utils import secure_filename


socketio = SocketIO(app)

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
        user = User.query.filter_by(username=username).first() #preluam user-ul dupa username sau
        if user:
            if user.password == password:
                login_user(user)
                return redirect(url_for('home'))
            else:
                msg = 'Parola gresita. Incercati din nou.'
        else:
            msg = "Nume de utilizator necunoscut. Va rugam sa incercati din nou sau sa va inregistrati."
    return render_template('layouts/default.html', content=render_template('pages/login.html', form=form, msg=msg, password=password)) #default distribuie roluri la pagini

#ruta principala
@app.route('/', methods=['GET', 'POST'])
def userprofile():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    msg=None
    form = FriendForm(request.form)
    formr = RegisterForm(request.form)
    formc = ConnectChatForm(request.form)
    user = User.query.all()
    server = Friend.query.all()
    if request.method == 'GET':
        return render_template('layouts/default.html', content=render_template('pages/user.html', server=server,
                                                                               user=user, form=form, formr=formr, formc=formc, msg=msg))

    user_username = [item.username for item in User.query.distinct(User.username).all()]

    #username = request.form.get('username', '', type=str)
    print(user_username)
    #username_f = User.query.filter_by(username=username).first()
    #print(username)
    if form.validate_on_submit:
        try:
            name_fr = request.form.get('name_fr', '', type=str)
            username_friend = request.form.get('username_friend', '', type=str)
            print(username_friend)
            username_fk = request.form.get('username_fk', '', type=str)
            server1 = Friend(name_fr, username_friend, username_fk)
            server1.save1()


            userfr_nume = Friend.query.filter_by(username_friend=username_friend).first()


            """
            if username_friend == username:
                server1 = Friend(name_fr, lastname_fr, username_friend, username_fk)
                server1.save1()
            else:
                msg = "Utilizatorul nu a putut fi gasit. Username-ul introdus de dvs. nu exista in aceasta aplicatie."
            return render_template('layouts/default.html',
                                   content=render_template('pages/' + path, server=server, user=user, form=form, msg=msg))
            """
        except Exception:
            return render_template('layouts/default.html', content=render_template('pages/user.html', server=server,
                                                                                   username_friend=username_friend, user=user, form=form, formr=formr, formc=formc, msg=msg))

    for i in user_username:
        if i == username_friend:
            user_pers1 = request.form.get('user_pers1', '', type=str)
            user_pers2 = request.form.get('user_pers2', '', type=str)
            prieteni = Chat(user_pers1, user_pers2)
            prieteni.save2()

    return render_template('layouts/default.html', content=render_template('pages/user.html', server=server,
                                                                           username_friend=username_friend, user=user, form=form, formr=formr, formc=formc, msg=msg))

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

@app.route("/sters", methods=["POST"])
def delete():
    username_friend = request.form.get("username_friend")
    servdel = Friend.query.filter_by(username_friend=username_friend).first()
    db.session.delete(servdel)
    db.session.commit()
    return render_template('layouts/default.html', content=render_template('pages/stergere.html', username_friend=username_friend))


@app.route('/index.html', methods=['GET', 'POST'])
def platforma():
    form = MessageForm(request.form)
    fisierele = FileContinut.query.all()
    messages = Message.query.all()
    membrii = [item.username_mes for item in Message.query.distinct(Message.username_mes).all()]
    membrii = list(dict.fromkeys(membrii))
    print(membrii)
    friend = Friend.query.all()
    if request.method == 'GET':
        return render_template('layouts/default.html',
                               content=render_template('pages/index.html', form=form, messages=messages, fisierele=fisierele, friend=friend, membrii=membrii))

    if form.validate_on_submit:
        try:
            username_mes = request.form.get('username_mes', '', type=str)
            print(username_mes)
            text_mes = request.form.get('text_mes', '', type=str)
            print(text_mes)
            dateTime = datetime.now()
            mesaj = Message(username_mes, text_mes, dateTime)
            mesaj.save()
        except Exception:
            return render_template('layouts/default.html',
                                   content=render_template('pages/index.html', form=form, messages=messages, fisierele=fisierele, friend=friend, username_mes=username_mes, text_mes=text_mes, dateTime=dateTime))

    return render_template('layouts/default.html',
                           content=render_template('pages/index.html', form=form, messages=messages, fisierele=fisierele, friend=friend, username_mes=username_mes, text_mes=text_mes, dateTime=dateTime))


@app.route('/ceva.html', methods=["POST"])
def upload_file():
    file = request.files["inputFile"]
    fisiere = FileContinut.query.all()
    name_fc = file.filename
    data_fc = file.read()
    newFile = FileContinut(name_fc, data_fc)

    newFile.save()
    username_mes = request.form.get('username_mes', '', type=str)
    print(username_mes)
    text_mes = request.form.get('text_mes', '', type=str)
    print(text_mes)
    dateTime = datetime.now()
    mesajfile = Message(current_user.username, file.filename, dateTime)
    mesajfile.save()
    return render_template('layouts/default.html',
                           content=render_template('pages/ceva.html', newFile=newFile, fisiere=fisiere, data_fc=data_fc,name_fc=name_fc))

@app.route('/pdf/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory='pdf', filename=filename)

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file1():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'

@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_bad_request(e):
    return 'Ruta nu a putut fi gasita!', 404

"""
@app.route('/chat')
def chat_view():
    if g.user:
        print(g.user)
        users = User.query.all()
        query = db.session.query(Message, User).filter(Message.sender_id==User.id)
        return render_template('/pages/index.html', currUser=g.user, users=users, query=query)
    return redirect(url_for('login'))
"""

@app.route('/user/<string:username>')
def user_profile(username):
    if g.user:
        user = User.query.filter_by(username=username).first()
        return render_template('/pages/user.html', user=user)
    return redirect(url_for('login'))

@app.route('/message', methods=['POST'])
def postMessage():
    if g.user:
        if not request.json or not 'username' in request.json or not 'messageText' in request.json:
            abort(400)
        messageData = request.json
        username = messageData['username']
        messageText = messageData['messageText']
        timeStamp = datetime.now()

        sender = User.query.filter_by(username=username).first()
        if sender is not None:
            message = Message(messageTxt=messageText, dateTime=timeStamp, sender_id=sender.id)

        msg = {}
        msg['timeStamp'] = timeStamp.strftime('%Y-%m-%d %H:%M:%S')
        msg['user'] = username
        msg['txt'] = messageText
        db.session.add(message)
        db.session.commit()
        socketio.emit('json_msg_response', msg, broadcast=True)
        return json.dumps(request.json)
    return redirect(url_for('login'))

"""
@socketio.on('json_msg')
def handleMessage(msg):
    receiveMessageDateTime = datetime.now()
    msg['timeStamp'] = receiveMessageDateTime.strftime("%Y-%m-%d %H:%M:%S")
    sender_id = request.form.get('username', '', type=str)
    #sender = User.query.filter_by(username=msg['user']).first()
    textul = request.form.get('messageTxt', '', type=str)
    message = Message(textul, receiveMessageDateTime, sender_id)
    db.session.add(message)
    db.session.commit()
    emit('json_msg_response', msg, broadcast=True)
    return render_template('/pages/index.html')
"""

@app.route('/messages')
def flutter():
    if g.user:
        messageList = Message.query.all()
        return jsonify(Message.serialize_list(messageList))
    return redirect(url_for('login'))

@app.route('/<usernamecrt>-<userfr>')
def convUserCrtFr(usernamecrt, userfr):
    username_friend = userfr
    username_crt = usernamecrt
    primul = Friend.query.filter_by(username_friend=username_friend).first()
    return render_template('layouts/default.html', content=render_template('pages/conv_1vs1.html', username_friend=username_friend, username_crt=username_crt))


@app.route("/corpus")
def corpusul():
    return "AB"

@app.route("/detectare")
def detect_referinte():
    userText = request.args.get('msg')
    if userText.lower() == "q":
        return 'Well, you just saw how things are going. ' \
               'I detected references. It was a strange conversation, between a human and me. I am glad that I met you. ' \
               'Now, I have to work on my abilities. See you soon. ' \
               'If you have more questions or doubts, please comeback to the application. ' \
               'Bye!'
    return functii.referinte(userText)

@app.route("/name", methods=["GET"])
def name():
    userText = request.args.get('msg')
    return functii.nume(userText)
#render_template('nimic.html', userText=userText)

@app.route("/discut")
def dialog():
    userText = request.args.get('msg')
    return functii.convorbireIT(userText)

@app.route("/discut_modif")
def dialogRef():
    userText = request.args.get('msg')
    return functii.convorbireREF(userText)

@app.route("/ceva", methods=["GET"])
def ceva():
    cv = request.args.get('msg')
    return render_template("home.html", cv=cv)

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    if userText.lower() == "exit":
        return 'Well, you just saw how things are going. ' \
               'I just talked with you about XAI and my reason. ' \
               'It was a strange conversation, between a human and me. I am glad that I met you. ' \
               'Now, I have to work on my abilities. See you soon. ' \
               'If you have more questions or doubts, please comeback to the application. ' \
               'Bye!'
    return manipulareYaml.convorbireXAI(userText)


@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/service-worker.js')
def sw():
    return send_from_directory('static', 'service-worker.js'), 200, {'Content-Type': 'text/javascript'}


@app.route('/sw.js')
def sw1():
    return send_from_directory('static', 'sw.js')

@app.route('/download')
def download_file():
    name_fc = request.form.get('name_fc', '', type=str)
    p = "gui6.png"
    return send_file(p, as_attachment=True)

