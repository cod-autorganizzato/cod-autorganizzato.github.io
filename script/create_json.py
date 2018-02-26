##########################################################################
######### AFAscript (Aggressioni Fasciste Ancora) V.0.2 by Bast1 #########
############## - CoDA - Collettivo Digitale Autorganizzato ###############
################################ GPL v3.0 #################################
##########################################################################

import metadata
import json
from bs4 import BeautifulSoup as bs
import urllib
import sys

home = "http://www.ecn.org/antifa/article/357/"

class info(object):
    def __init__(self,tag):
        self.tag = tag
        self.wlst =  [x.replace(":", "").replace(".","").replace(",","").replace("-","")  for x in tag.split('href="')[1].split('</b></a>')[0].split(' ')]


    @property
    def info(self):
        ctt = ([x for x in self.wlst if x.lower() in metadata.lplce] + ['N.A.'])[0].title()
        prv = metadata.dicprv[ctt]

        info = {'link': 'http://www.ecn.org' + self.tag.split('href="')[1].split('"')[0],
                'date': self.tag.split('"#000011"> ')[1].split(' </font')[0],
                'year': self.tag.split('"#000011"> ')[1].split(' </font')[0].split("-")[-1],
                'prov': prv,
                'cit': ctt,
                'reg': metadata.dicreg[prv],
                'crd': metadata.diccrd[ctt],
                'ass': ([metadata.dass[x.lower()] for x in self.wlst if x.lower() in metadata.dass] + ['generico'])[0]}
        return info




if __name__ == '__main__':
    site = urllib.urlopen(home)
    soup = bs(site, 'html.parser')
    soup = str(soup).decode('utf-8','ignore').split('AGGRESSIONI FASCISTE')[-1]
    data = [info(x).info for x in soup.split('</h3><h3>')[1:]]
    with open('../JSON/data.json', 'w') as outfile:
        json.dump(data, outfile)
    sys.exit()
