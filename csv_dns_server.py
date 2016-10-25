import csv, paramiko

def alive_server():
    data = []
    server = raw_input('Enter the path : ')
    servers = [ser.rstrip("\n") for ser in open(server)]
    for server in servers:
   	b = []
	a = server.split(" ")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
	    ssh.connect(a[0])
	    (stdin, stdout, stderr) = ssh.exec_command('cat /etc/resolv.conf')
	    for reads in stdout.readlines():                
                if read.startswith('namserver'):
                 (stdin, stdout, stderr) = ssh.exec_command("dig @"+read[11:]+" NS ges.example.com|grep -v ';' | wc -l")
	        if stdout.readlines() > 1:                                         
	            b.append(read[11:])    
        except:
            continue
        c = map(lambda x: x.strip() , b)
        d = a + c
	data.append(d)
    generate_csv(data) 


def generate_csv(data):
 with open("ou.csv", "wb") as f:
  writer = csv.writer(f)
  for row in data:
   writer.writerow(row)			
  
if __name__ == '__main__':
    alive_server()
