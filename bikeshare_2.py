import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        cities = ['chicago', 'new york city', 'washington']
        city = input('City name (select between Chicago, New York City, and Washington: ').lower()
        if city not in cities:
            print('Invalid input. Please enter Chicago, New York City, or Washington.')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        month = input('Month (select between January and June, or input ALL for all months): ').lower()
        if month not in months:
            print('Invalid input. Please enter month between January and June, or input ALL for all months.')
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = input('Day (input day name or ALL for all days): ').lower()
        if day not in days:
            print('Invalid input. Please enter any day name or input ALL for all days.')
            continue
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def sec_to_hours(seconds):
    """Converts seconds to hours, minutes, and seconds."""
    a=int(seconds//3600)
    b=int((seconds%3600)//60)
    c=int((seconds%3600)%60)
    d=("{} hours, {} mins, and {} seconds".format(a, b, c))
    return d

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    months = {1 : 'January',
              2 : 'February',
              3 : 'March',
              4 : 'April',
              5 : 'May',
              6 : 'June'}
    print('The most common month: {}'.format(months[popular_month]))

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    popular_day = df['day_of_week'].mode()[0]
    print('The most common day of week: {}'.format(popular_day))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most common start hour: {}:00'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station: {}'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station: {}'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    df['station_combination'] = 'Start from ' + df['Start Station'] + ' and end at ' + df['End Station']
    popular_station_combination = df['station_combination'].mode()[0]
    print('Most frequent combination of start station and end station trip: {}'.format(popular_station_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: {} seconds or {}'.format(round(total_travel_time, 2), sec_to_hours(total_travel_time)))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time: {} seconds or {}'.format(round(mean_travel_time, 2), sec_to_hours(mean_travel_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users. Gender, Year of Birth, and Mean Age statistics are not available for Washington.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('Counts of user types:\n{}\n'.format(user_type))

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('Counts of gender:\n{}\n'.format(gender_count))
    except KeyError:
        print('Counts of gender: Data is not available for Washington.\n')

    # Display earliest, most recent, most common year of birth, and mean age
    try:
        min_yob = df['Birth Year'].min()
        print('Earliest year of birth: {}'.format(int(min_yob)))
    except KeyError:
        print('Earliest year of birth: Data is not available for Washington.')

    try:
        max_yob = df['Birth Year'].max()
        print('Most recent year of birth: {}'.format(int(max_yob)))
    except KeyError:
        print('Most recent year of birth: Data is not available for Washington.')

    try:
        mode_yob = df['Birth Year'].mode()[0]
        print('Most common year of birth: {}'.format(int(mode_yob)))
    except KeyError:
        print('Most common year of birth: Data is not available for Washington.')

    try:
        currentyear = float(time.strftime("%Y"))
        df['yob'] = df['Birth Year'].interpolate(method = 'linear', axis = 0)
        df['age'] = currentyear - df['yob']
        mean_age = df['age'].mean()
        print('Mean age: {}'.format(int(mean_age)))
    except KeyError:
        print('Mean age: Data is not available for Washington.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):

    """
    Prompt the user if they would like to view raw data.
    Return 5 rows of raw data if the answer is 'yes'.
    Repeat the prompt and return the next 5 rows of raw data until user says 'no'.
    """

    raw_data = input('Would you like to view raw data? Enter yes or no.\n').lower()
    a = 0
    b = 5
    while raw_data == 'yes':
        print(df.iloc[a:b])
        a += 5
        b += 5
        raw_data = input('Would you like to see more data? Enter yes or no.\n').lower()


def main():
    while True:

        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
