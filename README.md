# urna_eletronica

***simula em partes, uma urna eletrônica verdadeira***

---

## Para instalar no Windows 10/11

1. Instalar Python 3.11.2:  
[Link do Instalador do Python 3.11.2](https://www.python.org/ftp/python/3.11.2/python-3.11.2-amd64.exe "Instalador do Python 3.11.2")

2. Instalar Git 2.39.1:  
[Link do Instalador do Git 2.39.1](https://github.com/git-for-windows/git/releases/download/v2.39.1.windows.1/Git-2.39.1-64-bit.exe "Instalador do Git 2.39.1")

3. Executar os seguintes comandos no CMD do Windows para instalar a urna eletrônica:  
```dos
cd .\path\to
git clone https://github.com/jmanoel7/urna_eletronica.git  
cd urna_eletronica  
mkdir .\venv  
virtualenv .\venv\urna_eletronica  
.\venv\urna_eletronica\Scripts\activate  
pip install -U pip   
pip install -r requirements.txt
```

4. Executar a seguinte linha de código para executar o software da urna eletrônica:
```dos
cd .\path\to\urna_eletronica\urnaEletronica
..\venv\urna_eletronica\Scripts\activate
python manage.py runserver
```

5. Executar a seguinte linha de código para saber quais opções estão disponíveis:
```dos
cd .\path\to\urna_eletronica\urnaEletronica
..\venv\urna_eletronica\Scripts\activate
python manage.py
```

**OBS: onde ponho .\path\to nos códigos acima, estou me referindo a pasta raíz, onde você vai colocar o código da urna eletrônica**

---

## Para instalar no Ubuntu GNU/Linux 22.04 LTS

1. Instalar Python PPA:
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
```

2. Instalar Python, Virtualenv e Git:
```bash
sudo apt install python3.11-full python3-pip virtualenv git
```

3. Executar os seguintes comandos no Terminal do GNU/Linux para instalar a urna eletrônica:
```bash
cd ~
mkdir -p git
cd git
git clone https://github.com/jmanoel7/urna_eletronica.git
cd urna_eletronica
mkdir ./venv
virtualenv ./venv/urna_eletronica
./venv/urna_eletronica/bin/activate
pip install -U pip
pip install -r requirements.txt
```

4. Executar a seguinte linha de código para executar o software da urna eletrônica:
```bash
cd ~/git/urna_eletronica/urnaEletronica
source ./venv/urna_eletronica/bin/activate
python manage.py runserver
```

5. Executar a seguinte linha de código para saber quais opções estão disponíveis:
```bash
cd ~/git/urna_eletronica/urnaEletronica
source ./venv/urna_eletronica/bin/activate
python manage.py
```

---

## Como Usar o Sistema

Uma vez instalado o sistema, ao excutá-lo conforme o item 4 acima, você terá 3 opções de login:

- admin: administrador do sistema, responsável pelos cadastros de usuários no sistema (gerente e assistente), urna, eleitor e político.

- gerente: gerente da urna, responsável por iniciar a urna (data, hora de início e de fim)para receber votos, término da urna para exibir o resultado da votação.

- assistente: para atender o eleitor e encaminhá-lo à urna para o voto, respeitando a data e os horários de início e de fim (cadastrados pelo gerente), e que o eleitor só pode votar uma única vez a cada eleição.

**OBS: todas as 3 opções de login acima (nome de usuário), tem a mesma senha: TESte!23$ .
Lembrando sempre que o voto em branco tem o número de partido 00, e que o voto nulo tem o número de parrtido 99, para votar em branco tem um botão só para isso, já para votar nulo é só votar um número diferente dos partidos políticos cadastrados (13 e 22) que ele se tranforma automaticamente em número 99.**

---
