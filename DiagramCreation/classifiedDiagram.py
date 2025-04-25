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

    cost_categories = ['Very High Cost', 'High Cost', 'Low Cost', 'Very Low Cost']
    data['target_label'] = pd.Categorical(data['target_label'], categories=cost_categories, ordered=True)

    # Create a color palette for the target classes (0, 1, 2, 3)
    palette = {0: 'red', 1: 'blue', 2: 'green', 3: 'purple'}

    # Plot scatter plot (for each feature in columns)
    for column in data.columns[:-2]:  # Exclude 'target' and 'target_label' columns
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=data[column], y=data['target_label'], hue=data['target'], palette=palette, legend=False)
        plt.title(column)
        plt.xlabel('')
        plt.ylabel('')
        plt.tight_layout()
        plt.show()