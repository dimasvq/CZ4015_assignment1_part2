import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm


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
        # Calculate maximum likelihood estimator for exponential distribution
        x = np.linspace(0, xlim, 1000)
        estimator = df['Interarrival time (sec)'].mean()
        pdf = 1/estimator * np.exp(-x/estimator)
        # Plot estimated pdf
        plt.plot(x,pdf,'r--')
        plt.savefig('figures/interarrival_time_pdf.png')

    plt.show()


def base_station_histogram(df, bins=20, pdf=False):
    """Generates histogram for base stations where calls are generated"""

    sns.set(style='whitegrid')
    plt.figure()
    plt.xlabel('Base station')
    plt.ylabel('Frequency')
    plt.title('Histogram of base stations')
    xlim = 21
    plt.xlim(0,xlim)

    if pdf is False:
        sns.histplot(data=df, x='Base station ', bins=bins)
        plt.savefig('figures/base_station_histogram.png')

    else:
        # Plot normalised histogram.
        sns.histplot(data=df, x='Base station ', bins=bins, stat='density')
        # Calculate maximum likelihood estimators a and b
        estimator_a = df['Base station '].min()
        estimator_b = df['Base station '].max()
        pdf = np.full((1000,), 1/(estimator_b - estimator_a))
        # Plot estimated pdf
        x = np.linspace(0, xlim, 1000)
        plt.plot(x,pdf,'r--')
        plt.savefig('figures/base_station_pdf.png')

    plt.show()


def call_duration_histogram(df, bins=40, pdf=False):
    """Generates histogram for call duration"""

    sns.set(style='whitegrid')
    plt.figure()
    plt.xlabel('Call duration')
    plt.ylabel('Frequency')
    plt.title('Histogram of call duration')
    xlim = 550
    plt.xlim(0, xlim)

    if pdf is False:
        # Plot histogram.
        sns.histplot(data=df, x='Call duration (sec)', bins=bins)
        plt.savefig('figures/call_duration_histogram.png')

    else:
        # Plot normalised histogram.
        sns.histplot(data=df, x='Call duration (sec)', bins=bins, stat='density')
        # Calculate maximum likelihood estimator for exponential distribution
        x = np.linspace(0, xlim, 1000)
        estimator = df['Call duration (sec)'].mean()
        pdf = 1/estimator * np.exp(-x/estimator)
        # Plot estimated pdf
        plt.plot(x,pdf,'r--')
        plt.savefig('figures/call_duration_pdf.png')
    
    plt.show()


def car_speed_histogram(df, bins=30, pdf=False):
    """Generates histogram for car speed"""

    sns.set(style='whitegrid')
    plt.figure()
    plt.xlabel('Car speed')
    plt.ylabel('Frequency')
    plt.title('Histogram of car speed')
    xlim_min = 90
    xlim_max = 152
    plt.xlim(xlim_min, xlim_max)

    if pdf is False:
        # Plot histogram
        sns.histplot(data=df, x='velocity (km/h)', bins=bins)
        plt.savefig('figures/car_speed_histogram.png')
    
    else:
        sns.histplot(data=df, x='velocity (km/h)', bins=bins,stat='density')
        # Calculate maximum likelihood estimators for normal distribution
        x = np.linspace(xlim_min, xlim_max, 1000)
        sample_mean = df['velocity (km/h)'].mean()
        sample_stdev = df['velocity (km/h)'].std(ddof=1)
        pdf = norm.pdf(x, loc=sample_mean, scale=sample_stdev)
        # Plot estimated pdf
        plt.plot(x,pdf,'r--')
        plt.savefig('figures/car_speed_pdf.png')

    plt.show()


if __name__ == '__main__':
    df = pd.read_excel('simulation_data.xls')
    interarrival_time_histogram(df,pdf=True)
    base_station_histogram(df, pdf=True)
    call_duration_histogram(df, pdf=True)
    car_speed_histogram(df, pdf=True)