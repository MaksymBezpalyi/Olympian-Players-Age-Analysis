import seaborn
import matplotlib.pyplot as plt
from tabulate import tabulate
import pandas as pd
import plotly.express as px

link_to_data = "https://raw.githubusercontent.com/KeithGalli/complete-pandas-tutorial/refs/heads/master/data/bios.csv"

bios = pd.read_csv(link_to_data)
bios.dropna(inplace=True)

bios.drop(['height_cm','born_city', 'weight_kg','born_country','born_region','athlete_id'], axis=1, inplace=True)
bios.rename(columns={'NOC':'team_country'}, inplace=True)

bios.dropna(subset=['died_date'], inplace=True)

bios['born_datetime'] = pd.to_datetime(bios['born_date'])

bios['died_datetime'] = pd.to_datetime(bios['died_date'])

bios['died_age'] = (bios['died_datetime'] - bios['born_datetime']).dt.days // 365

average_years = bios['died_age'].mean()
minimum_years = bios['died_age'].min()
maximum_years = bios['died_age'].max()

bios['age_40'] = bios['died_age'] <= 40
age_forty = 0
for n in bios['age_40']:
    if n == True:
        age_forty += 1

bios['between_40_60'] = (bios['died_age'] >=40) & (bios['died_age'] <=60)
age_sixty = 0
for n in bios['between_40_60']:
    if n == True:
        age_sixty += 1

bios['between_60_80'] = (bios['died_age'] >=60) & (bios['died_age'] <80)
age_eighty = 0
for n in bios['between_60_80']:
    if n == True:
        age_eighty += 1

bios['age_80_plus'] = bios['died_age'] >=80
age_eighty_plus = 0
for n in bios['age_80_plus']:
    if n == True:
        age_eighty_plus += 1

average_age_by_countries = bios.groupby('team_country', as_index=False)['died_age'].mean()
average_age_by_countries['average'] = average_age_by_countries['died_age'].astype(int)

bios.reset_index(drop=True, inplace=True)
average_age_by_countries.reset_index(drop=True, inplace=True)
print(tabulate(bios.head(), headers='keys', tablefmt='psql'))
print(tabulate(average_age_by_countries, headers='keys', tablefmt='psql'))
print("Average years: ", round(average_years))
print("Minimum years: ", minimum_years)
print("Maximum years: ", maximum_years)
print("Lived untill 40 years: ", age_forty)
print("Lived between 40 and 60 years: ", age_sixty)
print("Lived between 60 and 80 years: ", age_eighty)
print("Lived between 80 and 80 years: ", age_eighty_plus)

plt.figure(figsize=(8, 6))
age_groups = {
    'Under 40 years': age_forty,
    '40–60 years': age_sixty,
    '60–80 years': age_eighty,
    '80+ years': age_eighty_plus
}
seaborn.barplot(x=list(age_groups.keys()), y=list(age_groups.values()), palette="YlGnBu")
plt.title('Distribution of Olympic Athletes by Age at Death')
plt.xlabel('Age groups')
plt.ylabel('Number of athletes')
plt.show()


top_countries = average_age_by_countries.sort_values(by='average', ascending=False).head(20)
plt.figure(figsize=(10, 8))
seaborn.barplot(data=top_countries, y='team_country', x='average', palette='viridis')
plt.title('Average Age at Death of Athletes (Top 20 Countries)')
plt.xlabel('Average age at death (years)')
plt.ylabel('Country')
plt.show()


fig = px.choropleth(
    average_age_by_countries,
    locations='team_country',
    locationmode='ISO-3',
    color='average',
    color_continuous_scale='Viridis',
    title='Average Age at Death of Olympic Athletes by Country'
)
fig.show()






