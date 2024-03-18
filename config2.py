import socket
##Environment Values
server='GIVE YOUR SEREVR'
database='GIVE YOUR DATABASE NAME'
username='YOUR_USERNAME'
password='PASSWORD'
main_table=input("enter table to be archived")
schema_of_table=input('enter schema of table to be archived')
archival_column=input('Archival column name ')
hName = socket.gethostname()

if hName == "dev_ENV HOST":          # DEV Environment
  serverEnv = "DEV"
elif hName == "QA ENV HOST":        # QA Environment
  serverEnv = "QA"
elif hName == "PROD ENV HOST":        # PROD Environment
  serverEnv = "PROD"
else:
  print("Unidentified Host")

#serverEnv='DEV'
#environment based configuration
dev_Config = {
    'fromAddress' : 'abc@example.com',
    'toAddress' :['def@example.com',],
    'mailSubject' : f'{serverEnv} - DATA ARCHIVAL STATUS SQL SERVER  :',
    }

