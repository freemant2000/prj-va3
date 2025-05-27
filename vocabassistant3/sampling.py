import math

def calc_sample_size(population_size, margin_of_error, confidence_level, proportion=0.5):
    z_scores={90: 1.645, 95: 1.96, 99: 2.575}
    z_score=z_scores[confidence_level]
    margin_of_error=margin_of_error/100
    sample_size = ((z_score**2 * proportion * (1 - proportion)) / (margin_of_error**2)) / (1 + ((z_score**2 * proportion * (1 - proportion)) / (margin_of_error**2 * population_size)))
    return math.ceil(sample_size)

# population_size = 1000  # If population size is unknown, set it to None
# margin_of_error = 10  # 5% margin of error
# confidence_level = 95  # 95% confidence level
# proportion = 0.5  # Estimated proportion (use 0.5 if unknown)

# required_sample_size = calc_sample_size(population_size, margin_of_error, confidence_level, proportion)
# print("Required sample size:", required_sample_size)