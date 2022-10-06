# INF3995 - Station au sol - Interface Web

Ce répertoire inclut le client Web de la station au sol.

## Comment démarrer l'interface **avec** Docker

### Prérequis
- Docker

### Procédure
1. Exécuter la commande ``docker build --target=final -t webui .``
2. Lancer le conteneur à l'aide de la commande ``docker run -p 5001:5001 webui``
3. Naviguer à l'adresse `http://localhost:5001/`

## Comment démarrer l'interface **sans** Docker
### Prérequis
1. Node.js et npm. La version 16.17.1 est conseillée
2. yarn avec la commande ``npm install --global yarn``
### Procédure
1. Lancer la commande ``yarn install`` ou ``npm install``
2. Pour compiler il suffit ensuite de lancer ``ng build``
3. La commande ``ng serve`` permet de lancer la simulation
4. Enfin, il faut naviguer à l'adresse ``http://localhost:4200/``
