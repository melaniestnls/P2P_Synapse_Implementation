class SynapseNode:
    def __init__(self, ip):
        self.ip = ip  
        self.net_list = []  
        self.processed_tags = set()  

    # Génère un tag unique 
    def new_tag(self, ipsend):
        return hash((ipsend, id(self)))

    # Fonction simulée pour envoyer un message à un destinataire
    def send(self, message, ipdest):
        # Dans une vraie implémentation, cela impliquerait un mécanisme de communication réseau (à voir)
        print(f"Sending {message} to {ipdest}")

    # Réception d'un opcode 
    def on_ope(self, code, key, value, ipsend):
        tag = self.new_tag(ipsend)  
        # Envoi d'un message FIND au noeud lui-même pour initier une recherche
        self.send(("FIND", code, 5, 3, tag, key, value, ipsend), self.ip)

    # Réception d'un message FIND
    def on_find(self, code, ttl, mrr, tag, key, value, ipdest, ipsend):
        if ttl == 0 or self.game_over(tag):
            print("Lookup aborted: TTL is 0 or game over strategy")
        else:
            self.push_tag(tag)  
            next_mrr = self.distrib_mrr(mrr)  
            for net in self.net_list:
                if self.is_responsible(net, key):
                    self.send(("FOUND", code, net, mrr, key, value), ipdest)
                elif self.good_deal(net, ipsend):
                    self.send(("FIND", code, ttl - 1, next_mrr.get(net), tag, key, value), self.next_hop(key))

    # Réception d'un message FOUND
    def on_found(self, code, net, mrr, key, value, ipsend):
        self.good_deal_update(net, ipsend)  
        if code == "GET":
            self.send(("READ_TABLE", net, key), ipsend)
        elif code == "PUT":
            if mrr >= 0:  
                self.send(("WRITE_TABLE", net, key, value), ipsend)

    #Invitation à rejoindre un réseau
    def on_invite(self, net, ipsend):
        if self.good_deal(net, ipsend):  
            self.send(("JOIN", net), ipsend)  

    # Se joindre à un réseau
    def on_join(self, net, ipsend):
        if self.good_deal(net, ipsend):  
            self.insert_net(net, ipsend)  


    # Détermine si la recherche doit être arrêtée en vérifiant si le tag a déjà été traité
    def game_over(self, tag):
        return tag in self.processed_tags

    # Marque un tag comme traité 
    def push_tag(self, tag):
        self.processed_tags.add(tag)

    # Distribue le MRR 
    def distrib_mrr(self, mrr):
        if not self.net_list:
            return {}  # Gère le cas où il n'y a pas de réseau
        return {net: mrr // len(self.net_list) for net in self.net_list}  

    # Vérifie si le noeud est responsable pour la clé dans le réseau donné
    def is_responsible(self, net, key):
        if net not in self.net_list:
            return False  # Retourne False si le réseau n'est pas associé au noeud
        return hash(key) % len(self.net_list) == self.net_list.index(net)  # Vérifie la responsabilité via le hash

    # Détermine si bon deal
    def good_deal(self, net, ipsend):
        return True  # Simplification pour la simulation... (à voir si peut mieux faire)

    # Détermine le prochain noeud vers lequel envoyer le message
    def next_hop(self, key):
        return self.ip  # Simplification... (à voir si peut mieux faire)

    # Met à jour les informations sur les bons deals
    def good_deal_update(self, net, ipsend):
        print(f"Updating good deal tables for net {net} and ipsend {ipsend}")

    # Insère un réseau dans la liste des réseaux du noeud
    def insert_net(self, net, ipsend):
        if net not in self.net_list:  
            self.net_list.append(net)  
            print(f"Inserted {ipsend} in network {net}")  
