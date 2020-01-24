#!/usr/bin/python36

import socket
import subprocess as sp
import time
s=socket.socket()
ip="192.168.100.114"
port=1234
s.bind((ip,port))
s.listen(5)
while True:
	conn , addr = s.accept()
	ip = addr[0]
	#print("\nHey I know You : ", addr[0])
	#print("\n")

	#print("Enter Your Choice: ")

	x = conn.recv(10)
	loc = x.decode()
	if loc == "local" or loc == "Local" or loc == "l" or loc == "L":
		a=("""\nWhat do you want to setup on Local System? 
		1)HADOOP ENVIROMENT
		2)HDFS CLUSTER
		3)MAPRED CLUSTER
		4)CLIENT""")
		conn.send(a.encode())
		y = conn.recv(20)
		cl= y.decode()
		if int(cl) == 1 or cl == "hadoop" or cl == "Hadoop" or cl == "HADOOP" :
			c=sp.getstatusoutput("python36 /install1.py")
			if int(c[0]) == 0:
				print("Done...")
				a="Hadoop has been installed"
				conn.send(a.encode())
			else:
				print("Not Complete")
		elif cl == "HDFS" or cl == "Hdfs" or cl == "hdfs" or cl == "h" or int(cl)== 2:
			a="""1)Setup Namenode
2)Setup Datanode"""
			conn.send(a.encode())
			z = conn.recv(20)
			cz= z.decode()
			if int(cz) == 1:
				sp.getoutput("python36 /master.py")
				print("Done...")
				a="NameNode Is Setup"
				conn.send(a.encode())
			if int(cz) == 2:
				sp.getoutput("python36 /slave.py")
				print("Done...")
				a="DataNode Is Setup"
				conn.send(a.encode())
		elif cl == "MAPRED" or cl == "Mapred" or cl == "mapred" or cl == "m" or int(cl)== 3:
			a=("""1)Setup JobTracker
2)Setup TaskTracker""")
			conn.send(a.encode())
			r = conn.recv(20)
			cr= r.decode()
			if int(cr) == 1:
				sp.getoutput("python36 /jt.py")
				print("Done...")			
				a="JobTracker Is Setup"
				conn.send(a.encode())
			if int(cr) == 2:
				sp.getoutput("python36 /tt.py")
				print("Done...")
				a="TaskTracker Is Setup"
				conn.send(a.encode())
		elif cl == "CLIENT" or cl == "Client" or cl == "client" or cl == "c" or int(cl)== 4:
				sp.getoutput("python36 /client.py")
				print("Done...")
				a="Client Is Setup"
				conn.send(a.encode())

	elif loc == "remote" or loc == "Remote" or loc == "r" or loc == "R":
		uid = "Enter User's IP: "
		conn.send(uid.encode())
		i = conn.recv(20)
		u_id= i.decode()
		a=("""\nWhat do you want to setup on Remote System? 
		1)HADOOP ENVIROMENT
		2)HDFS CLUSTER
		3)MAPRED CLUSTER
		4)CLIENT""")
		conn.send(a.encode())
		y = conn.recv(20)
		cl= y.decode()

		if int(cl) == 1 or cl == "hadoop" or cl == "Hadoop" or cl == "HADOOP" :
			b=sp.getstatusoutput("ssh 192.168.43.{} rpm -q hadoop || rpm -ivh jdk".format(u_id))
			if int(b[0])== 0 :			
				print("Hadoop is already installed")
			else:
				sp.getoutput("rm -rf /etc/hadoop")
				sp.getstatusoutput("ssh 192.168.43.{} rpm -ivh /root/jdk-7u79-linux-x64.rpm".format(u_id))
				c=sp.getstatusoutput("ssh 192.168.43.{} rpm -ivh /root/hadoop-1.2.1-1.x86_64.rpm --force".format(u_id))
				if int(c[0]) == 0:
					print("Hadoop is Installed\nNow Setting Up Path")
				else:
					print("Hadoop not Installed")
				sp.getoutput("scp /copyrc 192.168.43.{}:/root/.bashrc".format(u_id))
				sp.getoutput("ssh 192.168.43.{} chmod +x /root/.bashrc".format(u_id))
			t="Hadoop has been Installed and Path is set"
			conn.send(t.encode())			

		elif cl == "HDFS" or cl == "Hdfs" or cl == "hdfs" or cl == "h" or int(cl)== 2:
			mid = "Enter Master's IP: "
			conn.send(mid.encode())
			j = conn.recv(20)
			m_id= j.decode()
			k=("""\n1)Setup NameNode
2)Setup DataNode""")
			conn.send(k.encode())
			l = conn.recv(20)
			co= l.decode()
			if int(co) == 1:
				sp.getoutput("ssh 192.168.43.{} rm -rvf /master".format(u_id))
				sp.getoutput("scp /masterhdfs.xml 192.168.43.{}:/etc/hadoop/hdfs-site.xml".format(u_id))
				z=open("/core.xml",'w+')
				z.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>fs.default.name</name>
<value>hdfs://192.168.43.{}:9001</value>
</property>

</configuration>""".format(m_id))
				z.close()
				sp.getoutput("scp /core.xml 192.168.43.{}:/etc/hadoop/core-site.xml".format(u_id))
				sp.getoutput("ssh 192.168.43.{} hadoop namenode -format".format(u_id))
				sp.getoutput("ssh 192.168.43.{} hadoop-daemon.sh start namenode".format(u_id))
				time.sleep(2)
				x=sp.getstatusoutput("ssh 192.168.43.{} jps | grep NameNode".format(u_id))
				if int(x[0])== 0:
					stat="Namenode Started successfully"
					conn.send(stat.encode())
				else:
					stat="Failed to start NameNode"
					conn.send(stat.encode())
			elif int(co)==2:
				sp.getoutput("ssh 192.168.43.{} rm -rvf /data".format(u_id))
				sp.getoutput("scp /slavehdfs.xml 192.168.43.{}:/etc/hadoop/hdfs-site.xml".format(u_id))		
				z=open("/core.xml",'w+')
				z.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>fs.default.name</name>
<value>hdfs://192.168.43.{}:9001</value>
</property>

</configuration>""".format(m_id))
				z.close()
				sp.getoutput("scp /core.xml 192.168.43.{}:/etc/hadoop/core-site.xml".format(u_id))
				sp.getoutput("ssh 192.168.43.{} hadoop-daemon.sh start datanode".format(u_id))
				time.sleep(2)
				y=sp.getstatusoutput("ssh 192.168.43.{} jps| grep DataNode".format(u_id))
				if int(x[0])== 0:
					stat="DataNode Started successfully"
					conn.send(stat.encode())
				else:
					stat="Failed to start DataNode"
					conn.send(stat.encode())
			else:
				print("Invalid option, Now Exiting...")

		elif cl == "MAPRED" or cl == "Mapred" or cl == "mapred" or cl == "m" or int(cl)== 3:
			jid = "Enter JobTracker's IP: "
			conn.send(jid.encode())
			j = conn.recv(20)
			j_id= j.decode()		
			i=("""______________________________________________________________________________
\t-----------------WARNING-------------
________________________________________________________________________________
Make Sure Your /etc/hosts file is configured in the following manner:- \n\n
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

NameNode's IP		nn.lw.com
DataNode1's IP		dn1.lw.com
DataNode2's IP		dn2.lw.com
DataNode3's IP		dn3.lw.com
JobTracker's IP		jt.lw.com
TaskTracker1's IP	tt1.lw.com
TaskTracker2's IP	tt2.lw.com
Client's IP		client.lw.com
________________________________________________________________________________""")
			conn.send(i.encode())
		
			time.sleep(1)
			k=("""1)Setup JobTracker
2)Setup TaskTracker""")
			conn.send(k.encode())
			l = conn.recv(20)
			func= l.decode()

			if int(func) == 1:
				mid = "Enter Master's IP: "
				conn.send(mid.encode())
				j = conn.recv(20)
				m_id= j.decode()
				sp.getoutput("scp /mapredcore.xml 192.168.43.{}:/etc/hadoop/core-site.xml".format(u_id))			
				z=open("/core.xml",'w+')
				z.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>fs.default.name</name>
<value>hdfs://192.168.43.{}:9001</value>
</property>

</configuration>""".format(j_id))
				z.close()
				sp.getoutput("scp /core.xml 192.168.43.{}:/etc/hadoop/core-site.xml".format(u_id))
				sp.getoutput("scp /blank.xml 192.168.43.{}:/etc/hadoop/hdfs-site.xml".format(u_id))
				y=open("/mapred.xml",'w+')
				y.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>mapred.job.tracker</name>
<value>192.168.43.{}:9002</value>
</property>

</configuration>""".format(m_id))
				y.close()
				sp.getoutput("scp /mapred.xml 192.168.43.{}:/etc/hadoop/mapred-site.xml".format(u_id))	
				sp.getoutput("scp /hosts.txt  192.168.43.{}:/etc/hosts")
				sp.getoutput("ssh 192.168.43.{} hadoop-daemon.sh start jobtracker".format(u_id))	
				time.sleep(2)
				x=sp.getstatusoutput("ssh 192.168.43.{} jps| grep JobTracker".format(u_id))
				if int(x[0])== 0:
					o="JobTracker Started Successfully"
					conn.send(o.encode())
				else:
					o="Failed to start JobTracker"
					conn.send(o.encode())
			elif int(func) == 2:
				sp.getoutput("scp /mapredcore.xml 192.168.43.{}:/etc/hadoop/core-site.xml".format(u_id))	
				sp.getoutput("scp /blank.xml 192.168.43.{}:/etc/hadoop/hdfs-site.xml".format(u_id))
				y=open("/mapred.xml",'w+')
				y.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>mapred.job.tracker</name>
<value>192.168.43.{}:9002</value>
</property>

</configuration>""".format(j_id))
				y.close()
				sp.getoutput("scp /mapred.xml 192.168.43.{}:/etc/hadoop/mapred-site.xml".format(u_id))	
				sp.getoutput("scp /hosts.txt 192.168.43.{}:/etc/hosts")
				sp.getoutput("ssh 192.168.43.{} hadoop-daemon.sh start tasktracker".format(u_id))	
				x=sp.getstatusoutput("ssh 192.168.43.{} jps| grep TaskTracker".format(u_id))
				if int(x[0])== 0:
					o="TaskTracker Started Successfully"
					conn.send(o.encode())
				else:
					o="Failed to start TaskTracker"
					conn.send(o.encode())
			else:
				print("Invalid option, Now Exiting...")

		elif cl == "CLIENT" or cl == "Client" or cl == "client" or cl == "c" or int(cl)== 4:
			sp.getoutput("scp /core.xml 192.168.43.{}:/etc/hadoop/core-site.xml".format(u_id))
			sp.getoutput("scp /blank.xml 192.168.43.{}:/etc/hadoop/hdfs-site.xml".format(u_id))
			j=("Hadoop Client is set for upload")
			conn.send(j.encode())
	#print("Do You Want To Continue?")	
	#u="Do You Want to Continue? (y/n)\n"
	#conn.send(u.encode())
	#v = conn.recv(20)
	#choice= v.decode()
	#if choice == "y":
	#	i=1
	#elif choice == "n":
	#	i=0
s.close()
