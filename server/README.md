# INF3995 - Station au sol - Interface Web
Contient le code de la section "serveur" de la station au sol.
## Prérequis

### Sans docker :
```bash
python3 requirements.py
```

### Avec docker :
```bash
docker build -t serveur .
```
## Exécution

### Sans docker
```bash
python3 app.py
```

### Avec docker :
```bash
docker run -p 5000:5000 serveur
```
