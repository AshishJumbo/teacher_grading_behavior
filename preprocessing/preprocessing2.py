import pandas as pd

# important: in this section we merge the filtered data with initila prior to experiment info,
#  student prior assignment information and then we will use all of the information to determine
#  the various conditions in the experiment when the teachers graded the student responses

df_filtered_fairness_graded_or = pd.read_csv("../data/processed1/filtered_fairness_graded_openresponse.csv")
df_fairness_raw_data = pd.read_csv("../data/raw/fairness_raw_data.csv")
df_fairness_prior_assignment_scores = pd.read_csv("../data/raw/fairness_prior_assignment_scores.csv")

# dev-note: there should be 5 more problem_log_ids in the raw data because there were 5 problem logs
#  in the initial training sample

df_filtered_fairness_graded_or['exp_batch_number'] = \
    (((df_filtered_fairness_graded_or.batch_number - df_filtered_fairness_graded_or.active_batch) + 5) % 5)
df_filtered_fairness_graded_or['experiment_condition'] = 'anonymized'
df_filtered_fairness_graded_or.loc[
    df_filtered_fairness_graded_or.exp_batch_number == 1, 'experiment_condition'] = 'ethnic_names'
df_filtered_fairness_graded_or.loc[
    df_filtered_fairness_graded_or.exp_batch_number == 2, 'experiment_condition'] = 'anonymized_w_prior'
df_filtered_fairness_graded_or.loc[
    df_filtered_fairness_graded_or.exp_batch_number == 3, 'experiment_condition'] = 'ethnic_names_w_prior'

learner_ethnic_names = {
    -1: "anonymized", 0: "Jaylen Alston", 1: "Jada Jackson", 2: "Gabriel Garcia",
    3: "Antonia Hernandez", 4: "Liam Smith", 5: "Emma Miller", 6: "Peng Chu", 7: "Hitomi Tanaka",
    8: "Sanjay Kumara", 9: "Aastha Valayaputhur", 10: "Zara Amin", 11: "Hassan Bilal",
    12: "Brianna Booker", 13: "Isabella Lopez", 14: "Emily Wilson"
}

learner_ethnicity = {
    -1: "anonymized", 0: "African American", 1: "African American", 2: "Hispanic", 3: "Hispanic",
    4: "Caucasian", 5: "Caucasian", 6: "Asian", 7: "Asian", 8: "South Asian", 9: "South Asian",
    10: "Middle Eastern", 11: "Middle Eastern", 12: "African American", 13: "Hispanic", 14: "Caucasian"
}

learner_gender = {
    -1: "anonymized", 0: "boy", 1: "girl", 2: "boy", 3: "girl", 4: "boy", 5: "girl",
    6: "boy", 7: "girl", 8: "boy", 9: "girl", 10: "girl", 11: "boy", 12: "girl", 13: "girl",
    14: "girl"
}

df_filtered_fairness_graded_or['learner_ethnic_names'] = df_filtered_fairness_graded_or.student_idx
df_filtered_fairness_graded_or['learner_ethnicity'] = df_filtered_fairness_graded_or.student_idx
df_filtered_fairness_graded_or['learner_gender'] = df_filtered_fairness_graded_or.student_idx

df_filtered_fairness_graded_or.replace({"learner_ethnic_names": learner_ethnic_names}, inplace=True)
df_filtered_fairness_graded_or.replace({"learner_ethnicity": learner_ethnicity}, inplace=True)
df_filtered_fairness_graded_or.replace({"learner_gender": learner_gender}, inplace=True)

df_filtered_fairness_graded_or = df_filtered_fairness_graded_or.merge(
    df_fairness_raw_data, how='inner', on='problem_log_id')

prior_assignment_scores = ['is_skb_10', 'score_percentage_10', 'is_skb_9', 'score_percentage_9', 'is_skb_8',
                           'score_percentage_8', 'is_skb_7', 'score_percentage_7', 'is_skb_6', 'score_percentage_6',
                           'is_skb_5', 'score_percentage_5', 'is_skb_4', 'score_percentage_4', 'is_skb_3',
                           'score_percentage_3', 'is_skb_2', 'score_percentage_2', 'is_skb_1', 'score_percentage_1',
                           'is_skb_0', 'score_percentage_0', 'currentassignemntlogid']

df_fairness_prior_assignment_scores_filtered = df_fairness_prior_assignment_scores[prior_assignment_scores]

# df_filtered_fairness_graded_or = df_filtered_fairness_graded_or.merge(
#     df_fairness_prior_assignment_scores[prior_assignment_scores], how='inner', left_on='assignment_log_id',
#     right_on='currentassignemntlogid')

df_filtered_fairness_graded_or['prior_assignment_score_percentage_1'] = 0
df_filtered_fairness_graded_or['prior_assignment_score_percentage_2'] = 0
df_filtered_fairness_graded_or['prior_assignment_score_percentage_3'] = 0
df_filtered_fairness_graded_or['prior_assignment_score_percentage_4'] = 0
df_filtered_fairness_graded_or['prior_assignment_score_percentage_5'] = 0

user_xids = df_filtered_fairness_graded_or.user_xid.unique()

for user_xid in user_xids:
    assignment_log_ids = df_filtered_fairness_graded_or.loc[
        df_filtered_fairness_graded_or.user_xid == user_xid].assignment_log_id.unique()
    print(assignment_log_ids)
    for assignment_log_id in assignment_log_ids:
        temp_df = df_fairness_prior_assignment_scores_filtered.loc[
            df_fairness_prior_assignment_scores_filtered.currentassignemntlogid == assignment_log_id]
        last_10_assign_scores = [i for i in range(10)]
        active_index = 0
        for i in range(1, 11):
            temp_df.fillna({'is_skb_' + str(i): False, 'score_percentage_' + str(i): 0}, inplace=True)
            print(temp_df['is_skb_' + str(i)])
            if ~(temp_df['is_skb_' + str(i)].unique()[0]):
                last_10_assign_scores[active_index] = temp_df['score_percentage_' + str(i)].unique()[0]
                active_index += 1

        for j in range(1, 6):
            df_filtered_fairness_graded_or.loc[(df_filtered_fairness_graded_or.user_xid == user_xid) &
                                               (df_filtered_fairness_graded_or.assignment_log_id == assignment_log_id),
                                               'prior_assignment_score_percentage_' + str(j)] = last_10_assign_scores[
                j - 1]

df_filtered_fairness_graded_or = df_filtered_fairness_graded_or[
    ['grade_feedback_id', 'problem_log_id', 'teacher_xid', 'grade', 'feedback', 'active_batch', 'time_taken_seconds',
     'created_at', 'fairness_assigned_pr_logs_id', 'batch_number', 'student_idx',  # 'username',
     'curricula', 'category',
     'exp_batch_number', 'experiment_condition', 'learner_ethnic_names', 'learner_ethnicity', 'learner_gender',
     'assignment_log_id', 'problem_id', 'start_time', 'end_time', 'score', 'answer_text', 'first_action_type_id',
     'attempt_count', 'first_response_time', 'teacher_comment', 'user_xid', 'assignment_xid', 'assignment_id',
     'owner_xid', 'name', 'problem_type_id', 'assistment_id', 'position', 'prior_assignment_score_percentage_1',
     'prior_assignment_score_percentage_2', 'prior_assignment_score_percentage_3',
     'prior_assignment_score_percentage_4', 'prior_assignment_score_percentage_5']]
df_filtered_fairness_graded_or.to_csv('../data/processed2/filtered_fairness_graded_openresponse_final.csv',
                                      index=False)
