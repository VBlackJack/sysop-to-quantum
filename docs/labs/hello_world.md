<!--
Auteur : Julien Bombled
Licence : Apache License 2.0
-->

# Lab 1 : "Hello World" (Smoke Test)

## Introduction : Le "Ping" Quantique

Dans le monde de l'infrastructure, la première action après une installation est un `ping` ou un `curl` pour vérifier la connectivité. Dans le monde quantique, l'équivalent est de créer un **État de Bell**.

Ce script ne réalise pas un calcul utile. Son seul but est de **valider la toolchain** :
1.  L'interpréteur Python est correct.
2.  Le SDK (Qiskit) est chargé.
3.  Le simulateur local fonctionne.

L'objectif est d'intriquer 2 qubits. Si ça marche, ils doivent toujours donner la même valeur lorsqu'on les mesure : soit tous les deux à 0, soit tous les deux à 1.

## Pré-requis

*   Python 3.10 ou supérieur.
*   Installation des librairies :
    ```bash
    pip install qiskit qiskit-aer
    ```

## Le Code de Test (`quantum_ping.py`)

Copiez ce code pour tester votre environnement local.

```python
#!/usr/bin/env python3
"""
Author: Julien Bombled
License: Apache License 2.0

Description:
This script acts as a "Smoke Test" for the quantum environment.
It creates a simple Bell State (Entanglement) between 2 qubits.
This is the quantum equivalent of a "Hello World" or "Ping".
"""

from qiskit import QuantumCircuit
from qiskit.primitives import Sampler
from qiskit.visualization import plot_histogram

def run_quantum_ping():
    print(">>> Starting Quantum Connectivity Test (Smoke Test)...")

    # 1. Allocation: Request 2 Qubits (like allocating 2 bits of RAM)
    #    and 2 Classical Bits to store the measurement result.
    qc = QuantumCircuit(2, 2)

    # 2. Logic: Create Entanglement (The "Circuit")
    #    Apply Hadamard gate (H) on qubit 0 -> Puts it in Superposition (0 and 1 at same time)
    qc.h(0)
    #    Apply CNOT gate (CX) between qubit 0 and 1 -> Entangles them.
    #    If q0 is 0, q1 stays 0. If q0 is 1, q1 flips to 1.
    qc.cx(0, 1)

    # 3. Measurement: Read the state of qubits into classical bits
    qc.measure([0, 1], [0, 1])

    print(">>> Circuit built successfully.")
    print(">>> Submitting job to local simulator...")

    # 4. Execution: Run the circuit on a local simulator
    #    We run the experiment 1000 times ("shots") to get statistics.
    sampler = Sampler()
    job = sampler.run(qc)
    result = job.result()
    
    # Get the probability distribution (quasi-probabilities)
    quasi_dists = result.quasi_dists[0]
    
    # Convert keys from integer to binary string for readability
    # e.g., 0 -> '00', 3 -> '11'
    counts = {format(k, '02b'): v for k, v in quasi_dists.items()}

    print(f">>> Result (Probabilities): {counts}")
    
    return counts

if __name__ == "__main__":
    try:
        results = run_quantum_ping()
        
        # Simple validation logic for the SysOp
        # We expect roughly 50% '00' and 50% '11'.
        # Small deviations are normal due to probabilistic nature, 
        # but seeing '01' or '10' would indicate a simulator error (noise).
        if '00' in results and '11' in results:
            print(">>> SUCCESS: Entanglement verified. Environment is healthy.")
        else:
            print(">>> FAILURE: Unexpected results. Check installation.")
            
    except Exception as e:
        print(f">>> CRITICAL ERROR: {e}")
        print(">>> Verify that 'qiskit' and 'qiskit-aer' are installed.")
```

## Interprétation pour le SysAdmin

Une fois le script exécuté (`python quantum_ping.py`), regardez la ligne `Result`.

*   **Résultat attendu :** Environ `{'00': 0.5, '11': 0.5}`.
    *   Cela signifie que les deux qubits sont **synchronisés** (intriqués). Si l'un vaut 0, l'autre vaut 0. Si l'un vaut 1, l'autre vaut 1.
*   **Résultat d'erreur :** Si vous voyez apparaître `'01'` ou `'10'` avec des probabilités significatives.
    *   Cela signifierait que l'intrication a échoué (les qubits sont désynchronisés). Sur un simulateur parfait, c'est impossible. Sur un vrai hardware, ce serait du "bruit" (décohérence).
