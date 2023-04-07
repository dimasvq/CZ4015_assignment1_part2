import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def interarrival_time_histogram(df, bins=40, pdf=False):
    """Generates histogram for intearrival times, or normalised histogram
    with estimated probability density function if pdf is set to True"""

    sns.set(style='whitegrid')
    plt.figure()
    plt.xlabel('Interarrival time (sec)')
    plt.ylabel('Frequency')
    plt.title('Histogram of interarrival time')
    xlim = 7.5
    plt.xlim(0,xlim)

    if pdf is False:
        # Plot histogram.
        sns.histplot(data=df, x='Interarrival time (sec)', bins=bins)
        plt.savefig('figures/interarrival_time_histogram.png')

    else:
        # Plot normalised histogram.
        sns.histplot(data=df, x='Interarrival time (sec)', bins=bins, stat='density')
        # Calculate estimator for exponential distribution
        x = np.linspace(0, xlim, 1000)
        estimator = df['Interarrival time (sec)'].mean()
        pdf = 1/estimator * np.exp(-x/estimator)
        # Plot estimated pdf
        plt.plot(x,pdf,'r')
        plt.savefig('figures/interarrival_time_pdf.png')

    plt.show()


def base_station_histogram(df, pde=True):
    """Generates histogram for base stations where calls are generated"""

    sns.set(style='whitegrid')
    sns.histplot(data=df, x='Base station ', bins=20)
    plt.xlabel('Base station')
    plt.ylabel('Frequency')
    plt.title('Histogram of base stations')
    plt.xlim(0,20.5)
    plt.savefig('figures/base_station_histogram.png')
    plt.show()


def call_duration_histogram(df, pde=True):
    """Generates histogram for call duration"""

    sns.set(style='whitegrid')
    sns.histplot(data=df, x='Call duration (sec)', bins=40)
    plt.xlabel('Call duration')
    plt.ylabel('Frequency')
    plt.title('Histogram of call duration')
    plt.xlim(0,600)
    plt.savefig('figures/call_duration_histogram.png')
    plt.show()


def car_speed_histogram(df):
    """Generates histogram for car speed"""

    sns.set(style='whitegrid')
    sns.histplot(data=df, x='velocity (km/h)', bins=30)
    plt.xlabel('Car speed')
    plt.ylabel('Frequency')
    plt.title('Histogram of car speed')
    plt.xlim(90,152)
    plt.savefig('figures/car_speed_histogram.png')
    plt.show()


if __name__ == '__main__':
    df = pd.read_excel('simulation_data.xls')
    interarrival_time_histogram(df,pdf=True)
    # base_station_histogram(df)
    # call_duration_histogram(df)
    # car_speed_histogram(df)