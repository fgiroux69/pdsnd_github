# Importing packages and functions
import time
import pandas as pd
import numpy as np

# loading files
CITY_DATA = {
    'chicago':'chicago.csv',
    'new york city':'new_york_city.csv',
    'washington':'washington.csv'
}

def city_select():
    '''
    This code introduce the user to the bikeshare interface and ask him/her to choose a city.
    '''
    print('Hi! Let\'s explore with you some US bikeshare data!')
    print(' ')

# get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Which city do you want to analyze?')
    print('Chicago, New York or Washington')
    print(' ')
    city = input('Please write the first character of city name for which you would like to see more info: ')
    city = city.lower()
    while True:
            if city  == 'c':
                print("\n Your choice is Chicago City\n")
                return 'chicago'
            elif city == 'n':
                print("\n Your choice is New York City\n")
                return 'new york city'
            elif city == 'w':
                print("\n Your choice is Washington City\n")
                return 'washington'
            else:
                print('\nPlease choose a city\n')
                city = input(f'Sorry, "{city}" is not a valid choice. Write the first character of city name:')
                city = city.lower()
    return city

def select_time():
    '''
    Ask the user to choose a filter between day, month or no filters
    '''
    print('Which filter do you want to apply to the data? Type "no" for no filter.')
    print('day')
    print('month')
    print('no')
    print(' ')
    period = input('Please write the filter that you would like to apply to the data:')
    period = period.lower()

    while True:
        if period == "month":
            print('\n The data will be filtered by month.\n')
            return 'month'
        elif period == "day":
            print('\n The data will be filtered by the day of the week.\n')
            return 'day_of_week'
        elif period == "no":
            print('\n No filter will be applied to the data.\n')
            return "none"
        else:
            period = input(f'Sorry, "{period}" is not a valid choice. Type the period filter:')
            print('\nPlease choose a period filter\n')
            period = period.lower()

# Ask user to select a month (january to june)
def month_data(mth_sel):
    if mth_sel == 'month':
        print('Select a month:')
        print('January')
        print('February')
        print('March')
        print('April')
        print('May')
        print('June')
        month = input('\nType the first 3 characters of the month name:\n')
        while month.strip().lower() not in ['jan', 'feb', 'mar', 'apr', 'may', 'jun']:
            month = input(f'Sorry, "{month}" is not a valid choice.  Please type the first 3 characters of the month name:\n')
        return month.strip().lower()
    else:
        return 'none'


# Ask the user to select a day of the week
def day_data(day_sel):
    if day_sel == 'day_of_week':
        print("\n Which day do you want to analyse? \n")
        print('Sunday:      Su')
        print('Monday:      M')
        print('Tuesday:     Tu')
        print('Wednesday:   W')
        print('Thursday:    Th')
        print('Friday:      F')
        print('Saturday:    Sa')
        day = input('\n Please type a day: Su, M, Tu, W, Th, F, Sa, \n')
        while day.lower().strip() not in ['su', 'm', 'tu', 'w', 'th', 'f', 'sa']:
            day = input(f'Sorry, "{day}" is not a valid day of the week. Please type a day: Su, M, Tu, W, Th, F, Sa, \n')
        return day.lower().strip()
    else:
        return 'none'


def load_file(city):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    print('\nThe data is loading.\n')
    df = pd.read_csv(CITY_DATA[city])
    # converts the Start Time column to datetime and creates new month and day of week columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df["day_of_month"] = df["Start Time"].dt.day
    return df

def filters(df, time, month, week_day):
    '''
    This section of the program will filter the data according to the criterias of the user:
    -city (Chicago, New York or Washington)
    -time (day, month, day of the week or no filter)
    '''
    #Filter by Month
    if time == 'month':
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #Filter by day
    if time == 'day_of_week':
        days = ['Monday', 'Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day_sel in days:
            if week_day.capitalize() in day_sel:
                day_of_week = day_sel
        df = df[df['day_of_week'] == day_of_week]

    return df

def freq_stat(df):
    '''What is the most popular times of travel?
    '''
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    m = df.month.mode()[0]
    print('\n 1. Statitics on the most frequent times of travel:')
    popular_month= months[m - 1].capitalize()
    print('\n - The most popular month for bike traveling is ' + str(popular_month) + "\n")
    popular_day = df['day_of_week'].value_counts().reset_index()['index'][0]
    print('\n - The most popular day of the week for bike traveling is ' + str(popular_day) + "\n")
    popular_hour = df['Start Time'].dt.hour.mode()[0]
    print('\n - The most popular hour of the day for bike traveling is '+ str(popular_hour) + "\n")
    return  popular_month, popular_day, popular_hour

def station_start_end(df):
    '''What is the most popular stations and tripl?
    '''
    # df - dataframe returned from time_filters
    print('\n 2. Statitics on the most popular stations:')
    start_station = df['Start Station'].value_counts().reset_index()['index'][0]
    print("\n - The most popular start station is " + str(start_station) + "\n")
    end_station = df['End Station'].value_counts().reset_index()['index'][0]
    print("\n - The most popular end station is " + str(end_station) + "\n")
    start_end = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\n - The most frequent combinaition of start and end station is: \n')
    print(start_end)
    return start_station, end_station

def ride_time(df):
    '''
    What is the total trip bike duration and average trip bike duration?
    '''
    print('\n 3. For 2017 and for the period of January to June:')
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    #sum for total trip time, mean for avg trip time
    avg_ride_sec = np.mean(df['Trip Duration'])
    avg_min = avg_ride_sec // 60
    avg_min_str = str(avg_min).split()[0]
    total_ride_time = np.sum(df['Travel Time'])
    total_days = str(total_ride_time).split()[0]
    print("- The total travel was " + total_days + " days \n")
    print("- The average travel was " + avg_min_str + " minutes \n")
    return total_ride_time, avg_min_str

def bike_users_data(df):
    '''What are the counts of users by type?
    '''
     # df - dataframe returned _filters
    print('\n 4. The count of users by type is:\n')
    return df['User Type'].value_counts()

def birth_yr_data(df):
    '''What is the earliest, most recent and most common year of birth?'''
    # df - dataframe returned from time_filters
    try:
        print('\n 5. The earliest, latest, and most common year of birth is:')
        earliest = np.min(df['Birth Year'])
        print ("\n - The earliest year of birth is " + str(earliest) + "\n")
        latest = np.max(df['Birth Year'])
        print ("\n - The latest year of birth is " + str(latest) + "\n")
        most_frequent= df['Birth Year'].mode()[0]
        print ("\n - The most common year of birth is " + str(most_frequent) + "\n")
        return earliest, latest, most_frequent
    except:
        print('No available data for this period.')

def gender_data(df):
    '''What are the count of bikers by gender?'''
    # df - dataframe returned from time_filters
    try:
        print('\n 6. The count of bikers by gender is:')
        return df['Gender'].value_counts()
    except:
        print('There is no gender data for this analyse.')

def process(f, df):
    '''Calculates the time it takes to commpute statistics
    '''
    start_time = time.time()
    TimeToCompute = f(df)
    print(TimeToCompute)
    print("This took %s seconds"  % +(time.time() - start_time)+ " to compute statistics. \n")

def disp_data(df):
    '''
    Displays the data that program used to compile the statistics
    Input:
        the df shows the bikeshare data
    Returns:
       none
    '''
    df = df.drop(['day_of_month'], axis = 1)
    row_index = 0

    bike_data = input("\nWould you like to see the data that the program use to compute the stats? Please write 'y' or 'n' \n").lower()
    while True:
        if bike_data == 'n':
            return
        if bike_data == 'y':
            print(df[row_index: row_index + 5])
            row_index = row_index + 5
        bike_data = input("\n Would you like to see five more rows? Please write 'y' or 'n' \n").lower()

def main():
    '''This function computes and shows the
    statistics for the requested city
    '''
    # This code executes the functions step by step
    city = city_select()
    df = load_file(city)
    period = select_time()
    month = month_data(period)
    day = day_data(period)

    df = filters(df, period, month, day)
    disp_data(df)

    # display the requested statistics
    function_step = [freq_stat, station_start_end,
     ride_time, bike_users_data, birth_yr_data, gender_data]

    # displays processing time for each section
    for x in function_step:
        process(x, df)

    # Restarting option
    restart = input("\n Would you like to do another analysis? Type \'y\' or \'n\'.\n")

    if restart.upper() == "Y":
        main()

if __name__ == '__main__':
    main()
