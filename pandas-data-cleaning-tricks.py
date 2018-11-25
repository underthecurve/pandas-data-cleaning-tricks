#!/usr/bin/env python
# coding: utf-8

# # Tricks for cleaning your data in Python using pandas
# 
# **By Christine Zhang ([ychristinezhang at gmail dot com](mailto:ychristinezhang@gmail.com / [@christinezhang](https://twitter.com/christinezhang) | [@christinezhang](https://twitter.com/christinezhang))**

# GitHub repository for Data+Code: https://github.com/underthecurve/pandas-data-cleaning-tricks
# 
# In 2017 I gave a talk called "Tricks for cleaning your data in R" which I presented at the [Data+Narrative workshop](http://www.bu.edu/com/data-narrative/) at Boston University. The repo with the code and data, https://github.com/underthecurve/r-data-cleaning-tricks, was pretty well-received, so I figured I'd try to do some of the same stuff in Python using `pandas`.
# 
# **Disclaimer:** when it comes to data stuff, I'm much better with R, especially the `tidyverse` set of packages, than with Python, but in my last job I used Python's `pandas` library to do a lot of data processing since Python was the dominant language there.
# 
# Anyway, here goes: 
# 
# Data cleaning is a cumbersome task, and it can be hard to navigate in programming languages like Python. 
# 
# The `pandas` library in Python is a powerful tool for data cleaning and analysis. By default, it leaves a trail of code that documents all the work you've done, which makes it extremely useful for creating reproducible workflows.
# 
# In this workshop, I'll show you some examples of real-life "messy" datasets, the problems they present for analysis in Python's `pandas` library, and some of the solutions to these problems.
# 
# Fittingly, I'll [start the numbering system at 0](http://python-history.blogspot.com/2013/10/why-python-uses-0-based-indexing.html).

# ## 0. Importing the `pandas` library

# Here I tell Python to import the `pandas` library as `pd` (a common alias for `pandas` — more on that in the next code chunk).

# In[1]:


import pandas as pd


# ## 1. Finding and replacing non-numeric characters like `,` and `$`

# Let's check out the city of Boston's [Open Data portal](https://data.boston.gov/), where the local government puts up datasets that are free for the public to analyze.
# 
# The [Employee Earnings Report](https://data.boston.gov/dataset/employee-earnings-report) is one of the more interesting ones, because it gives payroll data for every person on the municipal payroll. It's where the *Boston Globe* gets stories like these every year:
# 
# -   ["64 City of Boston workers earn more than $250,000"](https://www.bostonglobe.com/metro/2016/02/05/city-boston-workers-earn-more-than/MvW6RExJZimdrTlwdwUI7M/story.html) (February 6, 2016)
# 
# -   ["Police detective tops Boston’s payroll with a total of over $403,000"](https://www.bostonglobe.com/metro/2017/02/14/police-detective-tops-boston-payroll-with-total-over/6PaXwTAHZGEW5djgwCJuTI/story.html) (February 14, 2017)
# 
# Let's take at the February 14 story from 2017. The story begins:
# 
# > "A veteran police detective took home more than $403,000 in earnings last year, topping the list of Boston’s highest-paid employees in 2016, newly released city payroll data show."
# 
# **What if we wanted to check this number using the Employee Earnings Report?**

# We can use the `pandas` function [`pandas.read_csv()`](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html) to load the csv file into Python. We will call this DataFrame `salary`. Remember that I imported `pandas` "as `pd`" in the last code chunk. This saves me a bit of typing by allowing me to access `pandas` functions like `pandas.read_csv()` by typing `pd.read_csv()` instead. If I had typed `import pandas` in the code chunk under section `0` without `as pd`, the below code wouldn't work. I'd have to instead write `pandas.read_csv()` to access the function.
# 
# The `pd` alias for `pandas` is so common that the library's [documentation](http://pandas.pydata.org/pandas-docs/stable/install.html#running-the-test-suite) even uses it sometimes.
# 
# Let's try to use `pd.read_csv()`:

# In[2]:


salary = pd.read_csv('employee-earnings-report-2016.csv')


# That's a pretty long and nasty error. Usually when I run into something like this, I start from the bottom and work my way up — in this case, I typed `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 22: invalid continuation byte` into a search engine and came across [this discussion on the Stack Overflow forum](https://stackoverflow.com/questions/30462807/encoding-error-in-panda-read-csv). The last response suggested that adding `encoding ='latin1'` inside the function would fix the problem on Macs (which is the type of computer I have).

# In[3]:


salary = pd.read_csv('employee-earnings-report-2016.csv', encoding = 'latin-1')


# Great! (I don't know much about encoding, but this is something I run into from time to time so I thought it would be helpful to show here.)
# 
# We can use `head()` on the `salary` DataFrame to inspect the first five rows of `salary`. (Note I use the `print()` to display the output, but you don't need to do this in your own code if you'd prefer not to.)

# In[4]:


print(salary.head())


# There are a lot of columns. Let's simplify by selecting the ones of interest: `NAME`, `DEPARTMENT_NAME`, and `TOTAL.EARNINGS`. There are [a few different ways](https://medium.com/dunder-data/selecting-subsets-of-data-in-pandas-6fcd0170be9c) of doing this with `pandas`. The simplest way, imo, is by using the indexing operator `[]`.
# 
# For example, I could select a single column, `NAME`: (Note I also run the line `pd.options.display.max_rows = 20` in order to display a maximum of 20 rows so the output isn't too crowded.)

# In[5]:


pd.options.display.max_rows = 20

salary['NAME']


# This works for selecting one column at a time, but using `[]` returns a [Series](https://pandas.pydata.org/pandas-docs/stable/dsintro.html#series), not a [DataFrame](https://pandas.pydata.org/pandas-docs/stable/dsintro.html#dataframe). I can confirm this using the `type()` function:

# In[6]:


type(salary['NAME'])


# If I want a DataFrame, I have to use double brackets:

# In[7]:


salary[['NAME']]


# In[8]:


type(salary[['NAME']])


# To select multiple columns, we can put those columns inside of the second pair of brackets. We will save this into a new DataFrame, `salary_selected`. We type `.copy()` after `salary[['NAME','DEPARTMENT_NAME', 'TOTAL EARNINGS']]` because we are making a copy of the DataFrame and assigning it to new DataFrame. Learn more about `copy()` [here](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.copy.html).

# In[9]:


salary_selected = salary[['NAME','DEPARTMENT_NAME', 'TOTAL EARNINGS']].copy()


# We can also change the column names to lowercase names for easier typing. First, let's take a look at the columns by displaying the `columns` attribute of the `salary_selected` DataFrame.

# In[10]:


salary_selected.columns


# In[11]:


type(salary_selected.columns)


# Notice how this returns something called an "Index." In `pandas`, DataFrames have both row indexes (in our case, the row number, starting from 0 and going to 22045) and column indexes. We can use the [`str.lower()`](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.str.lower.html) function to convert the strings (aka characters) in the index to lowercase.

# In[12]:


salary_selected.columns = salary_selected.columns.str.lower()

salary_selected.columns


# Another thing that will make our lives easier is if the `total earnings` column didn't have a space between `total` and `earnings`. We can use a "string replace" function, [`str.replace()`](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.str.replace.html), to replace the space with an underscore. The syntax is: `str.replace('thing you want to replace', 'what to replace it with')` 

# In[13]:


salary_selected.columns.str.replace(' ', '_') 

salary_selected.columns


# We could have used both the `str.lower()` and `str.replace()` functions in one line of code by putting them one after the other (aka "chaining"):

# In[14]:


salary_selected.columns = salary_selected.columns.str.lower().str.replace(' ', '_') 

salary_selected.columns


# Let's use `head()` to visually inspect the first five rows of `salary_selected`:

# In[15]:


print(salary_selected.head()) 


# Now let's try sorting the data by `total.earnings` using the [`sort_values()`](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.sort_values.html) function in `pandas`:

# In[16]:


salary_sort = salary_selected.sort_values('total_earnings')


# We can use `head()` to visually inspect `salary_sort`:

# In[17]:


print(salary_sort.head())


# At first glance, it looks okay. The employees appear to be sorted by `total_earnings` from lowest to highest. If this were the case, we'd expect the last row of the `salary_sort` DataFrame to contain the employee with the highest salary. Let's take a look at the last five rows using `tail()`.

# In[18]:


print(salary_sort.tail())


# **What went wrong?**
# 
# The problem is that there are non-numeric characters, `,` and `$`, in the `total.earnings` column. We can see with  [`dtypes`](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.dtypes.html), which returns the data type of each column in the DataFrame, that `total_earnings` is recognized as an "object".

# In[19]:


salary_selected.dtypes


# [Here](http://pbpython.com/pandas_dtypes.html) is an overview of `pandas` data types. Basically, being labeled an "object" means that the column is not being recognized as containing numbers.

# We need to find the `,` and `$` in `total.earnings` and remove them. The `str.replace()` function, which we used above when renaming the columns, lets us do this.
# 
# Let's start by removing the comma and write the result to the original column. (The format for calling a column from a DataFrame in `pandas` is `DataFrame['column_name']`)

# In[20]:


salary_selected['total_earnings'] = salary_selected['total_earnings'].str.replace(',', '')


# Using `head()` to visually inspect `salary_selected`, we see that the commas are gone:

# In[21]:


print(salary_selected.head()) # this works - the commas are gone


# Let's do the same thing, with the dollar sign `$`:

# In[22]:


salary_selected['total_earnings'] = salary_selected['total_earnings'].str.replace('$', '')


# Using `head()` to visually inspect `salary_selected`, we see that the dollar signs are gone:

# In[23]:


salary_selected.head()


# **Now can we use `arrange()` to sort the data by `total_earnings`?**

# In[24]:


salary_sort = salary_selected.sort_values('total_earnings')

salary_sort.head()


# In[25]:


salary_sort.tail()


# Again, at first glance, the employees appear to be sorted by `total_earnings` from lowest to highest. But that would imply that John M. Bresnahan was the highest-paid employee, making 99,997.38 dollars in 2016, while the *Boston Globe* [story](https://www.bostonglobe.com/metro/2017/02/14/police-detective-tops-boston-payroll-with-total-over/6PaXwTAHZGEW5djgwCJuTI/story.html) said the highest-paid city employee made more than 403,000 dollars.

# **What's the problem?**
# 
# Again, we can use `dtypes` to check on how the `total_earnings` variable is encoded.

# In[26]:


salary_sort.dtypes


# It's still an "object" now (still not numeric), because we didn't tell `pandas` that it should be numeric. We can do this with `pd.to_numeric()`:

# In[27]:


salary_sort['total_earnings'] = pd.to_numeric(salary_sort['total_earnings'])


# Now let's run `dtypes` again:

# In[28]:


salary_sort.dtypes


# "float64" means ["floating point numbers"](http://pbpython.com/pandas_dtypes.html) — this is what we want.

# Now let's sort using `sort_values()`. 

# In[29]:


salary_sort = salary_sort.sort_values('total_earnings')

salary_sort.head() # ascending order by default


# One last thing: we have to specify `ascending = False` within `sort_values()` because the function by default sorts the data in ascending order.

# In[30]:


salary_sort = salary_sort.sort_values('total_earnings', ascending = False)

salary_sort.head() # descending order


# We see that Waiman Lee from the Boston PD is the top earner with &gt;403,408 per year, just as the *Boston Globe* [article](https://www.bostonglobe.com/metro/2017/02/14/police-detective-tops-boston-payroll-with-total-over/6PaXwTAHZGEW5djgwCJuTI/story.html) states.

# A bonus thing: maybe it bothers you that the numbers next to each row are no longer in any numeric order. This is because these numbers are the row index of the DataFrame — basically the order that they were in prior to being sorted. In order to reset these numbers, we can use the [`reset_index()`](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.reset_index.html) function on the `salary_sort` DataFrame. We include `drop = True` as a parameter of the function to prevent the old index from being added as a column in the DataFrame.

# In[31]:


salary_sort = salary_sort.reset_index(drop = True)

salary_sort.head() # index is reset


# The Boston Police Department has a lot of high earners. We can figure out the average earnings by department, which we'll call `salary_average`, by using the `groupby` and `mean()` functions in `pandas`.

# In[32]:


salary_average = salary_sort.groupby('department_name').mean()


# In[33]:


salary_average = salary_average

salary_average


# Notice that `pandas` by default sets the `department_name` column as the row index of the `salary_average` DataFrame. I personally don't love this and would rather have a straight-up DataFrame with the row numbers as the index, so I usually run `reset_index()` to get rid of this indexing: 

# In[34]:


salary_average = salary_average.reset_index() # reset_index

salary_average


# We should also rename the `total_earnings` column to `average_earnings` to avoid confusion. We can do this using [`rename()`](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.rename.html). The syntax for `rename()` is `DataFrame.rename(columns = {'current column name':'new column name'})`.

# In[35]:


salary_average = salary_average.rename(columns = {'total_earnings': 'dept_average'}) 


# In[36]:


salary_average


# We can find the Boston Police Department. Find out more about selecting based on attributes [here](https://chrisalbon.com/python/data_wrangling/pandas_selecting_rows_on_conditions/).

# In[37]:


salary_average[salary_average['department_name'] == 'Boston Police Department']


# Now is a good time to revisit "chaining." Notice how we did three things in creating `salary_average`:
# 1. Grouped the `salary_sort` DataFrame by `department_name` and calculated the mean of the numeric columns (in our case, `total_earnings` using `group_by()` and `mean()`.
# 2. Used `reset_index()` on the resulting DataFrame so that `department_name` would no longer be the row index.
# 3. Renamed the `total_earnings` column to `dept_average` to avoid confusion using `rename()`.
# 
# In fact, we can do these three things all at once, by chaining the functions together:

# In[38]:


salary_sort.groupby('department_name').mean().reset_index().rename(columns = {'total_earnings':'dept_average'})


# That's a pretty long line of code. To make it more readable, we can split it up into separate lines. I like to do this by putting the whole expression in parentheses and splitting it up right before each of the functions, which are delineated by the periods:

# In[39]:


(salary_sort.groupby('department_name')
 .mean()
 .reset_index()
 .rename(columns = {'total_earnings':'dept_average'}))


# ## 2. Merging datasets

# Now we have two main datasets, `salary_sort` (the salary for each person, sorted from high to low) and `salary_average` (the average salary for each department). What if I wanted to merge these two together, so I could see side-by-side each person's salary compared to the average for their department?
# 
# We want to join by the `department_name` variable, since that is consistent across both datasets. Let's put the merged data into a new dataframe, `salary_merged`:

# In[40]:


salary_merged = pd.merge(salary_sort, salary_average, on = 'department_name')


# Now we can see the department average, `dept_average`, next to the individual's salary, `total_earnings`:

# In[41]:


salary_merged.head()


# ## 3. Reshaping data

# Here's a dataset on unemployment rates by country from 2012 to 2016, from the International Monetary Fund's World Economic Outlook database (available [here](https://www.imf.org/external/pubs/ft/weo/2017/01/weodata/index.aspx)).
# 
# When you download the dataset, it comes in an Excel file. We can use the `pd.read_excel()` function from `pandas` to load the file into Python.

# In[42]:


unemployment = pd.read_excel('unemployment.xlsx')
unemployment.head()


# You'll notice if you open the `unemployment.xlsx` file in Excel that cells that do not have data (like Argentina in 2015) are labeled with "n/a". A nice feature of `pd.read_excel()` is that it recognizes these cells as NaN ("not a number," or Python's way of encoding missing values), by default. If we wanted to, we could explicitly tell pandas that missing values were labeled "n/a" using `na_values = 'n/a'` within the `pd.read_excel()` function:

# In[43]:


unemployment = pd.read_excel('unemployment.xlsx', na_values = 'n/a')


# Right now, the data are in what's commonly referred to as "wide" format, meaning the variables (unemployment rate for each year) are spread across rows. This might be good for presentation, but it's not great for certain calculations or graphing. "Wide" format data also becomes confusing if other variables are added.
# 
# We need to change the format from "wide" to "long," meaning that the columns (`2012`, `2013`, `2014`, `2015`, `2016`) will be converted into a new variable, which we'll call `Year`, with repeated values for each country. And the unemployment rates will be put into a new variable, which we'll call `Rate_Unemployed`.

# To do this, we'll use the [`pd.melt()`](https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.melt.html) function in `pandas` to create a new DataFrame, `unemployment_long`.

# In[44]:


unemployment_long = pd.melt(unemployment, # data to reshape
                            id_vars = 'Country', # identifier variable
                            var_name = 'Year', # column we want to create from the rows 
                            value_name = 'Rate_Unemployed') # the values of interest


# Inspecting `unemployment_long` using `head()` shows that we have successfully created a long dataset.

# In[45]:


unemployment_long.head()


# ## 4. Calculating year-over-year change in panel data

# Sort the data by `Country` and `Year` using the `sort_values()` function:

# In[46]:


unemployment_long = unemployment_long.sort_values(['Country', 'Year'])

unemployment_long.head()


# Again, we can use `reset_index(drop = True)` to reset the row index so that the numbers next to the rows are in sequential order.

# In[47]:


unemployment_long = unemployment_long.reset_index(drop = True)

unemployment_long.head()


# This type of data is known in time-series analysis as a panel; each country is observed every year from 2012 to 2016.
# 
# For Albania, the percentage point change in unemployment rate from 2012 to 2013 would be 16 - 13.4 = 2.5 percentage points. What if I wanted the year-over-year change in unemployment rate for every country?
# 
# We can use the [`diff()`](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.diff.html) function in `pandas` to do this. We can use `diff()` to calculate the difference between the `Rate_Unemployed` that year and the `Rate_Unemployed` for the year prior (the default for `lag()` is 1 period, which is good for us since we want the change from the previous year). We will save this difference into a new variable, `Change`.

# In[48]:


unemployment_long['Change'] = unemployment_long.Rate_Unemployed.diff()


# Let's inspect the first five rows again, using `head()`:

# In[49]:


unemployment_long.head()


# So far so good. It also makes sense that Albania's `Change` is `NaN` in 2012, since the dataset doesn't contain any unemployment figures before the year 2012.
# 
# But a closer inspection of the data reveals a problem. What if we used `tail()` to look at the *last* 5 rows of the data?

# In[50]:


unemployment_long.tail()


# **Why does Vietnam have a -18.493 percentage point change in 2012?**

# (Hint: use `tail()` to look at the last 6 rows of the data.)

# In[51]:


unemployment_long['Change'] = (unemployment_long
                               .groupby('Country')
                               .Rate_Unemployed.diff())

unemployment_long.tail()


# (Also notice how I put the entire expression in parentheses and put each function on a different line for readability.)

# ## 5. Recoding numerical variables into categorical ones

# Here's a list of some attendees for the 2016 workshop, with names and contact info removed.

# In[52]:


attendees = pd.read_csv('attendees.csv')

attendees.head()


# **What if we wanted to quickly see the age distribution of attendees?**

# In[53]:


attendees['Age group'].value_counts()


# There's an inconsistency in the labeling of the `Age group` variable here. We can fix this using `np.where()` in the `numpy` library. First, let's import the `numpy` library. Like `pandas`, `numpy` has a commonly used alias — `np`.

# In[54]:


import numpy as np


# In[55]:


attendees['Age group'] = np.where(attendees['Age group'] == '30 - 39', # where attendees['Age group'] == '30 - 39'
                                  '30-39', # replace attendees['Age group'] with '30-39'
                                  attendees['Age group']) # otherwise, keep attendees['Age group'] values the same


# This might seem trivial for just one value, but it's useful for larger datasets.

# In[56]:


attendees['Age group'].value_counts()


# Now let's take a look at the professional status of attendees, labeled in `Choose your status:`

# In[57]:


attendees['Choose your status:'].value_counts()


# "Nonprofit, Academic, Government" and "Nonprofit, Academic, Government Early Bird" seem to be the same. We can use `np.where()` (and the Python designation `|` for "or") to combine these two categories into one big category, "Nonprofit/Gov". Let's create a new variable, `status`, for our simplified categorization.
# 
# Notice the extra sets of parentheses around the two conditions linked by the `|` symbol.

# In[58]:


attendees['status'] = np.where((attendees['Choose your status:'] == 'Nonprofit, Academic, Government') |
                               (attendees['Choose your status:'] == 'Nonprofit, Academic, Government Early Bird'),
                           'Nonprofit/Gov', 
                           attendees['Choose your status:'])


# In[59]:


attendees['status'].value_counts()


# ## What else?
# 
# -   How would you create a new variable in the `attendees` data (let's call it `status2`) that has just two categories, "Student" and "Other"?
# 
# -   How would you rename the variables in the `attendees` data to make them easier to work with?
# 
# -   What are some other issues with this dataset? How would you solve them using what we've learned?
# 
# -   What are some other "messy" data issues you've encountered?
