# -*- utf-8 -*-
import pika
import json  
import random
import math

def encode(sPlaintext, iNumBits):
    byte_array = bytearray(sPlaintext, 'utf-8')
    z = []
    k = iNumBits // 8
    j = -1 * k
    num = 0

    for i in range(len(byte_array)):
        if i % k == 0:
            j += k
            num = 0
            z.append(0)

        z[j // k] += byte_array[i] * (2**(8 * (i % k)))

    return z



connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channelrec = connection.channel()
channelenv = connection.channel()

channelrec.queue_declare(queue='envio')
channelenv.queue_declare(queue='destino')



def callback(ch, method, properties, body):
	publica = body.split()

	A = int(publica[0])
	p = int(publica[1])
	g = int(publica[2])

	print "Ingresa la palabra a cifrar y enviar a la entidad"
	palabra = raw_input()
	
	numeroCod = encode(palabra, 256)[0]

	m = numeroCod % p
	x = int(numeroCod / p)

	#m = 10

	b = random.randint(2,p-1)
	

	y1 = (g ** b) % p

	y2 = ((A ** b) * m) % p

	channelenv.basic_publish(exchange='',
		routing_key='destino',
		body=str(y1)+" "+str(y2)+" "+str(p)+" "+str(x))

	connection.close()
	    

channelrec.basic_consume(callback,
                      queue='envio',
                      no_ack=True)



print(' [*] Esperando clave publica')
channelrec.start_consuming()