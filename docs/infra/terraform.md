<!--
Auteur : Julien Bombled
Licence : Apache License 2.0
-->

# Infrastructure as Code pour le Quantique

## Introduction : Le QPU "As a Service"

Pour un SysOp ou un Architecte Infrastructure, la première chose à comprendre est que le **QPU (Quantum Processing Unit)** n'est pas un matériel que vous allez installer dans vos baies serveurs (pour l'instant). Les contraintes de refroidissement (proche du zéro absolu) et d'isolation magnétique rendent l'hébergement "On-Premise" impossible pour la majorité des entreprises.

L'informatique quantique se consomme aujourd'hui exclusivement en modèle **PaaS/SaaS**.

Dans ce contexte, **Terraform** ne sert pas à provisionner le processeur quantique lui-même, mais à construire l'environnement périphérique (l'Hybrid Cloud) :
1.  **Le stockage** : Où atterrissent les résultats des mesures (souvent volumineux).
2.  **L'environnement de développement** : Notebooks Jupyter managés pour soumettre les jobs.
3.  **La sécurité (IAM)** : Qui a le droit de dépenser du budget sur un QPU à 5000$/heure.

## Architecture Hybride

Le schéma ci-dessous illustre le flux de provisionning et d'exécution. Terraform configure le "Control Plane" Cloud, qui fait le pont vers le hardware quantique.

```mermaid
graph LR
    Dev[DevOps / Researcher] -->|1. git push / apply| TF[Terraform]
    TF -->|2. Provision Resources| Cloud[Public Cloud Provider\n(AWS / Azure / GCP)]
    
    subgraph "Managed Environment"
        NB[Managed Notebook\n(Jupyter)]
        Store[Object Storage\n(S3 / Blob)]
        IAM[IAM Policies]
    end
    
    Cloud --> NB
    Cloud --> Store
    Cloud --> IAM
    
    NB -.->|3. Submit Job via API| QService[Quantum Service\n(Braket / Quantum)]
    QService ===|4. Execution| QPU[QPU Hardware\n(IonQ / Rigetti / IBM)]
```

## Exemple Concret : Environnement AWS Braket

Voici un exemple de code Terraform (HCL) pour déployer un environnement de travail complet sur AWS utilisant le service **Amazon Braket**.

Ce code déploie :
*   Un **Bucket S3** pour les inputs/outputs.
*   Un **Notebook SageMaker** pré-configuré pour Braket (l'IDE du développeur quantique).
*   Les **Rôles IAM** nécessaires.

```hcl
# main.tf
# Author: Julien Bombled
# License: Apache 2.0

provider "aws" {
  region = "us-east-1" # Many quantum devices are region-specific
}

# 1. Storage for Quantum Job Results
# The QPU will write measurement results directly here
resource "aws_s3_bucket" "quantum_results" {
  bucket = "company-quantum-results-prod-001"
  
  tags = {
    Environment = "Production"
    Project     = "Quantum-Hybrid"
  }
}

# 2. IAM Role for the Notebook
# This role allows the Notebook to talk to Braket and S3
resource "aws_iam_role" "quantum_notebook_role" {
  name = "QuantumNotebookRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "sagemaker.amazonaws.com"
      }
    }]
  })
}

# Attach standard Braket permissions
resource "aws_iam_role_policy_attachment" "braket_full_access" {
  role       = aws_iam_role.quantum_notebook_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonBraketFullAccess"
}

# 3. The Development Environment (Managed Notebook)
# This is where the Python SDK (Braket) runs
resource "aws_sagemaker_notebook_instance" "quantum_dev_env" {
  name          = "Quantum-Dev-Instance-XL"
  role_arn      = aws_iam_role.quantum_notebook_role.arn
  instance_type = "ml.t3.medium" # Classic CPU is enough to submit jobs
  
  tags = {
    Type = "Quantum-Gateway"
  }
}
```

## Analyse pour l'Opérationnel

Pour un admin Terraform habitué, ce code est trivial, et c'est tout l'intérêt. L'accès au quantique n'est "qu'une API de plus".

1.  **`aws_s3_bucket`** : C'est votre disque dur partagé. Le QPU (ex: un ordinateur de chez Rigetti ou IonQ) va uploader ses logs et résultats binaires ici. C'est le point de découplage.
2.  **`aws_iam_role`** : C'est ici que vous contrôlez les coûts et la sécu. La policy `AmazonBraketFullAccess` donne le droit d'envoyer des tâches aux machines quantiques.
3.  **`aws_sagemaker_notebook_instance`** : Notez le type d'instance `ml.t3.medium`. C'est du CPU classique standard. Le code Python tourne sur ce CPU, prépare le circuit quantique, et l'envoie au QPU via le réseau. **On n'a pas besoin de puissance de calcul local**, juste d'une connectivité réseau vers l'API Braket.

!!! warning "Cloud Privé et Souveraineté"
    Dans des contextes haute sécurité (**SecNumCloud**, Défense, Banque), vous ne pouvez pas installer de QPU dans votre datacenter privé.

    L'architecture de référence consiste alors à utiliser un **Proxy/Passerelle** en zone démilitarisée (DMZ). Vos serveurs internes envoient les circuits quantiques à ce proxy, qui filtre, anonymise potentiellement les données, et transmet la requête au fournisseur Cloud (AWS/Azure/IBM) via une liaison sécurisée. Le "backend" de calcul reste public ou dédié, mais jamais totalement interne.

