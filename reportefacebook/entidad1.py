# -*- utf-8 -*-
import pika
import json 
import random
import math

def is_prime(a):
    return all(a % i for i in xrange(2, a))


def decode(aiPlaintext, iNumBits):
    bytes_array = []

    k = iNumBits // 8

    for num in aiPlaintext:
        for i in range(k):

            temp = num
            for j in range(i + 1, k):
                temp = temp % (2**(8 * j))
            letter = temp // (2**(8 * i))
            bytes_array.append(letter)
            num = num - (letter * (2**(8 * i)))

    decodedText = bytearray(b for b in bytes_array).decode('utf-8')

    return decodedText




connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()
channelenv = connection.channel()

channel.queue_declare(queue='envio')
channelenv.queue_declare(queue='destino')

p = random.randint(2,300)
g = 3
while(True):
	if(is_prime(p)):
		break
	else:
		p = random.randint(2,300)

a = random.randint(1,p-1)


A = (g ** a) % p

channel.basic_publish(exchange='',
	routing_key='envio',
	body= str(A)+" "+str(p)+" "+str(g) )

def callback(ch, method, properties, body):
	publica = body.split()

	y1 = int(publica[0])
	y2 = int(publica[1])
	p = int(publica[2])
	x = int(publica[3])
	


	e = p - 1 - a
	m = ((y1 ** e) * y2) % p
	
	print "Mensaje descifrado: "
	print (decode([(x * p) + m], 256))

	connection.close()

channelenv.basic_consume(callback,
                      queue='destino',
                      no_ack=True)

print(' [*] Esperando Mensaje Cifrado')
channelenv.start_consuming()