import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTH_LIST = ['january', 'february', 'march', 'april', 'may', 'june']
DAY_LIST = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
FILTER_REMIND = 'Would you like to filter the data by month, day, both, or not at all? Type "None" for no time filter.\n'
MONTH_REMIND = 'Witch month? January, February, March, April, May, or June?\n'
DAY_REMIND = 'Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?\n'


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington?\n')
        city = format_input('city', city)
        if city:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    # 为了统一，month，day用户都输入英文，不区分大小写
    while True:
        filter_type = input(FILTER_REMIND).lower()
        if filter_type == 'both':
            while True:
                month = input(MONTH_REMIND)
                month = format_input('month', month)
                if month:
                    break
            while True:
                day = input(DAY_REMIND)
                day = format_input('day', day)
                if day:
                    break
            break
        elif filter_type == 'month':
            day = None
            month = input(MONTH_REMIND)
            month = format_input('month', month)
            if month:
                break
        elif filter_type == 'day':
            month = None
            day = input(DAY_REMIND)
            day = format_input('day', day)
            if day:
                break
        elif filter_type.lower() == 'none':
            month, day = None, None
            break
        else:
            print('Please input the right filter command!')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    # 因为存在both的情况所以dayofweek的筛选条件和month的筛选条件写到了一起
    print('-' * 40)
    # print(city, month, day)
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
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['start_hour'] = df['Start Time'].dt.hour
    if month:
        df = df[df['month'] == month]
    if day:
        df = df[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('The most common month is {}.'.format(MONTH_LIST[df['month'].mode()[0] - 1].title()))
    # TO DO: display the most common day of week
    print('The most common day of week is {}.'.format(DAY_LIST[df['day_of_week'].mode()[0]].title()))
    # TO DO: display the most common start hour
    print('The most common start hour is {}.'.format(df['start_hour'].mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most commonly used start station is {}.'.format(df['Start Station'].mode()[0]))
    # TO DO: display most commonly used end station
    print('The most commonly used end station is {}.'.format(df['End Station'].mode()[0]))
    # TO DO: display most frequent combination of start station and end station trip

    print('The most frequent combination of start station and end station trip is {}'.format(
        (df['Start Station'] + '->' + df['End Station']).mode()[0])
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('The total travel time is {}.'.format(format_time_output(df['Trip Duration'].sum())))

    # TO DO: display mean travel time
    print('The mean travel time is {}.'.format(format_time_output(df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    # print(df['User Type'].value_counts())
    output = 'There are '
    user_type = df['User Type'].value_counts()
    for i in user_type.index:
        if i == user_type.index[-1]:
            output += 'and ' + str(user_type[i]) + ' ' + str(i) + '.'
        else:
            output += str(user_type[i]) + ' ' + str(i) + ' '
    print(output)
    # TO DO: Display counts of gender
    output = 'There are '
    gender_type = df['Gender'].value_counts()
    for i in gender_type.index:
        if i == gender_type.index[-1]:
            output += 'and ' + str(gender_type[i]) + ' ' + str(i) + '.'
        else:
            output += str(gender_type[i]) + ' ' + str(i) + ' '
    print(output)
    # TO DO: Display earliest, most recent, and most common year of birth
    print('The earliest year of birth is {}.'.format(int(df['Birth Year'].min())))
    print('The most recent year of birth is {}.'.format(int(df['Birth Year'].max())))
    print('The most common year of birth is {}.'.format(int(df['Birth Year'].mode()[0])))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def format_input(type, input):
    '''
    用户输入的城市、月份、星期几是否有误，并格式化，用户输入英文，无需区分大小写，
    :param type: 需要格式化的类型（city/month/day）
    :param input: 用户输入的字符串
    :return: 小写的城市名/1-12 int类型月份/0-6对应monday-sunday
    '''
    default_type = {'city': CITY_DATA.keys(), 'month': MONTH_LIST, 'day': DAY_LIST}
    flag = True
    if type in default_type.keys():
        if not input.lower() in default_type[type]:
            print('Please input the right {}!'.format(type))
            flag = False
        else:
            input = input.lower()
            if type == 'month':
                input = default_type[type].index(input) + 1
            elif type == 'day':
                input = default_type[type].index(input)
        return flag and input
    else:
        raise Exception('不存在的格式化类型')


def format_time_output(time):
    '''
    用于格式化时间的输出，
    :param time: 时间（秒）
    :return: 字符串 xx hour(s) xx minute(s) xx second(s)
    '''
    output = ''
    time = int(time)
    hour = time // 3600
    minute = (time - hour * 3600) // 60
    second = time - hour * 3600 - minute * 60
    if hour:
        if hour == 1:
            output += '1 hour '
        else:
            output += (str(hour) + ' hours ')
    if minute:
        if minute == 1:
            output += '1 minute '
        else:
            output += (str(minute) + ' minutes ')
    if second:
        if second == 1:
            output += '1 second '
        else:
            output += (str(second) + ' seconds ')
    return output


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
