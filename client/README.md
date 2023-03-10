# INF3995 - Station au sol - Interface Web

Ce répertoire inclut le client Web de la station au sol.

## Comment démarrer l'interface **avec** Docker

### Prérequis

- docker

### Procédure

1. Exécuter la commande ``docker build --target=final -t server-client .``
2. Lancer le conteneur à l'aide de la commande ``docker run -p 5001:5001 server-client``
3. Naviguer à l'adresse `http://localhost:5001/`

## Comment démarrer l'interface **sans** Docker

### Prérequis

1. Node.js et npm. La version 16.17.1 est conseillée
2. yarn avec la commande ``npm install --global yarn``

### Procédure

1. Lancer la commande ``yarn install``
2. Pour compiler il suffit ensuite de lancer ``ng build``
3. La commande ``ng serve --open`` permet de lancer la simulation
4. Enfin, il faut naviguer à l'adresse ``http://localhost:4200/``

## Tests

Afin d'exécuter les tests :

```bash
docker build --target=test -t server-client-test .
docker run -p 5001:5001 server-client-test
```

## Formatage et lint

Le formatage est exécuté à l'aide d'[**eslint**](https://eslint.org/) qui suit les standards suivants :

- [angular-eslint/recommended](https://github.com/angular-eslint/angular-eslint)
- [prettier/recommended](https://github.com/prettier/eslint-plugin-prettier)

Le formatage peut être lancé à l'aide de :

```bash
yarn run lint
```

Les fichiers peuvent être formatés à l'aide de la commande suivante :

```bash
yarn run lint --fix
```
