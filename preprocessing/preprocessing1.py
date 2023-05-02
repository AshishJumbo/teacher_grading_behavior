import pandas as pd
import random

# important:
#  this is the initial cleanup code. There was a minor bug in the initial implementation of the code
#  that resulted in the teacher being exposed to a few problem logs more than once during grading.
#  This file checks for the duplicates and in instances where ther are duplicates we randomly select one and use
#  that in the cleaned dataset. A bit messy to be honest but this is the best option.
#  P.S. 16 instances where there were duplication but the teacher gave different grades only in 3 instances
#

teacher_problem_log_id_potential_corruption = {
    'teacher_xid': [3141985, 3097639, 2912675, 2912675, 2856866, 2835460, 2835460, 861463, 861254, 178649, 178649,
                    7629, 861463],
    'problem_log_id': [144485699, 144652730, 144485699, 132248161, 153804667, 132943963, 142080265, 136466591,
                       150674921, 142378339, 153804667, 144800293, 136466591]
}

df_fairness_graded_openresponse = pd.read_csv('../data/raw/fairness_graded_openresponse.csv')
df_fairness_assigned_pr_logs = pd.read_csv('../data/raw/fairness_assigned_pr_logs.csv')
df_fairness_xid_curricula_map = pd.read_csv('../data/raw/fairness_xid_curricula_map.csv')
teacher_xids = df_fairness_xid_curricula_map.teacher_xid.unique()

df_filtered = df_fairness_graded_openresponse  # .loc[
# df_fairness_graded_openresponse.created_at < '2022-07-11 19:00:00.000 -0400']

df_filtered_combined = pd.DataFrame(columns=['grade_feedback_id', 'problem_log_id', 'teacher_xid', 'grade', 'feedback',
                                             'active_batch', 'time_taken_seconds', 'created_at',
                                             'fairness_assigned_pr_logs_id', 'batch_number', 'student_idx'])

# TODO:
#  when accounting for the corrupted data there were 16 instances where data could potentially be corrupted but
#  the grades were the same for 13 and as such the grade data can only be potentially be impacted for 3 instances
#  Solution: randomly selecting one of the data as the difference was only 1 point across the board
for teacher_xid in teacher_xids:
    df_test = df_filtered.loc[(df_filtered.teacher_xid == teacher_xid) & (df_filtered.active_batch != 5)]
    teacher_category = df_fairness_xid_curricula_map.loc[
        df_fairness_xid_curricula_map.teacher_xid == teacher_xid].category.unique()[0]
    if teacher_category == 0:
        assigned_problem_logs = df_fairness_assigned_pr_logs.loc[
            (df_fairness_assigned_pr_logs.teacher_xid == -1) &
            (df_fairness_assigned_pr_logs.batch_number != 5)]
    else:
        assigned_problem_logs = df_fairness_assigned_pr_logs.loc[
            (df_fairness_assigned_pr_logs.teacher_xid == teacher_xid) &
            (df_fairness_assigned_pr_logs.batch_number != 5)]

    active_batches = sorted(df_test.active_batch.unique())
    for active_batch in active_batches:
        eligible_batches = [(active_batch + 0) % 5, (active_batch + 1) % 5, (active_batch + 2) % 5,
                            (active_batch + 3) % 5]
        eligible_problem_logs = assigned_problem_logs.loc[
            assigned_problem_logs.batch_number.isin(eligible_batches)].problem_log_id.unique()
        temp_df = df_test.loc[(df_test.active_batch == active_batch) &
                              (df_test.problem_log_id.isin(eligible_problem_logs))]
        temp_df_problem_log_id_count = temp_df.groupby(by=['problem_log_id']).size().reset_index(name='frequency')
        eligible_grade_feedback_ids = temp_df.loc[
            temp_df.problem_log_id.isin(
                temp_df_problem_log_id_count.loc[
                    temp_df_problem_log_id_count.frequency == 1].problem_log_id.unique())].grade_feedback_id.tolist()
        if temp_df_problem_log_id_count.frequency.max() > 1:
            # print("========================================")
            # print(teacher_xid, active_batch)
            # print(temp_df_problem_log_id_count.loc[temp_df_problem_log_id_count.frequency > 1])
            # print(temp_df.loc[
            #           temp_df.problem_log_id.isin(
            #               temp_df_problem_log_id_count.loc[
            #                   temp_df_problem_log_id_count.frequency > 1].problem_log_id.unique()
            #           ), ['problem_log_id', 'grade']])
            duplicate_probelm_log_ids = temp_df_problem_log_id_count.loc[
                temp_df_problem_log_id_count.frequency > 1].problem_log_id.unique()
            for duplicate_problem_log_id in duplicate_probelm_log_ids:
                temp_df_index = random.choice(
                    temp_df.loc[
                        temp_df.problem_log_id == duplicate_problem_log_id].grade_feedback_id.unique())
                eligible_grade_feedback_ids.append(temp_df_index)

            temp_df = temp_df.loc[temp_df.grade_feedback_id.isin(eligible_grade_feedback_ids)]

        temp_df = temp_df.merge(
            assigned_problem_logs.loc[
                assigned_problem_logs.batch_number.isin(eligible_batches),
                ['fairness_assigned_pr_logs_id', 'problem_log_id', 'batch_number', 'student_idx']],
            how='inner', on=['problem_log_id'])
        temp_df.reset_index(drop=True, inplace=True)
        df_filtered_combined = pd.concat([df_filtered_combined, temp_df])


df_filtered_combined = df_filtered_combined.merge(
    df_fairness_xid_curricula_map[['username', 'teacher_xid', 'curricula', 'category']], how='inner', on='teacher_xid')
df_filtered_combined.to_csv('../data/processed1/filtered_fairness_graded_openresponse.csv', index=False)

# dev-note:
#  check frequency on test and the frequency should always be 60 for all rows
#  check frequency on test2 and the frequency should always be 4 for all rows
test = df_filtered_combined.groupby(by=['teacher_xid', 'active_batch']).size().reset_index(name='frequency')
print(test.frequency.value_counts())
test2 = df_filtered_combined.groupby(
    by=['teacher_xid', 'active_batch', 'student_idx']).size().reset_index(name='frequency')
print(test2.frequency.value_counts())


