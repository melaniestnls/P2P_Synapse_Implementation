import time

from white_box import SynapseNode

def main():
    # Créer des noeuds
    node1 = SynapseNode("192.168.1.1")
    node2 = SynapseNode("192.168.1.2")

    # Ajouter des réseaux pour le noeud 1
    node1.insert_net("NetworkA", node2.ip)
    node1.insert_net("NetworkB", "192.168.1.3")

    # Tester la création de tags
    tag = node1.new_tag("192.168.1.2")
    print(f"Generated unique tag for IP {node2.ip}: {tag}")

    # Envoi d'une opération GET
    print("\n--- Sending GET Operation ---")
    node1.on_ope("GET", "key1", None, node2.ip)

    # Simuler la réception d'un message FIND
    print("\n--- Simulating FIND Response ---")
    node1.on_find("GET", 3, 5, tag, "key1", "value1", node2.ip, "192.168.1.2")

    # Simuler la réception d'un message FOUND
    print("\n--- Simulating FOUND Response ---")
    node1.on_found("GET", "NetworkA", 5, "key1", "value1", "192.168.1.2")

    # Tester l'invitation à rejoindre un réseau
    print("\n--- Inviting to NetworkA ---")
    node1.on_invite("NetworkA", "192.168.1.2")

    # Tester de joidnre un réseau
    print("\n--- Joining NetworkA ---")
    node1.on_join("NetworkA", "192.168.1.2")

    # Tester quand le TTL est à 0
    print("\n--- Testing TTL = 0 ---")
    node1.on_find("GET", 0, 5, tag, "key1", "value1", node2.ip, "192.168.1.2")

    # Vérifier les tags traités
    print(f"Processed tags: {node1.processed_tags}")

    # Tester des scénarios de distribution MRR
    print("\n--- Testing MRR Distribution ---")
    mrr = 10
    distribution = node1.distrib_mrr(mrr)
    print(f"MRR distribution among networks: {distribution}")

    # Tester la responsabilité sur les réseaux
    for net in node1.net_list:
        print(f"Is {net} responsible for key 'key1'? {node1.is_responsible(net, 'key1')}")

if __name__ == "__main__":
    main()
