from preswald import text, plotly, connect, get_df, table
import pandas as pd
import plotly.express as px

# -------------------- INITIALIZE APP --------------------
text("# Welcome to RhuDe")
text("## Crime Delving Dashboard")

# -------------------- LOAD DATA --------------------
connect()
df = get_df('filtered_csv')

# Clean missing/null age group entries
df = df[df['AGE_GROUP'].notna() & (df['AGE_GROUP'] != '(null)')]

# -------------------- BAR CHART: ARRESTS BY AGE GROUP --------------------
# Aggregate arrests by age group
age_group_counts = df['AGE_GROUP'].value_counts().reset_index()
age_group_counts.columns = ['Age Group', 'Count']
age_group_counts = age_group_counts.sort_values(by='Age Group')

# Plot age group distribution
fig = px.bar(
    age_group_counts,
    x='Age Group',
    y='Count',
    title='Arrests in Manhattan by Age Group',
    color='Age Group',
    text_auto=True,
    color_discrete_sequence=px.colors.sequential.Tealgrn
)
plotly(fig)

# Insight below chart
text("Most arrests in Manhattan are among individuals aged 25–44, followed by 45–64 and 18–24. "
     "This suggests working-age adults are most involved in arrest activity. Youth (<18) and seniors (65+) account for relatively few arrests.")

# -------------------- FILTER FOR AGE 25–44 --------------------
df_filtered = df[df['AGE_GROUP'] == '25-44']

# -------------------- BAR CHART: LEVEL OF OFFENSE --------------------
# Count offense types (LAW_CAT_CD)
LOO_counts = df_filtered['LAW_CAT_CD'].value_counts().reset_index()
LOO_counts.columns = ['LAW_CAT_CD', 'Count']

# Replace offense codes with readable labels
LOO_counts['LAW_CAT_CD'] = LOO_counts['LAW_CAT_CD'].replace({
    'F': 'Felony',
    'V': 'Violation',
    'M': 'Misdemeanor'
})
LOO_counts.rename(columns={"LAW_CAT_CD": "Level of Offense"}, inplace=True)

# Plot offense level distribution for age group
fig2 = px.bar(
    LOO_counts,
    x='Level of Offense',
    y='Count',
    title='Level of Offense for 25–44 Age Group',
    color='Level of Offense',
    text_auto=True,
    color_discrete_sequence=px.colors.sequential.Tealgrn
)
plotly(fig2)

# Insight below chart
text("The chart shows that among individuals aged 25–44 in Manhattan, misdemeanors account for the majority of arrests, "
     "followed by felonies. Violations are extremely rare in comparison. This suggests that while serious offenses occur, "
     "lower-level crimes dominate arrest records for this age group.")

# -------------------- MAP: GEOSPATIAL ARRESTS --------------------
# Plot map of arrests for this age group, color-coded by offense level
fig_map = px.scatter_mapbox(
    df_filtered,
    lat="Latitude",
    lon="Longitude",
    color="LAW_CAT_CD",  # Color by offense code (F/M/V)
    hover_data=["OFNS_DESC", "ARREST_DATE", "AGE_GROUP", "PERP_SEX"],
    zoom=10,
    title="Map of Arrests by Offense Level (25–44 Age Group, Manhattan)",
    height=600
)

# Use OpenStreetMap style and polish layout
fig_map.update_layout(mapbox_style="open-street-map")
fig_map.update_layout(
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    font=dict(size=12)
)
plotly(fig_map)

text("The scatter map shows the geographic distribution of arrests among individuals aged 25–44 in Manhattan, color-coded by offense level. Misdemeanor arrests are widespread across the borough, while felony and violation arrests are more sparsely distributed. This pattern indicates that lower-level offenses occur more broadly, while serious crimes may be more localized.")


