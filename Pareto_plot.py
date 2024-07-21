import pandas as pd
import matplotlib.pyplot as plt
import ast

def plot_results_from_csv(csv_filename1, csv_filename2):
    df = pd.read_csv(csv_filename1)
    
    df['Objective'] = df['Objective'].apply(ast.literal_eval)
    df[['Objective 1', 'Objective 2']] = pd.DataFrame(df['Objective'].tolist(), index=df.index)
    f1_values = df['Objective 1'].values
    f2_values = df['Objective 2'].values
    
    df2 = pd.read_csv(csv_filename2)
    f1_pareto = df2['Objective 1'].values
    f2_pareto = df2['Objective 2'].values

    plt.figure(figsize=(10, 6))
    plt.plot(f1_values, f2_values, 'bo')
    plt.plot(f1_pareto, f2_pareto, 'ro', label='Pareto front')
    plt.title('NSGA-II Results: Objective Space')
    plt.xlabel('Objective 1 (f1)')
    plt.ylabel('Objective 2 (f2)')
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.show()

csv_filename1 = 'try.csv'
csv_filename2 = 'try_Pareto.csv'
plot_results_from_csv(csv_filename1, csv_filename2)