##########################################################################
######### AFAscript (Aggressioni Fasciste Ancora) V.0.2 by Bast1 #########
############## - CoDA - Collettivo Digitale Autorganizzato ###############
################################ GPL v3.0 #################################
##########################################################################

import meta
import json

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
    data = [info(x).info for x in soup.split('</h3><h3>')]
    with open(output +'.json', 'w') as outfile:
        json.dump(data, outfile)
    sys.exit()
