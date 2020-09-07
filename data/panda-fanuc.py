import pandas as pd

df = pd.read_csv('fanuc.csv')
print(df.head())
print(df.columns)
print('DATE COLUMN')
print(df['DATE'])
print('MuLTIPLE COLUMN')
x  = df.loc[:,['TIME','DATE','@ActExtTorque6','@ActConsumpPower']]
x.to_csv('fanuc-torque-power.csv', index=False)
