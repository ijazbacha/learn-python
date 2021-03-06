from os import pardir
from urllib.request import urlretrieve
from numpy import datetime64, positive
from numpy.lib.function_base import cov, extract
import pandas as pd

#italy_covid_url = 'https://gist.githubusercontent.com/aakashns/f6a004fa20c84fec53262f9a8bfee775/raw/f309558b1cf5103424cef58e2ecb8704dcd4d74c/italy-covid-daywise.csv'

#urlretrieve(italy_covid_url, './data/italy-covid-daywise.csv')


# how to read csv file

covid_df = pd.read_csv('./data/italy-covid-daywise.csv')

print(type(covid_df))

print(covid_df)


# how to get info about file

print(covid_df.info())


# use describe to view statistical information about numeric column

print(covid_df.describe())


# how to get the list of column names

print(covid_df.columns)


# find shape of the column and rows

print(covid_df.shape)


# Retrieve data from data frame

print(covid_df['new_cases'])


# Retrieve data with index

print(covid_df['new_cases'][247])


# retrieve data using 'at'

print(covid_df.at[247, 'new_cases'])


# retrieve a list of column data

print(covid_df[['new_cases', 'new_tests']])


# create a copy of dataframe

create_copy = covid_df.copy()
print(create_copy)


# Retrieve data with row wise unig loc

print(covid_df.loc[1])

print(type(covid_df.loc[1]))

print(covid_df.loc[1:10])


# retrieve data from top to bottom using head

print(covid_df.head(10))


# retrieve data from bottom to top using tail

print(covid_df.tail(10))


# retrieve a data sample using sample

print(covid_df.sample(10))


# Analyzing data from data frames

total_cases = covid_df.new_cases.sum()
print(total_cases)

total_deaths = covid_df.new_deaths.sum()
print(total_deaths)

total_tests = covid_df.new_tests.sum()
print(total_tests)


test_per_day = total_tests / 248
print('test per day in italy: {:.2f}'.format(test_per_day))


death_rate = total_deaths / total_cases
print('death rate in italy: {:.2f} %'.format(death_rate*100))

initial_tests = 935310
total_tests = initial_tests + total_tests
print('total test in italy: ', total_tests)


positive_rate = total_cases / total_tests
print('positive rate in italy: {:.2f} %'.format(positive_rate*100))


# Querying and sorting rows

# one way
new_data = covid_df.new_cases > 1000
print(new_data)
high_cases_df = covid_df[new_data]
print(high_cases_df)


# another way
high_cases_df = covid_df[covid_df.new_cases > 1000]
print(high_cases_df)


# The data frame contains 72 rows, but only the first & last five rows are displayed by default 
# with Jupyter for brevity. We can change some display options to view all the rows.

# from IPython.display import display
# with pd.option_context('display.max_rows', 100):
#     display(covid_df[covid_df.new_cases > 1000])


# find high positive ratio data frame
high_ratio_df = covid_df[covid_df.new_cases / covid_df.new_tests > positive_rate]
print(high_ratio_df)


# adding and deleting column

# adding
covid_df['positive_rate'] = covid_df.new_cases / covid_df.new_tests
print(covid_df)


# deleting
covid_df.drop(columns=['positive_rate'], inplace=True)
print(covid_df)


# Sorting rows using column values

sort_data_asc = covid_df.sort_values('new_cases', ascending=False).head(10)
print(sort_data_asc)

sort_data_desc = covid_df.sort_values('new_cases').head(10)
print(sort_data_desc)

print(covid_df.loc[170:174])

'''
    For now, let's assume this was indeed a data entry error. We can use one of the 
    following approaches for dealing with the missing or faulty value:

   1. Replace it with 0.
   2. Replace it with the average of the entire column
   3. Replace it with the average of the values on the previous & next date
   4. Discard the row entirely
'''

covid_df.at[172, 'new_cases'] = covid_df.at[171, 'new_cases'] + covid_df.at[173, 'new_cases'] / 2
print(covid_df.loc[170:174])



# working with dates

date_column = covid_df.date
print(date_column)

# convert dtype: object into datetime64
covid_df['date'] = pd.to_datetime(date_column)
print(covid_df.date)


# extract day, weekday, month, year using DatetimeIndex()
covid_df['day'] = pd.DatetimeIndex(covid_df.date).day
covid_df['weekday'] = pd.DatetimeIndex(covid_df.date).weekday
covid_df['month'] = pd.DatetimeIndex(covid_df.date).month
covid_df['year'] = pd.DatetimeIndex(covid_df.date).year
print(covid_df)



# query the covid_df dataframe where month equal to 5 and create new df name as covid_df_may 
covid_df_may = covid_df[ covid_df.month == 5]
print(covid_df_may)

covid_df_may_matrix = covid_df_may[['new_cases', 'new_deaths', 'new_tests']]
print(covid_df_may_matrix)

covid_may_total = covid_df_may_matrix.sum()
print(covid_may_total)


# combine all the above queries
covid_may_total = covid_df[covid_df.month == 5][['new_cases', 'new_deaths', 'new_tests']].sum()
print(covid_may_total)

# other query example
print(covid_df.new_cases.sum())

print(covid_df[covid_df.weekday == 1].new_cases.mean())


# Grouping and aggregation
covid_month_df = covid_df.groupby('month')[['new_cases', 'new_deaths', 'new_tests']].sum()
print(covid_month_df)
print(covid_month_df.loc[1])

covid_weekday_df = covid_df.groupby('weekday')[['new_cases', 'new_deaths', 'new_tests']].mean()
print(covid_weekday_df)


covid_df['total_cases'] = covid_df.new_cases.cumsum()
covid_df['total_deaths'] = covid_df.new_deaths.cumsum()
covid_df['total_tests'] = covid_df.new_tests.cumsum()

print(covid_df)



# Merging data from multiple sources


# urlretrieve('https://gist.githubusercontent.com/aakashns/8684589ef4f266116cdce023377fc9c8/raw/99ce3826b2a9d1e6d0bde7e9e559fc8b6e9ac88b/locations.csv', 
#             './data/locations.csv')

location_df = pd.read_csv('./data/locations.csv')
print(location_df)

get_italy_location = location_df[location_df.location == 'Italy']
print(get_italy_location)

covid_df['location'] = 'Italy'


merge_df = covid_df.merge(location_df, on='location')
print(merge_df)


merge_df['cases_per_million'] = merge_df.new_cases * 1e6 / merge_df.population
merge_df['death_per_million'] = merge_df.new_deaths * 1e6 / merge_df.population
merge_df['test_per_million'] = merge_df.new_tests * 1e6 / merge_df.population

print('merge_df')


# Writing data back to files

result = merge_df[['date',
                       'new_cases', 
                       'total_cases', 
                       'new_deaths', 
                       'total_deaths', 
                       'new_tests', 
                       'total_tests', 
                       'cases_per_million', 
                       'death_per_million', 
                       'test_per_million']]

result.to_csv('./data/italy_covid_result.csv', index=None)

