import pandas as pd
import numpy as np

### Compute ASR
# Load your CSV file
def count_fast_success(df):
    # Filter the rows where fast_is_succ is True and fast_conversation_rounds <= i
    count = df[(df['slow_is_succ'] == True)].shape[0]
    return count
Result = []
trials = [1,2,3,4,5]

for trial in trials:
    print(f"Trial {trial}")
    df = pd.read_csv(f'./outputs/ablation_result/output_conversations_first_order_controlagent_claude_{trial}/final_results.csv')
    result = count_fast_success(df)

    print(result)
    Result.append(result*2)

print(f"ASR is {np.average(Result, axis=0)}")



### Compute average iteration number
# Load your CSV file
def compute_average_iteration(df):
    # Filter the rows where fast_is_succ is True and fast_conversation_rounds <= i
    count = df['slow_conversation_rounds'].mean()
    return count

Result = []
trials = [1,2,3,4,5]
for trial in trials:
    print(f"Trial {trial}")
    df = pd.read_csv(f'./outputs/ablation_result/output_conversations_first_order_controlagent_claude_{trial}/final_results.csv')

    result = compute_average_iteration(df)

    # print(result)
    Result.append(result)

print(np.average(Result, axis=0))

exit()

### Compute AgSR

def count_fast_success(dfs):
    total_rows = 25  # Each DataFrame has 50 rows
    success_count = 0
    
    # Iterate over each row index (0 to 49)
    for row in range(total_rows):
        # Check if any of the 5 DataFrames has a 'True' in 'is_succ' for this row
        for df in dfs:
            # print(df.loc[row, 'is_succ'][0])
            # exit()
            if (df.loc[row, 'is_succ'] == True):
                success_count += 1
                break  # No need to check other DataFrames for this row if one is True
    
    # Calculate the success rate
    success_rate = success_count / total_rows
    return success_rate

Result = []
# rounds = [1,2,4,6,8,10]

# print(f"Trial {trial}")
df1 = pd.read_csv(f'./outputs/baseline/zero_shot_cot_4o/output_conversations_higher_order_stable_4o_{1}/final_results.csv')
df2 = pd.read_csv(f'./outputs/baseline/zero_shot_cot_4o/output_conversations_higher_order_stable_4o_{2}/final_results.csv')
df3 = pd.read_csv(f'./outputs/baseline/zero_shot_cot_4o/output_conversations_higher_order_stable_4o_{3}/final_results.csv')
df4 = pd.read_csv(f'./outputs/baseline/zero_shot_cot_4o/output_conversations_higher_order_stable_4o_{4}/final_results.csv')
df5 = pd.read_csv(f'./outputs/baseline/zero_shot_cot_4o/output_conversations_higher_order_stable_4o_{5}/final_results.csv')


dfs = [df1, df2, df3, df4, df5]
result = count_fast_success(dfs)
print(f"AgSR is {result*100}")
# print(np.average(Result))


exit()
### Iteration Ablation

def count_fast_success(df, i):
    # Filter the rows where fast_is_succ is True and fast_conversation_rounds <= i
    count = df[(df['fast_is_succ'] == True) & (df['fast_conversation_rounds'] <= i)].shape[0]
    return count

Result = []
rounds = [1,2,4,6,8,10]
trials = [1,2,3,4,5]
# print(f"Trial {trial}")
df1 = pd.read_csv(f'/home/xingang/xingang/ControlAgent/outputs/main_result/second_order_4o/output_conversations_second_order_controlagent_{1}/final_results{1}.csv')
df2 = pd.read_csv(f'/home/xingang/xingang/ControlAgent/outputs/main_result/second_order_4o/output_conversations_second_order_controlagent_{2}/final_results{2}.csv')
df3 = pd.read_csv(f'/home/xingang/xingang/ControlAgent/outputs/main_result/second_order_4o/output_conversations_second_order_controlagent_{3}/final_results{3}.csv')
df4 = pd.read_csv(f'/home/xingang/xingang/ControlAgent/outputs/main_result/second_order_4o/output_conversations_second_order_controlagent_{4}/final_results{4}.csv')
df5 = pd.read_csv(f'/home/xingang/xingang/ControlAgent/outputs/main_result/second_order_4o/output_conversations_second_order_controlagent_{5}/final_results{5}.csv')


dfs = [df1, df2, df3, df4, df5]

for i in rounds:
    Succ = []
    for trial in trials:
        df = pd.read_csv(f'/home/xingang/xingang/ControlAgent/outputs/main_result/second_order_4o/output_conversations_second_order_controlagent_{trial}/final_results{trial}.csv')
        succ = count_fast_success(df, i)
        Succ.append(succ)
    print(f"The average succ rate less than round {i} is {np.mean(Succ)*2}.")


# result = count_fast_success(df, i)
# print(f"AgSR is {result}")
# # print(np.average(Result))
