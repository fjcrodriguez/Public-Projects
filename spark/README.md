# Spark + Random Forests + Linear Regression (ML Lib)

Using a spark cluster, Random Forest and Linear Regression  models were combined to make
a "meta" ensemble model, and then used to predict returns for a given financial instrument in
a given time period. The dataset was large with over 2 million observations and over 100 features.
The performance of the model was evaluated using correlation between the predictions and target.
What makes this project interesting is that the data fields are actually anonymized,
which means there was not much intuitive feature engineering to be done. So instead,
linear regression was used with two features that had the highest correlations
with the target. But this alone was not enough to achieve even a positive correlation coefficient.
Random Forest was then added to the model with all features in the dataset to create
the ensemble model. The predictions consisted of a weighted average between
Linear Regression and Random Forest with the weights being 15% and 85%, respectively. This model
achieved 0.026 correlation, and although this sounds insignificant, in financial
modeling small positive correlation coefficients are very impactful.
