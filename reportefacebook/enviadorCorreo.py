# coding: utf-8
import smtplib
from datetime import datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
 
class EnviadorCorreo:

	def extraerConfiguracion(self,archivo):
		config = {}
		with open(archivo) as f:
		  for line in f:
		   (key, val) = line.split()
		   if(key== "correos"):
		   	correos = []
		   	for v in val.split(","):
		   		correos.append(v)
		   	config[key] = correos
		   elif(key== "formula"):
		   	pass
		   else:
		   	config[key] = datetime.strptime(val,'%Y-%m-%d')
		return config

	def enviarCorreo(self):
		fromaddr = "repFace350@gmail.com"
		config = self.extraerConfiguracion("configuracion.txt")
		msg = MIMEMultipart()
		 
		msg['From'] = fromaddr
		msg['To'] = ", ".join(config['correos'])
		msg['Subject'] = "Reporte de Facebook, "+config['inicio'].strftime('%d-%m-%Y')+" al "+config['fin'].strftime('%d-%m-%Y')

		 
		body = ""
		 
		msg.attach(MIMEText(body, 'plain'))
		 
		filename = "RepSemFace_"+config['inicio'].strftime('%d-%m-%Y')+"_"+config['fin'].strftime('%d-%m-%Y')+".html"
		attachment = open("ReporteSemanalFacebook.html", "rb")
		 
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
		 
		msg.attach(part)
		 
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(fromaddr, "basico4000")
		text = msg.as_string()
		server.sendmail(fromaddr, config['correos'], text)
		server.quit()