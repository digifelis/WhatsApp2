# WhatsApp2
WhatsApp ile tek numaranın çoklu kullanıcı ile kullanılması.

Kurulum Adımları

1)
hesk284.zip dosyası ile Hesk kurulumu yapılır.
https://www.hesk.com/

2)
2019.1.0.zip dosyası ile Hesk Mod yüklemesi yapılır.
https://www.mods-for-hesk.com/

3)
wp_hesk.zip dosyasında bulunan dosyalar hesk kurulumu üzerine gönderilir.


4)
zadmin_destekyeni.sql dosyası içerisindeki VT tabloları oluşturulur.
tablo isimleri verilirken hesk kurulumundaki prefix kullanılarak oluşturulmalıdır.

5)
wp_hesk\wp içerisnde bulunan vt.php dosyasındaki bilgiler hesk_settings.inc.php dosyası ile uyumlu olmalıdır.
özellikle prefix bilgisine dikkat edilmelidir.

6)
python_kodu.py dosyası kütüphaneleri yüklü bir sunucuda çalıştırılır. PyCharm tavsiye edilir.
Dosya içerisinde panel_adresi hesk sisteminin yüklü olduğu adres olmalıdır.
token Bilgisi Hesk sistemi çerisinde oluşturulup burada belirtilmelidir.


Ek bilgi ve Destek için mansur[at]siirt.edu.tr adresini kullanabilirsiniz.





Use single number with WhatsApp with multiple users.

Installation Steps 

1) Hesk is installed with hesk284.zip file. https://www.hesk.com/

2) The Hesk Mode installation is done with the 2019.1.0.zip file. https://www.mods-for-hesk.com/

3) The files in the wp_hesk.zip file are sent to the account setup.

4) The DB tables in the zadmin_support new.sql file are created. the table names must be created using prefix in the account setup.

5) The information in the vt.php file in wp_hesk \ wp must match the hesk_settings.inc.php file. especially prefix information should be paid attention.

6) The python_code.py file is run on a server with libraries installed. PyCharm is recommended. In the file, panel_adres must be the address where the account system is installed. token Information must be created and specified here within the account system.

For additional information and support, please contact mansur [at] siirt.edu.tr.
