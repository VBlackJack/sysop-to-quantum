<!--
Auteur : Julien Bombled
Licence : Apache License 2.0
-->

# Sécurité Post-Quantique (PQC)

## La Menace : "Harvest Now, Decrypt Later"

Pourquoi un SysAdmin devrait-il se soucier du quantique aujourd'hui, alors que les ordinateurs capables de casser le chiffrement RSA n'existeront peut-être pas avant 10 ou 15 ans ?

La réponse tient en une phrase : **Récolter maintenant, déchiffrer plus tard**.

Les acteurs malveillants (ou étatiques) interceptent et stockent dès aujourd'hui des téraoctets de trafic chiffré (VPN, HTTPS, SSH). Ces données sont illisibles pour l'instant. Mais si ces données ont une durée de vie longue (secrets industriels, données médicales, dossiers défense), elles seront exposées dès qu'un ordinateur quantique suffisamment puissant ("Cryptographically Relevant Quantum Computer" - CRQC) sera disponible.

La migration vers la cryptographie post-quantique n'est pas un projet pour 2035, c'est une urgence pour protéger les flux actuels.

## Les Nouveaux Standards (NIST)

En 2024, le NIST a officialisé les algorithmes conçus pour résister aux attaques quantiques. Pour l'Ops, ce sont simplement de "nouveaux noms" à ajouter dans les fichiers de configuration SSL/TLS et SSH.

*   **ML-KEM (anciennement Kyber)** :
    *   **Usage :** Échange de clés (Key Encapsulation Mechanism). C'est ce qui remplace RSA et Elliptic Curve (ECDH) lors de l'établissement d'une connexion sécurisée (Handshake).
    *   **Caractéristique :** Très rapide, mais clés légèrement plus grosses.

*   **ML-DSA (anciennement Dilithium)** :
    *   **Usage :** Signatures numériques. Utilisé pour signer des certificats, des documents ou authentifier des serveurs.
    *   **Caractéristique :** Remplace RSA/ECDSA pour l'identité.

## Mise en Pratique : Hardening SSH avec Ansible

En attendant le support natif et généralisé des algorithmes PQC (Post-Quantum Cryptography) dans toutes les distros, la première étape est l'hygiène cryptographique : supprimer les algos faibles qui seront les premiers à tomber.

Voici un playbook Ansible pour durcir un parc de serveurs Linux.

```yaml
# ssh_hardening.yml
# Author: Julien Bombled
# License: Apache 2.0
---
- name: Hardening SSH for Post-Quantum Preparation
  hosts: all
  become: true
  tasks:

    - name: Check OpenSSL version
      command: openssl version
      register: openssl_ver
      changed_when: false

    - name: Display OpenSSL Version
      debug:
        msg: "Current OpenSSL Version: {{ openssl_ver.stdout }}. Look for 3.x+ for future PQC support."

    - name: Ensure weak ciphers are disabled in sshd_config
      lineinfile:
        path: /etc/ssh/sshd_config
        regexp: "^Ciphers"
        # We enforce ChaCha20 and AES-GCM. We explicitly drop CBC and weaker modes.
        line: "Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com"
        state: present
        validate: 'sshd -t -f %s'
      notify: Restart SSH

    - name: Ensure weak Key Exchange Algorithms (KEX) are disabled
      lineinfile:
        path: /etc/ssh/sshd_config
        regexp: "^KexAlgorithms"
        # We prioritize Curve25519. In the future, this is where 'sntrup761x25519-sha512' (Hybrid) will be added.
        # Dropping Diffie-Hellman-Group1-SHA1 and other legacy KEX.
        line: "KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512"
        state: present
        validate: 'sshd -t -f %s'
      notify: Restart SSH

    - name: Disable DSA and RSA host keys (Prefer ED25519)
      lineinfile:
        path: /etc/ssh/sshd_config
        regexp: "^HostKey {{ item }}"
        state: absent
      loop:
        - /etc/ssh/ssh_host_dsa_key
        - /etc/ssh/ssh_host_rsa_key
      notify: Restart SSH

  handlers:
    - name: Restart SSH
      service:
        name: sshd
        state: restarted
```

### Note sur les algorithmes hybrides
Dans un futur proche (déjà dispo sur OpenSSH récents), vous verrez apparaître des KEX hybrides comme `sntrup761x25519-sha512`. L'idée est de combiner un algo classique robuste (X25519) avec un algo quantique. Si l'algo quantique est cassé, la protection classique reste. C'est la stratégie de sécurité recommandée pour la transition.

## L'impact sur la Performance (Note SysOp)

La migration vers le Post-Quantique a un coût physique que l'Ops doit anticiper :

1.  **Taille des paquets** : Les clés et signatures PQC sont **beaucoup plus lourdes** que celles de RSA/ECC.
    *   *RSA-2048* : Clé publique ~256 octets.
    *   *ML-KEM (Kyber)* : Clé publique ~800 à 1500 octets.
    *   *ML-DSA (Dilithium)* : Signature ~2400 octets.
2.  **Impact Réseau** : Ces tailles peuvent causer la fragmentation des paquets IP (dépassement du MTU de 1500 bytes). Cela peut augmenter la latence lors des handshakes TLS, surtout sur les réseaux mobiles ou instables.
3.  **Charge Load-Balancers** : Vos terminaux SSL/TLS (Nginx, HAProxy, F5) devront gérer des buffers plus gros et consommeront un peu plus de RAM par connexion concurrente.

*Préparez vos capacités de bande passante et surveillez le "Time To First Byte" (TTFB) lors de la migration.*
