import random


def generate(category_list, selection_size, lower_bound, upper_bound):
    # Randomly select categories
    categories = random.sample(category_list, selection_size)

    # Randomly assign ratios to the categories respecting the boundaries
    ratios = [random.uniform(lower_bound, upper_bound) for sc in categories]

    # Create a dictionary with the categories and their associated ratio limit for the constraints
    limit_category = {category: ratio for category, ratio in zip(categories, ratios)}

    return limit_category
