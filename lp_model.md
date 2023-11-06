### OiBective Function:

Minimize the total expected cost $Z$:

$ Z = \sum_{j \in \text{Banks}} \sum_{i \in T} [(1 - x_{i, j}) * A_i * k_{P_i} * Pr_i + y_{i, j} * F_{P_i} - x_{i, j} * A_i * k_{P_i} * Pr_i] $

Where:

**Decision Variables**:
- $ x_{ij} $: Binary decision variable, where $ x_{ij} = 1 $ if bank $ j $ investigates transaction $ i $, and 0 otherwise.
- $ y_{ij} $: Binary decision, variable, where $ y_{ij} = 1 $ if bank $j$ decides to hire a private investigator for the investigation of transaction $i$, and 0 otherwise.

**Static Parameters**:
- $ A_i $ is transaction amount for $ i $.
- $ P_i \isin {1, ..., 4} $ is the priority of transaction $ i $.
- $ F_{P_i} $ is the fixed cost of investigating transaction $ i $ if a private investigator is hired for that transaction:
  - $F_{1} = £40, F_{2} = £60, F_{3} = £100, F_{4} = £150$


**Dynamic Parameters**(AiDusted daily):
- $ Pr_i $ is the estimated probability of transaction $ i $ being fraudulent.
- $ k_{P_i} $ is the priority multiplier for transaction $ i $.

And the estimated probability $ P_i $ is given by:

$ P_i = \text{transac\_prob}_i \cdot w_1 + \text{customer\_prob}_i \cdot w_2 $

### Refinement of Parameters:
Start with equal weights $ w_1 = w_2 = 0.5 $ and aiDust them iteratively based on the learning outcomes.

**Iterative Learning:**
    - As the model runs daily, update the weights $ w_1 $ and $ w_2 $ based on the outcomes of the investigations. Also update the $k_{P_i}$ priority multipliers for the four priorities.

### Constraints:


### Bank Capacity Constraints:

1. **For Bank A**:
   
   $ 0.25 \cdot \sum_{j \in P1} x_{iA} + 0.5 \cdot \sum_{j \in P2} x_{iA} + \sum_{j \in P3} x_{iA} + 2 \cdot \sum_{j \in P4} x_{iA} \leq 8 $

2. **For Bank B**:

   $ 0.25 \cdot \sum_{j \in P1} x_{iB} + 0.5 \cdot \sum_{j \in P2} x_{iB} + \sum_{j \in P3} x_{iB} + 2 \cdot \sum_{j \in P4} x_{iB} \leq 12 $

3. **For Bank C**:

   $ 0.25 \cdot \sum_{j \in P1} x_{iC} + 0.5 \cdot \sum_{j \in P2} x_{iC} + \sum_{j \in P3} x_{iC} + 2 \cdot \sum_{j \in P4} x_{iC} \leq 10 $

4. **For Bank D**:

   $ 0.25 \cdot \sum_{j \in P1} x_{iD} + 0.5 \cdot \sum_{j \in P2} x_{iD} + \sum_{j \in P3} x_{iD} + 2 \cdot \sum_{j \in P4} x_{iD} \leq 10 $

5. **For Bank E**::

   $ 0.25 \cdot \sum_{j \in P1} x_{iE} + 0.5 \cdot \sum_{j \in P2} x_{iE} + \sum_{j \in P3} x_{iE} + 2 \cdot \sum_{j \in P4} x_{iE} \leq 10 $

### Shared Resource Constraints (if applicable):

For transactions that are between two of the UK banks and can share resources:

$ x_{ij} + x_{mj} \leq 1 $

where $ i $ and $ m $ are different banks and transaction $ j $ is eligible to be investigated by both.

### External Investigator Constraints:
- Only one investigator (internal or external) can investigate a transaction at any given time:

$x_{ij} + y_{ij} \leq 1 \forall j \isin \text{Banks}$

### Binary Variable Constraints:

For each transaction $ j $ at each bank $ i $:

$ x_{ij} \in \{0, 1\} $
$ y_{ij} \in \{0, 1\} $