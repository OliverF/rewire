import optparse
import sys
import socket
import time
import threading

def stream(s1, s2):
	data = s1.recv(1024)
	s2.sendall(data)

def joinSockets(s1, s2):
	# Make a thread for each one
	# In each thread, on receive, send to other socket
	stream1 = threading.Thread(target = stream, kwargs = {'s1': s1, 's2': s2})
	stream2 = threading.Thread(target = stream, kwargs = {'s1': s2, 's2': s1})

	stream1.start()
	stream2.start()

def waitConnection(socket, port):
	clientSock, addr = socket.accept()

	print 'Received connection on port %i' % port

	sockets.append(clientSock)

op = optparse.OptionParser(usage = '%prog [options]')
op.add_option('-o', '--outgoing', action='append', help = 'Outgoing connection, can specify  up to 2')
op.add_option('-i', '--incoming', action='append', help = 'Incoming connection port, can specify up to 2')

options, args = op.parse_args()

specifiedConnections = 0
if (options.outgoing):
	specifiedConnections += len(options.outgoing)

if (options.incoming):
	specifiedConnections += len(options.incoming)

if (specifiedConnections != 2):
	op.print_help()
	sys.exit()

sockets = []

if (options.outgoing):
	for i, opt in enumerate(options.outgoing):
		addr, port = opt.split(':')
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((addr, int(port)))
		print 'Connected to %s' % opt
		sockets.append(s)

listenThreads = []

if (options.incoming):
	for i, opt in enumerate(options.incoming):
		port = int(opt)
		print 'Waiting for connection on port %i' % port
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(("0.0.0.0", port))
		s.listen(0)
		listenThread = threading.Thread(target = waitConnection, kwargs = {'socket': s, 'port': port})
		listenThreads.append(listenThread)
		listenThread.start()

for thread in listenThreads:
	thread.join()

print 'All sockets connected'

joinSockets(sockets[0], sockets[1])

raw_input('Press enter to quit')