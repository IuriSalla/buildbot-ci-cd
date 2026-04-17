# Configuração do Setup pela primeira vez
### Builder (Master)

cd /usr/local/src/buildbot

python -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements-buildbot.txt

buildbot create-master master

cp -rfv /usr/local/src/buildbot/master.cfg.sample /usr/local/src/buildbot/master.cfg.ori

ln -s /usr/local/src/buildbot/master.cfg.sample /usr/local/src/buildbot/master.cfg

buildbot start master
buildbot upgrade-master /usr/local/src/buildbot/master

### Worker

mkdir /usr/local/src/buildbot/worker
buildbot-worker create-worker worker localhost example-worker pass

## Ansible
pip install -r requirements-ansible.txt

# Iniciando o ambiente
cd /usr/local/src/buildbot

./start.bash

# Interrompendo o ambiente
cd /usr/local/src/buildbot

./stop.bash