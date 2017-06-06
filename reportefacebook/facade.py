from subprocess import call
from enviadorCorreo import EnviadorCorreo
from generadorReporte import GeneradorReporte
class Facade:
	def generarReporte(self):
		generador = GeneradorReporte()
		generador.generarReporte()
		call('Rscript -e "require(\'knitr\'); rmarkdown::render(\'ReporteSemanalFacebook.Rmd\', encoding = \'UTF-8\')"', shell=True)
		enviador = EnviadorCorreo()
		enviador.enviarCorreo()