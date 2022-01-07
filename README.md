# MikrotikBackup
Python program for backup Mikrotik with SSH. Program use config.conf (see config-example.conf).  
Main idea: Create export backup on mikrotik. Download it and compare with previous version backup. If exist differences, additionally create binary backup and store both as archive history.  
Now program store files as on local disk, but they can be saved anywhere if add this functionality.   
(ATTENTION: export backup files .rsc contain passwords in clear text, therefore it is unsafe to store them in public repositories like github.com)  

## Run (more convenient to use docker)
```commandline
# First of all, install the python 3.10 in accordance with the python installation documentation for the corresponding specific OS.
cd /home/user/MikrotikBackup (or /opt/MikrotikBackup)
git clone https://github.com/MinistrBob/MikrotikBackup.git .
# Create venv or not.
python3 -m pip install --upgrade pip
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
python3 main.py
```

## Docker
### Docker build (example for me)
```commandline
cd c:\MyGit\MikrotikBackup\
git clone https://github.com/MinistrBob/MikrotikBackup.git .
docker build . -t ministrbob/mikrotik-backup:latest
docker push ministrbob/mikrotik-backup:latest
```
### Docker run (example for Windows)
```commandline
docker run --rm -it -e MIKROTIK_BACKUP_PATH="/backup" -v c:\!SAVE\backup\:/backup ministrbob/mikrotik-backup:latest
```

## For developer
### Update requirements (on Windows)
```
pip freeze | Out-File -Encoding UTF8 requirements.txt
```
