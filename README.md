# climb

## Installation
clone the deploy file:
<code>
wget https://raw.githubusercontent.com/computingify/climbBackEnd/develop/deploy_app.sh
</code>

enable executable
<code>
chmod +x /home/pi/deployement/deploy_app.sh
</code>

install
<code>
/home/pi/deployement/deploy_app.sh
</code>

## Update
From an host machine
<code>
chmod +x /home/pi/deployement/deploy_RPi.sh
./home/pi/deployement/deploy_RPi.sh
</code>

## Advance
### Start python virtual environnement
source venv/bin/activate

### Instalation
just install requirements.txt:
<code>
pip install -r requirements.txt
</code>

### Launch server side:
<code>
flask --app main.py --debug run
</code>

### Manually modify database
Use sqllitebrowser tool: https://sqlitebrowser.org
if the database is on ssh remote FS, follow this tuto: https://www.petergirnus.com/blog/how-to-use-sshfs-on-macosyes