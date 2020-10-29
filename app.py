import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


@st.cache
def load_baseball_data():
    return pd.read_csv('baseball-salaries-simplified.csv')


def percentile_in_year(year, percent):
    return focus[focus.year == year].salary.quantile(percent/100)


def full_position_names(option):
    return choices[option]


df = load_baseball_data()

st.title('Major League Baseball Player Salaries')

first_year, last_year = st.sidebar.slider('Select the Years to Look At:', 1988, 2016, (2000, 2011), 1)

choices = {'P': 'Pitcher',
           'C': 'Catcher',
           '1B': 'First Base',
           '2B': 'Second Base',
           'SS': 'Short Stop',
           '3B': 'Third Base',
           'LF': 'Left Field',
           'CF': 'Center Field',
           'RF': 'Right Field',
           'OF': 'Outfield',
           'DH': 'Designated Hitter'}

position = st.sidebar.selectbox('Select Position:', options=list(choices.keys()), format_func=full_position_names)

year_range = (df.year >= first_year) & (df.year <= last_year)
this_position = df.pos == position
focus = df[year_range & this_position]

years = range(first_year, last_year + 1)

df_pcts = pd.DataFrame({"year": years})





for percent in range(0, 110, 10):
    df_pcts[percent] = [percentile_in_year(year, percent) for year in years]

df_pcts.index = df_pcts.year
del df_pcts['year']

df_pcts /= 1000000

df_pcts.plot(legend='upper left')
plt.gcf().set_size_inches(8, 10)
plt.title(f'Salaries for {choices[position]}, {first_year}-{last_year} ({len(focus)} players)', fontsize=20)
plt.xticks(df_pcts.index, rotation=90)
plt.ylabel('Salary percentiles in $1M', fontsize=14)
plt.xlabel(None)
st.pyplot()

st.header(f'Highest Salaries for {choices[position]}, {first_year}-{last_year}')
st.write(focus.nlargest(10, 'salary').reset_index(drop=True))
