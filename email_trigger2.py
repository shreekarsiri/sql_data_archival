from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from config2 import main_table,schema_of_table,archival_column
import config2
import smtplib
now = datetime.now()
datetime_ms = now.strftime("%d-%m-%Y %H:%M:%S")

def mailTrigger(errResponse,errMsg=""):
    html=""#initialize html variable
    msg = MIMEMultipart()
    msg["From"] = config2.dev_Config['fromAddress']
    to_address =",".join( config2.dev_Config['toAddress'])
    msg["To"]=to_address
    msg["Subject"] = config2.dev_Config['mailSubject']+" "+errResponse+" "+datetime_ms
    server = smtplib.SMTP("forwarder.mail.xerox.com")
    print(errResponse)
    if errResponse == "Success":
        html = f"""<body>
            Hello Team,<br><br>
            Data Archival for table {schema_of_table}.{main_table} is completed . .<br>

            Platform Team
            </body>
        """
    elif errResponse == "Failed":
        html = f"""<body>
            Hello Team,<br><br>
            failed case...Error msg <br>{errMsg}<br><br>
            Regards,<br>
            Platform Team
            </body>
        """
    elif errResponse =="NOT REQ":
       html = f"""<body>
          Hello Team,<br><br>
          Data Archival not required...<br>{errMsg}<br><br>
          Regards,<br>
          Platform Team
          </body>
           """
    msg.attach(MIMEText(html, 'html'))
    server.sendmail(config2.dev_Config['fromAddress'], config2.dev_Config['toAddress'], msg.as_string())
    print("mail sent")

