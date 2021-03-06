nach talk-python course data-driven-web-app-with-flask ch15

Linode zum laufen bringen
========================= 
ein Ubuntu Betriebssystem installieren  
Zugang vom Terminal über Normalnutzer  
Zugang als root mit sudo bzw. su  

Server Verzeichnis erstellen
============================

server  
    pypi.nginx  
    pypi.service  
    server_setup.sh  
    
 von git@github.com:butayama/data-driven-web-apps-with-flask.git
 ins Hauptverzeichnis der App kopieren 
 
für das App Verzeichnis den user und die group von root auf uwe setzen    

sudo chown -R uwe:uwe <App-Verzeichnis>

installieren der Firewall ufw:  
https://www.linode.com/docs/security/firewalls/configure-firewall-with-ufw/  
https://linuxize.com/post/how-to-setup-a-firewall-with-ufw-on-ubuntu-18-04/  

(3.8.1/envs/flasky) ➜  flasky git:(linode-deploy) ✗ sudo ufw status               
Status: active


 To | Action | From  
--- | ------ | ----
22/tcp | ALLOW | Anywhere
OpenSSH | ALLOW | Anywhere                  
5000 | ALLOW  | Anywhere                  
80/tcp | ALLOW  | Anywhere                  
443/tcp | ALLOW  | Anywhere                  
22/tcp (v6) | ALLOW  | Anywhere (v6)             
OpenSSH (v6) | ALLOW  | Anywhere (v6)             
5000 (v6) | ALLOW  | Anywhere (v6)             
80/tcp (v6) | ALLOW  | Anywhere (v6)             
443/tcp (v6) | ALLOW  | Anywhere (v6)

nicht vergessen die sqlite Datenbankdatei (data.sqlite) und die Environment Datei (.env) ins Hauptverzeichnis zu kopieren.  
Das geht gut mit FileZilla

Datenbank einrichten:  

history | Command
------- | -------
  889 | export FLASKY_APP=flasky.py
  890 | flask shell
  
Anwendung starten mit 

history | Command
------- | -------
  886 | cd flasky
  887 | gunicorn --workers=3 flasky:app
  
gunicorn kann im Terminal in welchem es gestartet wurde mit ^C beendet werden  
  
Passwort an User vergeben:

flask shell  
 from flasky import db  
 user_role = Role.query.filter_by(name='User').first()  
 users = user_role.users  
 User.query.all()  
[<User 'hpi5'>, <User 'uwe'>, <User 'lorenz'>, <User 'sabine'>]  
 user_lorenz = User.query.filter_by(username='lorenz').first()  
 user_lorenz.password = '********'  
 user_lorenz.email = '********@***.de'  

 user_lorenz = User.query.filter_by(username='lorenz').first()  
 user_lorenz.password = '9SEQm6Pp'  
 user_lorenz.email = 'lolo.p10@web.de'  
 user_sabine = User.query.filter_by(username='sabine').first()  
 user_sabine.email = 'sabine.schweinsberg@t-online.de'  
 user_sabine.password = '8SEQm6Pp'  
 db.session.add_all([user_lorenz, user_sabine])    
 db.session.commit()    

hat beim Einloggen mit lolo.p10@web.de nicht funktioniert.

Einrichten und starten von **Supervisord**  
https://serversforhackers.com/c/monitoring-processes-with-supervisord  

Konfigurationsdatei osteotomy.conf im Verzeichnis:  
/etc/supervisor/conf.d  

[program:osteotomy]  
command=/home/uwe/.pyenv/shims/gunicorn --workers=3 flasky:app  
directory=/home/flasky  
autostart=true  
autorestart=true  
startretries=3  
stderr_logfile=/home/log/webhook/osteotomy.err.log  
stderr_logfile=/home/log/webhook/osteotomy.out.log  
user=uwe  
environment=FLASKY_APP='flasky.py',FLASK_CONFIG='linode' 

Controlling Processes with Supervisord  
read the configuration in and then reload Supervisord, using the supervisorctl tool:

$ sudo supervisorctl reread  
$ sudo supervisorctl update

Our Node process should be running now. We can check this by simply running supervisorctl:

$ sudo supervisorctl

SSH Certificate with  
https://certbot.eff.org/lets-encrypt/debianstretch-nginx  
### sudo certbot --nginx

Um Sicherungskopien zu erstellen kann FileZilla verwandt werden.  
Falls die zu sichernden Dateien in einem root Verzeichnis liegen sind sie zuvor von der Shell aus in /hom/uwe/temp Ordner zu kopieren.  

# gunicorn erfolgreich gestartet
## mit ^C gestoppt
mit   
gunicorn --workers=3 flasky:app  
neu gestartet funktioniert für http://139.162.152.56/ und theaterfreak.de


## start nach reboot mit osteotomy.conf

[program:osteotomy]
/# command=/etc/init.d/apache2 stop
command=/home/uwe/.pyenv/shims/gunicorn --workers=3 flasky:app
directory=/home/flasky
autostart=true
autorestart=true
startretries=3
stderr_logfile=/home/log/webhook/osteotomy.err.log
stderr_logfile=/home/log/webhook/osteotomy.out.log
user=uwe
environment=FLASKY_APP='flasky.py',FLASK_CONFIG='linode'


bei Eingabe von http://139.162.152.56/ und theaterfreak.  
_** in einem neuen Firefox Tab**_   
läuft die app 

bei Eingabe von ostheotomy.de,  http://osteotomy.de/
_** in einem neuen Firefox Tab**_   
kommt die Fehlermeldung:  
403 Forbidden
nginx  

# Abarbeiten der Liste von 
https://www.scalescale.com/tips/nginx/403-forbidden-nginx/  
## Set 755 permissions from the shell, using chmod 755 /path/of/your/directory/ -v  
Eingabe in /home/:  
chmod -R 755 flasky -v  

Fehlermeldung nicht beseitigt. 

## Directory restrictions by IP and 403 Forbidden error

Check your nginx.conf file, or your sites nginx .conf file in case you have an allow/deny rule that may be blocking your network  

All NGINX configuration files are located in the /etc/nginx/ directory. The primary configuration file is /etc/nginx/nginx.conf.  

kein **deny** in nginx.conf gefunden  

## Lack of index files and 403 Forbidden error

When you don’t have any files uploaded named as ‘index’ (it could be index.php, index.html, index.shtml, etc) this is a common reason it will show a 403 Forbidden error.  
File app/templates/index.html vorhanden


## Autoindex is off

If you don’t have any index file, but also have autoindex off set at Nginx config, you will have to turn it on using this method:
autoindex nicht in nginx.conf gefunden.  


# https://www.linode.com/docs/web-servers/nginx/how-to-configure-nginx/  

File: `/etc/nginx/nginx.conf `

File: `/etc/nginx/conf.d/139.162.152.56.conf`  

server {
    # listen         80 default_server;
    listen         [::]:80 default_server;
    server_name    139.162.152.56 www.139.162.152.56;
    root           /home/flasky;
    index          index.html;

    gzip             on;
    gzip_comp_level  3;
    gzip_types       text/plain text/css application/javascript image/*;
}

modifiziert zu:

server {
        listen 80 default_server;
        listen [::]:80 default_server;

        # SSL configuration
        #
        listen 443 ssl default_server;
        listen [::]:443 ssl default_server;
}



File: `/etc/nginx/sites-enabled/flaskapp`

server {
    server_name    osteotomy.de *.osteotomy.de;
    root           /home/flasky;
    index          index.html;    

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

File: `/etc/nginx/sites-available/default`

## Nach Modigfikation ohne reboot Verhalten wie vor der Modifikation
## Nach Modigfikation mit reboot folgendes Verhalten:


bei Eingabe von http://139.162.152.56/ und theaterfreak.  
_**homepage index.html wird nicht gefunden**_   
`Welcome to nginx!

If you see this page, the nginx web server is successfully installed and working. Further configuration is required.

For online documentation and support please refer to nginx.org.  
Commercial support is available at nginx.com.  

Thank you for using nginx.`

bei Eingabe von ostheotomy.de,  http://osteotomy.de/
_** Hompage wird gefunden**_   
keine https Verbindung!


# File: `/etc/nginx/conf.d/139.162.152.56.conf`  
modifiziert zu:  

server {
        listen         80 default_server;  
        listen         [::]:80 default_server;  
        server_name    139.162.152.56 www.139.162.152.56;  

        # SSL configuration
        #
        listen 443 ssl default_server;
        listen [::]:443 ssl default_server;
}

## Nach Modigfikation mit reboot folgendes Verhalten:


bei Eingabe von http://139.162.152.56/ und theaterfreak.  
_**homepage index.html wird nicht gefunden**_   
`Welcome to nginx!

If you see this page, the nginx web server is successfully installed and working. Further configuration is required.

For online documentation and support please refer to nginx.org.  
Commercial support is available at nginx.com.  

Thank you for using nginx.`

bei Eingabe von ostheotomy.de,  http://osteotomy.de/
_** Apache2 Debian Default Page**_   
keine https Verbindung!

# File: /etc/nginx/conf.d/139.162.152.56.conf  
 
server {
        listen         80 default_server;
        listen         [::]:80 default_server;

        # SSL configuration
        #
        listen 443 ssl default_server;
        listen [::]:443 ssl default_server;
}


# File: `/etc/nginx/sites-enabled/flaskapp`

server {
    server_name    osteotomy.de *.osteotomy.de 139.162.152.56 *.139.162.152.56;
    root           /home/flasky;
    index          index.html;    

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

## Nach Modigfikation mit reboot folgendes Verhalten:


bei Eingabe von http://139.162.152.56/ und theaterfreak.  
_**homepage index.html wird nicht gefunden**_   
`Welcome to nginx!

If you see this page, the nginx web server is successfully installed and working. Further configuration is required.

For online documentation and support please refer to nginx.org.  
Commercial support is available at nginx.com.  

Thank you for using nginx.`

bei Eingabe von ostheotomy.de,  http://osteotomy.de/
_** wie bei theaterfreak.de**_   
keine https Verbindung!

# https://nginx.org/en/docs/beginners_guide.html

(3.8.1/envs/flasky) ➜  flasky git:(linode-deploy) ✗ cd /etc/nginx/conf.d
(3.8.1/envs/flasky) ➜  conf.d ls
139.162.152.56.conf  139.162.152.56.conf.save  139.162.152.56.conf.save.1
(3.8.1/envs/flasky) ➜  conf.d sudo rm *.save*

`(3.8.1/envs/flasky) ➜  flasky git:(linode-deploy) ✗ sudo nginx -s quit  
[sudo] password for uwe:   
nginx: [warn] conflicting server name "osteotomy.de" on 0.0.0.0:80, ignored`  

`sudo nginx -s reload  
nginx: [warn] conflicting server name "osteotomy.de" on 0.0.0.0:80, ignored  
nginx: [error] open() "/run/nginx.pid" failed (2: No such file or directory)  
(3.8.1/envs/flasky) ➜  flasky git:(linode-deploy) ✗ cd /etc/nginx/sites-enabled  
(3.8.1/envs/flasky) ➜  sites-enabled ls  
flaskapp  flaskapp.old  
(3.8.1/envs/flasky) ➜  sites-enabled sudo rm flaskapp.old   
(3.8.1/envs/flasky) ➜  sites-enabled sudo nginx -s reload         
nginx: [error] open() "/run/nginx.pid" failed (2: No such file or directory)  
(3.8.1/envs/flasky) ➜  sites-enabled ps aux | grep nginx  
uwe       2478  0.0  0.0  14316   956 pts/0    S+   19:55   0:00 grep --color=auto --exclude-dir=.bzr --exclude-dir=CVS --exclude-dir=.git --exclude-dir=.hg --exclude-dir=.svn --exclude-dir=.idea --exclude-dir=.tox nginx  
`
## https://stackoverflow.com/questions/35093534/no-such-file-or-directory-error-on-reload-command-in-nginx
In your case, nginx cannot find /run/nginx.pid file. It's probably caused by two reasons: 1. there is no currently running nginx process, 2. the PID file is located in different a location instead of the path, which is shown in nginx.conf.


## File: /etc/nginx/nginx.conf 
pid /run/nginx.pid;

When manually creating the Nginx service, you need to make sure, that both locations within your Systemd nginx.service file and within your Nginx nginx.conf configuration file match.  
habe nginx.service nicht gefunden

# File: `/etc/nginx/sites-enabled/flaskapp`

server {
    server_name    osteotomy.de *.osteotomy.de;
    root           /home/flasky;
    index          index.html;    

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

## Nach Modigfikation mit reboot folgendes Verhalten:


bei Eingabe von http://139.162.152.56/ und theaterfreak.  
_**homepage index.html wird nicht gefunden**_   
`Welcome to nginx!

If you see this page, the nginx web server is successfully installed and working. Further configuration is required.

For online documentation and support please refer to nginx.org.  
Commercial support is available at nginx.com.  

Thank you for using nginx.`

bei Eingabe von ostheotomy.de,  http://osteotomy.de/
_** wie bei theaterfreak.de**_   
keine https Verbindung!

## daraufhin folgende Befehle:
Last login: Sat Mar 21 20:04:20 2020 from 91.33.168.29  
(3.8.1/envs/flasky) ➜  flasky git:(linode-deploy) ✗ sudo supervisorctl reread  
[sudo] password for uwe:   
No config updates to processes  
(3.8.1/envs/flasky) ➜  flasky git:(linode-deploy) ✗ sudo supervisorctl update  
(3.8.1/envs/flasky) ➜  flasky git:(linode-deploy) ✗ sudo supervisorctl  
osteotomy                        RUNNING   pid 1135, uptime 0:08:17  

danach war Osteotomy.de wieder ansprechbar. Allerdings hat die html / scc Formatierung gelitten...  

nun mit laufendem Server neuer Versuch mit 
# sudo certbot --nginx

Output:
(3.8.1/envs/flasky) ➜  flasky git:(linode-deploy) ✗ sudo certbot --nginx
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator nginx, Installer nginx

Which names would you like to activate HTTPS for?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
1: osteotomy.de
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Select the appropriate numbers separated by commas and/or spaces, or leave input
blank to select all options shown (Enter 'c' to cancel): 
Obtaining a new certificate
Performing the following challenges:
http-01 challenge for osteotomy.de
Waiting for verification...
Cleaning up challenges
Failed authorization procedure. osteotomy.de (http-01): urn:ietf:params:acme:error:unauthorized :: The client lacks sufficient authorization :: Invalid response from http://osteotomy.de/.well-known/acme-challenge/XN4d8mWGYc91OFZCBRF5PT_AJ1smJolHM-KVRrVhFX4 [2a01:7e01::f03c:91ff:fea4:f75a]: "<html>\r\n<head><title>404 Not Found</title></head>\r\n<body bgcolor=\"white\">\r\n<center><h1>404 Not Found</h1></center>\r\n<hr><center>"

IMPORTANT NOTES:
 - The following errors were reported by the server:

   Domain: osteotomy.de
   Type:   unauthorized
   Detail: Invalid response from
   http://osteotomy.de/.well-known/acme-challenge/XN4d8mWGYc91OFZCBRF5PT_AJ1smJolHM-KVRrVhFX4
   [2a01:7e01::f03c:91ff:fea4:f75a]: "<html>\r\n<head><title>404 Not
   Found</title></head>\r\n<body bgcolor=\"white\">\r\n<center><h1>404
   Not Found</h1></center>\r\n<hr><center>"

   To fix these errors, please make sure that your domain name was
   entered correctly and the DNS A/AAAA record(s) for that domain
   contain(s) the right IP address.

889 | export FLASKY_APP=flasky.py
 1332  sudo nginx -s stop
 1334  sudo nginx
 1335  sudo supervisorctl reread
 1336  sudo supervisorctl update
 1337  sudo supervisorctl
 1338  /home/uwe/.pyenv/shims/gunicorn --workers=3 flasky:app
 1339  sudo nginx -s reload
 1340  sudo /etc/init.d/apache2 stop
 1341  sudo nginx -s reload
 1358  cd /etc/nginx/conf.d
 1359  conf.d ls
 1372  cd sites-available
 1375  cd sites-enabled
 
 website nicht erreichbar:
#_**homepage index.html wird nicht gefunden**_   
`Welcome to nginx!....


# Versuch mit uwsgi
sudo nano 139.162.152.56.conf  
 1456  sudo service nginx restart  
 1457  sudo /usr/sbin/nginx -t   
 1458  sudo nano /etc/nginx/nginx.conf  
 1459  sudo nano 139.162.152.56.conf  
 1460  cd /etc/nginx/conf.d  
 1463  pip install uwsgi  
 1465  nano uwsgi.ini  
 1466  cd /var/log/uwsgi/  
 1473  uwsgi --ini uwsgi.ini  
 1474  sudo uwsgi --ini uwsgi.ini  
 1475  cat uwsgi.ini  
 1476  sudo nano /etc/nginx/nginx.conf  
 1479  sudo service nginx restart  
 1480  /home/uwe/.pyenv/shims/gunicorn --workers=3 flasky:app  
 1481  cd /var/log/nginx/access.log  
 1484  cd /var/log/nginx/  
 1491  sudo nano /etc/nginx/conf.d/139.162.152.56.conf  
 1492  sudo service nginx restart  
 1493  /home/uwe/.pyenv/shims/gunicorn --workers=3 flasky:app  
 1494  sudo supervisorctl reread  
 1495  sudo supervisorctl update  
 1496  sudo supervisorctl  
 
 Habe uwsgi nach Anleitung von
 https://learning.oreilly.com/library/view/nginx-cookbook/9781786466174/6fc524b6-d224-47c3-9fdb-08fc05188ea7.xhtml  
 "Easy Flask with nginx
 unklar, ob uwsgi parallel zu gunicorn laufen kann....
 
 Die config Dateien sehen zur Zeit so aus:
 ## File: /etc/nginx/nginx.conf                             

user uwe;  
worker_processes auto;  

error_log  /var/log/nginx/error.log warn;  
pid /run/nginx.pid;  

include /etc/nginx/modules-enabled/*.conf;  

events {  
        worker_connections 768;  
        # worker_processes auto;  
        # multi_accept on;  
}  

http {  

        ##
        # Basic Settings
        ##

        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;
        types_hash_max_size 2048;
        server_tokens off;

        # server_names_hash_bucket_size 64;
        # server_name_in_redirect off;

        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        ##
        # SSL Settings
        ##

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
        ssl_prefer_server_ciphers on;

        ##
        # Logging Settings
        ##

        log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

        access_log /var/log/nginx/access.log main;


  
 


## File: /etc/nginx/conf.d/139.162.152.56.conf                

server {  
        listen         80 default_server;  
        listen         [::]:80 default_server;  
        server_name osteotomy.de www.osteotomy.de *.osteotomy.de;  

        # SSL configuration
        #
        listen 443 ssl default_server;
        listen [::]:443 ssl default_server;
}

## File: /home/flasky/uwsgi.ini                       

      [uwsgi]
      socket = 127.0.0.1:8000
      uid = www-data gid = www-data
      chdir = /home/flasky
      module = flasky
      callable = app
      master = True
      pidfile = /tmp/uwsgi-flaskdemo.pid
      max-requests = 5000
      daemonize = /var/log/uwsgi/flasky.log

