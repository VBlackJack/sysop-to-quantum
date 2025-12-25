<!--
Auteur : Julien Bombled
Licence : Apache License 2.0
-->

# Glossaire Quantique pour l'Infrastructure

Ce glossaire définit les concepts fondamentaux du calcul quantique à travers le prisme de l'administration système et de l'architecture cloud.

## Qubit
**Théorie :** L'unité de base de l'information quantique. Contrairement au bit classique (0 ou 1), il peut exister dans une superposition d'états.

**Vision SysAdmin :** Considérez le qubit comme une cellule de RAM extrêmement volatile et dépourvue de correction d'erreurs (ECC). Alors qu'un bit est un interrupteur stable, le qubit est une toupie en rotation : il contient une information complexe tant qu'il tourne, mais devient une simple valeur binaire dès qu'on tente de le "lire" (mesure). Sa gestion nécessite un environnement physique ultra-contrôlé, bien au-delà de n'importe quel datacenter Tier IV.

## Superposition
**Théorie :** Propriété permettant à un qubit d'être dans plusieurs états simultanément jusqu'à ce qu'il soit mesuré.

**Vision SysAdmin :** C'est une forme de "parallélisme natif". Imaginez lancer un script de recherche sur une base de données : là où un CPU classique itère sur chaque entrée (ou utilise plusieurs threads), un processeur quantique "voit" toutes les solutions possibles en un seul cycle d'horloge. C'est comme si votre application pouvait explorer toutes les branches d'un `if/else` simultanément sans avoir à instancier plusieurs processus.

## Intrication (Entanglement)
**Théorie :** Phénomène où deux qubits deviennent liés de telle sorte que l'état de l'un dépend instantanément de l'état de l'autre, quelle que soit la distance.

**Vision SysAdmin :** L'analogie la plus proche est celle d'un **RAID 1 (Mirroring) instantané** et sans aucune latence réseau. Si vous modifiez une donnée sur le "disque A", le "disque B" reflète ce changement immédiatement, même s'il se trouve dans une région Cloud différente. C'est une synchronisation d'état qui ne passe par aucun câble, défiant les limites habituelles de la bande passante et de la propagation du signal.

## Décohérence
**Théorie :** Perte de l'état quantique d'un qubit due aux interactions avec son environnement (chaleur, vibrations, ondes).

**Vision SysAdmin :** C'est le "bruit" ultime ou la corruption de données massive. En tant qu'Ops, nous luttons contre le bit-rot ou les pannes matérielles ; ici, la donnée a un **Time-to-Live (TTL)** ultra-court. La décohérence, c'est ce qui arrive quand votre "système" s'effondre parce qu'un technicien a ouvert la porte de la salle serveur ou qu'un ventilateur a vibré trop fort. C'est l'ennemi numéro 1 de la haute disponibilité quantique.

## QPU (Quantum Processing Unit)
**Théorie :** Le processeur physique qui manipule les qubits pour effectuer des calculs.

**Vision SysAdmin :** Ne voyez pas le QPU comme un remplaçant du CPU, mais comme un **accélérateur spécialisé**, à l'image d'un GPU pour le rendu ou d'un FPGA pour le réseau. Dans une architecture hybride, votre code s'exécute sur un serveur classique (Python/C++), et délègue des tâches spécifiques (optimisation, simulation chimique) au QPU via une API Cloud (Azure Quantum, AWS Braket). C'est une ressource externe managée.

## NISQ (Noisy Intermediate-Scale Quantum)
**Théorie :** L'ère actuelle de l'informatique quantique, caractérisée par des processeurs de taille moyenne et très sensibles aux erreurs.

**Vision SysAdmin :** C'est l'équivalent d'un hardware en **version Alpha instable**. Imaginez administrer un cluster de serveurs qui produisent des erreurs de calcul aléatoires toutes les 100 millisecondes. En tant qu'ingénieurs, notre rôle dans l'ère NISQ est de mettre en place des "mécanismes de retry" et des algorithmes de correction logicielle pour compenser le manque de fiabilité du matériel. On fait de la résilience applicative au-dessus d'une infrastructure qui n'est pas encore "Fault Tolerant".
