
# In[Modules]:
import sys
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.metrics import mean_squared_error


# In[Methods]
def dummy_variable(column_idx, dataframe):
    enc = OneHotEncoder()
    labler = LabelEncoder()

    # get the column name for the column index given
    colname = dataframe.columns[column_idx]

    # fit and transform the the column of categories into int labels
    labels = labler.fit_transform(dataframe[colname])
    labels = labels.reshape(-1,1)

    # fit and transform 1 dimensional labels into binary features
    categor_vars = enc.fit_transform(labels)
    categor_vars = categor_vars.toarray()

    # convert the features into a dataframe
    df = pd.DataFrame(categor_vars)

    # get the orignal categories that coresspond to the int labels and reset columns
    # in dataframe of features
    columns = df.columns
    column_labels = labler.inverse_transform(columns)
    df.columns = column_labels

    # remove the feature and merge the original dataset with the new dataframed features
    del dataframe[colname]
    dataframe = pd.concat([dataframe.reset_index(drop=True), df.reset_index(drop=True)], axis=1)

    return dataframe
     
# feature extractor
def feature_extractor(columns, data):
    df = pd.DataFrame(columns=columns)
    columns = pd.Series(columns)
    print len(data[0])
    for i in range(len(data[0])):
        df.loc[i] = list( (data.iloc[i, 0] == columns) + 0)

    return pd.concat([data.iloc[:,1], df], axis=1)

# In[]
input_filename = sys.argv[1]
output_filename = sys.argv[2]

# In[]
# read in train data
train_data = pd.read_csv('train.csv')

# In[]
countries = train_data.columns[1:-1]


# read in test data from given input filename
test_data = pd.read_csv(input_filename, header=None).iloc[:,:2]
test_data = feature_extractor(countries, test_data)


# In[]
# split in X and Y train
X_train = train_data.drop("target", axis=1)
Y_train = train_data["target"].reshape(-1,1)

# fit Decision tree regressor
reg = DecisionTreeRegressor(max_depth=200)
reg.fit(X_train, Y_train)


# predict variables and create data frame
y_pred = reg.predict(test_data)
predicted_vals = pd.DataFrame({'pred':y_pred})

# write to csv file name as the second argument in sys
predicted_vals.to_csv(output_filename, index=False, header=False)
