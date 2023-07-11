"""
This file contains the class MetricCalculator,
which is used to calculate a metric.

ags:
    variable (int): The variable to use in the metric calculation.

Returns:
    int: The metric value.
"""


class MetricCalculator:
    def __init__(self):
        self.variable = 5

    def calculate_metric(self):
        return self.variable * 2
