#! /usr/bin/python36

import subprocess as sp
cip = '192.168.43.55'
core = """<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>fs.default.name</name>
<value>hdfs://{}:9001</value>
</property>

</configuration>""".format(cip)
t2 = "echo '{}' > /etc/hadoop/core-site.xml".format(core)
sp.getoutput(t2)

