import pandas
import urllib
from bs4 import BeautifulSoup as bs
import numpy as np

########### Codici Comuni ###########
istat = pandas.read_excel('./meta/Elenco-comuni-italiani.xls').fillna('NA')
istat['Denominazione provincia'] = np.where(istat['Denominazione provincia']=='-', istat['Denominazione Citta metropolitana'], istat['Denominazione provincia'])

lplce = list(istat['Denominazione in italiano']) + list(istat['Sigla automobilistica'].unique())
lplce = [x.lower() for x in lplce]
lplce.remove('to')
lplce.remove('-')
dicprc = dict(zip(istat['Sigla automobilistica'],istat['Denominazione provincia']))
dicprv = dict(zip(istat['Denominazione in italiano'],istat['Sigla automobilistica']))
dicprv.update({x.title(): x.upper() for x in dicprc})
dicprv['N.A.'] = 'N.A.'
dicreg = dict(zip(istat['Sigla automobilistica'],istat['Denominazione regione']))
dicreg['N.A.'] = 'N.A.'


########### Dizionario associazioni ###########
dass = {'fascista' : 'fascista',
'ultradestra' : 'ultradestra',
'lega' : 'lega',
'leghista' : 'lega',
'casapound' : 'casapound',
'blocco' : 'blocco studentesco',
"fronte" : 'fronte della gioventu',
"naziskin" : 'naziskin',
"nazi": "naziskin",
"forza" : "forza nuova",
"razzista" : "razzista",
"razzisti" : "razzista",
"omofobo" : "omofoba",
"gay" : "omofoba",
"lesbica" : "omofoba",
"omosessuali": "omofoba",
"stranieri" : "xenofoba",
"straniero" : "xenofoba",
"extracomunitari" : "xenofoba",
"neofascista" : "fascista",
"fascisti" : "fascista",
"neofascisti" : "fascista",
'skinhead' : "fascista",
"destra" : "destra"}

########### Funzioni Geo ###########
def GetCoordinate():
    Dfcomun = istat[['Codice Comune formato alfanumerico','Denominazione in italiano']].rename(columns={'Codice Comune formato alfanumerico':'com'})
    Dfcomun['com'] = Dfcomun['com'].map(str)
    dcoord = MetaGeo()
    Dfcoord = pandas.DataFrame().from_dict(dcoord)
    Dfctot  = pandas.merge(Dfcomun, Dfcoord, how='outer')
    diccrd = dict(zip(Dfctot['Denominazione in italiano'],Dfctot['pnt']))
    diccrd['N.A.'] = 'N.A.'
    diccrd.update({x.title(): diccrd[dicprc[x]] for x in dicprc if dicprc[x] in diccrd})
    return diccrd

def MetaGeo():
    home = "meta/italia_comuni.svg"
    site = urllib.urlopen(home)
    soup = bs(site, 'html.parser')
    soup = str(soup)
    rawdata    = soup.split("</g>\n")
    rawdata[0] = rawdata[0].split('comuni">\n')[1]
    for x in rawdata:
        if '22084' in x or '65011' in x: rawdata.remove(x)
    rawdata = rawdata[:8092]
    geodata = [geoinfo(x).info for x in rawdata]
    return geodata

class geoinfo(object):
    def __init__(self, tag):
        self.tag = tag
        self.coord = tag.split('points="')[1].split('">')[0]
        self._cods = tag.split('id="')[1].split('"')[0].split("-")

    @staticmethod
    def _centering(coord):
        lcoord = [[float(x) for x in y.split(',')] for y in coord.split(' ')]
        x,y=zip(*lcoord)
        center=round((max(x)+min(x))/2.,2), round((max(y)+min(y))/2.,2)
        return center

    @property
    def info(self):
        info = { "reg" : self._cods[0][5:],
                 "pro" : self._cods[1][3:],
                 "com" : self._cods[2][3:],
                 "pnt" : self._centering(self.coord)
        }
        return info

diccrd = GetCoordinate()
