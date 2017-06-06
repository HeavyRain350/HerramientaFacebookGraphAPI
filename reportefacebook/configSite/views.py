from django.shortcuts import render, redirect
from facade import Facade
# Create your views here.
def configurarReporte(request):
	try:
		config = open("configuracion.txt","rb")
		datosConfiguracion = []
		for line in config:
			datosConfiguracion.append(line.split()[1])

		return render(request,'index.html',{'alcance':str(int(float(datosConfiguracion[2])*10.0)),
								'share':str(int(float(datosConfiguracion[3])*10.0)),
								'reacciones':str(int(float(datosConfiguracion[4])*10.0)),
								'likes':str(int(float(datosConfiguracion[5])*100.0)),
								'love':str(int(float(datosConfiguracion[6])*100.0)),
								'haha':str(int(float(datosConfiguracion[7])*100.0)),
								'wow':str(int(float(datosConfiguracion[8])*100.0)),
								'sad':str(int(float(datosConfiguracion[9])*100.0)),
								'angry':str(int(float(datosConfiguracion[10])*100.0)),
								'correo':datosConfiguracion[11],})
	except Exception as e:
		return render(request,'index.html')

def	generarReporte(request):
	fechaInicio = request.POST.get('fechaInicio','')
	fechaFin = request.POST.get('fechaFin','')

	alcance = request.POST.get('alcance','')
	share = request.POST.get('shares','')
	reacciones = request.POST.get('reacciones','')
	likes = request.POST.get('likes','')
	love = request.POST.get('love','')
	haha = request.POST.get('haha','')
	wow = request.POST.get('wow','')
	sad = request.POST.get('sad','')
	angry = request.POST.get('angry','')

	correo = request.POST.get('correo','')

	config = open("configuracion.txt","w")

	
	
	config.write("inicio "+fechaInicio+"\n")
	config.write("fin "+fechaFin+"\n")

	config.write("formula "+str(int(alcance)/10.0)+"\n")
	config.write("formula "+str(int(share)/10.0)+"\n")
	config.write("formula "+str(int(reacciones)/10.0)+"\n")

	config.write("formula "+str(int(likes)/100.0)+"\n")
	config.write("formula "+str(int(love)/100.0)+"\n")
	config.write("formula "+str(int(haha)/100.0)+"\n")
	config.write("formula "+str(int(wow)/100.0)+"\n")
	config.write("formula "+str(int(sad)/100.0)+"\n")
	config.write("formula "+str(int(angry)/100.0)+"\n")
	
	config.write("correos "+correo)

	config.close()

	facade = Facade()
	facade.generarReporte()

	return redirect('/')

