import models as md
import limits


def calculate_loss(limits_category, transactions, budget_daily, fraudulent_transactions):
    """
    Calculates the loss for a given limits_category configuration.

    Parameters:
    - limits_category (dict): Dictionary mapping categories to their respective investigation limits.
    - transactions (pd.DataFrame): DataFrame containing transaction details.
    - budget_daily (float): Daily budget available for external investigations.
    - fraudulent_transactions (set): IDs of transactions that are actually fraudulent.

    Returns:
    float: The loss value calculated as value_at_stake - total_saved.
    """
    # Solve the second model to get the value at stake
    _, _, value_at_stake = md.solve_second_model(transactions, fraudulent_transactions, budget_daily)

    # Solve the initial model to get the transactions investigated internally and externally
    investigated_internal, investigated_external, _ = md.solve_initial_model(transactions, limits_category,
                                                                             budget_daily)

    # Compute the actual value saved
    total_saved = md.compute_actual_value_saved(investigated_internal, investigated_external, transactions,
                                                fraudulent_transactions)

    # Calculate and return the loss
    return value_at_stake - total_saved


def find_minimizer_random(transactions, budget_daily, fraudulent_transactions, categories, Nruns):
    limits_minimizer = {}
    min_loss = 1000000

    for _ in range(Nruns):
        limits_category = limits.generate(categories, 5, 0, 1)
        loss_iter = calculate_loss(limits_category, transactions, budget_daily, fraudulent_transactions)
        if loss_iter <= min_loss:
            min_loss = loss_iter
            limits_minimizer = limits_category

    return limits_minimizer, min_loss
