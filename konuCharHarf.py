#NOTES
# Konu:, char(full) ve boşluk kaldırma(harf)--------> konuJoin
# Konu:, char(ful) ve ilk 10 kelime dosya adı için ------->dosyaKonu


def konuRemove(konuJoined):
# Kelimeleri ayırıp liste yapar, "Konu:"'yu listeden çıkarıp tekrar listeyi str çevirir.
    konuYazim=str(konuJoined).split()
    konuYazim.remove("Konu:")
    joinKonuSon=" ".join(konuYazim)

def konuJoin(konuJoined):
# Kelimeleri ayırıp liste yapar, "Konu:"'yu listeden çıkarıp tekrar listeyi str çevirir.
    konuYazim=str(konuJoined).split()
    konuYazim.remove("Konu:")
    joinKonuSon=" ".join(konuYazim)


# Konudaki belli karakterleri kaldırır, yerine boşluk koyar
    karakter=[]
    for char in '?\/:*"><|-,':  
        if char in joinKonuSon:
            #print(f"{char} konuda var")
            karakter.append(char)


    konuYazim=[]
    for item in joinKonuSon:
        konuYazim.append(item)
    #print(konuYazim)

    for kar in karakter:
        for i in konuYazim:
            if kar==i:
                indexKar=konuYazim.index(kar)
                konuYazim.pop(indexKar)
                konuYazim.insert(indexKar," ")

# tüm konudaki boşlukları kaldırır, lowercase yapar
    gelenHarfListe=[]
    for harf in konuYazim:
        if harf!=" ":
            gelenHarfListe.append(harf)
    #print(gelenHarfListe)
    gelenKonuJoin=("".join(gelenHarfListe)).lower()
    return gelenKonuJoin

def dosyaKonu(konuJoined):
    konuYazim=str(konuJoined).split()
    konuYazim.remove("Konu:")
    joinKonuSon=" ".join(konuYazim)
      

    karakter=[]
    for char in '?\/:*"><|-,':  
        if char in joinKonuSon:
            #print(f"{char} konuda var")
            karakter.append(char)
    for char in "'":  
        if char in joinKonuSon:
            #print(f"{char} konuda var")
            karakter.append(char)


    konuYazim=[]
    for item in joinKonuSon:
        konuYazim.append(item)
    #print(konuYazim)

    for kar in karakter:
        for i in konuYazim:
            if kar==i:
                indexKar=konuYazim.index(kar)
                konuYazim.pop(indexKar)
                konuYazim.insert(indexKar," ")
                #print(indexKar)
                #print(kar)
    #print(konuYazim)
    
    joinKonuYazim="".join(konuYazim)

    konuDosya=joinKonuYazim.split()
    indexKonu=(len(konuYazim))-1
    if indexKonu>10:  
        konuDosyam=konuDosya[0:11]          
        konuDosyaAdi=" ".join(konuDosyam)
    elif indexKonu<=10:  
        konuDosyam=" ".join(konuDosya)        
        konuDosyaAdi=str(konuDosyam)
    if konuDosyaAdi.endswith("."):
        konuDosyaAdi=konuDosyaAdi.rstrip(".")

    return konuDosyaAdi #RN 20057221 ve RN 20066839 No'lu IV. Grup Demir-Bakır Ocağı, Kırma-Eleme-Öğütme

def harf(konuYazim):
    gelenHarfListe=[]
    for harf in konuYazim:
        if harf!=" ":
            gelenHarfListe.append(harf)

    #print(gelenHarfListe)
    gelenKonuJoin=str("".join(gelenHarfListe)).lower()
    return gelenKonuJoin






def char (karak):
    karakter=[]
    for char in "'":  
        if char in karak:

            karakter.append(char)


    karakListe=[]
    for item in karak:
        karakListe.append(item)
    #print(konuYazim)

    for kar in karakter:
        for i in karakListe:
            if kar==i:
                indexKar=karakListe.index(kar)
                karakListe.pop(indexKar)
                karakListe.insert(indexKar,"")

    joinKonuYazim="".join(karakListe)
    return joinKonuYazim