import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def classified_diagram(columns, target):
    # Create a DataFrame for easier manipulation
    data = pd.DataFrame(columns)
    data['target'] = target

    # Map numeric target values to custom labels
    cost_labels = {
        0: 'Very Low Cost',
        1: 'Low Cost',
        2: 'High Cost',
        3: 'Very High Cost'
    }

    # Replace target values with the custom labels
    data['target_label'] = data['target'].map(cost_labels)

    # Set the correct order of categories
    cost_categories = ['Very High Cost', 'High Cost', 'Low Cost', 'Very Low Cost']
    data['target_label'] = pd.Categorical(data['target_label'], categories=cost_categories, ordered=True)

    # Create a color palette for the target classes (using the string labels)
    palette = {
        'Very Low Cost': 'green',
        'Low Cost': 'blue',
        'High Cost': 'purple',
        'Very High Cost': 'red'
    }

    # Plot the distribution of each feature (column) for each class
    for column in data.columns[:-2]:  # Exclude 'target' and 'target_label' columns
        plt.figure(figsize=(8, 6))
        sns.histplot(data=data, x=column, hue='target_label', multiple="stack", palette=palette, kde=True)
        plt.title(column)
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.legend(title='Price Range', loc='upper right', labels=['Very Low Cost', 'Low Cost', 'High Cost', 'Very High Cost'])
        plt.tight_layout()
        plt.show()