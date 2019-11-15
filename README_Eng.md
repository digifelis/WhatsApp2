Use single number with WhatsApp with multiple users.

Installation Steps 1) Hesk is installed with hesk284.zip file. https://www.hesk.com/

The Hesk Mode installation is done with the 2019.1.0.zip file. https://www.mods-for-hesk.com/

The files in the wp_hesk.zip file are sent to the account setup.

The VT tables in the zadmin_support new.sql file are created. the table names must be created using prefix in the account setup.

The information in the vt.php file in wp_hesk \ wp must match the hesk_settings.inc.php file. especially prefix information should be paid attention.

The python_code.py file is run on a server with libraries installed. PyCharm is recommended. In the file, panel_address must be the address where the account system is installed. token Information must be created and specified here within the account system.

For additional information and support, please contact mansur [at] siirt.edu.tr.
