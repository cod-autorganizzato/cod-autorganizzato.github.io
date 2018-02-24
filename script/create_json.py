##########################################################################
######### AFAscript (Aggressioni Fasciste Ancora) V.0.2 by Bast1 #########
############## - CoDA - Collettivo Digitale Autorganizzato ###############
################################ GPL v3.0 #################################
##########################################################################

import meta
import json
from bs4 import BeautifulSoup as bs
import urllib


home = "http://www.ecn.org/antifa/article/357/"

class info(object):
    def __init__(self,tag):
        self.tag = tag
        self.wlst =  [x.replace(":", "") for x in tag.split('href="')[1].split('"')[1].split(' ')]

    @property
    def info(self):
        info = {'link': 'http://www.ecn.org' + tag.split('href="')[1].split('"')[0],
                'date': self.tag.split('"#000011"> ')[1].split(' </font')[0],
                'year': tag.split('"#000011"> ')[1].split(' </font')[0]r,
                'prov': meta.dicprv[ctt],
                'cit': ([x for x in self.wlst if x.lower() in meta.lplce] + ['N.A'])[0].title(),
                'reg': meta.dicreg[prv],
                'crd': meta.diccrd[ctt],
                'ass': ([x for x in self.wlst if x.lower() in meta.dass] + ['generico'])[0]}
        return info

if __name__ == '__main__':
    output = sys.argv[1]
    site = urllib.urlopen(home)
    soup = bs(site, 'html.parser')
    soup = str(soup).decode('utf-8','ignore').split('AGGRESSIONI FASCISTE')[-1]
    data = [info(x).info for x in soup.split('\n')]
    with open(output +'.json', 'w') as outfile:
        json.dump(data, outfile)
    sys.exit()



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

def MetaGeo():
    home = "http://cdn.dataninja.it/shapes/maps/it/italia_comuni.svg"
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

def GetCoordinate():
    istat = pandas.read_excel('/home/bastone/Scaricati/Elenco-comuni-italiani.xls').fillna('NA')
    Dfcomun = istat[['Codice Comune formato alfanumerico','Denominazione in italiano']].rename(columns={'Codice Comune formato alfanumerico':'com'})
    Dfcomun['com'] = Dfcomun['com'].map(str)
    dcoord = MetaGeo()
    Dfcoord = pandas.DataFrame().from_dict(dcoord)
    Dfctot  = pandas.merge(Dfcomun, Dfcoord, how='outer')
    diccrd = dict(zip(Dfctot['Denominazione in italiano'],Dfctot['pnt']))
    return diccrd
