# INF3995 - Station au sol - Interface Web
Contient le code de la section "serveur" de la station au sol.
## Prérequis

### Sans docker :
On roule le serveur dans un environement virtuel python nommé venv (garder le même nom pour que le gitignore fonctionne bien)
```bash
sudo python3 -m venv venv
source venv/bin/activate
sudo pip install -r requirements.txt
sudo python3 requirements.py
```

### Avec docker :
```bash
docker build -t serveur .
```
## Exécution

### Sans docker
Toujours dans l'environement virtuel, on fait
```bash
sudo python3 app.py
```

### Avec docker :
```bash
docker run -p 5000:5000 serveur
```
