from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import urllib.parse
from urllib.request import Request, urlopen
from datetime import datetime
from flask import Flask, request, render_template,redirect
from twilio.rest import Client
from fonction import sms_reply


app = Flask(__name__) 

@app.route("/", methods=['GET'])
def retrievePassWord():
    global phone
    wts='whatsapp:+'
    num=str(request.args.get('phone')[10:])
    phone=wts+num 
    sess=request.args.get('sessionid')
    if sess=="idsessiontest4": 
        return render_template('password.html')
    else:
        return "hello"
  
    

@app.route('/envoi', methods = ['GET', 'POST'])
def envoi():
    if request.method == 'POST':
        password = request.form['password']
    account_sid = 'AC89c7cf15d429617da0f4dbe4ad393744'
    auth_token = '75b6f0ce16d7b0b713aaf7d70a11605e'
    client = Client(account_sid, auth_token)
    
    url = 'https://inputpass.chakamobile.com/?sessionid=idsessiontest4'
    parsed = urllib.parse.urlparse(url)
    idsession=urllib.parse.parse_qs(parsed.query)['sessionid'][0]
    resultat1=(str(sms_reply(password,idsession))).replace('<?xml version="1.0" encoding="UTF-8"?><Response><Message>',"")
    resultat2=resultat1.replace('</Message></Response>','')
    message = client.messages.create(
                              body=resultat2,
                              from_='whatsapp:+14155238886',
                              to=phone
                                     )
    return redirect('https://wa.me/+14155238886')
if __name__ == "__main__":
    #app.run(debug =True)
    app.run(host='10.10.180.195', port= 5000, debug=False)
  
