Profile Match:

You have been given a machine learning model trained on user profiles.

Your goal is to find the hidden profile that the model considers a perfect match.

The model takes five values:

age
height_cm
weight_kg
birth_month
birth_year

Your objective is to reach:

100%

Anything below a perfect match is incorrect.

`provide netcat server and pkl file`


flag: d4rk{pr0f1le_m4tched_ez!!}

solution:

Inputs that give a 100% (perfect) score of 1.0:
Any profile [[age, height, weight, month, year]] satisfying these ranges:

age: $> 17.5$ and $\leq 18.5$ (e.g. 18)
height: $> 171$ and $\leq 191.5$ (e.g. 172–191)
weight: $> 70$ and $\leq 74.5$ (e.g. 71–74)
month: $> 6.5$ and $\leq 10.5$ (e.g. 7–10)
year: $> 2002.5$ (e.g. 2003 or later)

The pickle file is a scikit-learn DecisionTreeRegressor (trained with squared_error, max_depth=20, ~17k nodes / 8695 leaves). It takes the 5 features age height weight month year and predicts a score in [0, 1]. There is exactly one leaf whose value is 1.0; every other leaf is strictly less

The path to that unique perfect leaf imposes the inequalities above (all other intermediate splits are subsumed by the tightest bounds)
