#!/usr/bin/env python
import subprocess
from datetime import datetime
import MySQLdb
#-------------------------
def start_mysql():
	subprocess.call(['sudo /usr/local/mysql/support-files/mysql.server start'],shell=True)
#-------------------------	
def format(data):					#format for display
	return [str(x)[str(x).find("'")+1:str(x).find("'",str(x).find("'")+2)] for x in data]
#-------------------------
def command(cur,command):			#execute command and return results as formatted/enumerated list
	cur.execute(command)
	return list(enumerate(format(cur.fetchall())))
#-------------------------	
def get_selection(item_list,msg):	#item_list is enumerated list
	selected = ''
	while selected not in [x[0] for x in item_list]:
		try: selected = int(raw_input(msg))
		except: pass
	return selected
#-------------------------		
def main():
	start_mysql()
	
	db_obj = MySQLdb.connect(host='localhost')
	cur=db_obj.cursor()
	
	#------------get databases
	databases = command(cur, 'show databases')
	print 'Select database by number:',''.join([ '\n  '+str(x[0])+' '+x[1] for x in databases ])
	database = get_selection(databases,'Database: ')
	print '  Fetching database "'+databases[database][1]+'"...';print
	cur.execute('use '+databases[database][1])
	#------------end get databases
	
	#------------get tables	
	tables = command(cur, 'show tables')
	print 'Select table in '+databases[database][1]+':',''.join(['\n  '+str(x[0])+' '+x[1] for x in tables])
	table = get_selection(tables,'Select table by number: ')
	print '  Fetching table "'+tables[table][1]+'"...';print
	#------------end get tables
	
	#cur.execute("select column_name from information_schema.columns where table_name = \'"+tables[table][1]+"\'")
	com = "select column_name from information_schema.columns where table_name = \'"+tables[table][1]+"\'"
	all_cols = command(cur, com)
	print 'Columns in '+tables[table][1]+': '
	print '  '+' | '.join([x[1] for x in all_cols]);print
	
	
	'''
	a=cur.execute('show columns from '+tables[table][1])
	print ' | '.join([x[0] for x in cur.description])
	for i in cur.fetchall():
		print i
	'''

	
if __name__ == '__main__':
	main()