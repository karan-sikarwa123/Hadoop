import subprocess as sp

print("install java")
sp.getoutput("rpm -ivh jdk-8u171-linux-x64.rpm")

print("export java home")
print("export path")
sp.getoutput("echo 'export JAVA_HOME=/usr/java/jdk1.8.0_171-amd64/' >> /root/.bashrc")
sp.getoutput("echo 'export PATH=/usr/java/jdk1.8.0_171-amd64/bin:$PATH' >> /root/.bashrc")

print("install hadoop")
sp.getoutput("rpm -ivh /root/Desktop/hadoop-1.2.1-1.x86_64.rpm --force")




