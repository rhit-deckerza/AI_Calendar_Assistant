import pandas as pd
import matplotlib.pyplot as plt

def plot_statistics_by_directory(csv_file):
    # Load the CSV file into a DataFrame
    data = pd.read_csv(csv_file)

    # Sorting data by directory for consistent plotting
    data.sort_values('directory', inplace=True)

    # Create figures for mean, median, and standard deviation comparisons
    fig, axs = plt.subplots(3, 1, figsize=(14, 18))

    # Plotting the means
    axs[0].bar(data['directory'], data['score_mean'], width=0.2, label='Score', align='center')
    axs[0].bar(data['directory'], data['clarity_mean'], width=0.2, label='Clarity', align='edge')
    axs[0].bar(data['directory'], data['accuracy_mean'], width=0.2, label='Accuracy', align='edge')
    axs[0].set_title('Mean Comparison by Directory')
    axs[0].set_ylabel('Mean Values')
    axs[0].legend()

    # Plotting the medians
    axs[1].bar(data['directory'], data['score_median'], width=0.2, label='Score', align='center')
    axs[1].bar(data['directory'], data['clarity_median'], width=0.2, label='Clarity', align='edge')
    axs[1].bar(data['directory'], data['accuracy_median'], width=0.2, label='Accuracy', align='edge')
    axs[1].set_title('Median Comparison by Directory')
    axs[1].set_ylabel('Median Values')
    axs[1].legend()

    # Plotting the standard deviations
    axs[2].bar(data['directory'], data['score_std'], width=0.2, label='Score', align='center')
    axs[2].bar(data['directory'], data['clarity_std'], width=0.2, label='Clarity', align='edge')
    axs[2].bar(data['directory'], data['accuracy_std'], width=0.2, label='Accuracy', align='edge')
    axs[2].set_title('Standard Deviation Comparison by Directory')
    axs[2].set_ylabel('Standard Deviation Values')
    axs[2].legend()

    # Improving layout
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

# Usage
csv_path = 'scores_statistics.csv'
plot_statistics_by_directory(csv_path)
