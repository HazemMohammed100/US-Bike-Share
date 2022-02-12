import pandas as pd
import time

CITIES = {1: 'Chicago', 2: 'New York City', 3: 'Washington'}
CITY_DATA = {1: 'chicago.csv', 2: 'new_york_city.csv', 3: 'washington.csv'}
MONTHS = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
DAYS = {1: 'Sunday', 2: 'Monday', 3: 'Tuesday', 4: 'Wednesday', 5: 'Thursday', 6: 'Friday', 7: 'Saturday'}


def check_input(available_input):
    """ It is a function that takes the input and checks it and returns a valid input """

    # Infinite loop to check input until it is valid
    while True:
        entered_input = input('Your Choice: ')

        # Deciding whether the input is integer or not
        if entered_input.isdigit():
            entered_input = int(entered_input)
            # If it is integer, then we check if it is a valid input
            if entered_input <= available_input and entered_input >= 1:
                return int(entered_input)

            else:
                print('Please pick a number between 1 and {}'.format(available_input))

        else:
            print('Please pick a number between 1 and {}'.format(available_input))


def get_filters():
    """
        Asks user to specify a city, month, and day to analyze.

        Returns:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "No Filter" to apply no month filter
            (str) day - name of the day of week to filter by, or "No Filter" to apply no day filter
        """

    print('\n' + '#' * 20 + " Hello Let's Explore Some US BikeShare Data " + '#' * 20 + '\n')

    # get user input for city (chicago, new york city, washington).
    print("Which city would you like to choose ? (Pick a number) \n",
          '1: Chicago \n',
          '2: New York City \n',
          '3: Washington\n')
    # Checking the input
    city = check_input(3)

    # get user input for month (all, january, february, ... , june)
    print('#' * 20 + " Let's Explore {} BikeShare Data ".format(CITIES[city]) + '#' * 20 + '\n')
    print("Would you like to filter by month ? (Pick a number)",
          "\n1:January | 2:February | 3:March | 4:April | 5:May | 6:June | 7:No Filter \n")
    # Checking the input
    month = check_input(7)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print("\nWould you like to filter by day ? (Pick a number)",
          "\n1:Sunday | 2:Monday | 3:Tuesday | 4:Wednesday | ",
          "\n5:Thursday | 6:Friday | 7:Saturday | 8:No Filter \n")
    # Checking the input
    day = check_input(8)

    print('*' * 100 + '\n')
    return city, month, day


def load_data(city, month, day):
    """
        Loads data for the specified city and filters by month and day if applicable.

        Args:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "No Filter" to apply no month filter
            (str) day - name of the day of week to filter by, or "No Filter" to apply no day filter
        Returns:
            df - Pandas DataFrame containing city data filtered by month and day
        """

    df = pd.read_csv(CITY_DATA[city])

    # Converting "Start Time" column to "datetime" data type
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Extracting month into new column
    df['Month'] = df['Start Time'].dt.month_name()
    # Extracting day into new column
    df['Day'] = df['Start Time'].dt.day_name()
    # Extracting hour into new column
    df['Hour'] = df['Start Time'].dt.hour

    # Filtering the dataframe by month
    if month != 7:
        df = df[df['Month'] == MONTHS[month]]

    # Filtering the dataframe by day
    if day != 8:
        df = df[df['Day'] == DAYS[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('# Calculating The Most Frequent Times of Travel By The Filter You Chose...\n')
    start_time = time.time()

    # display the most common month and number of trips
    print('Most common month:', df['Month'].mode()[0], ' ' * 20,
          'No. Trips:', df[df['Month'] == df['Month'].mode()[0]].shape[0])

    # display the most common day of week and count
    print('Most common day of week:', df['Day'].mode()[0], ' ' * 15,
          'Count:', df[df['Day'] == df['Day'].mode()[0]].shape[0])

    # display the most common start hour and count
    print('Most common hour in all months:', df['Hour'].mode()[0], ' ' * 15,
          'Count:', df[df['Hour'] == df['Hour'].mode()[0]].shape[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*' * 100 + '\n')


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('# Calculating The Most Popular Stations and Trip By The Filter You Chose...\n')
    start_time = time.time()

    # display most commonly used start station and count
    print('Most common start station:',
          '\n  ', df['Start Station'].mode()[0], ' '*5,
          'Count:', df[df['Start Station'] == df['Start Station'].mode()[0]].shape[0])

    # display most commonly used end station and count
    print('\nMost common end station:',
          '\n  ', df['End Station'].mode()[0], ' '*5,
          'Count:', df[df['End Station'] == df['End Station'].mode()[0]].shape[0])

    # display most frequent combination of start station and end station trip and count
    print('\nMost common trip:',
          '\n  ', ('Start:(' + df['Start Station'] + ') || End:(' + df['End Station'] + ')').mode()[0],  ' '*5,
          'Count:', df[(df['Start Station'] + df['End Station']) == (df['Start Station'] + df['End Station']).mode()[0]].shape[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*' * 100 + '\n')


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('# Calculating Trip Duration By The Filter You Chose...\n')
    start_time = time.time()

    # Calculating total time traveled
    total_travel_time = df['Trip Duration'].sum()

    # Calculating mean time traveled
    mean_travel_time = int(df['Trip Duration'].mean())

    # display total travel time and number of trips
    print('Total travel time of {} trips:\n    '.format(df['Trip Duration'].shape[0]),
          total_travel_time, 'Seconds\n    ',
          int(total_travel_time/60), 'Minutes\n    ',
          int(total_travel_time/3600), 'Hours\n')

    # display mean travel time
    print('Mean travel time:\n    ',
          mean_travel_time, 'Seconds\n    ',
          int(mean_travel_time / 60), 'Minutes\n    ',
          int(mean_travel_time / 3600), 'Hours')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*' * 100 + '\n')


def user_stats(df, city, month, day):
    """Displays statistics on BikeShare users."""

    print('# Calculating User Stats By The Filter You Chose...\n')
    start_time = time.time()

    # Display counts of user types
    print('# Calculating User Types... \n')
    print('No. Subscribers:', df['User Type'].value_counts()['Subscriber'])
    print('No. Customers:', df['User Type'].value_counts()['Customer'])
    # Since dependent users are only available in Chicago in February in a Saturday day
    if city == 1 and (month == 2 or month == 7) and (day == 7 or day == 8):
        print('No. Dependents:', df['User Type'].value_counts()['Dependent'])


    # Display counts of gender
    # Since gender column is only available in Chicago and New York dataframes
    if city <= 2:
        print('\n# Calculating User Genders... \n')
        print('No. Males:', df['Gender'].value_counts()['Male'])
        print('No. Females:', df['Gender'].value_counts()['Female'])


    # Display earliest, most recent, and most common year of birth
    # Since Birth Year column is only available in Chicago and New York dataframes
    if city <= 2:
        print('\n# Calculating Birth Year Stats...\n')
        print('Oldest User Born in:', int(df['Birth Year'].min()))
        print('Youngest User Born in:', int(df['Birth Year'].max()))
        print('Most Users Born in:', int(df['Birth Year'].mode()[0]))

    # Notifying the user that (Gender) and (Birth Year) data are not available for Washington city
    if city == 3:
        print('\n## The (Gender) and (Birth Year) data are not available for Washington city ##')

    print('*' * 100 + '\n')


    # Ask the user to display raw data
    print('Would You Like To See Some Individual Trip Data ? (Pick a number)',
          '\n  1: Yes',
          '\n  2: No')

    # Checking the input
    raw_data_display = check_input(2)
    print('-'*50)

    if raw_data_display == 1:
        # Loops to iterate through the dataframe and display 5 rows
        for i in range(5, df.shape[0], 5):
            for j in range(i-5, i):
                print(df.iloc[j, 1:])
                print('-'*50, '\n')

            # Asking the user if he/she wants to see more individual trip data
            print('Would You Like To See More Individual Trip Data ? (Pick a number)',
                  '\n  1: Yes',
                  '\n  2: No')

            # Checking the input
            raw_data_display = check_input(2)
            print('-' * 50, '\n')

            # If he/she chooses no we exit the loops
            if raw_data_display == 2:
                break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*' * 100 + '\n')


def main():
    # A variable to check if the user wants to restart the program
    restart = 1

    while restart == 1:

        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city, month, day)

        print('Would You Like To Restart The Program ? (Pick a number)',
              '\n  1: Yes',
              '\n  2: No')

        # Checking the input
        restart = check_input(2)
        print('-' * 100 + '\n')


if __name__ == "__main__":
    main()
