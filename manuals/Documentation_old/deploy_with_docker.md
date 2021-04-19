nach talk-python course data-driven-web-app-with-flask ch15

Docker zum laufen bringen
========================= 
## Installation von docker
Achtung, Fehler bei Installation von docker über Snap. Siehe meinen Kommentar in stack overflow:
https://stackoverflow.com/questions/51729836/error-response-from-daemon-cannot-stop-container/64120350#64120350
   
danach ist ein reboot erfordelich!

 docker build -t yetigo/osteotomy:latest .  
 docker run --name pum -d -p 8000:5000 --rm yetigo/osteotomy:latest  
 docker push yetigo/osteotomy:latest  

# download docker container image 
 docker pull yetigo/osteotomy:latest  
 docker run --name pum -d -p 8000:5000 --rm yetigo/osteotomy:latest   
 
## display active containers 
 docker ps  
 docker container ls  
 
 ## stop Container:
docker container stop pum  
