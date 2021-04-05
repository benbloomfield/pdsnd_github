import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# List validations

months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
yes_no = ['yes', 'no']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) date_filter - whether the user wants to filter by any date
        (str) period_filter - whether the user would like to filter by month, day of the week or both
        (str) month - name of the month to filter by, if date_filter is yes and period_filter is month
        (str) day - name of the day of week to filter by, if date_filter is yes and period_filter is weekday
    """

    print('Hello! Let\'s explore some US bikeshare data! \n')

# Retrieve city input. Test for validity and prompt again until a valid answer is given

    while True:
        city = input('Please choose a city from Chicago, New York City or Washington: ').lower()
        if city in CITY_DATA:
            break
        print('\nPlease enter one valid city name from Chicago, New York City or Washington.')
        print('You tried:', city, '\n')

    # Determine whether the user would like to apply a time filter, validate input.
    while True:
        date_filter = input('\nWould you like to filter by time period? Please enter yes or no: ').lower()
        if date_filter in yes_no:
            break
        print('Please enter yes or no.')
    # User picks yes for time filter, determine what period the user would like to filter by, validate input.
    if date_filter == 'yes':
        while True:
            period_filter = input('\nWould you like to filter by month, weekday or both? ').lower()
            if period_filter in ['month', 'weekday', 'both']:
                break
            print('Please enter month, weekday or both')
        # User picks month and day, determine which month and day, validate input.
        if period_filter == 'both':
            while True:
                month = input('\nWhich month? Choose from January, February, March, April, May and June: ').lower()
                if month in months:
                    break
                print('Please provide a valid month name.')
            while True:
                day = input('\nPlease select a day of the week by entering the name of the day: ').lower()
                if day in days:
                    break
                print('Please provide a valid day name.')
        # User picks month only, determine which month, validate input.
        elif period_filter == 'month':
            while True:
                month = input('\nWhich month? Choose from January, February, March, April, May and June: ').lower()
                if month in months:
                    break
                print('Please provide a valid month name.')
            day = 'all'
        # User picks day only, determine which day, validate input.
        elif period_filter == 'weekday':
            while True:
                day = input('\nPlease select a day of the week by entering the name of the day: ').lower()
                if day in days:
                    break
                print('Please provide a valid day name.')
            month = 'all'
    # No date filter is applied
    else:
        period_filter = 'none'
        month = 'all'
        day = 'all'

    print('-'*40)
    return city, month, day, date_filter, period_filter

def load_data(city, month, day, date_filter, period_filter):

    """
    Takes inputs from the get_filters function and loads a dataframe for the chosen city and filters.

    Returns:
        Dataframe from the underlying raw data for the chosen city, filtered by time period if applicable.
    """

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if date_filter != 'no' and period_filter != 'weekday':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if date_filter != 'no' and period_filter != 'month':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df, period_filter):
    """Displays statistics on the most frequent times of travel."""

    print('-'*40)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Calculate the most common month

    popular_month = df['month'].mode()[0]
    pop_m_print = months[popular_month - 1].title()
    pop_m_count = df['month'].value_counts()[popular_month]

    # Calculate the most common day of week

    popular_day = df['day_of_week'].mode()[0]
    pop_d_count = df['day_of_week'].value_counts()[popular_day]

    # Create additional dataframe column with start time converted into hour

    df['hour'] = df['Start Time'].dt.hour

    # Calculate the most popular hour

    popular_hour = df['hour'].mode()[0]
    pop_h_count = df['hour'].value_counts()[popular_hour]

    # Print results

    print('Month:', pop_m_print, '    Count:', pop_m_count, '\nDay:', popular_day, '    Count:', pop_d_count, '\nHour:', popular_hour, '    Count:', pop_h_count, '\nFilter:', period_filter)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df, period_filter):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Calculate most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    pop_ss_count = df['Start Station'].value_counts()[popular_start_station]

    # Calculate most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    pop_es_count = df['End Station'].value_counts()[popular_end_station]

    # Display most frequent combination of start station and end station trip

    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    pop_t_count = df['Trip'].value_counts()[popular_trip]

    # Print results

    print('Start:', popular_start_station, '    Count:', pop_ss_count, '\nEnd:', popular_end_station, '    Count:', pop_es_count, '\nTrip:', popular_trip, '    Count:', pop_t_count, '\nFilter:', period_filter)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df, period_filter):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate total travel time

    total_travel = df['Trip Duration'].sum() / 60 / 60 / 24
    num_trips = df['Trip Duration'].count()

    # Calculate mean travel time

    average_trip = df['Trip Duration'].mean() / 60

    # Print results

    print('Total Trip Duration in Days:', total_travel, '\nAverage Trip Duration in Minutes:', average_trip, '\nTotal Number of Trips:', num_trips, '\nFilter:', period_filter)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city, period_filter):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Calculate counts of user types for Washington and print results

    if city == 'washington':

        user_types = df['User Type'].value_counts()
        sub_count = user_types['Subscriber']
        cust_count = user_types['Customer']
        print('There were', sub_count, 'subscribers and', cust_count, 'customers.', 'Filter:', period_filter)
        print('No gender or birth year data was available for Washington')
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:

        # Calculate counts of user types for other cities

        user_types = df['User Type'].value_counts()
        sub_count = user_types['Subscriber']
        cust_count = user_types['Customer']

        # Calculate counts of genders for other cities

        gender_count = df['Gender'].value_counts()
        male_count = gender_count['Male']
        female_count = gender_count['Female']

        # Calculate minimum, maximum and mode of birth year for other cities

        min_year = int(df['Birth Year'].min())
        max_year = int(df['Birth Year'].max())
        mode_year = int(df['Birth Year'].mode()[0])

        # Print results

        print('There were', sub_count, 'subscribers and', cust_count, 'customers.\n', female_count, 'users were Female and', male_count, 'users were Male.')
        print('Birth Year Data:\nMinimum:', min_year, '    Maximum:', max_year, '    Most Common:', mode_year)
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def main():
    while True:
        city, month, day, date_filter, period_filter = get_filters()
        print('Your Filters:\nCity: {}\nMonth: {}\nWeekday: {}'.format(city, month, day).title())
        while True:
            data_restart = input('Is that correct? Enter yes or no: ')
            if data_restart in yes_no:
                break
            print('Please enter yes or no.')
        if data_restart == 'no':
            continue

        df = load_data(city, month, day, date_filter, period_filter)

        time_stats(df, period_filter)
        station_stats(df, period_filter)
        trip_duration_stats(df, period_filter)
        user_stats(df, city, period_filter)

        df = pd.read_csv(CITY_DATA[city])
        data_prompt = input('Would you like to see a sample of data? Enter yes or no: ')
        while data_prompt not in yes_no:
            print('Please enter yes or no.')
            data_prompt = input('Would you like to see a sample of data? Enter yes or no: ')
        while data_prompt == 'yes':
            print(df.sample(n = 5))
            data_prompt = input('\nWould you like to see a sample of data? Enter yes or no: ')
            continue
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while restart not in yes_no:
            print('Please enter yes or no.')
            restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
