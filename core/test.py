__author__ = 'Code_Cola'

from support.mysql_join import Connect

mysql = Connect()

print 'test'
s = mysql.query("SELECT username, password FROM core_judge_account WHERE oj = 'hdu' AND user_index = '0'")
print s
print 'test'