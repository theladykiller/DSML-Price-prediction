# constants.py
cost_labels = {
    0: 'Very Low Cost',
    1: 'Low Cost',
    2: 'High Cost',
    3: 'Very High Cost'
}

cost_categories = ['Very Low Cost', 'Low Cost', 'High Cost', 'Very High Cost']
#cost_categories = list(cost_labels.values())[::-1]

palette = {
    label: color for label, color in zip(cost_labels.values(), ['gold', 'darkcyan', 'mediumvioletred', 'orangered'])
}