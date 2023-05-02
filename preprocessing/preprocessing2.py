import pandas as pd

# important: in this section we merge the filtered data with initila prior to experiment info,
#  student prior assignment information and then we will use all of the information to determine
#  the various conditions in the experiment when the teachers graded the student responses

df_filtered_fairness_graded_or = pd.read_csv("../data/processed1/filtered_fairness_graded_openresponse.csv")
df_fairness_raw_data = pd.read_csv("../data/raw/fairness_raw_data.csv")

# dev-note: there should be 5 more problem_log_ids in the raw data because there were 5 problem logs
#  in the initial training sample



