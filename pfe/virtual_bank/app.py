from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import urllib.parse
from urllib.request import Request, urlopen
import mysql.connector
import getRespFromUrl



app = Flask(__name__)

@app.route("/sms", methods=['POST'])

def sms_reply(): 
    
    phone_no = request.form.get('From')
    num=str(phone_no[10:])
    msg = request.form.get('Body')
    resp = MessagingResponse()
    mySQL_conn = mysql.connector.connect(host='localhost',
                                   database='session_id_bd',
                                   user='lakram',
                                   password='passer')
    cursor = mySQL_conn.cursor()
    args = [0,'','',num,msg]
    
    resultats=cursor.callproc('ps_getsessionid',args)
   
    sessionid=str(resultats[2])
    if len(sessionid)==26:
            sessionid='0'+sessionid
    mySQL_conn.commit()
    cursor.close()
    
    mySQL_conn.close()

    url='http://10.10.180.167:7092/mtncg/requests'
    
    return getRespFromUrl.urlChange(msg,sessionid,url,resp)
   

if __name__ == "__main__":
    app.run(host='10.10.180.195', port= 5001, debug=False)
    
