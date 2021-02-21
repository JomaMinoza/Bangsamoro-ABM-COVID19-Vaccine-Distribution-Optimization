import pandas as pd

def epi_data_extractor(data, filter_column, filter_value):

    if filter_column == "BarangayPSGC":
        df = data[data[filter_column].isin(filter_value)]
    else:
        df = data[data[filter_column] == filter_value]
        
    df.head(10)
    
    # Checking if the df exists
    
    if not df.empty:
        # Filter fields
        
        df = df[['Age','AgeGroup','Sex','DateResultRelease','DateRecover','DateDied', 'RegionRes', 'ProvRes', 'CityMunRes','BarangayPSGC', 'RemovalType']]
        df['DateResultRelease'] = pd.to_datetime(df['DateResultRelease'])
        df['DateRecover']       = pd.to_datetime(df['DateRecover'])
        df['DateDied']          = pd.to_datetime(df['DateDied'])

        # Case Incidence Data
        
        I_df = df['DateResultRelease'].dt.floor('d').value_counts().rename_axis('Date').reset_index(name='Case Incidence')
        I_df.sort_values(by='Date', inplace= True)
        I_df.set_index('Date', inplace=True)

        # Recovered Data

        R_df = df['DateRecover'].dt.floor('d').value_counts().rename_axis('Date').reset_index(name='Reported Recovered')
        R_df.sort_values(by='Date', inplace= True)
        R_df.set_index('Date', inplace=True)
        
        # Deaths Data
        
        D_df = df['DateDied'].dt.floor('d').value_counts().rename_axis('Date').reset_index(name='Reported Died')
        D_df.sort_values(by='Date', inplace= True)
        D_df.set_index('Date', inplace=True)
        
        # Merging of Data
        
        IRD_df = pd.concat([I_df, R_df, D_df], axis=1, sort=False)
        IRD_df.fillna(0, inplace=True)
        
        # Calculation of Removed

        IRD_df['Removed'] = IRD_df.apply(lambda row: (row['Reported Recovered'] + row['Reported Died']) if (row['Reported Recovered'] + row['Reported Died']) < row['Case Incidence'] else row['Reported Recovered'] , axis=1)
        IRD_df["Active Cases"] = IRD_df[['Case Incidence']].values.cumsum() - IRD_df[['Removed']].values.cumsum()
        
        return IRD_df
    