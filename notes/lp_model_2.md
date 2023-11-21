### Objective Function:

Minimize $ Z $, the total expected cost, which is:

$
Z = \sum_{i \in T}
\left[(1 - x_{i}) \cdot A_{i} \cdot k \cdot Pr_{i} + y_{i} \cdot F_i - x_{i} \cdot A_{i} \cdot k_i \cdot Pr_{i}\right]
$

### Sets:

- Let $ T $ be the set of transaction IDs.

### Decision Variables:

- $ x_{i} $: Binary variable where $ x_{i} = 1 $ if transaction $ i $ is investigated, 0 otherwise.
- $ y_{i} $: Binary variable where $ y_{i} = 1 $ if a private investigator is hired for transaction $ i $, 0
  otherwise.

### Parameters:

- $ A_{i} $: Amount for transaction $ i $.
- $ Pr_{i} $: Estimated probability of transaction $ i $ being fraudulent.
- $ k_i $: Priority multiplier (which would be set based on the priority of transaction $ i $ in the previous
  formulation).
- $ F_i $: Fixed cost of investigation (which would vary based on the priority level in the previous formulation).

### Probability and Multipliers:

Since the model no longer indexes by priority $ p $, you would need a way to determine $ k $ and $ F $ for each
transaction $ i $ outside of the LP formulation, such as through pre-processing.

### Constraints:

#### Capacity Constraint:

Each bank $ j $ is replaced by a set of transactions $ T_j \subset T $ that it can investigate:

$
\sum_{i \in T_j} x_{i} *  \leq C_j
$

#### Investigator Constraint:

The constraint for hiring an external investigator is:

$
x_{i} + y_{i} \leq 1 \quad \forall i \in T
$

#### Binary Constraints:

$
x_{i} \in \{0, 1\}, \quad y_{i} \in \{0, 1\}
$