import bs4 as bs
import urllib.request as urlReq
urun_listesi=[]
siyah_urunler=[]
beyaz_urunler=[]
kaynak=urlReq.urlopen('http://www.bambistore.com.tr/spor-27')
sayfa=bs.BeautifulSoup(kaynak,'lxml')
#print(sayfa)

for i in sayfa.findAll('a'):
    if(i.get('title')!=None and i.get('title')!="Favorilere Ekle"):
        urun_listesi.append(i.get('title'))

del urun_listesi[0]
del urun_listesi[-1]
si="siyah"
sayac=1
for j in urun_listesi:

    if(j.find(si)):
        sayac+=1

print(sayac)