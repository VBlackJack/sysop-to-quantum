# Guide Ops : Transition vers le Quantique

Bienvenue dans ce référentiel technique dédié aux équipes Infrastructure et Opérations.

## Pourquoi ce guide ?

En tant que **SysOp** ou **Architecte Cloud**, l'informatique quantique peut sembler être un sujet lointain, réservé aux chercheurs en physique. Cependant, l'impact sur nos infrastructures est imminent, notamment sur la sécurité des flux et la manière dont nous consommons les ressources de calcul.

Ce guide a été conçu pour anticiper l'obsolescence de nos standards actuels et préparer la sécurisation des infrastructures dès aujourd'hui, sans nécessiter de bagage mathématique complexe.

## Contenu du Guide

Le référentiel est divisé en trois piliers fondamentaux :

1.  **[Glossaire SysAdmin](glossaire.md)** : Comprendre les concepts (Qubit, Intrication, Décohérence) par l'analogie avec le hardware et le réseau classique.
2.  **[Infra Hybride (Terraform)](infra/terraform.md)** : Apprendre à provisionner des environnements de calcul quantique via le code (IaC) sur les fournisseurs Cloud (AWS Braket).
3.  **[Sécurité Post-Quantique](securite.md)** : Identifier la menace "Harvest Now, Decrypt Later" et durcir vos configurations (SSH, Ansible) avec les nouveaux standards du NIST.

---

!!! info "Work in Progress"
    Ce projet est en cours de rédaction. Les exemples de code et les scripts de déploiement sont testés sur des simulateurs quantiques et des instances de développement.

**Projet maintenu par Julien Bombled**  
*Licence Apache 2.0*
