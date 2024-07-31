import pandas as pd
import matplotlib.pyplot as plt


file_name = 'roung1_stats.csv'
df = pd.read_csv(file_name)
print(df)




# Plotting
fig, axs = plt.subplots(3, 1, figsize=(10, 15))  # 3 plots in one column

# Request Count plot
axs[0].bar(df['Name'], df['Request Count'], color='blue')
axs[0].set_title('Request Count by Name')
axs[0].set_xlabel('Name')
axs[0].set_ylabel('Request Count')

# Failure Count plot
axs[1].bar(df['Name'], df['Failure Count'], color='red')
axs[1].set_title('Failure Count by Name')
axs[1].set_xlabel('Name')
axs[1].set_ylabel('Failure Count')

# Average Response Time plot
axs[2].bar(df['Name'], df['Average Response Time'], color='green')
axs[2].set_title('Average Response Time by Name')
axs[2].set_xlabel('Name')
axs[2].set_ylabel('Average Response Time (ms)')

plt.tight_layout()
plt.show()

