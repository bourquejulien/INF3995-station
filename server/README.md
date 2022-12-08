# INF3995 - Station au sol - Interface Web

Ce répertoire contient le code de la section "serveur" de la station au sol.

## Prérequis

### Base de données Mongo

Il est nécessaire de donner accès au serveur à une base de données de type Mongo.
Pour ce faire, il est possible d'indiquer à l'aide de la variable d'environnement ``DB_CONNECTION_STRING`` une chaine de
connexion standardisée (connection string).

Par défaut, la chaine utilisée est la suivante : ``mongodb://local:lacol@localhost:5002/``.
Cette chaine permet de se connecter à une base de données locale, celle lancée par le
fichier ``docker-compose.db.yml`` :

```bash
docker compose -f docker-compose.db.yml up -d
```

> **À noter** : Cette commande lance également *mongoexpress* sur le port 8081. Ce second conteneur permet de mettre à
jour manuellement la BD.

### Optionnel - Remote compiler

Le "remote compiler" est un petit service permettant de compiler de manière distante.
Il doit être lancé afin de pouvoir utiliser la fonctionnalité d'édition du firmware à même la station au sol.
Le serveur est en mesure de détecter la présence du ``remote compiler``, celui-ci est donc optionnel.

La variable d'environnement ``REMOTE_COMPILER_CONNECTION_STRING`` doit être initialisée, sinon la valeur par défaut sera
utilisée.

Pour plus de détails, voir : ``firmware/remote-compiler``.

### Optionnel - Sans docker

On exécute le serveur dans un environnement virtuel python nommé venv (garder le même nom pour que le gitignore fonctionne
bien).

```bash
python3 -m venv venv
source venv/bin/activate
python3 requirements.py
```

## Exécution

### Variables d'environnement

Les variables d'environnement suivantes permettent de se connecter à différents services :

- ``IS_SIMULATION`` : À ``True`` si le serveur doit être lancé en mode simulation, ``False`` sinon.
- ``ARGOS_HOSTNAME`` : L'adresse du service argos.
- ``DB_CONNECTION_STRING`` : L'adresse de la base de données.
- ``REMOTE_COMPILER_CONNECTION_STRING`` : L'adresse du remote compiler.

### Sans docker

Toujours dans l'environnement virtuel, on fait :

```bash
python3 app.py
```

### Avec docker

1. Exécuter la commande ``docker build --target=final -t server .``
2. Lancer le conteneur à l'aide de la commande ``docker run -p 5000:5000 server``

## Test

Les tests sont réalisés à l'aide de **pytests**.

Afin de valider les tests, il est possible d'exécuter :

```bash
docker build --target=test -t server-tests .
docker run server-tests
```

## Formatage

Le formatage est exécuté à l'aide de [*black*](https://github.com/psf/black) qui suit le
standard [**PEP8**](https://peps.python.org/pep-0008/).

Afin de valider le formatage, il est possible de lancer :

```bash
python3 format.py
```

L'ajout de l'option ``--fix`` permet de formater les fichiers.
