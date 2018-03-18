##########################################################################
######### AFAscript (Aggressioni Fasciste Ancora) V.0.2 by Bast1 #########
############## - CoDA - Collettivo Digitale Autorganizzato ###############
################################ GPL v3.0 ################################
##########################################################################
import metadata
import json
import logging
from time import gmtime, strftime, time
from bs4 import BeautifulSoup as bs
import urllib
import sys

home = "http://www.ecn.org/antifa/article/357/"
jpth = '../JSON/data.json'
lpth = '../LOG/info.log'

logging.basicConfig(filename=lpth, filemode='w', level=logging.INFO)

################## Functions ##################
def CheckData(jpath):
# This function read the missing data from Json
# and write the count in the log
    def RoundQuote(var):
        return str(round(var*1.0/len(data)*100)) + '%'

    with open(jpath) as json_data:
        data = json.load(json_data)
    return ['Tot: ' + str(len(data)),
            'Mass: ' + RoundQuote(sum([1 for x in data if x['ass'] == 'generico'])),
            'Mcit: ' + RoundQuote(sum([1 for x in data if x['cit'] == 'N.A.'])) ]


def DownloadData(home, jpath):
# This scrape the data from the site
    class info(object):
    #the info object take an entry from the site and get
    #the information out as a dictionary
        def __init__(self,tag):
            self.tag = tag
            for sign in [',', '.', '-', ':']: tag = tag.replace(sign, "")
            self.wlst =  [x for x in tag.split('href="')[1].split('</b></a>')[0].split(' ')]

        @property
        def info(self):
            ctt = ([x for x in self.wlst if x.lower() in metadata.lplce] + ['N.A.'])[0].title()
            prv = metadata.dicprv[ctt]
            info = {'link': 'http://www.ecn.org' + self.tag.split('href="')[1].split('"')[0],
                    'date': self.tag.split('"#000011"> ')[1].split(' </font')[0],
                    'year': self.tag.split('"#000011"> ')[1].split(' </font')[0].split("-")[-1],
                    'cit': ctt,
                    'prv': prv,
                    'reg': metadata.dicreg[prv],
                    'crd': metadata.diccrd[ctt],
                    'ass': ([metadata.dass[x.lower()] for x in self.wlst if x.lower() in metadata.dass] + ['generico'])[0]}
            return info


    site = urllib.urlopen(home)
    soup = bs(site, 'html5lib')
    soup = str(soup).decode('utf-8','ignore').split('AGGRESSIONI FASCISTE')[-1]
    data = [info(x).info for x in soup.split('</h3><h3>')]
    with open(jpath, 'w') as outfile:
        json.dump(data, outfile)
    return

################## Launcher ##################
if __name__ == '__main__':
    logging.info('{0} - Inizio aggiornamento dati'.format(strftime("%Y/%m/%d %H:%M:%S", gmtime())))
    try:
        DownloadData(home, jpth)
        logging.info('{0} - Check Dati: {1}'.format(strftime("%Y/%m/%d %H:%M:%S", gmtime()), str(CheckData(jpth))))
        logging.info('{0} - Aggiornamento dati completato con successo'.format(strftime("%Y/%m/%d %H:%M:%S", gmtime())))
    except:
        logging.info(('{0} - Processo Abortito').format(strftime("%Y/%m/%d %H:%M:%S", gmtime())))
    sys.exit()
