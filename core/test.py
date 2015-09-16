__author__ = 'Code_Cola'

from support.mysql_join import Connect

mysql = Connect()

s = mysql.query("SELECT problem_id, language, code FROM status_solve WHERE id = '1'")
print s[0][0]