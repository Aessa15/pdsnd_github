import time
import pandas as pd
import numpy as np
import calendar as cal

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
    while True:
        try:                
            # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
            
            city = str(input('Enter city name (chicago, new york city, washington): '))
            assert (city == 'chicago' or city == 'new york city' or city == 'washington')
         
            # get user input for month (all, january, february, ... , june)
            month = str(input('Enter the month of interest (all, january, february, ... , june):'))
            assert (month == 'all' or month == 'january' or month == 'february' or month == 'march' or month == 'april' or month == 'may' or month == 'june')
            
            # get user input for day of week (all, monday, tuesday, ... sunday)
            day = str(input('Enter day of week (all, monday, tuesday, ... sunday):' ))
            assert (day == 'all' or day == 'monday' or day == 'tuesday' or day == 'wednesday' or day == 'thursday' or day == 'friday' or day == 'saturday' or day == 'sunday')

            break
        except ValueError:
            print('That\'s not a valid input. Try again.')
        except KeyError:
            print('That\'s not a valid input. Try again.')
        except AssertionError:
            print('That\'s not a valid input. Try again.')
        finally:
            print('-'*40)
            print('Attempted Input')
            print('-'*40)
    
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    # display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]


    print('The most popular month is', cal.month_name[popular_month])
    print('\nThe most popular day of the week is', popular_dow)
    print('\nThe most popular hour is', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    #Most Common Start Station = mcss
    mcss = df['Start Station'].mode()[0]

    # display most commonly used end station
    #Most Common End Station = mces

    mces = df['End Station'].mode()[0]
    # display most frequent combination of start station and end station trip
    df["Station combination"] = mcss + " & " + mces
    mfc = df["Station combination"].mode()[0]

    print("Start Station")
    print(mcss)
    print("\nEnd Station")
    print(mces)
    print('\nMost frequent combination',mfc)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum())

    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean(),3)

    print('The total travel time is', total_travel_time, "seconds")
    print('\nThe mean travel time is', mean_travel_time, "seconds")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    # Display counts of gender
    user_gender = df['Gender'].value_counts()

    # Display earliest, most recent, and most common year of birth
    earliest = int(df['Birth Year'].min())
    most_recent = int(df['Birth Year'].max())
    most_common = int(df['Birth Year'].mode()[0])

    print('User types counts are\n', user_types)
    print('\nUser gender counts are\n', user_gender)
    print('\nthe oldest user birth year:', earliest)
    print('\nthe youngest user birth year:', most_recent)
    print('\nthe most commen user birth year:', most_common)
    print("\nThis took %s seconds." % (time.time() - start_time))

def raw_data(df):
    """Displays raw data of the filtered input by the user
    
    Everytime the user inputs yes, 5 rows of raw data would be displayed 
    
    """
    raw = input("Would like to see first five rows of raw data about this city of interest? (yes or no)")
    m=0
    n=5
    while raw.lower() == "yes":
        
        raw_data = df.filter(range(m,n), axis = 0)
        print(raw_data)
        m += 5
        n += 5
        raw = input("Would like to see more five rows of raw data about this city of interest? (yes or no)")

def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        trip_duration_stats(df)
        station_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\Do you want to restart the program?(yes or no)\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()