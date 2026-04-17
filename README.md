# Buildbot — CI/CD

Guia rápido para subir o **master** e o **worker** do Buildbot e integrar com **Ansible**. Os scripts de arranque e paragem vivem em [`/usr/local/src/buildbot`](/usr/local/src/buildbot) (ativam o venv, iniciam ou param o master e o worker).

---

## Pré-requisitos

- Python 3 com `venv`
- Pacotes listados em `requirements-buildbot.txt` e `requirements-ansible.txt` (no diretório do Buildbot)
- Credenciais do worker alinhadas com o que está em `master.cfg` (os valores abaixo são só exemplo)

---

## 1. Master (builder)

Todos os passos assumem o diretório do Buildbot:

```bash
cd /usr/local/src/buildbot
```

Criar ambiente virtual e instalar dependências:

```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements-buildbot.txt
```

Criar e preparar o master:

```bash
buildbot create-master master
cp -rfv /usr/local/src/buildbot/master.cfg.sample /usr/local/src/buildbot/master.cfg.ori
ln -sfn /usr/local/src/buildbot/master.cfg.sample /usr/local/src/buildbot/master.cfg
buildbot start master
buildbot upgrade-master /usr/local/src/buildbot/master
```

> **Dica:** depois de editar `master.cfg`, use `buildbot checkconfig master` antes de reiniciar o serviço.

---

## 2. Worker

```bash
mkdir -p /usr/local/src/buildbot/worker
buildbot-worker create-worker worker localhost example-worker pass
```

Substitua `example-worker` e `pass` por utilizador e palavra que o master aceite, e mantenha o worker a apontar para o host/porta corretos do master.

---

## 3. Ansible

Com o mesmo `venv` (ou outro dedicado), instale as dependências de automação:

```bash
pip install -r requirements-ansible.txt
```

Use os playbooks ou roles no diretório de Ansible da vossa árvore (por exemplo [`../ansible-scripts`](../ansible-scripts), se existir ao lado deste projeto).

---

## 4. Iniciar e parar o ambiente

A partir do diretório do Buildbot:

```bash
cd /usr/local/src/buildbot
./start.bash    # ativa venv, buildbot start master, buildbot-worker start worker
```

```bash
cd /usr/local/src/buildbot
./stop.bash     # para master e worker de forma ordenada
```

---

## Referência rápida

| Componente | Caminho típico |
|------------|----------------|
| Master     | `/usr/local/src/buildbot/master` |
| Worker     | `/usr/local/src/buildbot/worker` |
| Config     | `/usr/local/src/buildbot/master.cfg` → `master.cfg.sample` |

Para mais detalhes do projeto Buildbot local, consulte também o [README do repositório `buildbot`](../buildbot/README.md).
