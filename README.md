# climb

## Installation
clone the deploy file:
<code>
wget https://raw.githubusercontent.com/computingify/climbBackEnd/develop/deploy_app.sh
</code>

enable executable
<code>
chmod +x /home/pi/deploy_app.sh
</code>

install
<code>
/home/pi/deploy_app.sh
</code>

## Update
go to installation directory
and launch update_app.sh:
<code>
chmod +x /home/pi/deploy_app.sh
/home/pi/update_app.sh
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
