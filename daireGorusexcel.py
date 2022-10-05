# KURUM 01.12.2021 KISA ve EXCEL DAHİL VERSİYON #
#*******************************************#
from belgenetUser import username, password
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from CED_TCO import ExcelDosya
import konuCharHarf



import os
import shutil
import glob
import warnings
warnings.filterwarnings("ignore")

class Belgenet:
    def __init__(self, username, password):
        self.browser=webdriver.Chrome("C:/Users/tugbacanan.oguz/Desktop/python_temelleri_iş/PROJECT_1/chromedriver.exe")
        self.username=username
        self.password=password
        
             
    
    def signIn(self):
        self.browser.get("https://e-belge.tarim.gov.tr/edys-web/sistemeGiris.xhtml")
        self.browser.implicitly_wait(60)

        self.browser.find_element(By.XPATH,"//*[@id='parolaSertifikaAccordion:uForm:txtUKullaniciAdi']").send_keys(self.username)
        self.browser.find_element(By.XPATH,"//*[@id='loginUSifre']").send_keys(self.password)

        self.browser.implicitly_wait(60)

        self.browser.find_element(By.XPATH,"/html/body/div[5]/div[2]/div/div[2]/div/div[2]/div[2]/div/form/button/span").click()

        self.browser.implicitly_wait(60)



    def letter(self):

        ####GELEN KUTUSUNDAKİ İLK 10 YAZIYI GELDİĞİ YER VE KONUSUNU ALIP DICT'YE ATAR
        import time
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.implicitly_wait(60)
        WebDriverWait(self.browser, 60).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='esm_246802192_emi_286053589']"))).click()      # gelen kutusunu tıklar
        #WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='mainInboxForm:inboxDataTable:j_id21']"))).click()
        
        # identify dropdown with Select class
        time.sleep(2)
        self.browser.implicitly_wait(60)
        sel100 = Select(self.browser.find_element_by_xpath("//div[@class='ui-paginator ui-paginator-top ui-widget-header']//select[@name='mainInboxForm:inboxDataTable_rppDD']"))   #sayfada görünen yazı sayısını 100'e çıkarır
        self.browser.implicitly_wait(60)
        time.sleep(2)
        #select by select_by_visible_text() method
        sel100.select_by_visible_text("100")
        self.browser.implicitly_wait(60)
        time.sleep(4)
        print("OK-100")

        gelenReadevenList=self.browser.find_elements(By.CSS_SELECTOR,f"#mainInboxForm\:inboxDataTable_data > tr.ui-widget-content.ui-datatable-even.ui-datatable-selectable.ui-inbox-read")    #aşağıdaki satırlarla beraber tüm gelen yazı listesini alır (sayı olarak)
        self.browser.implicitly_wait(60)
        print("1")
        #time.sleep(1)
        gelenReadoddList=self.browser.find_elements(By.CSS_SELECTOR,f"#mainInboxForm\:inboxDataTable_data > tr.ui-widget-content.ui-datatable-odd.ui-datatable-selectable.ui-inbox-read")
        self.browser.implicitly_wait(60)
        print("2")
        #time.sleep(1)
        gelenUnreadevenList=self.browser.find_elements(By.CSS_SELECTOR,f"#mainInboxForm\:inboxDataTable_data > tr.ui-widget-content.ui-datatable-even.ui-datatable-selectable.ui-inbox-unread")
        self.browser.implicitly_wait(60)
        #time.sleep(1)
        print("3")
        gelenUnreadoddList=self.browser.find_elements(By.CSS_SELECTOR,f"#mainInboxForm\:inboxDataTable_data > tr.ui-widget-content.ui-datatable-odd.ui-datatable-selectable.ui-inbox-unread")
        self.browser.implicitly_wait(60)
        print("4")

        gelenList=gelenUnreadevenList+gelenUnreadoddList+gelenReadevenList+gelenReadoddList#+gelenreadevenivediList+gelenreadoddivediList#+gelenUnreadevenivediList+gelenUnreadoddivediList
         #tüm gelen yazı listesini tek liste yapar(okunmuş-okunmamış-tek-çift)
                
        print(len(gelenList))
  
        time.sleep(3)

        gelenYaziCokluList=[]


        for i in gelenList:
            sira=int(i.get_attribute("data-ri"))
            self.browser.implicitly_wait(120)
            time.sleep(1)
            h3Konu=(i.find_element_by_tag_name("h3")).text
            self.browser.implicitly_wait(120)
            #print(h3Konu)
            h3Konu2=konuCharHarf.konuRemove(h3Konu)
            h3KonuJoin=konuCharHarf.konuJoin(h3Konu)
            h3KonuJoinDosya=konuCharHarf.dosyaKonu(h3Konu)
            h3KonuJoinDosya2=konuCharHarf.harf(h3KonuJoinDosya)
            #print(f"h3KonuJoinDosya2-{h3KonuJoin}")



            gelYer=(i.find_element(By.XPATH,"td[2]/table[1]/tbody[1]/tr[2]")).text                                                                            
            self.browser.implicitly_wait(120)
            # print(gelYer)
            # print("gelyer")
        
            if gelYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / İzleme ve Su Bilgi Sistemi Daire Başkanlığı":
                geldigiYerD="izleme"
                
            elif gelYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Havza Yönetimi Daire Başkanlığı":
                geldigiYerD="havza"
                
            elif gelYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Taşkın ve Kuraklık Yönetimi Daire Başkanlığı":
                
                geldigiYerD="taşkın"
                
            elif gelYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Su Kalitesi Daire Başkanlığı":
                geldigiYerD="kalite"
                
            else:
                geldigiYerD="diğer"              
        


            #gelenYaziDict.update({sira:{h3KonuJoin:geldigiYerD}})
            if geldigiYerD=="diğer":                                 
                
                 
                print("value diğermiş")       

            else:
                gelenYaziCokluList.append((int(sira), h3KonuJoin, h3KonuJoinDosya2, geldigiYerD))
                print("OKK")


        if len(gelenYaziCokluList)==0:
            print("""
            *************************************************
            YENİ GELEN GÖRÜŞ YAZISI YOK, PROGRAM ÇALIŞTIRILMAYACAK
            *************************************************
            """)
        elif len(gelenYaziCokluList)!=0:

            print(gelenYaziCokluList)

            #KİŞİSEL ARŞİV
            
            WebDriverWait(self.browser, 120).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='leftMenuForm:kisiselArsivPanel:kisiselArsivKlasoruTab_header']"))).click() #kişisel arşiv
            self.browser.implicitly_wait(60)            
            WebDriverWait(self.browser, 120).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[9]/div[2]/form/div[2]/div[2]/div/ul/li/span/span[1]"))).click()  #altmenü kişisel arşiv
            self.browser.implicitly_wait(60)
            WebDriverWait(self.browser, 120).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='leftMenuForm:kisiselArsivPanel:kisiselArsivKlasoruTree:0_3']"))).click()   # 4. sıradaki klasörü seçme
            self.browser.implicitly_wait(120)
     

            time.sleep(20)
            bakYaziEven=self.browser.find_elements(By.CSS_SELECTOR,f".ui-widget-content.ui-datatable-even.ui-datatable-selectable.ui-inbox-read[data-ri]")         
            self.browser.implicitly_wait(120)

            bakYaziOdd=self.browser.find_elements(By.CSS_SELECTOR,f".ui-widget-content.ui-datatable-odd.ui-datatable-selectable.ui-inbox-read[data-ri]") 
            self.browser.implicitly_wait(120)

            bakYaziListe=bakYaziOdd+bakYaziEven
            #print(len(bakYaziListe))
            
            for y in range((len(bakYaziListe))-1):   
                konuYaz=self.browser.find_element(By.XPATH,f"//*[@id='mainInboxForm:inboxDataTable:{y}:evrakTable']/tbody/tr[1]/td[2]/div[1]/h3").text   #yazının konusunu text halinde veriyor  (kişisel arşiv) 
                self.browser.implicitly_wait(120)
                time.sleep(2)   
                print("konuYaz")  
                print(konuYaz)
                

                gelenKonuJoin=konuCharHarf.konuJoin(konuYaz)
                konuDosyaAdi=konuCharHarf.dosyaKonu(konuYaz)
                konuDosyaAdi2=konuCharHarf.harf(konuDosyaAdi)

                for nestedTuple in gelenYaziCokluList:
                    nestedKonu=nestedTuple[1]
                    nestedDosya=nestedTuple[2]

                    print(gelenKonuJoin)
                    print(nestedKonu)

                    if nestedKonu==gelenKonuJoin: 
                        #print(konuDosyaAdi2) 



                        geldYerYazi=self.browser.find_element(By.XPATH,f"//*[@id='mainInboxForm:inboxDataTable:{y}:evrakTable']/tbody/tr[2]/td/div").text
                        self.browser.implicitly_wait(120)
                        time.sleep(1)
                        geldYerYazim=str(geldYerYazi).lstrip("Geldiği Yer:").strip()
                        geldYerList=str(geldYerYazim).split("/")
                        geldYerSon=str(geldYerList[0]).strip()
                        print(geldYerSon)

                        #time.sleep(3)

                        sayiYazi=self.browser.find_element(By.XPATH,f"//*[@id='mainInboxForm:inboxDataTable:{y}:evrakTable']/tbody[1]/tr[3]/td[1]/div[1]/span").text
                        self.browser.implicitly_wait(60)
                        #time.sleep(1)
                        print(sayiYazi)


                        dosyaListem=os.listdir("C:/Users/tugbacanan.oguz/Desktop/CED")    #ÇED kaydedilen klasörün listesini alıyor, yeni klasör numarasını tespit etmek için
                        
                        

                        dosyaListem2=[]
                        for i in dosyaListem:
                            klasorAdi=(i.split("-"))[1]

                            klasorAdiKonu=(klasorAdi.split("_"))[2]
                            klasorAdiKonu2=konuCharHarf.harf(klasorAdiKonu)

                            dosyaListem2.append(klasorAdiKonu2)
                            

                        print(dosyaListem2)


                        indexDosyam=""
                        count=dosyaListem2.count(nestedDosya)
                        print(count)
                        print("count")   
                        
                        klasorKayıt=""     
                        if count>1:
                            x=0
                            for i in range(1,count):
                                indexDosya=(dosyaListem2.index(nestedDosya))+301
                                print(f"eski dosya {i}: {indexDosya} ")
                                
                                dosyaListem2.pop(indexDosya-301)
                                x+=i
                                indexDosya=(dosyaListem2.index(nestedDosya))+(301+x)
                                klasorKay= dosyaListem[indexDosya-(301)]
                                klasorKayıt=klasorKay

                                print(klasorKayıt)
                                print(indexDosya)
                                print("OK-doğru dosya bulundu")
                                indexDosyam=indexDosya                        
                        elif count==1:
                            indexDosya=(dosyaListem2.index(nestedDosya))+301
                            klasorKayıt2=dosyaListem2[dosyaListem2.index(nestedDosya)]
                            klasorKay=dosyaListem[dosyaListem2.index(nestedDosya)]
                            klasorKayıt=klasorKay
                            print(klasorKayıt2)
                            print(klasorKayıt)#
                            print(indexDosya)
                            print("OK-doğru dosya bulundu")
                            indexDosyam=indexDosya

                            WebDriverWait(self.browser, 120).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='esm_246802192_emi_286053589']"))).click()      # gelen kutusunu tıklar

                            self.browser.implicitly_wait(60)
                            time.sleep(4)
                            
                            sel100 = Select(self.browser.find_element_by_xpath("//div[@class='ui-paginator ui-paginator-top ui-widget-header']//select[@name='mainInboxForm:inboxDataTable_rppDD']"))   #sayfada görünen yazı sayısını 100'e çıkarır
                            self.browser.implicitly_wait(60)
                            time.sleep(2)

                            sel100.select_by_visible_text("100")
                            self.browser.implicitly_wait(60)
                            time.sleep(6)
                            print("OK-100")
                            gelYaziNo=self.browser.find_element(By.CSS_SELECTOR,"a[id='esm_246802192_emi_286053589'] span[class='ui-menuitem-text']").text
                            #gelYaziNo=self.browser.find_element(By.XPATH,"//a[@class='ui-menuitem-link ui-corner-all ui-menuitem-default ui-menuitem-unread ui-menuitem-selected ui-state-highlight']").text
                            self.browser.implicitly_wait(120)
                            time.sleep(4)        
                            gelYaziNoList=str(gelYaziNo).lstrip("Gelen Evraklar ").split("/")
                            gelYaziNom=int(gelYaziNoList[1].rstrip(")"))
                            print(gelYaziNom) 


                            time.sleep(1)

                            daireListe=["Geldiği Yer: Su Yönetimi Genel Müdürlüğü / İzleme ve Su Bilgi Sistemi Daire Başkanlığı","Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Havza Yönetimi Daire Başkanlığı","Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Taşkın ve Kuraklık Yönetimi Daire Başkanlığı","Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Su Kalitesi Daire Başkanlığı"]
                            for i in range(0,(gelYaziNom-4)):
                                time.sleep(1)
                                gelenKonu=self.browser.find_element(By.XPATH,f"//*[@id='mainInboxForm:inboxDataTable:{i}:evrakTable']/tbody/tr[1]/td[2]/div[1]/h3").text        # tüm gelen yazıların konusunu alır
                                self.browser.implicitly_wait(120)
                                print(gelenKonu)

                                gelenKonuJoinSonn=konuCharHarf.konuJoin(gelenKonu)
                                gelenKonuJoindosya=konuCharHarf.dosyaKonu(gelenKonu)
                                gelenKonuJoindosya2=konuCharHarf.harf(gelenKonuJoindosya)



                                time.sleep(1)
                                geldigiYer=self.browser.find_element(By.XPATH,f"//*[@id='mainInboxForm:inboxDataTable:{i}:evrakTable']/tbody/tr[2]/td/div").text        # tüm gelen yazıların geldiği yeri alır
                                self.browser.implicitly_wait(120)
                                print(geldigiYer)
                                time.sleep(1)
                                #gelenSayi=self.browser.find_element(By.XPATH,f"//*[@id='mainInboxForm:inboxDataTable:{i}:evrakTable']/tbody/tr[4]/td/div/span").text
                                if geldigiYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / İzleme ve Su Bilgi Sistemi Daire Başkanlığı":
                                    geldigiYerD="izleme"
                                elif geldigiYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Havza Yönetimi Daire Başkanlığı":
                                    geldigiYerD="havza"
                                elif geldigiYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Taşkın ve Kuraklık Yönetimi Daire Başkanlığı":
                                    geldigiYerD="taşkın"
                                elif geldigiYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Su Kalitesi Daire Başkanlığı":
                                    geldigiYerD="kalite"
                                else:
                                    geldigiYerD="diğer"
                                    
                                
                                print(geldigiYerD)
                                time.sleep(2)

                                print("*********###************")
                                print(gelenKonuJoinSonn)
                                print(nestedKonu)

                                if ((gelenKonuJoinSonn in nestedKonu) or (nestedKonu in gelenKonuJoinSonn)) and (geldigiYer in daireListe):       # kişisel arşivde işlem yapılması istenen yazı konusu ile gelen kutusundaki yazıların konusunu karşılaştırır
                                    self.browser.find_element(By.XPATH,f"//table[@id='mainInboxForm:inboxDataTable:{i}:evrakTable']").click() 
                                    self.browser.implicitly_wait(120)
                                    time.sleep(2)                                                   
                                    print("OK")


                                    self.browser.switch_to.frame("ustYaziOnizlemeId1")  # en sağdaki frame'e iframe id'si ile gitme
                                    self.browser.implicitly_wait(120)
                                    time.sleep(4)
                                    print("OK-frame")                                    
                                    
                                    textim=self.browser.find_elements(By.XPATH,"//*[@id='viewer']/div[1]/div[2]/div")
                                    self.browser.implicitly_wait(120)
                                    #print(textim)
                                    time.sleep(6)
                                    print("OK-textyazi")
                                    #print(textim[12].text)
                                    
                                    

                                    cedMetinListem=[]
                                    for text in textim:
                                        print(text.text)
                                        cedMetinListem.append(text.text)  
                                    time.sleep(3)                 

                                            
                                    ilgiIndex=(cedMetinListem.index("İlgi"))+2  #ilgi yazının sayısını alıp karşılaştırır

                                    time.sleep(3) 
                                    ilgiListe=cedMetinListem[ilgiIndex].split()
                                    ilgiSayiIndexim=""
                                    for z in ilgiListe: # ilgi yazının tarih indexini alır
                                        while z=="tarihli":
                                            tarihIndex=ilgiListe.index("tarihli")-1
                                            print(tarihIndex)
                                            break
                                        while z=="sayılı":  #ilgi yazının sayı indexini alır                        
                                            sayiIndex=ilgiListe.index("sayılı")-1
                                            print(sayiIndex)                    
                                            ilgiSayiIndex=ilgiListe[sayiIndex].split("-")[3]
                                            ilgiSayiIndexim=ilgiSayiIndex
                                            break

                                        print(ilgiSayiIndexim)                        
                                    

                                    if sayiYazi==ilgiSayiIndexim:   # görüş yazısının sayısı ile cevabi yazının ilgisinin sayısını karşılaştırır, aynıysa  
                                        self.browser.implicitly_wait(60)
                                        self.browser.find_element(By.XPATH,"//*[@id='secondaryToolbarToggle']").click() # pencere max değilken sağdaki >> menüyü tıklar
                                        self.browser.implicitly_wait(60)
                                        self.browser.find_element(By.XPATH,"//*[@id='secondaryDownload']").click()  # açılan menüden "indir" seçeneğini tıklayarak yazıyı indirir                    
                                        self.browser.implicitly_wait(60)
                                        time.sleep(10)
                                        os.mkdir(f'C:/Users/tugbacanan.oguz/Desktop/CED/{klasorKayıt}/{geldigiYerD}')  
                                        list_of_files = glob.glob('C:/Users/tugbacanan.oguz/Downloads/*') # * means all if need specific format then *.csv
                                        latest_file = max(list_of_files, key=os.path.getctime)
                                        print(latest_file)
                                        dosyaAdi=str(latest_file).lstrip("C:/Users/tugbacanan.oguz/Downloads/")

                                        ustYazipath=f"C:/Users/tugbacanan.oguz/Desktop/CED/{klasorKayıt}/{geldigiYerD}/{geldigiYerD}.pdf"
                                        shutil.move(f"C:/Users/tugbacanan.oguz/Downloads/{dosyaAdi}", ustYazipath)                    

                                        print("OK")
                                        
                                    self.browser.implicitly_wait(60)
                                    time.sleep(1)
                                    self.browser.execute_script("window.open()")
                                    self.browser.implicitly_wait(120)
                                    self.browser.switch_to.window(self.browser.window_handles[1])   # yeni sekmede belgenet
                                    self.browser.implicitly_wait(120)
                                    self.browser.get("https://e-belge.tarim.gov.tr/edys-web/sistemeGiris.xhtml") 
                                    self.browser.implicitly_wait(60)
                                    self.browser.switch_to.window(self.browser.window_handles[0])
                                    self.browser.implicitly_wait(60)
                                    time.sleep(5)
                                    x=self.browser.find_element(By.XPATH,"//form[@name='mainPreviewForm']//li[5]").text        
                                    self.browser.implicitly_wait(60)
                                    time.sleep(1)
                                    print(x)
                                    if x=="Evrak Ekleri":
                                        self.browser.find_element(By.XPATH,"//form[@name='mainPreviewForm']//li[5]").click()
                                        self.browser.implicitly_wait(60)
                                        ek=self.browser.find_elements(By.XPATH,"//div[@class='ui-datatable ui-widget myLovGrid']//table[@role='grid']//tbody//tr")
                                        self.browser.implicitly_wait(120)
                                        print(len(ek))
                                        for i in range(1,len(ek)+1):
                                            
                                            dosyaText=self.browser.find_element(By.XPATH,f"//div[@class='ui-datatable ui-widget myLovGrid']//table[@role='grid']//tbody//tr[{i}]/td[4]/div[1]/span[1]").text
                                            self.browser.implicitly_wait(60)
                                            self.browser.find_element(By.XPATH,f"//div[@class='ui-datatable ui-widget myLovGrid']//table[@role='grid']//tbody//tr[{i}]/td[5]/button[1]/span[1]").click()  
                                            self.browser.implicitly_wait(60)
                                            time.sleep(10)
                                            print(dosyaText)  
                                            list_of_files2 = glob.glob('C:/Users/tugbacanan.oguz/Downloads/*') # * means all if need specific format then *.csv
                                            latest_file2 = max(list_of_files2, key=os.path.getctime)
                                            print(latest_file2)
                                            dosyaAdi2=str(latest_file2).lstrip("C:/Users/tugbacanan.oguz/Downloads/")

                                            ekPath=f"C:/Users/tugbacanan.oguz/Desktop/CED/{klasorKayıt}/{geldigiYerD}/{dosyaAdi2}"
                                            shutil.move(f"C:/Users/tugbacanan.oguz/Downloads/{dosyaAdi2}", ekPath)              
                                                
                                        print("OK-tüm ekler")  
                                    

                                    else:
                                        print("else") 

                                    self.browser.implicitly_wait(60)         
                                    self.browser.find_element(By.XPATH,f"//*[@id='mainPreviewForm:onizlemeRightTab:uiRepeat:5:cmdbutton'] ").click() # evrak kapat sekmesini tıklar   
                                    self.browser.implicitly_wait(60)
                                    time.sleep(3)
                                    self.browser.find_element(By.XPATH,f"//*[@id='mainPreviewForm:klasorLov_id:favoriteTreeButton']").click()  #favori(yıldız butonu) klasör seç 
                                    self.browser.implicitly_wait(60)
                                    time.sleep(3)
                                    self.browser.find_element(By.XPATH,f"//*[@id='mainPreviewForm:klasorLov_id:lovTree:0']/span/span[3]/div").click()      # klasörü tıkla
                                    self.browser.implicitly_wait(60)
                                    time.sleep(3)
                                    self.browser.find_element(By.XPATH,f"//*[@id='mainPreviewForm:onaysizKapatId']").click()   #evrak kapat butonunu tıklar
                                    self.browser.implicitly_wait(60)  
                                    time.sleep(8) 
                                    print("OK-x")

                                    from datetime import datetime
                                    import locale
                                    locale.setlocale(locale.LC_ALL, '') # local dili ayarlar, böylece aşağıdaki datetime çıktılarını türkçe verir

                                    simdi= datetime.today()
                                    result=datetime.strftime(simdi, "%d.%m.%Y %A") # gün.ay.yıl gün adı formatında bugünün tarihini verir
                                    print(result)



                                    daireListesiKısa=["havza","izleme","taşkın","kalite"]
                                    klasorKayitList=os.listdir(f'C:/Users/tugbacanan.oguz/Desktop/CED/{klasorKayıt}')

                                    a_set = set(daireListesiKısa)
                                    b_set = set(klasorKayitList)

                                    ortakDaire=(a_set & b_set)

                                    if ortakDaire:
                                        print(len(ortakDaire))                        

                                    gorusSayi=len(ortakDaire)

                                    if gorusSayi==4:                          
                                        file=open(f"C:/Users/tugbacanan.oguz/Desktop/Kapatma Listesi.txt","a", encoding="utf-8") # türkçe karakterler de dahil pek çok karakteri tanıması için encoding yapıyoruz
                                        file.write(f"{result}.....{klasorKayıt}.........{geldigiYerD}\n****{gorusSayi} YAZI TAMAMLANDI, cevap yazılabilir...****\n")
                                        file.close()
                                        time.sleep(3) 
                                    else:
                                        file=open(f"C:/Users/tugbacanan.oguz/Desktop/Kapatma Listesi.txt","a", encoding="utf-8") # türkçe karakterler de dahil pek çok karakteri tanıması için encoding yapıyoruz
                                        time.sleep(1)
                                        file.write(f"{result}.....{klasorKayıt}.........{geldigiYerD}(*{gorusSayi})\n")
                                        time.sleep(1)
                                        file.close()


                                    time.sleep(2)


                                    if geldigiYerD=="izleme":
                                        excel=ExcelDosya((int(indexDosyam)+2),10, "")
                                        excel.xSil()

                                    elif geldigiYerD=="havza":
                                        excel=ExcelDosya((int(indexDosyam)+2),11, "")
                                        excel.xSil()

                                    elif geldigiYerD=="taşkın":
                                        excel=ExcelDosya((int(indexDosyam)+2),12, "")
                                        excel.xSil()

                                    elif geldigiYerD=="kalite":
                                        excel=ExcelDosya((int(indexDosyam)+2),13, "")
                                        excel.xSil()
                                    else:
                                        print("hata var")

                                    if gorusSayi==4:
                                        excel=ExcelDosya((int(indexDosyam)+2),17, "")
                                        excel.fillYellow()





                                else: 
                                    print("no match")
                                


                            time.sleep(2)           
                            WebDriverWait(self.browser, 120).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='leftMenuForm:kisiselArsivPanel:kisiselArsivKlasoruTree:0_3']"))).click()   # 3. sıradaki klasörü seçme
                            self.browser.implicitly_wait(60)
                            time.sleep(2)
                            print("*********YENİ YAZI*********")                               
                        else:
                            klasorKayıt=konuDosyaAdi
                            indexDosyam=(dosyaListem2.index(konuDosyaAdi2))+301
                            indexDosya=indexDosyam
                            dosyaMevcutmu=os.path.exists(f'C:/Users/tugbacanan.oguz/Desktop/CEDgorus/{klasorKayıt}')

                            if dosyaMevcutmu==True:
                                print("klasör mevcut")
                            elif dosyaMevcutmu!=True:
                                time.sleep(1)
                                os.mkdir(f'C:/Users/tugbacanan.oguz/Desktop/CEDgorus/{klasorKayıt}')
                                time.sleep(1)
                                print("klasör oluşturuldu")   
                            time.sleep(3)

                            WebDriverWait(self.browser, 60).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='esm_246802192_emi_286053589']"))).click()      # gelen kutusunu tıklar

                            # identify dropdown with Select class
                            time.sleep(4)
                            self.browser.implicitly_wait(60)
                            sel100 = Select(self.browser.find_element_by_xpath("//div[@class='ui-paginator ui-paginator-top ui-widget-header']//select[@name='mainInboxForm:inboxDataTable_rppDD']"))   #sayfada görünen yazı sayısını 100'e çıkarır
                            self.browser.implicitly_wait(120)
                            time.sleep(2)
                            #select by select_by_visible_text() method
                            sel100.select_by_visible_text("100")
                            self.browser.implicitly_wait(60)
                            print("OK-100")
                            time.sleep(4)

                            gelYaziNo=self.browser.find_element(By.CSS_SELECTOR,"a[id='esm_246802192_emi_286053589'] span[class='ui-menuitem-text']").text
                            #gelYaziNo=self.browser.find_element(By.XPATH,"//a[@class='ui-menuitem-link ui-corner-all ui-menuitem-default ui-menuitem-unread ui-menuitem-selected ui-state-highlight']").text
                            self.browser.implicitly_wait(60)
                            time.sleep(2)        
                            gelYaziNoList=str(gelYaziNo).lstrip("Gelen Evraklar ").split("/")
                            gelYaziNom=int(gelYaziNoList[1].rstrip(")"))
                            print(gelYaziNom) 
                            


                            time.sleep(1)

                            daireListe=["Geldiği Yer: Su Yönetimi Genel Müdürlüğü / İzleme ve Su Bilgi Sistemi Daire Başkanlığı","Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Havza Yönetimi Daire Başkanlığı","Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Taşkın ve Kuraklık Yönetimi Daire Başkanlığı","Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Su Kalitesi Daire Başkanlığı"]
                            for i in range(0,(gelYaziNom-2)):
                                time.sleep(1)
                                gelenKonu=self.browser.find_element(By.XPATH,f"//*[@id='mainInboxForm:inboxDataTable:{i}:evrakTable']/tbody/tr[1]/td[2]/div[1]/h3").text        # tüm gelen yazıların konusunu alır
                                self.browser.implicitly_wait(120)
                                print(gelenKonu)

                                gelenKonuJoinSon=konuCharHarf.konuJoin(gelenKonu)



                                time.sleep(1)
                                geldigiYer=self.browser.find_element(By.XPATH,f"//*[@id='mainInboxForm:inboxDataTable:{i}:evrakTable']/tbody/tr[2]/td/div").text        # tüm gelen yazıların geldiği yeri alır
                                self.browser.implicitly_wait(120)
                                print(geldigiYer)
                                time.sleep(1)

                                if geldigiYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / İzleme ve Su Bilgi Sistemi Daire Başkanlığı":
                                    geldigiYerD="izleme"
                                elif geldigiYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Havza Yönetimi Daire Başkanlığı":
                                    geldigiYerD="havza"
                                elif geldigiYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Taşkın ve Kuraklık Yönetimi Daire Başkanlığı":
                                    geldigiYerD="taşkın"
                                elif geldigiYer=="Geldiği Yer: Su Yönetimi Genel Müdürlüğü / Su Kalitesi Daire Başkanlığı":
                                    geldigiYerD="kalite"
                                else:
                                    geldigiYerD="diğer"
                                    
                                
                                print(geldigiYerD)
                                time.sleep(2)



                                if ((gelenKonuJoinSon in gelenKonuJoin) or (gelenKonuJoin in gelenKonuJoinSon)) and (geldigiYer in daireListe):       # kişisel arşivde işlem yapılması istenen yazı konusu ile gelen kutusundaki yazıların konusunu karşılaştırır
                                    self.browser.find_element(By.XPATH,f"//table[@id='mainInboxForm:inboxDataTable:{i}:evrakTable']").click() 
                                    self.browser.implicitly_wait(120)
                                    time.sleep(1)                                                   
                                    print("OK")
                                    self.browser.implicitly_wait(60)
                                    time.sleep(2)
                                    self.browser.switch_to.frame("ustYaziOnizlemeId1")  # en sağdaki frame'e iframe id'si ile gitme
                                    self.browser.implicitly_wait(120)
                                    print("OK-frame")
                                    time.sleep(2)
                                    textim=self.browser.find_elements(By.XPATH,"//*[@id='viewer']/div[1]/div[2]/div")
                                    self.browser.implicitly_wait(120)
                                    #print(textim)
                                    print("OK-textyazi")
                                    #print(textim[12].text)
                                    self.browser.implicitly_wait(60)
                                    time.sleep(2)

                                    cedMetinListem=[]
                                    for text in textim:
                                        print(text.text)
                                        cedMetinListem.append(text.text)  
                                    time.sleep(2)                 

                                            
                                    ilgiIndex=(cedMetinListem.index("İlgi"))+2  #ilgi yazının sayısını alıp karşılaştırır

                                    time.sleep(2) 
                                    ilgiListe=cedMetinListem[ilgiIndex].split()
                                    ilgiSayiIndexim=""
                                    for z in ilgiListe: # ilgi yazının tarih indexini alır
                                        while z=="tarihli":
                                            tarihIndex=ilgiListe.index("tarihli")-1
                                            print(tarihIndex)
                                            break
                                        while z=="sayılı":  #ilgi yazının sayı indexini alır                        
                                            sayiIndex=ilgiListe.index("sayılı")-1
                                            print(sayiIndex)                    
                                            ilgiSayiIndex=ilgiListe[sayiIndex].split("-")[3]
                                            ilgiSayiIndexim=ilgiSayiIndex
                                            break

                                        print(ilgiSayiIndexim)                        
                                    

                                    if sayiYazi==ilgiSayiIndexim:   # görüş yazısının sayısı ile cevabi yazının ilgisinin sayısını karşılaştırır, aynıysa  
                                        self.browser.implicitly_wait(60)
                                        self.browser.find_element(By.XPATH,"//*[@id='secondaryToolbarToggle']").click() # pencere max değilken sağdaki >> menüyü tıklar
                                        self.browser.implicitly_wait(60)
                                        self.browser.find_element(By.XPATH,"//*[@id='secondaryDownload']").click()  # açılan menüden "indir" seçeneğini tıklayarak yazıyı indirir                    
                                        self.browser.implicitly_wait(60)
                                        time.sleep(10)
                                        os.mkdir(f'C:/Users/tugbacanan.oguz/Desktop/CEDgorus/{klasorKayıt}/{geldigiYerD}')  
                                        list_of_files = glob.glob('C:/Users/tugbacanan.oguz/Downloads/*') # * means all if need specific format then *.csv
                                        latest_file = max(list_of_files, key=os.path.getctime)
                                        print(latest_file)
                                        dosyaAdi=str(latest_file).lstrip("C:/Users/tugbacanan.oguz/Downloads/")

                                        ustYazipath=f"C:/Users/tugbacanan.oguz/Desktop/CEDgorus/{klasorKayıt}/{geldigiYerD}/{geldigiYerD}.pdf"
                                        shutil.move(f"C:/Users/tugbacanan.oguz/Downloads/{dosyaAdi}", ustYazipath)                    

                                        print("OK")
                                        
                                    self.browser.implicitly_wait(60)
                                    time.sleep(1)
                                    self.browser.execute_script("window.open()")
                                    self.browser.implicitly_wait(120)
                                    self.browser.switch_to.window(self.browser.window_handles[1])   # yeni sekmede belgenet
                                    self.browser.implicitly_wait(120)
                                    self.browser.get("https://e-belge.tarim.gov.tr/edys-web/sistemeGiris.xhtml") 
                                    self.browser.implicitly_wait(60)
                                    self.browser.switch_to.window(self.browser.window_handles[0])
                                    self.browser.implicitly_wait(60)
                                    time.sleep(5)
                                    x=self.browser.find_element(By.XPATH,"//form[@name='mainPreviewForm']//li[5]").text        
                                    self.browser.implicitly_wait(60)
                                    time.sleep(1)
                                    print(x)
                                    
                                    if x=="Evrak Ekleri":
                                        self.browser.find_element(By.XPATH,"//form[@name='mainPreviewForm']//li[5]").click()
                                        self.browser.implicitly_wait(60)
                                        ek=self.browser.find_elements(By.XPATH,"//div[@class='ui-datatable ui-widget myLovGrid']//table[@role='grid']//tbody//tr")
                                        self.browser.implicitly_wait(120)
                                        print(len(ek))
                                        for i in range(1,len(ek)+1):
                                            #self.browser.find_element(By.XPATH,f"/html[1]/body[1]/div[10]/div[3]/div[1]/form[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[5]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[{i}]/td[5]/button[1]/span[1]").click()
                                            dosyaText=self.browser.find_element(By.XPATH,f"//div[@class='ui-datatable ui-widget myLovGrid']//table[@role='grid']//tbody//tr[{i}]/td[4]/div[1]/span[1]").text
                                            self.browser.implicitly_wait(60)
                                            self.browser.find_element(By.XPATH,f"//div[@class='ui-datatable ui-widget myLovGrid']//table[@role='grid']//tbody//tr[{i}]/td[5]/button[1]/span[1]").click()
                                            
                                            self.browser.implicitly_wait(60)
                                            time.sleep(10)
                                            print(dosyaText)  
                                            list_of_files2 = glob.glob('C:/Users/tugbacanan.oguz/Downloads/*') # * means all if need specific format then *.csv
                                            latest_file2 = max(list_of_files2, key=os.path.getctime)
                                            print(latest_file2)
                                            dosyaAdi2=str(latest_file2).lstrip("C:/Users/tugbacanan.oguz/Downloads/")

                                            ekPath=f"C:/Users/tugbacanan.oguz/Desktop/CEDgorus/{klasorKayıt}/{geldigiYerD}/{dosyaAdi2}"
                                            shutil.move(f"C:/Users/tugbacanan.oguz/Downloads/{dosyaAdi2}", ekPath)              
                                                
                                        print("OK-tüm ekler")  
                                    

                                    else:
                                        print("else") 

                                    self.browser.implicitly_wait(60)         
                                    self.browser.find_element(By.XPATH,f"//*[@id='mainPreviewForm:onizlemeRightTab:uiRepeat:5:cmdbutton'] ").click() # evrak kapat sekmesini tıklar   
                                    self.browser.implicitly_wait(60)
                                    time.sleep(3)
                                    self.browser.find_element(By.XPATH,f"//*[@id='mainPreviewForm:klasorLov_id:favoriteTreeButton']").click()  #favori(yıldız butonu) klasör seç 
                                    self.browser.implicitly_wait(60)
                                    time.sleep(3)
                                    self.browser.find_element(By.XPATH,f"//*[@id='mainPreviewForm:klasorLov_id:lovTree:0']/span/span[3]/div").click()      # klasörü tıkla
                                    self.browser.implicitly_wait(60)
                                    time.sleep(3)
                                    self.browser.find_element(By.XPATH,f"//*[@id='mainPreviewForm:onaysizKapatId']").click()   #evrak kapat butonunu tıklar
                                    self.browser.implicitly_wait(60)  
                                    time.sleep(8) 
                                    print("OK-x")

                                    from datetime import datetime
                                    import locale
                                    locale.setlocale(locale.LC_ALL, '') # local dili ayarlar, böylece aşağıdaki datetime çıktılarını türkçe verir

                                    simdi= datetime.today()
                                    result=datetime.strftime(simdi, "%d.%m.%Y %A") # gün.ay.yıl gün adı formatında bugünün tarihini verir
                                    print(result)



                                    daireListesiKısa=["havza","izleme","taşkın","kalite"]
                                    klasorKayitList=os.listdir(f'C:/Users/tugbacanan.oguz/Desktop/CEDgorus/{klasorKayıt}')

                                    a_set = set(daireListesiKısa)
                                    b_set = set(klasorKayitList)

                                    ortakDaire=(a_set & b_set)

                                    if ortakDaire:
                                        print(len(ortakDaire))                        

                                    gorusSayi=len(ortakDaire)

                                    if gorusSayi==4:                          
                                        file=open(f"C:/Users/tugbacanan.oguz/Desktop/Kapatma Listesi.txt","a", encoding="utf-8") # türkçe karakterler de dahil pek çok karakteri tanıması için encoding yapıyoruz
                                        file.write(f"{result}.....{klasorKayıt}.........{geldigiYerD}\n****{gorusSayi} YAZI TAMAMLANDI, cevap yazılabilir...****\n")
                                        file.close()
                                        time.sleep(3) 
                                    else:
                                        file=open(f"C:/Users/tugbacanan.oguz/Desktop/Kapatma Listesi.txt","a", encoding="utf-8") # türkçe karakterler de dahil pek çok karakteri tanıması için encoding yapıyoruz
                                        time.sleep(1)
                                        file.write(f"{result}.....{klasorKayıt}.........{geldigiYerD}(*{gorusSayi})\n")
                                        time.sleep(1)
                                        file.close()


                                    time.sleep(2)


                                    if geldigiYerD=="izleme":
                                        excel=ExcelDosya((int(indexDosyam)+2),10, "")
                                        excel.xSil()
                                        print("izleme x silindi")

                                    elif geldigiYerD=="havza":
                                        excel=ExcelDosya((int(indexDosyam)+2),11, "")
                                        excel.xSil()
                                        print("havza x silindi")

                                    elif geldigiYerD=="taşkın":
                                        excel=ExcelDosya((int(indexDosyam)+2),12, "")
                                        excel.xSil()
                                        print("taşkın x silindi")

                                    elif geldigiYerD=="kalite":
                                        excel=ExcelDosya((int(indexDosyam)+2),13, "")
                                        excel.xSil()
                                        print("kalite x silindi")
                                    else:
                                        print("hata var")

                                    if gorusSayi==4:
                                        excel=ExcelDosya((int(indexDosyam)+2),17, "")
                                        excel.fillYellow()




                                time.sleep(3) 
                                


                            time.sleep(2)           
                            WebDriverWait(self.browser, 60).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='leftMenuForm:kisiselArsivPanel:kisiselArsivKlasoruTree:0_3']"))).click()   # 3. sıradaki klasörü seçme
                            self.browser.implicitly_wait(60)
                            time.sleep(2)
                            print("*********YENİ YAZI*********")    



belge = Belgenet(username,password)
belge.signIn()
belge.letter()
