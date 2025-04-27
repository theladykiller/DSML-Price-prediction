import pandas as pd
import matplotlib.pyplot as plt

def regression_curve_plot(columns, target):
    # Create a DataFrame
    data = pd.DataFrame(columns)
    data['target'] = target

    cost_labels = {
        0: 'Very Low Cost',
        1: 'Low Cost',
        2: 'High Cost',
        3: 'Very High Cost'
    }
    data['target_label'] = data['target'].map(cost_labels)

    palette = {
        'Very Low Cost': 'green',
        'Low Cost': 'blue',
        'High Cost': 'purple',
        'Very High Cost': 'red'
    }

    cost_categories = ['Very Low Cost', 'Low Cost', 'High Cost', 'Very High Cost']

    for column in data.columns[:-2]:
        plt.figure(figsize=(6, 6))

        # Draw dots
        mean_values = []
        for label in cost_categories:
            subset = data[data['target_label'] == label]
            x = [label] * len(subset)
            y = subset[column]
            plt.scatter(
                x, y, color=palette[label],
                alpha=0.7, edgecolor='k', s=40
            )
            # Calculate mean values for each class
            mean_value = subset[column].mean()
            mean_values.append(mean_value)

        # Draw line graph for mean values
        plt.plot(cost_categories, mean_values, color='black', marker='o', linestyle='-', label='Mean Value per Class', linewidth=2)

        # Check if the feature only contains 0 and 1
        unique_values = data[column].dropna().unique()
        if set(unique_values).issubset({0, 1}):
            plt.ylim(-0.1, 1.1)  # Force the y-axis between -0.1 and 1.1
            plt.yticks([0, 0.5, 1], labels=["No", "Center", "Yes"])
            plt.axhline(0.5, color='black', linestyle='-', linewidth=0.5)

        # Styling
        plt.ylabel('Value')
        plt.xlabel('')
        plt.title(column)
        plt.xticks(ticks=cost_categories)
        plt.legend(title='Legend', loc='upper right')
        plt.tight_layout()
        '''
        INSTRUCTIONS
        plt.show() only shows plots without saving
        plt.savefig() & plt.close() saves images into Plots directory
        You may want to chose one or the other
        '''
        plt.show()
        #plt.savefig(f'../Plots/Curve_{column}.png')
        #plt.close()