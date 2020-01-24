import subprocess as sp
tip = '192.168.43.247'
str2 ='''?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>mapred.job.tracker</name>
<value>{}:9002</value>
</property>

</configuration> '''.format(tip)
tr1="echo '{}' > /etc/hadoop/mapred-site.xml".format(str2)
sp.getoutput(tr1)
