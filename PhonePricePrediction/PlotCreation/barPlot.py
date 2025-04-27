import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle

def bar_plot(columns, target):
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

    # Plot
    for column in data.columns[:-2]:  # Exclude 'target' and 'target_label' columns
        plt.figure(figsize=(6, 6))
        ax = sns.histplot(
            data=data, x=column, hue='target_label', multiple="stack",
            palette=palette, kde=False, element="bars", stat="count"
        )

        # Add the labels inside the bars
        for p in ax.patches:    # type: Rectangle
            height = p.get_height()
            if height > 10:
                ax.annotate(
                    f'{int(height)}',
                    (p.get_x() + p.get_width() / 2., p.get_y() + height / 2.),
                    ha='center', va='center', fontsize=8, color='white', weight='bold'
                )

        # Check if the feature only contains 0 and 1
        unique_values = data[column].dropna().unique()
        if set(unique_values).issubset({0, 1}):
            plt.xlim(-0.1, 1.1)
            plt.xticks([0, 1], labels=["No", "Yes"])
            plt.xlabel('')
        else:
            plt.xlabel('Value')

        # Styling
        plt.title(column)
        plt.ylabel('Frequency')
        plt.legend(title='Price Range', labels=['Very Low Cost', 'Low Cost', 'High Cost', 'Very High Cost'])
        plt.tight_layout()
        '''
        INSTRUCTIONS
        plt.show() only shows plots without saving
        plt.savefig() & plt.close() saves images into Plots directory
        You may want to chose one or the other
        '''
        plt.show()
        #plt.savefig(f'../Plots/Bar_{column}.png')
        #plt.close()