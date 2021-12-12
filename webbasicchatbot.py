#!/usr/bin/env /SoftDev/telefacebot-python3/bin/python
import telebot
#import pyTelegramBotAPI
import traceback
import sys
import time
import random
import nltk
import numpy as mynumpy
import string
import warnings
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


from flask import Flask, render_template, request, session
#from firebase import firebase
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect, CSRFError
from wtforms import DateField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from wtforms_components import TimeField
import threading
import os


import matplotlib.pyplot as myploter
import glob

global mybot
global myTOKEN
global jawaban
myTOKEN = "5013582202:AAF4KM0le6NMJRbsyHfVLnDbh6sdW9Hu9Rw"
mybot = telebot.TeleBot(myTOKEN)
salam_ketemu = ['Hallo', 'Hi']
jawaban_salamketemu = ['Hallo juga', 'Hi juga']
ucapan_terimakasih = ['Terima-kasih', 'Thanks', 'Thank you', 'Makasih']
jawaban_ucapanterimakasih = ['Terima-kasih banyak juga', 'Makasih-banyak', 'Makasih-banget']
pamit = ['Bye']
jawaban_pamit = ['Bye juga', 'We are so happy for serving you', 'Kami sangat-senang melayani Anda']
global berkas
global myparagraf
global tokenkalimat
global kataterkirim
global mylemmer
global katakata
global tokenterlemmetasi
global tokentoken
global mystopwords





def telegram_polling():
    try:
        print("Mulai Telegram_Polling")
        mybot.polling(none_stop=True, timeout=6000)
    except:
        traceback_error_string=traceback.format_exc()
        with open("Error-nya_basicchatbot.log", "a") as myfile:
            myfile.write("\r\n\r\n" + time.strftime("%c")+"\r\n<<ERROR polling>>\r\n"+ traceback_error_string + "\r\n<<ERROR polling>>")
        myfile.close()
        mybot.stop_polling()
        time.sleep(10)
        telegram_polling()



def bikinstemming(local_myparagraftemp):
    #print("String yang mau di-stemming (word_tokenize): " + local_myparagraftemp)
    try:
        myparagrafstem = word_tokenize(local_myparagraftemp)
        return myparagrafstem
    except:
        traceback_error_string=traceback.format_exc()
        with open("Error-nya_basicchatbot.log", "a") as myfile:
            myfile.write("\r\n\r\n" + time.strftime("%c")+"GAGAL STEMMING(word_tokenize)"+ traceback_error_string  + "\r\n")
        myfile.close()



def buangnoisedata(localmyparagraf):
    mynoise=["\r","\n"]
    myparagraftanpanoise=[]
    localmyparagraftanpanoisetemp=[]
    myparagraftanpanoisetemp = list(filter(None, localmyparagraf))
    for localbaris in myparagraftanpanoisetemp:
        if (localbaris != None):
            myparagraftanpanoise.append(localbaris)
    myparagraftanpanoise = list(map(lambda x:x.strip(),myparagraftanpanoise))
    myparagraftanpanoise.remove('')
    print("\r\nMyParagraf tanpa-NOISE-->")
    print(myparagraftanpanoise)
    return myparagraftanpanoise



def buangtandabaca(myparagraftemp):
    myparagraftanpatandabaca=[]
    print("\r\nMyParagraf masih dengan-tandabaca-->")
    print(myparagraftemp)
    #translator = str.maketrans('','',string.punctuation)
    #translator = str.maketrans(dict.fromkeys(string.punctuation))
    mytranslator = str.maketrans({kunci:' ' for kunci in string.punctuation})
    #tokenterlemmetasitanpatandabaca = myparagraf.translate(string.maketrans('', '', string.punctuation))
    #myparagraftanpatandabaca = myparagraftemp.lower().translate(mytranslator)
    for localbaris in myparagraftemp:
        myparagraftanpatandabaca.append(localbaris.translate(mytranslator))
    print("\r\nMyParagraf tanpa-tandabaca-->")
    print(myparagraftanpatandabaca)
    return myparagraftanpatandabaca



def buangstopword(myparagraftemp):
    mystopwords = set(stopwords.words('indonesian'))
    try:
        word_tokens_no_stopwords = [w for w in myparagraftemp if not w in mystopwords]
        return word_tokens_no_stopwords
    except:
        traceback_error_string=traceback.format_exc()
        with open("Error-nya_basicchatbot.log", "a") as myfile:
            myfile.write("\r\n\r\n" + time.strftime("%c")+"GAGAL BUANG-STOPWORD"+ traceback_error_string + "\r\n")
        myfile.close()



def lemmetasi(local_tokentoken):
    #print("Local-TokenToken: " + local_tokentoken)
    #mylemmer = nltk.stem.wordnet.WordNetLemmatizer()
    mylemmer = WordNetLemmatizer()
    tokentoken = Normalisasi_sebelum_Lemmetasi(local_tokentoken)
    try:
        local_myparagraftemp = [mylemmer.lemmatize(token) for token in tokentoken]
        print("Local_myParagrafTemp (hasil lemmetasi)-->")
        print(local_myparagraftemp)
        return local_myparagraftemp
    except:
        traceback_error_string=traceback.format_exc()
        with open("Error-nya_basicchatbot.log", "a") as myfile:
            myfile.write("\r\n\r\n" + time.strftime("%c")+"GAGAL LEMITASI[lemmatize()]"+ traceback_error_string  + "\r\n")
        myfile.close()



def Normalisasi_sebelum_Lemmetasi(local_myparagraf):
    local_myparagraftanpatandabaca = buangtandabaca(local_myparagraf)
    print("Hasil Buang-tandabaca=>")
    print(local_myparagraftanpatandabaca)
    local_myparagraftanpastopword = buangstopword(local_myparagraftanpatandabaca)
    print("Hasil Buang-stopword-->")
    print(local_myparagraftanpastopword)
    local_myparagrafstem = bikinstemming(local_myparagraftanpastopword)
    print("Hasil Stemming(word_tokenize)-->")
    print(local_myparagrafstem)
    return local_myparagrafstem



def cetakdaftarmenu(localpesan):
    berkas = open("bahankonten/daftarmenu.txt", "r", errors="ignore", encoding="utf-8")
    #myparagraf = berkas.readline()
    myparagraf = berkas.read()
    #mybot.reply_to(localpesan, myparagraf)
    berkas.close()
    return myparagraf



def buka_semua_file_folder_bahankonten(mypath):
    myparagraf=[]
    localmyparagraftemp=[]
    for namaberkas in glob.glob(os.path.join(mypath, '*.*')):
        berkas = open(namaberkas, "r", errors="ignore", encoding="utf-8")
        localmyparagraftemp=berkas.readlines()
        myparagraf += localmyparagraftemp
    berkas.close()
    print("\r\nmyParagraf(fungsi buka_semua_file_folder_bahankonten)==>")
    print(myparagraf)
    myparagraf=buangnoisedata(myparagraf)
    return myparagraf



def pustakadata(pesan):
    print("\r\nPesan bakal dijawab oleh Robotchat-->" + pesan)
    myparagraf=buka_semua_file_folder_bahankonten("bahankonten")
    print("\r\nMyParagraf(isi semua-file dalam folder bahankonten)==>")
    print(myparagraf)
    stringmyparagraf=''
    for localbaris in myparagraf:
        stringmyparagraf = stringmyparagraf + '  ' + localbaris
    print("\r\n"+"Sebelum-cincang data ke dalam masing-masing kalimat (nltk.sent_tokenize)-->")
    print(stringmyparagraf)
    tokenkalimat = nltk.sent_tokenize(stringmyparagraf)
    print("\r\n"+"Hasil-Cincang data ke dalam masing-masing kalimat (nltk.sent_tokenize)-->")
    print(tokenkalimat)
    return tokenkalimat



def bikin_jawaban_pake_pustakadata(local_pesan):
    #print("Local-Pesan: " + local_pesan)
    tokenkalimat = pustakadata(local_pesan)
    print("\r\ntokenkalimat (hasil sent_tokenize)-->")
    print(tokenkalimat)
    local_jawabanrobotchat = ''
    localtokenkalimattemp=[]
    tokenkalimat.append(local_pesan.lower())
    for kata in tokenkalimat:
        localtokenkalimattemp.append(kata.lower())
    #nyarijawaban = TfidfVectorizer(tokenizer=Normalisasi_sebelum_Lemmetasi, stop_words='english')
    mystopwords = set(stopwords.words('indonesian'))
    #nyarijawaban = TfidfVectorizer(tokenizer=Normalisasi_sebelum_Lemmetasi(tokenkalimat), stop_words=mystopwords)
    nyarijawaban = TfidfVectorizer(tokenizer=lemmetasi(tokenkalimat), stop_words=mystopwords)
    nyarinyarijawaban = nyarijawaban.fit_transform(localtokenkalimattemp)
    bandingkan_data_dan_pertanyaan = cosine_similarity(nyarinyarijawaban[-1], nyarinyarijawaban)
    hasilperbandingan_data_dan_pertanyaan = bandingkan_data_dan_pertanyaan.argsort()[0][-2]
    kemiripan_data_dan_pertanyaan = bandingkan_data_dan_pertanyaan.flatten()
    kemiripan_data_dan_pertanyaan.sort()
    tingkatkemiripan_data_dan_pertanyaan = kemiripan_data_dan_pertanyaan[-2]
    if(tingkatkemiripan_data_dan_pertanyaan==0):
        local_jawabanrobotchat = local_jawabanrobotchat + "Saya gak-paham pertanyaan Anda. Mohon di-ulang pertanyaan nya dalam kalimat lebih-jelas. Jangan pake kata yang disingkat dan jangan pake istilah yang keliwat-gaul."
        return local_jawabanrobotchat
    else:
        #local_jawabanrobotchat = local_jawabanrobotchat + tokenkalimat[tingkatkemiripan_data_dan_pertanyaan]
        local_jawabanrobotchat = local_jawabanrobotchat + tokenkalimat[hasilperbandingan_data_dan_pertanyaan]
        return local_jawabanrobotchat



def bikin_jawabanrandom_pake_array(local_pesan):
    print("\r\nlocal_pesan-->" + local_pesan)
    for localkata in salam_ketemu:
        if (local_pesan.lower() == localkata.lower()): return random.choice(jawaban_salamketemu)
    for localkata in ucapan_terimakasih:
        if (local_pesan.lower() == localkata.lower()): return random.choice(jawaban_ucapanterimakasih)
    for localkata in pamit:
        if (local_pesan.lower() == localkata.lower()): return random.choice(jawaban_pamit)
    if ((local_pesan.lower()=='assalamualaikum') or local_pesan.lower()=='asalamualaikum'): return "Waalaikumsalam"
    return ''



@mybot.message_handler(commands=['help', 'start'])
def send_welcome(pesan):
    mybot.reply_to(pesan, "Selamat-Datang di Restoran-MinangSedap. Untuk daftar-menu selengkapnya, silahkan ketik:\"/daftarmenu\"")
    if(pesan.text=="daftarmenu"): cetakdaftarmenu()



@mybot.message_handler(func=lambda message: True)
def jawab_pesan(pesan:str):
    print("\r\nPertanyaan: " + pesan.text)
    if (pesan.text.lower()=='/daftarmenu'):
        local_daftarmenu=cetakdaftarmenu(pesan.text)
        local_daftarmenutemp=sent_tokenize(local_daftarmenu)
        for baris in local_daftarmenutemp:
            mybot.reply_to(pesan, baris)
        return
    jawaban = bikin_jawabanrandom_pake_array(pesan.text)
    if (jawaban!=''):
        try:
            print("\r\nJawaban dari array-> "+jawaban)
            mybot.reply_to(pesan, jawaban)
            jawaban=''
        except:
            traceback_error_string=traceback.format_exc()
            with open("Error-nya_basicchatbot.log", "a") as myfile:
                myfile.write("\r\n\r\n" + time.strftime("%c")+"GAGAL LEMITASI[lemmatize()]"+ traceback_error_string  + "\r\n")
                myfile.close()
    else:
        local_jawabanrobotchat = bikin_jawaban_pake_pustakadata(pesan.text)
        print("\r\nJawaban RobotChat-> " + local_jawabanrobotchat)
        mybot.reply_to(pesan, local_jawabanrobotchat)
        #mybot.send_message(pesan.chat.id, local_jawabanrobotchat)
        local_jawabanrobotchat=''




class formulirnama(FlaskForm):
    namaanda = StringField('Siapa nama kamu?', validators=[DataRequired()])
    kirim = SubmitField('Kirim')




#app1 = Flask(__name__, static_url_path="", static_folder="htdocs/gambar")
app1 = Flask(__name__, static_url_path = "", static_folder = "static")
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app1.config.from_object(env_config)
SECRET_KEY = os.urandom(32)
app1.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app1)

@app1.route('/', methods=['GET','POST'])
#@app1.route('/index')
def index():
    secret_key = app1.config.get("SECRET_KEY")
    #return f"The configured secret key is {secret_key}."
    #namaanda = None
    #formulir = formulirnama()
    #if formulir.validate_on_submit():
    #    session['namaanda'] = formulir.namaanda.data
    #    formulir.namaanda.data = ''
    #    return redirect(url_for('index'))
    #return render_template('index.html', form=formulir, name=session.get['namaanda'])
    #berkas = open('/static/index.html', "r", errors="ignore", encoding="utf-8")
    #halamanutama=berkas.read()
    #FOLDER_TEMPAT_UPLOAD = os.path.join('static', 'htdocs/gambar')
    #full_namaberkas = os.path.join(app1.config['FOLDER_TEMPAT_UPLOAD'], 'logominangkabau.jpg')
    #app1.config['FOLDER_TEMPAT_UPLOAD'] = full_namaberkas
    #return(halamanutama)
    #return render_template("htdocs/index.html", gambarnya = full_namaberkas)
    #return render_template(halamanutama, gambarnya = full_namaberkas)
    #return render_template("index.html", gambarnya="gambar/logominangkabau.jpg")
    return render_template("index.html")



if __name__ == '__main__':
    nltk.download('popular', quiet=True)
    nltk.download("punkt")
    nltk.download("wordnet")
    nltk.download("corpus")
    mytelegram_polling = threading.Thread(name='daemon-myrobotresto', target=telegram_polling)
    mytelegram_polling.setDaemon(True)
    mytelegram_polling.x=1
    mytelegram_polling.start()
    mytelegram_polling.join(6)
    if (mytelegram_polling.is_alive() == True ):
        print("RobotChat is running as a daemon->" + str(mytelegram_polling.is_alive() ) )
        app1.debug = True
        #app1.run(host="127.0.0.1", port=5000, threaded=True)
        porthttp = int(os.environ.get("PORT", 5000))
        #app1.run(host='0.0.0.0', port=porthttp)
        app1.run(host='0.0.0.0', debug=True, threaded=True, use_reloader=True)
    else:
        print("RobotChat dead")
