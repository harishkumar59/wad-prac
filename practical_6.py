import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

# Example dataset
dataset = [['bread', 'milk', 'eggs'],
           ['bread', 'diapers', 'beer', 'eggs'],
           ['milk', 'diapers', 'beer', 'cola'],
           ['bread', 'milk', 'diapers', 'beer', 'cola'],
           ['bread', 'milk', 'diapers', 'beer']]

# Convert the dataset to a one-hot encoded matrix
te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)

# Optimization: Explicitly cast to bool to prevent future Pandas/Mlxtend warnings
df = pd.DataFrame(te_ary, columns=te.columns_).astype(bool)

# Apply the Apriori algorithm to generate frequent itemsets
frequent_itemsets = apriori(df, min_support=0.6, use_colnames=True)

# Print the frequent itemsets
print(frequent_itemsets)