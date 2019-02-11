#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
from time import sleep
from log import logger
log = logger("Client")


class client:
	"""
	Socket client that can connect to a server and send/receive data.
	"""

	host = "127.0.0.1"
	port_init = 7777
	socket_num = 6
	
	def __init__(self):

		self.msg_len = 0
		self.p_list = []
		for i in range(self.socket_num):
			self.p_list.append(self.port_init + i)

	def close(self, c_socket):
		"""
		Close connection to server
		"""
		
		portnum = c_socket.getsockname()[1]
		c_socket.close()
		log.debug("%s has disconnected" % str((self.host, portnum)))

	def receive(self, c_socket):
		"""
		Receive echo of a sent message from server
		"""
		
		data = b""
		length = 0
		
		#receive message from the server and stop receiving
		#when the original message has been fully echoed
		while length < self.msg_len:
			try:
				recvd = c_socket.recv(1024)
				if not recvd:
					break
				log.debug("Received echo: %s" % recvd)
				data += recvd
				length += len(data)
			except:
				raise
		#reset message length to avoid errors when sending multiple messages
		self.msg_len = 0
		self.close(c_socket)
		
	def send(self, c_socket, message):
		"""
		Send a message to server as bytes
		"""
		
		c_socket.sendall(message)
		log.debug("Sent message: %s" % message)
		#save message length in variable for later comparison with the echo message
		self.msg_len = len(message)
		self.receive(c_socket)
		
	def connect(self, port, client_number):
		"""
		Connect to the server
		"""
	
		c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		c_socket.connect((self.host, port))
		log.debug("%s has connected" % str((self.host, port)))
		#personalized message from each client
		message = "Hello there, this is client %s" % str(client_number)
		self.send(c_socket, str.encode(message))
		
if __name__ == "__main__":

	c = client()
	for i in range(len(c.p_list)):
		threading.Thread(target = c.connect, args = (c.p_list[i], i + 1)).start()