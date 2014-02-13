from lxml import etree

tree = etree.parse(’portada.xml’)
rss = tree.getroot()
channel = rss[0]
for e in channel:
       if (e.tag == ’item’):
              e.set(’modificado’, ’hoy’)
              # Los atributos funcionan como diccionarios
              print (e.keys(), e.get(’modificado’))
              otro = etree.Element(’otro’)
              otro.text = ’Texto de otro’
              e.insert(0, otro)
print (etree.tounicode(rss, pretty_print=True))



'''
	PRIMERA OPCIÓN ETREE SAX

class ParseRssNews ():

	def __init__ (self):
		print (’---- Principio del archivo’)

	def start (self, tag, attrib): 
		print (’< %s>’ % tag)
		for k in attrib:
			print (’ %s = " %s"’ % (k,attrib[k]))

	def end (self, tag): 
		print (’</ %s>’ % tag)

	def data (self, data):
		print (’- %s-’ % data)

	def close (self):
		print (’---- Fin del archivo’)


parser = etree.XMLParser (target=ParseRssNews ())
etree.parse (’portada.xml’, parser)
'''