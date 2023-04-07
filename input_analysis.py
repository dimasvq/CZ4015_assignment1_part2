import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def interarrival_time_histogram(df, bins=50):
    """Generates histogram for intearrival times"""

    sns.set(style='whitegrid')
    sns.histplot(data=df, x='Interarrival time (sec)', bins=50, kde=True)
    plt.xlabel('Interarrival time (sec)')
    plt.ylabel('Frequency')
    plt.title('Histogram of interarrival time')
    plt.show()