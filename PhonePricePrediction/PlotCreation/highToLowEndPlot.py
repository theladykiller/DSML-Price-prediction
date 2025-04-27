import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def low_to_high_end_plot(columns, target):
    # Calculate the mean value for each data point (row)
    mean_values = columns.mean(axis=1)

    # Create a DataFrame for plotting
    data = pd.DataFrame({
        'mean_value': mean_values,
        'target': target
    })

    # Map target to labels
    cost_labels = {
        0: 'Very Low Cost',
        1: 'Low Cost',
        2: 'High Cost',
        3: 'Very High Cost'
    }
    data['target_label'] = data['target'].map(cost_labels)

    # Set correct order
    cost_categories = ['Very High Cost', 'High Cost', 'Low Cost', 'Very Low Cost']
    data['target_label'] = pd.Categorical(data['target_label'], categories=cost_categories, ordered=True)

    # Plot
    plt.figure(figsize=(8, 6))
    sns.stripplot(
        data=data,
        x='mean_value',
        y='target_label',
        hue='target_label',
        palette={
            'Very Low Cost': 'green',
            'Low Cost': 'blue',
            'High Cost': 'purple',
            'Very High Cost': 'red'
        },
        dodge=False,
        jitter=True,  # Spread points a bit for better visibility
        alpha=0.7,
        size=5,
        marker='o'
    )

    # Set x-axis ticks
    plt.xticks([0.15, 0.775], labels=["Low-End", "High-End"])
    plt.xlim(0.1, 0.825)

    plt.xlabel('')
    plt.ylabel('')
    plt.title('Device Position from Low-End to High-End by Average Feature Value')
    plt.legend([], [], frameon=False)
    plt.tight_layout()
    '''
    INSTRUCTIONS
    plt.show() only shows plots without saving
    plt.savefig() & plt.close() saves images into Plots directory
    You may want to chose one or the other
    '''
    plt.show()
    #plt.savefig(f'../Plots/LowToHighEndPlot.png')
    #plt.close()