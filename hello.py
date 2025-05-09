from preswald import text, plotly, connect, get_df, table
import pandas as pd
import plotly.express as px

text("# Welcome to Preswald!")
text("This is your first app. 🎉")

# Load the CSV
connect()
df_arrest = get_df('sample_csv')
df_hate = get_df('filtered_hate.csv')

print(df_arrest)