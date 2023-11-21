from pulp import *
import itertools

# Global Constants
COST_EXTERNAL_INVESTIGATOR = {1: 40, 2: 60, 3: 100, 4: 150}
TIME_REQUIRED = {1: 0.25, 2: 0.5, 3: 1, 4: 2}
SIZE_INVESTIGATION_TEAM = {"bank_a": 8, "bank_b": 12, "bank_c": 10, "bank_d": 10, "bank_e": 10}


def solve_initial_model(transactions, limits_category, limits_description, budget_daily):
    """
    Solves an optimization problem to maximize the expected value saved from fraud investigations.

    Parameters:
    - transactions (pd.DataFrame): DataFrame containing transaction details.
    - limits_category (dict): Dictionary mapping categories to their respective investigation limits.
    - limits_description (dict): Dictionary mapping descriptions to their respective investigation limits.
    - budget_daily (float): Daily budget available for external investigations.

    Returns:
    Tuple (list, list, float): Lists of transactions selected for internal and external investigations, and the expected value saved.
    """
    # Calculating combined probability, cost, and time for each transaction
    amount = transactions["amount"]
    probability_combined = 0.5 * transactions["customer_prob"] + 0.3 * transactions["description_prob"] + 0.2 * \
                           transactions["transac_prob"]
    cost = transactions["priority"].map(COST_EXTERNAL_INVESTIGATOR)
    time_investigation = transactions["priority"].map(TIME_REQUIRED)

    # Initialize the model
    model = LpProblem("Optimize_Fraud_Investigation", LpMaximize)

    # Decision Variables
    internal_investigation = LpVariable.dicts("InternalInvestigate", transactions.index, cat="Binary")
    external_investigation = LpVariable.dicts("ExternalInvestigate", transactions.index, cat="Binary")
    shared_investigation = LpVariable.dicts("SharedInvestigate", transactions.index, cat="Binary")

    # Objective function
    model += lpSum([amount[trans] * probability_combined[trans] * (
                internal_investigation[trans] + external_investigation[trans]) - cost[trans] * external_investigation[
                        trans] for trans in transactions.index])

    # Constraints
    # Single Investigation Constraint
    for trans in transactions.index:
        model += internal_investigation[trans] + external_investigation[trans] + shared_investigation[trans] <= 1

    # Shared Investigation Constraint
    for trans in transactions.index:
        if transactions.loc[trans, 'bank_from'] != transactions.loc[trans, 'bank_to']:
            model += shared_investigation[trans] <= 1
        else:
            model += shared_investigation[trans] == 0

    # Investigation Time Constraint for Each Bank
    for bank in SIZE_INVESTIGATION_TEAM:
        time_allocated = []
        for trans in transactions.index:
            # Time allocated for internal investigations
            time_allocated.append(time_investigation[trans] * internal_investigation[trans])

            # Allocate time for shared investigations
            if transactions.loc[trans, 'bank_from'] == bank or transactions.loc[trans, 'bank_to'] == bank:
                time_allocated.append(0.5 * time_investigation[trans] * shared_investigation[trans])

        model += lpSum(time_allocated) <= SIZE_INVESTIGATION_TEAM[bank]

    # Budget Constraint
    model += lpSum([external_investigation[trans] * cost[trans] for trans in transactions.index]) <= budget_daily

    # Category and Description Constraints
    for category in limits_category:
        trans_category = transactions[transactions["category"] == category].index
        model += lpSum([internal_investigation[trans] + external_investigation[trans] + shared_investigation[trans] for trans in trans_category]) <= limits_category[category]

    for description in limits_description:
        trans_description = transactions[transactions["description"].str.contains(description)].index
        model += lpSum([internal_investigation[trans] + external_investigation[trans] + shared_investigation[trans] for trans in trans_description]) <= limits_description[description]



    # Solve and return results
    model.solve()
    investigated_internal = [trans for trans in transactions.index if internal_investigation[trans].varValue == 1]
    investigated_shared = [trans for trans in transactions.index if shared_investigation[trans].varValue == 1]
    investigated_internal += investigated_shared

    investigated_external = [trans for trans in transactions.index if external_investigation[trans].varValue == 1]

    value_saved_expected = pulp.value(model.objective)

    return investigated_internal, investigated_external, value_saved_expected


def compute_actual_value_saved(investigated_internal, investigated_external, transactions, fraudulent_transactions):
    """
    Calculates the actual value saved by the investigations based on the transactions flagged as fraudulent.

    Parameters:
    - investigated_internal (list): Transaction IDs selected for internal investigation.
    - investigated_external (list): Transaction IDs selected for external investigation.
    - transactions (pd.DataFrame): DataFrame containing transaction details.
    - fraudulent_transactions (set): IDs of transactions that are actually fraudulent.

    Returns:
    float: Total value saved by the investigations.
    """
    cost = transactions["priority"].map(COST_EXTERNAL_INVESTIGATOR)

    total_saved = 0

    # Calculate total value saved
    for trans in investigated_internal + investigated_external:
        if trans in fraudulent_transactions:
            amount = transactions.at[trans, "amount"]
            fraud_flag = 1
            external_investigate_flag = 1 if trans in investigated_external else 0

            total_saved += amount * fraud_flag - cost[trans] * external_investigate_flag

    return total_saved


def solve_second_model(transactions, fraudulent_transactions, budget_daily):
    """
    Solves a second optimization model focusing on maximizing the value saved by investigating known fraudulent transactions.

    Parameters:
    - transactions (pd.DataFrame): DataFrame containing transaction details.
    - fraudulent_transactions (set): Transaction IDs known to be fraudulent.
    - budget_daily (float): Daily budget available for external investigations.

    Returns:
    Tuple (list, list, float): Lists of transactions selected for internal and external investigations, and the value at stake.
    """
    # Extract test_data
    amount = transactions["amount"]
    cost = transactions["priority"].map(COST_EXTERNAL_INVESTIGATOR)
    time_investigation = transactions["priority"].map(TIME_REQUIRED)

    # Define the model
    model = LpProblem("Optimize_Fraud_Investigation_Focused", LpMaximize)

    # Decision variables
    internal_investigate = LpVariable.dicts("InternalInvestigate", transactions.index, cat="Binary")
    external_investigate = LpVariable.dicts("ExternalInvestigate", transactions.index, cat="Binary")
    team_assign = LpVariable.dicts("TeamAssign", [(bank, trans) for bank in SIZE_INVESTIGATION_TEAM.keys() for trans in
                                                  transactions.index], cat="Binary")

    # Objective function (focus on fraudulent transactions)
    model += lpSum([amount[trans] * (internal_investigate[trans] + external_investigate[trans]) - cost[trans] *
                    external_investigate[trans] for trans in transactions.index if trans in fraudulent_transactions])

    # Constraints similar to the first model
    for trans in transactions.index:
        model += internal_investigate[trans] + external_investigate[trans] <= 1

    for bank in SIZE_INVESTIGATION_TEAM:
        model += lpSum([time_investigation[trans] * team_assign[(bank, trans)] for trans in transactions.index]) <= \
                 SIZE_INVESTIGATION_TEAM[bank]

    for trans in transactions.index:
        model += lpSum([team_assign[(bank, trans)] for bank in SIZE_INVESTIGATION_TEAM]) == internal_investigate[trans]

    model += lpSum([external_investigate[trans] * cost[trans] for trans in transactions.index]) <= budget_daily

    # Solve and return results
    model.solve()
    investigated_internal = [trans for trans in transactions.index if internal_investigate[trans].varValue == 1]
    investigated_external = [trans for trans in transactions.index if external_investigate[trans].varValue == 1]
    value_at_stake = pulp.value(model.objective)

    return investigated_internal, investigated_external, value_at_stake