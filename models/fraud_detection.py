import pandas as pd
from pulp import *

# Global Constants
EXTERNAL_INVESTIGATOR_COST = {1: 40, 2: 60, 3: 100, 4: 150}
TIME_NEEDED = {1: 0.25, 2: 0.5, 3: 1, 4: 2}
INVESTIGATION_TEAM_SIZE = {"bank_a": 8, "bank_b": 12, "bank_c": 10, "bank_d": 10, "bank_e": 10}

def solve_initial_model(transactions_df, lambda_c, lambda_d, daily_budget):
    """
    Solves an optimization problem to maximize the expected value saved from fraud investigations.

    Parameters:
    - transactions_df (pd.DataFrame): DataFrame containing transaction details.
    - lambda_c (dict): Dictionary mapping categories to their respective investigation limits.
    - lambda_d (dict): Dictionary mapping descriptions to their respective investigation limits.
    - daily_budget (float): Budget available for external investigations.

    Returns:
    Tuple (list, list, float): Returns a tuple containing lists of transactions selected for
    internal and external investigations, and the expected value saved.
    """
    # Calculating combined probability, cost, and time for each transaction
    value = transactions_df["amount"]
    prob = 0.5 * transactions_df["customer_prob"] + 0.3 * transactions_df["description_prob"] + 0.2 * transactions_df["transac_prob"]
    cost = transactions_df["priority"].map(EXTERNAL_INVESTIGATOR_COST)
    investigation_time = transactions_df["priority"].map(TIME_NEEDED)

    # Initialize the linear programming model
    model = LpProblem("Fraud_Investigation", LpMaximize)

    # Define decision variables for internal (x), external (y), and team assignments (z)
    x = LpVariable.dicts("x", transactions_df.index, cat="Binary")
    y = LpVariable.dicts("y", transactions_df.index, cat="Binary")
    z = LpVariable.dicts("z", [(b, i) for b in INVESTIGATION_TEAM_SIZE.keys() for i in transactions_df.index], cat="Binary")

    # Define the objective function
    model += lpSum([value[i] * prob[i] * (x[i] + y[i]) - cost[i] * y[i] for i in transactions_df.index])

    # Add constraints to the model
    # 1. Investigation Exclusivity Constraint
    for i in transactions_df.index:
        model += x[i] + y[i] <= 1

    # 2. Bank Capacity Constraints for Internal Investigation
    for b in INVESTIGATION_TEAM_SIZE:
        model += lpSum([investigation_time[i] * z[(b, i)] for i in transactions_df.index]) <= INVESTIGATION_TEAM_SIZE[b]

    # 3. Bank Investigation Assignment Constraint
    for i in transactions_df.index:
        model += lpSum([z[(b, i)] for b in INVESTIGATION_TEAM_SIZE]) == x[i]

    # 4. Budget Constraint for External Investigation
    model += lpSum([y[i] * cost[i] for i in transactions_df.index]) <= daily_budget

    # 5. Variable Investigation per Category Ratio Constraint
    for c in lambda_c:
        I_c = transactions_df[transactions_df["category"] == c].index
        model += lpSum([x[i] + y[i] for i in I_c]) <= lambda_c[c] * lpSum([x[i] + y[i] for i in transactions_df.index])

    for d in lambda_d:
        I_d = transactions_df[transactions_df["description"].str.contains(d)].index
        model += lpSum([x[i] + y[i] for i in I_d]) <= lambda_d[d] * lpSum([x[i] + y[i] for i in transactions_df.index])

    # Solve the model and extract results
    model.solve()
    internally_investigated = [i for i in transactions_df.index if x[i].varValue == 1]
    externally_investigated = [i for i in transactions_df.index if y[i].varValue == 1]
    expected_value_saved = value(model.objective)

    return internally_investigated, externally_investigated, expected_value_saved

def compute_real_value_saved(x_ids, y_ids, transactions_df, fraudulent_transactions):
    """
    Calculates the actual value saved by the investigations based on the transactions flagged as fraudulent.

    Parameters:
    - x_ids (list): List of transaction IDs selected for internal investigation.
    - y_ids (list): List of transaction IDs selected for external investigation.
    - transactions_df (pd.DataFrame): DataFrame containing transaction details.
    - fraudulent_transactions (set): Set of IDs of transactions that are actually fraudulent.

    Returns:
    float: The total value saved by the investigations.
    """
    cost = transactions_df["priority"].map(EXTERNAL_INVESTIGATOR_COST)

    total_value_saved = 0

    # Iterate over identified transactions and calculate total value saved
    for i in x_ids + y_ids:
        if i in fraudulent_transactions:
            value = transactions_df.at[i, "amount"]  # Transaction value
            is_fraud = 1  # Flag indicating the transaction is fraudulent
            externally_investigated = 1 if i in y_ids else 0  # Flag for external investigation

            # Calculating value saved for each transaction
            total_value_saved += value * is_fraud - cost[i] * externally_investigated

    return total_value_saved

def solve_second_model(transactions_df, fraudulent_transactions, daily_budget):
    """
    Solves a second optimization model focusing on maximizing the value saved by investigating known fraudulent transactions.

    Parameters:
    - transactions_df (pd.DataFrame): DataFrame containing transaction details.
    - fraudulent_transactions (set): Set of transaction IDs known to be fraudulent.
    - daily_budget (float): Budget available for external investigations.

    Returns:
    Tuple (list, list, float): Returns a tuple containing lists of transactions selected for 
    internal and external investigations, and the value at stake.
    """
    # Initialize parameters for the model
    external_investigator_cost = {1: 40, 2: 60, 3: 100, 4: 150}
    time_needed = {1: 0.25, 2: 0.5, 3: 1, 4: 2}
    value = transactions_df["amount"]
    prob = 0.5 * transactions_df["customer_prob"] + 0.3 * transactions_df["description_prob"] + 0.2 * transactions_df["transac_prob"]
    cost = transactions_df["priority"].map(external_investigator_cost)
    investigation_time = transactions_df["priority"].map(time_needed)
    INVESTIGATION_TEAM_SIZE = {"bank_a": 8, "bank_b": 12, "bank_c": 10, "bank_d": 10, "bank_e": 10}

    # Define the linear programming model
    model = LpProblem("Fraud_Investigation", LpMaximize)

    # Define decision variables for internal (x), external (y), and team assignments (z)
    x = LpVariable.dicts("x", transactions_df.index, cat="Binary")
    y = LpVariable.dicts("y", transactions_df.index, cat="Binary")
    z = LpVariable.dicts("z", [(b, i) for b in INVESTIGATION_TEAM_SIZE.keys() for i in transactions_df.index], cat="Binary")

    # Define the objective function
    model += lpSum([value[i] * (x[i] + y[i]) - cost[i] * y[i] for i in transactions_df.index if i in fraudulent_transactions])

    # Add constraints similar to the first model
    for i in transactions_df.index:
        model += x[i] + y[i] <= 1
    for b in INVESTIGATION_TEAM_SIZE:
        model += lpSum([investigation_time[i] * z[(b, i)] for i in transactions_df.index]) <= INVESTIGATION_TEAM_SIZE[b]
    for i in transactions_df.index:
        model += lpSum([z[(b, i)] for b in INVESTIGATION_TEAM_SIZE]) == x[i]
    model += lpSum([y[i] * cost[i] for i in transactions_df.index]) <= daily_budget

    # Solve the model and extract results
    model.solve()
    internally_investigated = [i for i in transactions_df.index if x[i].varValue == 1]
    externally_investigated = [i for i in transactions_df.index if y[i].varValue == 1]
    value_at_stake = value(model.objective)

    return internally_investigated, externally_investigated, value_at_stake