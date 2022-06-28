from tabula import read_pdf
import pandas as pd
df = read_pdf('test.pdf', pages='all')


print(df[1])

data = pd.DataFrame(df)
data.to_csv('DGTU.csv')
