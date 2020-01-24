#! /usr/bin/python36

import subprocess as sp
sip = '192.168.43.247'
hdfs = """<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>dfs.data.dir</name>
<value>/data</value>
</property>

</configuration>"""
t1= "echo '{}' > /etc/hadoop/hdfs-site.xml".format(hdfs)
sp.getoutput(t1)

core = """<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>


<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>fs.default.name</name>
<value>hdfs://{}:9001</value>
</property>

</configuration>""".format(sip)
t2 = "echo '{}' > /etc/hadoop/core-site.xml".format(core)
sp.getoutput(t2)
