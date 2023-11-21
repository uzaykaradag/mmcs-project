# Fraud Detection Model

## Preface
This model runs daily to iteratively "learn" from the past day's result for better detection. It utilizes a loss function for parameter tuning in the constraints. The loss function parameters are the right-hand side for the values of the constraints related to category of the transaction and the description of the transaction.

### Sets
**Transaction ID Sets**
- $I$: Set of transaction_id's for the given day
- $I_{b_f, b_t}$: Set of transaction_id's that are from a bank $b_f$ to bank $b_t$, note that $b_f, b_t \isin \text{Banks}$
- $I_{c}$: Set of transaction_id's that are identified in category $c$
- $I_{d}$: Set of transaction_id's that are identified in description $d$

**Data Columns**
- $\text{Banks}$: Set containing all possible banks and international transactions = ['bank_C', 'bank_D', 'bank_A', 'bank_E', 'Intrnl', 'bank_B']
- $\text{Categories}$: Set containing all possible categories for transactions = ['Utilities',
 'Housing',
 'Groceries',
 'Dining Out',
 'Transfers',
 'Credit Card Payment',
 'Healthcare',
 'Home Improvement',
 'Shopping',
 'Charity',
 'Online Shopping',
 'Loan Payment',
 'Transportation',
 'Electronics',
 'Bank Fees',
 'Investment',
 'Streaming Services',
 'Entertainment',
 'Holiday',
 'Personal care']
- $\text{Description}$: Set containing all possible descriptions for transactions

### Parameters
- $V_i$: The value associated with transaction $i$
- $P_i$: The fraud probability associated with transaction $i$ (Calculated as a weighted average of *customer_prob, transac_prob* and *description_prob*)
- $C_i$: The fixed cost for hiring an external investigator for transaction $i$ (depends on the priority)
= P

### Variables 
- $x_i$: Binary decision variable denoting if transaction $i$ is going to be internally investigated, 1 if yes, 0 if no
- $y_i$: Binary decision variable denoting if transaction $i$ is going to be externally investigated, 1 if yes, 0 if no

### Initial Model:
#### Objective Function
- **Maximize the total value saved**

$\text{max} \sum_{i \isin I} V_i * P_i * x_i + V_i * P_i * y_i - C_i * y_i$

#### Constraints
- An investigation can be investigated either internally or externally:

$x_i + y_i \leq 1, \forall i \isin I$ 

- Bank capacity constraints for internal investigation

**TODO** How to model the bank_from and bank_to sharing investigators for investigation of transaction

- Budget constraint for external investigation

$\sum_{i \isin I} y_i * C_i \leq \text{Daily Budget}$

- Variable investigation per category ratio constraint

$\frac{\sum_{i \isin I_c} x_i + y_i}{\sum_{i \isin I} x_i + y_i} \leq \lambda_c$  for $c$ = Utilities, Shopping, Holiday

- Variable investigation per category ratio constraint

$\frac{\sum_{i \isin I_d} x_i + y_i}{\sum_{i \isin I} x_i + y_i} \leq \lambda_d$  for $d$ = Sport event tickets,Facebook Marketplace Upfront payment, ClothesOnline additional posting payment

### Computation of Possible Values
We solve the Initial Model for combinations of each $\lambda_c, \lambda_d$ and obtain an optimal solution associated with that combination denoted with $\tilde{x}$ and $\tilde{y}$.

Next we use $\tilde{x}$ and $\tilde{y}$ to compute the **value saved for the day**.

To do this we have to define a new variable:
$f_i$ where $f_i = 1$ if transaction $i$ is fraudulent and 0 otherwise.

- Compute value saved for the day as:

$\tilde{z} = \sum_{i \isin I} V_i * f_i * \tilde{x_i} + V_i * f_i * \tilde{y_i} - C_i * \tilde{y_i}$

### Second Model
Here know that we know the fraud cases for the day we try to find the optimal value under only the resource constraints. The variable constraints are omitted, because of perfect information. Keep in mind that $\hat{x}$ and $\hat{y}$ are decision variables unlike $\tilde{x}$ and $\tilde{y}$ which were already known.

- Optimize the value saved under perfect information

$\hat{z} = \sum_{i \isin I} V_i * f_i * \hat{x_i} + V_i * f_i * \hat{y_i} - C_i * \hat{y_i}$

- An investigation can be investigated either internally or externally:

$x_i + y_i \leq 1, \forall i \isin I$ 

- Bank capacity constraints for internal investigation

**TODO** How to model the bank_from and bank_to sharing investigators for investigation of transaction

- Budget constraint for external investigation

$\sum_{i \isin I} y_i * C_i \leq \text{Daily Budget}$


### The Loss Function and Parameter Tuning
Now that we have the optimal solutions for value saved for the day for both perfect information and imperfect information, we can define the loss function as the following, $\Lambda$ is defined as the combined vector for all $\lambda_c$ and $\lambda_d$ values:

$f(\Lambda) = \hat{z} - \tilde{z}$

Now what we need to do is find the minimizer $\Lambda^*$ of $f(\Lambda)$ and use $\Lambda^*$ for next day's respective constraints.

The model should be checked to see if it iteratively gets better by using the confusion matrix and plots that are off value saved vs day.


Certainly! I will integrate the shared investigator capacity constraint into your existing fraud detection model, ensuring all other parts of the model remain unchanged. The integration will include the additional parameters and constraints as discussed. Here's the updated model:

### Updated Fraud Detection Model

#### Sets
- $I$: Set of transaction_id's for the given day
- $I_{b_f, b_t}$: Set of transaction_id's that are from a bank $b_f$ to bank $b_t$, note that $b_f, b_t \in \text{Banks}$
- $I_{c}$: Set of transaction_id's that are identified in category $c$
- $I_{d}$: Set of transaction_id's that are identified in description $d$

#### Data Columns
- $\text{Banks}$: Set containing all possible banks and international transactions = ['bank_C', 'bank_D', 'bank_A', 'bank_E', 'Intrnl', 'bank_B']
- $\text{Categories}$: Set containing all possible categories for transactions = ['Utilities', 'Housing', 'Groceries', 'Dining Out', 'Transfers', 'Credit Card Payment', 'Healthcare', 'Home Improvement', 'Shopping', 'Charity', 'Online Shopping', 'Loan Payment', 'Transportation', 'Electronics', 'Bank Fees', 'Investment', 'Streaming Services', 'Entertainment', 'Holiday', 'Personal care']
- $\text{Description}$: Set containing all possible descriptions for transactions

#### Parameters
- $V_i$: The value associated with transaction $i$

- $P_i$: The fraud probability associated with transaction $i$

- $C_i$: The fixed cost for hiring an external investigator for transaction $i$


- $T_\text{Bank}$: Total investigator capacity for bank $b$ per day
    - $T_\text{bank\_a} = 8$
    - $T_\text{bank\_b} = 12$
    - $T_\text{bank\_c} = 10$
    - $T_\text{bank\_d} = 10$
    - $T_\text{bank\_e} = 10$


- $t_i$: Time required in days to investigate transaction $i$ (depends on the priority)
    - $t_i = 0.25$ if priority of transaction $i$ is 1 
    - $t_i = 0.5$ if priority of transaction $i$ is 1 
    - $t_i = 1$ if priority of transaction $i$ is 1 
    - $t_i = 2$ if priority of transaction $i$ is 1 

- $D$: Number of days in the period being considered (typically 1)

#### Variables 
- $x_i$: Binary decision variable for internal investigation of transaction $i$
- $y_i$: Binary decision variable for external investigation of transaction $i$
- $z_{b,i}$: Binary decision variable for bank $b$ investigating transaction $i$ internally

#### Objective Function
- **Maximize the total value saved**
  $
  \text{max} \sum_{i \in I} V_i * P_i * x_i + V_i * P_i * y_i - C_i * y_i
  $

#### Constraints
1. **Investigation Exclusivity Constraint**:
   $
   x_i + y_i \leq 1, \forall i \in I
   $

2. **Bank Capacity Constraints for Internal Investigation**:

   $
   \sum_{i \in I} t_i \cdot z_{b_f,i} + \sum_{i \in I_{b_f, b_t}} t_i \cdot z_{b_t,i} \leq T_{b_f} \cdot D, \quad \forall b_f, b_t \in \text{Banks}, b_f \neq b_t
   $

3. **Bank Investigation Assignment Constraint**:

   $
   \sum_{b \in \text{Banks}} z_{b,i} = x_i, \forall i \in I
   $

4. **Budget Constraint for External Investigation**:

   $
   \sum_{i \in I} y_i * C_i \leq \text{Daily Budget}
   $

5. **Variable Investigation per Category Ratio Constraint**:

   - For Categories: 

     $
     \frac{\sum_{i \in I_c} x_i + y_i}{\sum_{i \in I} x_i + y_i} \leq \lambda_c$
     for  c = Utilities, Shopping, Holiday

   - For Descriptions: 

     $
     \frac{\sum_{i \in I_d} x_i + y_i}{\sum_{i \in I} x_i + y_i} \leq \lambda_d$ for $d$ = Sport event tickets, Facebook Marketplace Upfront payment, Clothes Online additional posting payment

#### Computation of Possible Values
- Detailed as in your original model description.

#### The Loss Function and Parameter Tuning
- Defined as in your original model description.

This integration ensures that your model now includes the capability to handle shared investigator resources between banks for internal investigations. The constraints are formulated to respect each bank's capacity while allowing for the flexibility of shared resources.