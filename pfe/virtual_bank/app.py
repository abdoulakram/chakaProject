from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import urllib.parse
from urllib.request import Request, urlopen
from datetime import datetime
import random
import string
import mysql.connector
#import MySQLdb




#sessionid="idsessiontest4"#datetime.now().strftime("%d-%b-%Y-%H:%M:%S.%f") 


app = Flask(__name__)

@app.route("/sms", methods=['POST'])

def sms_reply():
    #global sessionid
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
    sessionid=resultats[2]
    mySQL_conn.commit()
    cursor.close()
    
    mySQL_conn.close()
    
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                      'AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
        }
    req = Request('http://10.10.180.167:7092/mtncg/requests', headers=headers)
    params={
    "sessionid":sessionid,
    "msisdn":"242055565990",
    "input":msg
            }
    
    query_string=urllib.parse.urlencode(params)
    data=query_string.encode("ascii")
    with urllib.request.urlopen(url=req,data=data) as response:
        
        response_text=response.read()
       # header=response.headers  
   
        response_text_str=str(response_text)
        liste=response_text_str.split("\\n")
    
    
        liste.remove("'")
        chaine=""
        for i in range(len(liste)):
            chaine+=liste[i]+"\n"
        if(str(chaine).__contains__("SECRET")):
            resp.message(str(chaine.replace("b'",""))+str("\nhttps://inputpass.chakamobile.com/?sessionid="+str(sessionid)+"&phone="+phone_no))
            
        else:
            resp.message(str(chaine.replace("b'","")))
        
        return str(resp)
   

if __name__ == "__main__":
    app.run(host='10.10.180.195', port= 5001, debug=False)
    
