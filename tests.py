import time
from white_box import SynapseNode

def main():
    # Créer des noeuds avec de nouvelles IP
    node1 = SynapseNode("10.0.0.1")
    node2 = SynapseNode("10.0.0.2")

    # Ajouter des réseaux pour le noeud 1
    node1.insert_net("LocalNetwork", node2.ip)
    node1.insert_net("ExternalNetwork", "10.0.0.3")

    # Tester la création de tags avec une nouvelle IP
    tag = node1.new_tag("10.0.0.2")
    print(f"Generated unique tag for IP {node2.ip}: {tag}")

    # Envoi d'une opération GET
    print("\n--- Sending GET Operation ---")
    node1.on_ope("GET", "new_key", None, node2.ip)

    # Simuler la réception d'un message FIND
    print("\n--- Simulating FIND Response ---")
    node1.on_find("GET", 3, 5, tag, "new_key", "new_value", node2.ip, "10.0.0.2")

    # Simuler la réception d'un message FOUND
    print("\n--- Simulating FOUND Response ---")
    node1.on_found("GET", "LocalNetwork", 5, "new_key", "new_value", "10.0.0.2")

    # Tester l'invitation à rejoindre un réseau
    print("\n--- Inviting to LocalNetwork ---")
    node1.on_invite("LocalNetwork", "10.0.0.2")

    # Tester de rejoindre un réseau
    print("\n--- Joining LocalNetwork ---")
    node1.on_join("LocalNetwork", "10.0.0.2")

    # Tester quand le TTL est à 0
    print("\n--- Testing TTL = 0 ---")
    node1.on_find("GET", 0, 5, tag, "new_key", "new_value", node2.ip, "10.0.0.2")

    # Vérifier les tags traités
    print(f"Processed tags: {node1.processed_tags}")

    # Tester des scénarios de distribution MRR
    print("\n--- Testing MRR Distribution ---")
    mrr = 20  # Valeur MRR modifiée
    distribution = node1.distrib_mrr(mrr)
    print(f"MRR distribution among networks: {distribution}")

    # Tester la responsabilité sur les réseaux
    for net in node1.net_list:
        print(f"Is {net} responsible for key 'new_key'? {node1.is_responsible(net, 'new_key')}")

if __name__ == "__main__":
    main()
