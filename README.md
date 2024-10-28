# Synapse Implémentation /  White Box

## Utilisation

### Création d'un noeud

Pour créer un noeud, on instancie la classe `SynapseNode` avec une adresse IP :

```python
node = SynapseNode("192.168.1.1")
```

### Insertion d'un réseau

Pour insérer un réseau associé au noeud :

```python
node.insert_net("NetworkA", "192.168.1.2")
```

### Envoi d'opérations

Pour envoyer une opération à un autre noeud :

```python
node.on_ope("GET", "key1", None, "192.168.1.2")
```

### Gestion des messages

Les méthodes `on_find` et `on_found` gèrent les réponses des autres noeuds lors des opérations de recherche.

### Exécution des tests

Le fichier `tests.py` contient des tests pour jouer les fonctionnalités de la classe `SynapseNode`.
```bash
python tests.py
```

## Tests

Les tests incluent :

- Création de tags uniques.
- Envoi d'opérations `GET`.
- Simulation de réponses `FIND` et `FOUND`.
- Invitation à rejoindre un réseau et gestion de l'adhésion à un réseau.
- Tests des scénarios de distribution MRR et de responsabilité sur les clés.