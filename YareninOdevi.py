from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sqlite3

class okunanSayfasiHesaplama(QDialog):
    def __init__(self,e=None):
        super(okunanSayfasiHesaplama,self).__init__(e)
#Tasarım
        grid=QGridLayout()
        
        #line0
        grid.addWidget(QLabel("Okunan Kitap"),0,0)
        self.kitap=QLineEdit()
        grid.addWidget(self.kitap,0,1)

        #line1
        grid.addWidget(QLabel("Okunan Dergi"),1,0)
        self.dergi=QLineEdit()
        grid.addWidget(self.dergi,1,1)

        #line2
        grid.addWidget(QLabel("Okunan Makale"),2,0)
        self.makale=QLineEdit()
        grid.addWidget(self.makale,2,1)

        #line3
        grid.addWidget(QLabel("Ad Soyad :"),3,0)
        self.adSoyad = QLineEdit()
        grid.addWidget(self.adSoyad,3,1)

        #line4
        grid.addWidget(QLabel("Toplam"),4,0)
        self.toplam=QLabel('')
        grid.addWidget(self.toplam,4,1)

        #line5
        hesaplaButton=QPushButton('Hesapla')
        grid.addWidget(hesaplaButton,5,0,1,2)

        #line6
        gosterButton = QPushButton('Kaydet ve Görüntüle')
        grid.addWidget(gosterButton,6,0,1,2)

        #line7
        self.sonucLabel = QLabel("")
        grid.addWidget(self.sonucLabel,7,0,1,2)

        self.setLayout(grid)
        self.setWindowTitle('Okunan Sayfası Hesaplama')
##############################################################
        self.connect(hesaplaButton,SIGNAL('pressed()'),self.islem)
        self.connect(gosterButton,SIGNAL('pressed()'),self.databaseIslem)


    def databaseIslem(self):

        self.conn = sqlite3.connect('kitapKayitlari.db')
        self.conn.row_factory = sqlite3.Row
        self.isr = self.conn.cursor()

        db = self.isr.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kitapSayi'")
        if len(db.fetchall()) == 0:
            self.isr.execute('''CREATE TABLE kitapSayi(adSoyad VARCHAR(50) NOT NULL,kitap INTEGER NOT NULL,dergi INTEGER NOT NULL,makale INTEGER NOT NULL)''')
            self.conn.commit()
            self.dbKayit()
            self.goruntuleIslemleri()

        else:
            self.dbKayit()
            self.goruntuleIslemleri()

    def goruntuleIslemleri(self):

        sql=self.isr.execute('''SELECT adSoyad,MAX(kitap) FROM kitapSayi GROUP BY kitap''')
        skorBilgileri=[]

        for i in sql.fetchall():
            skorBilgileri.append(str(i['adSoyad']))
            skorBilgileri.append(str(i['MAX(kitap)']))

        sql = self.isr.execute('''SELECT adSoyad,MAX(dergi) FROM kitapSayi GROUP BY dergi''')
        for i in sql.fetchall():
            skorBilgileri.append(str(i['adSoyad']))
            skorBilgileri.append(str(i['MAX(dergi)']))

        sql = self.isr.execute('''SELECT adSoyad,MAX(makale) FROM kitapSayi GROUP BY makale''')
        for i in sql.fetchall():
            skorBilgileri.append(str(i['adSoyad']))
            skorBilgileri.append(str(i['MAX(makale)']))


        sonucText = "SKOR KIRANLAR: \n"+skorBilgileri[0]+" adlı kişi "+skorBilgileri[1]+" kitap \n"+skorBilgileri[2]+" adlı kişi "+skorBilgileri[3]+" dergi \n"+skorBilgileri[4]+" adlı kişi "+skorBilgileri[5]+" makale \n okumuştur. \n KAZANLANLARI TEBRİK EDERİZ."
        self.sonucLabel.setText(sonucText)
        # ... DEVAM EDİLECEK

    def dbKayit(self):

        self.isr.execute('''INSERT INTO kitapSayi(adSoyad,kitap,dergi,makale) VALUES (?,?,?,?)''',(self.adSoyad.text(),self.kitap.text(),self.dergi.text(),self.makale.text()))
        self.conn.commit()

    def islem(self):
        kitap=0
        try:
            kitap=float(self.kitap.text())
        except:
            pass
        dergi=0
        try:
            dergi=int(self.dergi.text())
        except:
            pass
        makale=0
        try:
            makale=float(self.makale.text())
        except:
            pass
        if not kitap:
            self.toplam.setText("<font color='black'><i>Kitap Giriniz</i>sayfa</font>")
            self.kitap.setFocus()
        elif not dergi:
            self.toplam.setText("<font color='black'><i>Dergiyi Giriniz</i>sayfa</font>")
            self.dergi.setFocus()
        elif not makale:
            self.toplam.setText("<font color='black'><i>Makaleyi Giriniz</i>sayfa</font>")
            self.makale.setFocus()
        else:
            toplam=(kitap+makale+dergi)
            self.toplam.setText("<font color='purple'><b>%0.2f</b>"
                                ""
                                "</font>"%toplam)


uyg=QApplication([])
pencere=okunanSayfasiHesaplama()
pencere.show()
uyg.exec_()