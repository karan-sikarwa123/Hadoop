import subprocess as sp
jip = '192.168.43.247'
str1='''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>mapred.job.tracker</name>
<value>{}:9002</value>
</property>

</configuration> '''.format(jip)

tr="echo '{}' > /etc/hadoop/mapred-site.xml".format(str1)
sp.getoutput(tr)

str2 ='''?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>fs.default.name</name>
<value>hdfs://{}:9002</value>
</property>

</configuration> '''.format(jip)
tr1="echo '{}' > /etc/hadoop/core-site.xml".format(str2)
sp.getoutput(tr1)



