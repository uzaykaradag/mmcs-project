### Objective Function:

Minimize the total expected cost $Z$:

$ Z = \sum_{i \in T}\sum_{j \in \text{Banks}}\sum_
{p=1}^{4} [(1 - x_{i, j}) * A_i * k_{p} * Pr_i + y_{ijp} * F_{p} - x_{i, j} * A_i * k_{p} * Pr_i] $

Where:

**Decision Variables**:

- $ x_{ijp} $: Binary decision variable, where $ x_{ij} = 1 $ if bank $ j $ investigates transaction $ i $, and 0
  otherwise, p denotes the priority of the transaction.
- $ y_{ijp} $: Binary decision, variable, where $ y_{ij} = 1 $ if bank $j$ decides to hire a private investigator for
  the investigation of transaction $i$, and 0 otherwise, p denotes the priority of the transaction.

**Static Parameters**:

- $ A_i $ is transaction amount for $ i $.
- $ F_{p} $ is the fixed cost of investigating transaction $ i $ if a private investigator is hired for that
  transaction:
    - $F_{1} = £40, F_{2} = £60, F_{3} = £100, F_{4} = £150$

**Dynamic Parameters**(AiDusted daily):

- $ Pr_i $ is the estimated probability of transaction $ i $ being fraudulent.
- $ k_{p} $ is the priority multiplier for transaction $ i $.

And the estimated probability $ Pr_i $ is given by:

$ p = \text{transac\_prob}_i \cdot w_1 + \text{customer\_prob}_i \cdot w_2 $

### Refinement of Parameters:

Start with equal weights $ w_1 = w_2 = 0.5 $ and aiDust them iteratively based on the learning outcomes.

**Iterative Learning:**
- As the model runs daily, update the weights $ w_1 $ and $ w_2 $ based on the outcomes of the investigations. Also
update the $k_{p}$ priority multipliers for the four priorities.

### Constraints:

### Bank Capacity Constraints:

1. **For Bank A**:

   $ 0.25 \cdot \sum_{i \in T}\sum_{p \in P1} x_{iAp} + 0.5 \cdot \sum_{i \in T}\sum_{p \in P2} x_{iAp} + \sum_{i \in
   T}\sum_{p \in P3} x_{iAp} + 2 \cdot \sum_{i \in T}\sum_{p \in P4} x_{iAp} \leq 8 $

2. **For Bank B**:

   $ 0.25 \cdot \sum_{i \in T}\sum_{p \in P1} x_{iBp} + 0.5 \cdot \sum_{i \in T}\sum_{p \in P2} x_{iBp} + \sum_{i \in
   T}\sum_{p \in P3} x_{iBp} + 2 \cdot \sum_{i \in T}\sum_{p \in P4} x_{iBp} \leq 12 $

3. **For Bank C**:

   $ 0.25 \cdot \sum_{i \in T}\sum_{p \in P1} x_{iCp} + 0.5 \cdot \sum_{i \in T}\sum_{p \in P2} x_{iCp} + \sum_{i \in
   T}\sum_{p \in P3} x_{iCp} + 2 \cdot \sum_{i \in T}\sum_{p \in P4} x_{iCp} \leq 10 $

4. **For Bank D**:

   $ 0.25 \cdot \sum_{i \in T}\sum_{p \in P1} x_{iDp} + 0.5 \cdot \sum_{i \in T}\sum_{p \in P2} x_{iDp} + \sum_{i \in
   T}\sum_{p \in P3} x_{iDp} + 2 \cdot \sum_{i \in T}\sum_{p \in P4} x_{iDp} \leq 10 $

5. **For Bank E**::

   $ 0.25 \cdot \sum_{i \in T}\sum_{p \in P1} x_{iEp} + 0.5 \cdot \sum_{i \in T}\sum_{p \in P2} x_{iEp} + \sum_{i \in
   T}\sum_{p \in P3} x_{iEp} + 2 \cdot \sum_{i \in T}\sum_{p \in P4} x_{iEp} \leq 10 $

### Shared Resource Constraints (if applicable):

For transactions that are between two of the UK banks and can share resources:

$ x_{ijp} + x_{mjp} \leq 1 $

where $ i $ and $ m $ are different banks and transaction $ j $ is eligible to be investigated by both.

### External Investigator Constraints:

- Only one investigator (internal or external) can investigate a transaction at any given time:

$x_{ijp} + y_{ijp} \leq 1 \forall j \isin \text{Banks}$

### Binary Variable Constraints:

For each transaction $ j $ at each bank $ i $:

$ x_{ijp} \in \{0, 1\} $
$ y_{ijp} \in \{0, 1\} $