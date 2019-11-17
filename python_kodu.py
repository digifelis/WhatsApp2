# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import datetime
import time
import urllib.request, json
import requests
from binascii import a2b_base64
import base64
import os

panel_adresi = "http://website.address"
istemci_adi = "Mansur"
istemci_tel_no = ""
#token = ""
token = ""
user_id = "1"

# user id için indirilen fotoların geçici olarak kaydedileceği klasör oluşturma
if not os.path.exists(user_id):
    os.makedirs(user_id)


# bu prosedür silinecek
def KarakodOkuma(user_id):
    try:
        driver = webdriver.Chrome()
    except:
        driver = webdriver.Firefox()

    time.sleep(1)
    print(" [*] Starting attacker session...")
    try:
        driver.get('https://web.whatsapp.com/')
        time.sleep(1)
    except:
        print(" [!] Error Check your internet connection")
        time.sleep(1)

    while True:
        try:
            button = driver.find_element_by_class_name('qr-button')
            print(" [*] Idle detected, Reloading QR code image (Good job WhatsApp)...")
            button._execute(webdriver.remote.command.Command.CLICK_ELEMENT)
            time.sleep(1)
        except:
            pass

        try:
            img = driver.find_elements_by_tag_name('img')[0]
            src = img.get_attribute('src').replace("data:image/png;base64,", "")
            print(" [*] QR code image detected !")
            print(" [*] Downloading the image...")
            binary_data = a2b_base64(src)
            qr = open(user_id + ".png", "wb")
            qr.write(binary_data)
            print(" [*] Saved To tmp.png")
            qr.close()
            time.sleep(5)
            continue
        except:
            break


def yazi_temizle(yazi):
    text = yazi.split('<br />')
    x = ''
    for i in text:
        if len(i) > 0:
            x = x + ' ' + i
    return x


def veri_getir(panel_adresi):
    with urllib.request.urlopen(panel_adresi + "/wp/wp1.php?operator=1") as url:
        data = json.loads(url.read().decode('utf-8-sig'))
        if len(data) > 0:
            x = 0
            while x < len(data):
                yazi = data[x].split('|')
                send_whatsapp_msg(yazi[1], yazi_temizle(yazi[2]), yazi[0], yazi[3])
                x = x + 1


def veri_duzelt(bilgi, panel_adresi):
    urllib.request.urlopen(panel_adresi + "/wp/wp_durum.php?bilgi=" + bilgi)


def zaman(bilgi):
    an = datetime.datetime.now()
    tarih = datetime.datetime.strftime(an, '%c')
    print(tarih + "-" + bilgi)


def element_presence(by, xpath, time):
    element_present = EC.presence_of_element_located((By.XPATH, xpath))
    WebDriverWait(driver, time).until(element_present)


def dosya_link(panel_adresi, veri):
    link = panel_adresi + '/wp/dosya.php?d=' + veri
    return link


def send_whatsapp_msg(phone_no, text, veri_id, dosya):
    driver.get("https://web.whatsapp.com/send?phone={}&source=&data=#".format(phone_no))
    try:
        driver.switch_to_alert().accept()
    except Exception as e:
        pass

    try:
        element_presence(By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]', 30)
        txt_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        #txt_box = driver.find_element_by_class_name('_3u328')
        txt_box.send_keys(text)
        txt_box.send_keys("\n")
        if dosya != '':
            a = dosya.split(',')
            for i in a[:len(a) - 1]:
                b = i.split('#')
                #txt_box.send_keys(dosya_link(panel_adresi, b[2]))
                ''' dosya gönderme kodları yeni olan '''
                dosya_indir(panel_adresi, b[2])
                dosya_gonder(b[2])

                #time.sleep(3)
                #txt_box.send_keys("\n")

        veri_duzelt(veri_id, panel_adresi)
    except Exception as e:
        print("invailid phone no :" + str(phone_no) + e)

'''
sayfa değiştirmeden kullanıcı adını bularak mesaj gönderme bölümü
düzeltilecek daha bitmedi
'''
def send_whatsapp_msg_yeni(phone_no, text, veri_id, dosya):
    try:
        user = driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/input'.format(phone_no))
        user = driver.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div[1]/div/div')
        user.click()
        txt_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        txt_box.send_keys(text)
        txt_box.send_keys("\n")
        if dosya != '':
            a = dosya.split(',')
            for i in a[:len(a) - 1]:
                b = i.split('#')
                txt_box.send_keys(dosya_link(panel_adresi, b[2]))
                time.sleep(3)
                txt_box.send_keys("\n")

        veri_duzelt(veri_id, panel_adresi)
    except Exception as e:
        print("invailid phone no :" + str(phone_no) + e)
''' dosya gönderme. kişi seçili iken verilen dosyayı gönderir dosya uzantısına göre resim yada belge yollayacak'''
def dosya_gonder(filepath):
    attachment_box = driver.find_element_by_xpath('//div[@title = "Attach"]')
    attachment_box.click()
    image_box = driver.find_element_by_xpath('//input[@accept="*"]')
    image_box.send_keys(os.getcwd() + "\/" + filepath )
    time.sleep(3)
    send_button = driver.find_element_by_xpath('//span[@data-icon="send-light"]')
    send_button.click()
'''dosya indirme '''
def dosya_indir(panel_adresi,url):
    r = requests.get(panel_adresi+ '/attachments/'+ url)
    with open('./' + url, 'wb') as f:
        f.write(r.content)
########################################################################
def karakter_temizleme(metin):
    liste = {"ı": "i",
             "I": "i",
             "Ç": "c",
             "ç": "c",
             " ": "-",
             "ş": "s",
             "Ş": "s",
             "Ğ": "g",
             "ğ": "g",
             "Ü": "u",
             "ü": "u",
             "Ö": "o",
             "ö": "ö",
             "İ": "i"}
    for karakter in liste:
        metin = metin.replace(karakter, liste[karakter])
    return metin.lower()


def api_cevap(adres, trackingid, mesaj, token):
    icerik = {
        "email": "mansur@siirt.edu.tr",
        "trackingId": trackingid,
        "message": mesaj,
        "html": "false",
        "ip": "127.0.0.1"
    }
    r = requests.post(adres, json=icerik, headers={'X-AUTH-TOKEN': token})
    return r.text


def api_gonder(adres, isim, mesaj, token):
    icerik = {
        "name": isim,
        "email": "mansur@siirt.edu.tr",
        "priority": 2,
        "category": 1,
        "subject": isim + "  WhatsApp",
        "message": mesaj,
        "html": "false",
        "userAgent": "SomeRESTClient",
        "language": "English"

    }
    r = requests.post(adres, json=icerik, headers={'X-AUTH-TOKEN': token})
    # print(r.status_code)
    return r.text


def api_ticket(trackingid, adres, token):
    url = adres
    querystring = {"trackingId": trackingid}
    response = requests.request("GET", url, params=querystring, headers={'X-AUTH-TOKEN': token})
    return response.text


def veri_getir1(tel, panel_adresi):
    with urllib.request.urlopen(panel_adresi + "/wp/durum_sorgula.php?tel=" + tel) as url:
        data = json.loads(url.read().decode('utf-8-sig'))
        # print(len(data))
        if len(data) > 0:
            x = 0
            sonuc = ""
            while x < len(data):
                sonuc = data[x]
                x = x + 1
    return sonuc


def get_file_content_chrome(driver, uri):
    result = driver.execute_async_script("""
    var uri = arguments[0];
    var callback = arguments[1];
    var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'arraybuffer';
    xhr.onload = function(){ callback(toBase64(xhr.response)) };
    xhr.onerror = function(){ callback(xhr.status) };
    xhr.open('GET', uri);
    xhr.send();
    """, uri)
    if type(result) == int:
        raise Exception("Request failed with status %s" % result)
    return base64.b64decode(result)


def dosya_yukleme(panel_adresi, trakingid, dosya, mesaj):
    values = {'ticketid': trakingid, 'mesaj': mesaj}
    with open(dosya, 'rb') as f:
        r = requests.post(panel_adresi + '/wp/dosya_yukleme.php', files={'dosya': f}, data=values)
    return r.text


''' okuma bölümü kodları başlangıcı'''


def yeni_gelen(istemci_adi, panel_adresi, token):
    istemciler = {istemci_adi}  # A dictionary that stores all the users that sent activate bot
    resimler = []
    resim_varmi = 0
    unread = driver.find_elements_by_class_name("P6z4j")  # The green dot tells us that the message is new  # _1ZMSM
    name, message = '', ''
    if len(unread) > 0:
        ele = unread[-1]
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(ele, 0, -20)  # move a bit to the left from the green dot
        print("yeni gelen mesaj sayısı " + ele.text)
        if ele.text == '':
            yeni_mesaj_sayisi = 1
        else:
            yeni_mesaj_sayisi = int(ele.text)
        # Clicking couple of times because sometimes whatsapp web responds after two clicks
        try:
            action.click()
            action.perform()
            action.click()
            action.perform()
        except Exception as e:
            pass
        time.sleep(2)
        toplam_mesaj = ""
        resim1 = ""

        if driver.find_elements_by_class_name("_19RFN"):
            name = driver.find_element_by_class_name("_19RFN").text  # Contact name # copyable-text
            # print(len(driver.find_elements_by_class_name("vW7d1")))
            mesaj_sayisi = len(driver.find_elements_by_class_name("FTBzM"))
            print("mesaj sayısı : " + str(mesaj_sayisi))
            print("yeni mesaj sayisi : " + str(yeni_mesaj_sayisi))
            print("name bilgisi :" + name)
            x = 1
            # baloncuk içerisindeki sayı kadar son mesajı okuyor
            if yeni_mesaj_sayisi > 0:
                while x <= yeni_mesaj_sayisi:
                    message = driver.find_elements_by_class_name("FTBzM")[-x]  # the message content
                    if message.find_elements_by_class_name("selectable-text"):
                        # message.find_element_by_class_name("selectable-text")
                        message1 = message.find_element_by_class_name("selectable-text").text
                        gonderen = message.find_element_by_class_name("copyable-text")
                        gonderen1 = gonderen.get_attribute('data-pre-plain-text')
                        name1 = gonderen1.split(']')
                        name2 = name1[1].split(':')
                        name3 = name2[0].strip()
                        name = name3
                        print('ilk' + name + '---' + message1 + '---' + gonderen1 + '---')
                    else:
                        message1 = ""
                        gonderen1 = "1sallama birşeyler sonra burayı düzeltirim +90 555 999 88 77"

                    # resim varmı kontrol
                    if message.find_elements_by_class_name("_18vxA"):  # _1JVSX
                        resim = message.find_element_by_class_name("_18vxA")
                        resim1 = resim.get_attribute("src")
                        print("resim bilgisi : " + "---" + str(resim1))
                        bytes = get_file_content_chrome(driver, str(resim1))
                        # print(bytes)
                        # şimdilik jpg alıyorum. diğer resim formatlarında afallıyor.
                        file_name = "./" + user_id + "/" + str(x) + ".jpg"
                        userImage = open(file_name, "wb")
                        resimler.append(file_name)
                        userImage.write(bytes)
                        userImage.close()
                        resim_varmi = 1
                    else:
                        print("resim yok 1")
                        resim_varmi = 0

                    toplam_mesaj = message1 + ' <br> ' + toplam_mesaj
                    x = x + 1

        if len(toplam_mesaj) == 0:
            toplam_mesaj = toplam_mesaj + "ek dosya"
        name = karakter_temizleme(name)
        durum = veri_getir1(name, panel_adresi)
        durum1 = durum.split('|')
        print(durum)

        if durum1[0] == '0':
            # yeni ticket oluştur ve vt ye traking bilgilerini kaydet
            ticket_olustur = api_gonder(panel_adresi + '/api/index.php/v1/tickets', name, toplam_mesaj, token)
            print(ticket_olustur)
            j = json.loads(ticket_olustur)
            if 'type' in j:
                print("hata oluştu1")
            else:
                parametre = 'islem=yeni&t_id=' + str(j['id']) + '&trackingid=' + j['trackingId'] + '&tel=' + j[
                    'name'] + '&durum=acik'
                print(parametre)
                print("ilk defa iletişim")
                urllib.request.urlopen(panel_adresi + "/wp/track_ekle.php?" + parametre)
                if resim_varmi == 1:
                    for i in resimler:
                        sonuc = dosya_yukleme(panel_adresi, j['trackingId'], i, toplam_mesaj)
                        os.unlink(i)
                        print(sonuc)
        elif durum1[0] == 'kapali':
            # ticket kapalıdır yeni ticket oluştur ve vt ye tracking bilgilerini kaydet
            ticket_olustur = api_gonder(panel_adresi + '/api/index.php/v1/tickets', name, toplam_mesaj, token)
            j = json.loads(ticket_olustur)
            if 'type' in j:
                print("hata oluştu2")
            else:
                urllib.request.urlopen(
                    panel_adresi + "/wp/track_ekle.php?islem=yeni&t_id=" + str(j['id']) + '&trackingid=' + j[
                        'trackingId'] + '&tel=' + j['name'] + '&durum=acik')
                print("ticket kapalı yenisi oluşturuldu")
                if resim_varmi == 1:
                    for i in resimler:
                        sonuc = dosya_yukleme(panel_adresi, j['trackingId'], i, toplam_mesaj)
                        os.unlink(i)
                        print(sonuc)
        elif durum1[0] == 'acik':
            # durum1[2] bilgisine göre api kullanarak cevap ekle
            adres = panel_adresi + '/api/index.php/v1/tickets/' + str(durum1[1]) + '/replies'
            pinli_olana_tikla()
            ticket_olustur = api_cevap(adres, durum1[2], toplam_mesaj, token)
            print(ticket_olustur)
            print("ticket var ve açık cevap yazıldı")
            if resim_varmi == 1:
                for i in resimler:
                    sonuc = dosya_yukleme(panel_adresi, durum1[2], i, toplam_mesaj)
                    os.unlink(i)
                    print(sonuc)
        else:
            print("işlem yok")
        # print('api bilgisi : ' + ticket_olustur)


# tarayıcıyı başlat
driver = webdriver.Chrome(executable_path="chromedriver.exe")

# adrese git
driver.get('https://web.whatsapp.com/')
# driver.get('https://api.whatsapp.com/send?phone='+istemci_tel_no+'&text=test mesajı')



def karekod(user_id):
    try:
        img = driver.find_elements_by_tag_name('img')[0]
        src = img.get_attribute('src').replace("data:image/png;base64,", "")
        # print(" [*] QR bulundu !")
        # print(" [*] resim indiriliyor...")
        binary_data = a2b_base64(src)
        qr = open(str(user_id) + "_karekod.png", "wb")
        qr.write(binary_data)
        # print(" [*] Saved To tmp.png")
        qr.close()
        time.sleep(5)
        return True
    except:
        return False


def karekod_yukle(durum, user_id):
    values = {'durum': durum, 'user_id': user_id}
    with open(user_id + '_karekod.png', 'rb') as f:
        r = requests.post(panel_adresi + '/wp/karekod.php', files={'dosya': f}, data=values)
    return r.text


def giris_kontrol():
    if (driver.find_elements_by_class_name('_3Jvyf')):
        return True
    if (driver.find_elements_by_class_name('_1pw2F')):
        return False

def kara_liste_sil(url):
    response = requests.request("GET", url+'/wp/kara_liste.php')
    return response

def pinli_olana_tikla():
    #attachment_box = driver.find_element_by_xpath('//span[@data-icon = "pinned"]')
    attachment_box = driver.find_element_by_xpath('//div[@class="_1ZMSM"]')
    attachment_box.click()
    attachment_box.click()
    attachment_box.click()
    attachment_box.click()




a = datetime.datetime.now()
try:
    while True:
        b = datetime.datetime.now()
        c = b - a
        if giris_kontrol() == False:
            if int(c.seconds) > 5:
                karekod('1')
                cevap = karekod_yukle('0', user_id)
                #print(cevap)
                #print("karekod gonderildi")
                a = datetime.datetime.now()
        if giris_kontrol() == True:
            kara_liste_sil(panel_adresi)
            veri_getir(panel_adresi)
            if int(c.seconds) > 15:
                cevap = karekod_yukle('1', user_id)
                #print(str(datetime.datetime.now()) + '  kare kod yükleme verisi : '+cevap)
                # gelen kontrolü
                yeni_gelen(istemci_adi, panel_adresi, token)
                #pinli_olana_tikla()
                a = datetime.datetime.now()
        #time.sleep(15)
except KeyboardInterrupt:
    print("hata uretti")
    pass
