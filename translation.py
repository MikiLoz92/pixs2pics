class Translation:

	def __init__(self):

		pass

	def getText(lang, ident):

		return d[lang][ident]


hola = {
	"es": "Hola", 
	"en": "Hello",
	"fr": "Bonjour"
}

adios = {
	"es": "Adios", 
	"en": "Goodbye",
	"fr": "Au revoir"
}

dict = {
	"hola": hola
	"adios": adios
}

dict["hola"]["es"]
t = Translation()
t.getText(lang, "hola")