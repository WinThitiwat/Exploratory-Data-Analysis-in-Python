# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 11:33:47 2018

@author: win.thitiwat
"""

"""
Purpose of this file:
    
    Try to apply the Exploratory Data Analysis concept using Python (Pandas,
    Matplotlib, seaborn, Numpy)  and get some interesting insight from the
    analysis with some external research to the findings
    
    Data source:  World Bank Dataset 2014

"""


import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


filename1 = "world_data_hult_regions.xlsx"
filename2 = "world_data_hult_regions_northern_asiapacific.xlsx"
wd_df = pd.read_excel(filename2)
world_df =  pd.read_excel(filename1)

###############################################################
########### Explore dataset ###########
        
# missing value ratio
m_pct = (wd_df.isnull().sum() / len(wd_df)).round(2)

wd_df.count()

wd_df.shape

wd_df.isnull().sum()/len(wd_df)

# Missing value heatmap
wd_null = wd_df.isnull()
fig, ax = plt.subplots(figsize=(15,15))
sns.heatmap(wd_null,
            cmap = 'Blues',
            square = True,
            annot = False,
            linecolor = 'yellow',
            linewidths = 0.5)


###############################################################
# backup some data prior to filling missing values and drop some column

wd_df_backup = pd.DataFrame.copy(wd_df)
world_backup = pd.DataFrame.copy(world_df)

###############################################################
# flag the categorical data into number
inc_type = {"Low income":1,"Lower middle income":2,"Upper middle income":3,"High income":4}
for row_no, value in enumerate(wd_df_backup.loc[:,"income_group"]):
    wd_df_backup.loc[row_no,"income_group_num" ]=  inc_type.get(value)


###############################################################
# backup before imputing missing value using mean
wd_df_dropped = wd_df_backup.drop(["country_index","Hult_Team_Regions", "country_name",
                            "country_code","income_group","homicides_per_100k",
                            "adult_literacy_pct", "incidence_hiv"], axis=1)
wd_df_mean  = pd.DataFrame.copy(wd_df_dropped)

for col in wd_df_mean:
        print(col)
        if wd_df_mean[col].isnull().any():
            col_median = wd_df_mean[col].mean()
            wd_df_mean[col] = (wd_df_mean[col].fillna(col_median).round(2))



######################################################
# Heatmap to check correlation of each variable
df_corr_mean = wd_df_mean.corr()

sns.palplot(sns.color_palette('coolwarm', 12))
fig, ax = plt.subplots(figsize=(15,15))
sns.heatmap(df_corr_mean,
            cmap = 'coolwarm',
            square = True,
            annot = True,
            linecolor = 'black',
            linewidths = 0.5
            )

plt.savefig('World Bank Data corr heat map_2.png')
plt.show()

######################################################
# create boxplot of each variable and save into image
for each_var in wd_df_mean:
    wd_df_mean[[each_var]].boxplot()
    plt.title(f'Boxplot for {each_var}')
    plt.show()
    
 
######################################################
# check number of varibles that has correlation more than 70% and flag
#       and get the total amount of vars 
df_corr = pd.DataFrame.copy(df_corr_mean)
corr_benchmark = 0.7
for each_row in df_corr:
    for col_no, col_val in enumerate(df_corr[each_row]):
        if abs(col_val) > corr_benchmark:
            df_corr[each_row][col_no] = 1
        else:
            df_corr[each_row][col_no] = 0
            
df_corr.sum()

 
######################################################
# finalize the variables to run correlation
selected_variables = ['child_mortality_per_1k', 'pct_agriculture_employment', 'pct_male_employment', 'pct_female_employment', 'CO2_emissions_per_capita','access_to_electricity_pop','internet_usage_pct','urban_population_pct','income_group_num', 'pct_services_employment']


# create variables-selected var and run correlation
wd_selected_var = wd_df_mean.loc[:, selected_variables]


######################################################
# run correlation matrix for the finalized dataset
df_selVar_corr = wd_selected_var.corr().round(2)

fig, ax = plt.subplots(figsize=(15,15))

sns.heatmap(df_selVar_corr,
            cmap = 'coolwarm',
            square = True,
            annot = True,
            linecolor = 'black',
            linewidths = 0.5)
sns.set(font_scale=2.0)

plt.tight_layout()
plt.savefig('WD_selected corr.png')
plt.show()


############################################################
# Research data from the whole world

inc_type = {"Low income":1,"Lower middle income":2,"Upper middle income":3,"High income":4}
for row_no, value in enumerate(world_backup.loc[:,"income_group"]):
    world_backup.loc[row_no,"income_group_num" ]=  inc_type.get(value)

world_df_dropped = world_backup.drop(["country_index","Hult_Team_Regions", "country_name",
                            "country_code","income_group","homicides_per_100k",
                            "adult_literacy_pct", "incidence_hiv"], axis=1)
world_df_mean  = pd.DataFrame.copy(world_df_dropped)

for col in world_df_mean:
        print(col)
        if world_df_mean[col].isnull().any():
            col_median = world_df_mean[col].mean()
            world_df_mean[col] = (world_df_mean[col].fillna(col_median).round(2))

world_selected_var = world_df_mean.loc[:, selected_variables]



############################################################
# compare mean data from the whole world to our target region
         
n_groups = 10

fig, ax = plt.subplots(figsize=(15,15))

index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = ax.bar(index, world_selected_var.mean().round(2), bar_width,
                yerr = world_selected_var.std().round(2),
                alpha=opacity, color='b',
                error_kw=error_config,
                label='World')

rects2 = ax.bar(index + bar_width, wd_selected_var.mean().round(2), bar_width,
                yerr = wd_selected_var.std().round(2),
                alpha=opacity, color='r', error_kw=error_config,
                label='Region')
ax.set_xticks(index+bar_width/2)
plt.xticks(rotation=90)
ax.set_xticklabels((selected_variables))
ax.legend()
fig.tight_layout()
plt.show()


############################################################
# compare whole world and regional data using violinplot
for each in selected_variables:
    sns.violinplot(
                   y = each,
                   data = world_selected_var,
                   orient = 'v',
                   inner = None,
                   color = 'white'
                   )  
    
    sns.violinplot(
                  y = each,
                  data = wd_selected_var,
                  size = 5,
                  orient = 'v',
                  color = 'white',
                  inner = None
                  )
    
    plt.title(f'{each} Comparison')
    plt.savefig(f'violinplot2 for {each}.png')
    plt.show()
        




