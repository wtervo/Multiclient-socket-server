#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import socket
from log import logger
log = logger("Server")
	 

class server(threading.Thread):
	"""
	Socket echo server that sends received message back to the client
	"""
	
	address = "127.0.0.1"
	port_init = 7777
	socket_num = 10
	
	def __init__(self):
		"""
		Inherit constructor from parent and create server socket
		"""
	
		super(server, self).__init__()
		self.s_list = []
		self.p_list = []
		
		#create sockets with different port numbers in a loop
		for i in range(self.socket_num):
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.p_list.append(self.port_init + i)
			s.bind((self.address, self.p_list[i]))
			self.s_list.append(s)

	def listen(self, s_socket):
		"""
		Server starts listening on predefined IP and port
		"""
	
		s_socket.listen(1)
		log.debug("Begun listening on %s" % str((self.address, s_socket.getsockname()[1])))
	
	def stop_server(self, s_socket):
		"""
		Server stops listening by closing the socket
		"""
	
		portnum = s_socket.getsockname()[1]
		s_socket.close()
		log.debug("Stopped listening on %s" % str((self.address, portnum)))
		
	def new_client(self, client_socket):
		"""
		Receive and echo back messages from client
		"""
	
		#loop receiveing a new messages
		while True:
			data = client_socket.recv(1024)
			if not data:
				#escape when the message has been fully received
				break
			log.debug("Received message: %s" % data)
			#send all received data back to client
			client_socket.sendall(data)
			log.debug("Echo message: %s" % data)
			
		client_socket.close()
		
	def start_listening(self, s_socket):
		"""
		Set up connection with the client and terminate it after inactivity
		"""
	
		#timeout after some seconds if no new connections are made
		socket_timeout = 5
		s_socket.settimeout(socket_timeout)
		self.listen(s_socket)
		
		#endless loop to receive new connections
		while True:
			try:
				client_socket, client_address = s_socket.accept()
				log.debug("Client connected: %s" % str(client_address))
				self.new_client(client_socket)
			
			#when timeout occurs, escape the loop and proceed to close the server
			except socket.timeout as e:
				log.debug(e)
				log.debug("Connection timed out after %s second(s) of inactivity" % str(socket_timeout))
				self.stop_server(s_socket)
				break
			except:
				raise
				
if __name__ == "__main__":

	s = server()
	for i in range(len(s.s_list)):
		threading.Thread(target = s.start_listening, args = (s.s_list[i],)).start()