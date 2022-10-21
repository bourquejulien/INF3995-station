# INF3995 - Station au sol - Interface Web
Contient le code de la section "serveur" de la station au sol.
## Prérequis

### Sans docker :
On roule le serveur dans un environnement virtuel python nommé venv (garder le même nom pour que le gitignore fonctionne bien)
```bash
python3 -m venv venv
source venv/bin/activate
python3 requirements.py
```

### Avec docker :
```bash
docker build -t serveur .
```
## Exécution

### Sans docker
Toujours dans l'environnement virtuel, on fait
```bash
python3 app.py
```

### Avec docker :
```bash
docker run -p 5000:5000 serveur
```

## Base de données Mongo
Il est nécessaire de donner accès au serveur à une base de données de type Mongo.
Pour ce faire il est possible d'indiquer à l'aide de la variable d'environnement ``DB_CONNECTION_STRING`` une chaine de connexion standardisée (connection string).

Par défaut la chaine utilisée est la suivante : ``mongodb://local:lacol@localhost:5002/``.
Cette chaine permet de se connecter à une base de données locale, celle lancée par le fichier ``docker-compose.db.yml`` :
```bash
docker compose -f docker-compose.db.yml up -d
```

**À noter** : Cette commande lance également *mongoexpress* sur le port 8081. Ce second conteneur permet de mettre à jour manuellement la BD.
