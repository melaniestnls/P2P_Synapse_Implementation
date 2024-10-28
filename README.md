# Synapse Implémentation / white box

## Introduction

Ce README fournit des instructions sur l'utilisation de la classe `SynapseNode`, ainsi qu'une explication détaillée du fonctionnement du protocole white box.

## Fonctionnement du protocole white box

### 1. Envoi d'opérations

Lorsqu'un noeud souhaite effectuer une opération (comme GET ou PUT), il appelle la méthode `on_ope`. Cela crée un tag unique pour l'opération et envoie un message FIND à lui-même pour initier la recherche.

```python
node.on_ope("GET", "key", None, "192.168.1.2")
```

### 2. Réception d'un message FIND

Le noeud reçoit un message FIND, ce qui déclenche la méthode `on_find`. Ce qu'il s'y passe : 
- **TTL** : Si le TTL est 0 ou si le tag a déjà été traité, la recherche est arrêtée.
- **Responsabilité** : Si le noeud est responsable de la clé, il envoie un message FOUND avec la valeur correspondante. Le noeud est responsable de la clé si le hash de celle-ci modulo le nombre de noeud dans le réseau correspond à l'index de notre noeud courant dans la liste.
- **Goog deal** : Si le noeud n'est pas responsable, mais que la connexion est jugée fiable, il envoie une nouvelle requête FIND à un autre noeud. (Dans l'implémentation, la fonction est simplifiée eet retourne True.)

```python
def on_find(self, code, ttl, mrr, tag, key, value, ipdest, ipsend):
    if ttl == 0 or self.game_over(tag):
        print("Lookup aborted: TTL is 0 or game over strategy")
    else:
        self.push_tag(tag)
        # ... vérifications et envois
```

### 3. Réception d'un message FOUND

Lorsqu'un noeud reçoit un message FOUND, il exécute les opérations suivantes :
- Met à jour ses tables de good deal.
- En fonction du code, il peut envoyer un message READ_TABLE (pour GET) ou WRITE_TABLE (pour PUT) à l'adresse IP d'origine.

```python
def on_found(self, code, net, mrr, key, value, ipsend):
    self.good_deal_update(net, ipsend)
    if code == "GET":
        self.send(("READ_TABLE", net, key), ipsend)
    elif code == "PUT":
        if mrr >= 0:
            self.send(("WRITE_TABLE", net, key, value), ipsend)
```

### 4. Gestion des réseaux

Les noeuds peuvent inviter d'autres noeuds à rejoindre leur réseau ou répondre à ces invitations. Les méthodes `on_invite` et `on_join` gèrent ces processus.

```python
def on_invite(self, net, ipsend):
    if self.good_deal(net, ipsend):
        self.send(("JOIN", net), ipsend)
```

## Utilisation

### Création d'un noeud

Pour créer un noeud, instanciez la classe `SynapseNode` avec une adresse IP :

```python
node = SynapseNode("10.149.44.206")
```

### Insertion d'un réseau

Pour insérer un réseau associé au noeud :

```python
node.insert_net("NetworkA", "10.149.44.207")
```

### Envoi d'opérations

Pour envoyer une opération à un autre noeud :

```python
node.on_ope("GET", "key1", None, "10.149.44.207")
```

### Gestion des messages

Les méthodes `on_find` et `on_found` gèrent les réponses des autres noeuds lors des opérations de recherche.

## Exécution des tests

Le fichier `tests.py` contient des tests pour vérifier les fonctionnalités de la classe `SynapseNode`.

```bash
python tests.py
```

## Tests

Les tests incluent :

- Création de tags uniques.
- Envoi d'opérations GET.
- Simulation de réception de messages FIND et FOUND.
- Invitation à rejoindre un réseau et gestion de l'adhésion à un réseau.
- Tests des scénarios de réplication MRR et de responsabilité sur les clés.

---

### Remarques

-  A noter que ce modèle simplifie la ditribution des responsabilités. En effet l'algorithme de responsabilité doit calculer le modulo du hash en fonction de l'ensemble des noeuds sur le réseau. Pour ce faire, les noeuds doivent avoir la même liste de noeuds pour respecter l'implémentation actuelle basée sur les indexs.

- Il serait plus judicieux d'utiliser un hashage uniforme qui ne dépende pas de l'ordre d'ajout des réseaux dans celui-ci.

La méthode on_write_table n'a pas été implémentée car non utilsée pour démontrer la répartition des données sur le réseau de noeuds Synaspes.

---