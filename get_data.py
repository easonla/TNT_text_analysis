# __author__ = 'easonla'
#  -*- coding: utf-8 -*-
# coding: utf-8
import urllib2 as ul
import requests, json
import pandas as pd
NLAPI = str("https://api.nationaltreasure.tw/v1/upload")
def get_TNT_data(tag='中美斷交',n=1000):
	uid_list = get_uid_list(tag)
	df = get_data(uid_list)
	return df

def get_uid_list(tag):
	link = NLAPI + "?tag=" + ul.quote(tag)
	parsed_data = json.loads(ul.urlopen(link).read())
	uid_list = [u.get('uid') for u in parsed_data['Items']]
	print 'link:'+link 
	print 'sample uid list'
	for uid in uid_list[:5]:
		print NLAPI+'?uid='+uid
	return uid_list

def get_data(uid_list):
	docs = {}
	index = 0 
	for uid in uid_list:
		link = NLAPI+'?uid='+uid
		temp = json.load(ul.urlopen(link))
		docs[index]=temp['Item']
		if index%100 == 0: print "{:d} data downloaded".format(index)
		index+=1
	df = pd.DataFrame.from_dict(docs,orient='index')
	ocr = df[['ocr','uid']]
	cols = ['uid','name','type','salience','count']
	nlp = []
	for i,d in enumerate(df['nlpEn']):
		uid = df['uid'][i]
		if len(d)!=0:
			for p in d[0]['entities']:
				count = len(p['mentions'])
				name = p['name'].lower()
				t = p['type']
				s = p['salience']
				nlp.append(dict( zip( cols, [uid,name,t,s,count])))
	nlp = pd.DataFrame(nlp)
	df = pd.merge(nlp,ocr,on='uid',how='outer')
	return df 
