import urllib
import json
import requests
import pandas as pd
TNTAPI = str("https://api.nationaltreasure.tw/v1/upload")

class TNT_Api:
    
    def __init__(self,tag='中美斷交',nlimit=200):
        self.tags = tag
        self.uid_list = list()
        self.df_docs = pd.DataFrame()
        self.ocr = pd.DataFrame()
        self.nlp = pd.DataFrame()
        self.n = nlimit
    
    def get_data(self):
        self.get_uid_list()
        self.download()
        self.find_ocr_data()
        self.find_nlp_data()
        
    def get_uid_list(self):
        tag = self.tags
        link = TNTAPI + "?tag=" + urllib.parse.quote(tag)
        uid_list = list()
        while True:
            res = requests.get(link).json()
            uid_list.extend([u.get('uid') for u in res['Items']])
            if 'LastEvaluatedKey' in res.keys():
                link = 'https://76k76zdzzl.execute-api.us-east-1.amazonaws.com/stage/upload?limit=1000&tag={:s}&lastKey={:s}'.format(urllib.parse.quote(tag),urllib.parse.quote(json.dumps(res['LastEvaluatedKey'])))
            else: break
        print ('{:d} documents found in tag {:s}'.format(len(uid_list),tag))
        self.uid_list = uid_list
        
    def download(self):
        print ('downloading, {:d} to go'.format(self.n))
        docs = {}
        for indx, uid in enumerate(self.uid_list):
            link = TNTAPI + '?uid=' +uid
            docs[uid] = requests.get(link).json()['Item']
            if indx%100 == 0: print ("{:d} data downloaded".format(indx))
            elif indx > self.n: break
        self.df_docs = pd.DataFrame.from_dict(docs,orient='index')

    def find_ocr_data(self):
        self.ocr = self.df_docs['ocr']
        
    def find_nlp_data(self):
        df = self.df_docs.copy()
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
        self.nlp = pd.DataFrame(nlp)