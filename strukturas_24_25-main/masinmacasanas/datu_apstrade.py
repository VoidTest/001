import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

# Set Seaborn style and Matplotlib figure size
sb.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (15, 10)

def plot_graph_and_heatmap(filepath):
    # Load the dataset
    datu_fails = pd.read_csv(filepath)
    
    # Extract numeric columns, excluding 'Year'
    if 'Year' in datu_fails.columns:
        numeric_data = datu_fails.select_dtypes('number').drop(columns=['Year'], errors='ignore')
    else:
        numeric_data = datu_fails.select_dtypes('number')
    
    # Plot heatmap
    if not numeric_data.empty:
        plt.figure(figsize=(12, 8))
        sb.heatmap(numeric_data.corr(), annot=True, cmap='magma')
        plt.title("Correlation Heatmap (Excluding 'Year')")
        plt.show()
    else:
        print("No numeric data for heatmap.")
    
    # Plot graph for 'Value' column
    if 'Value' in datu_fails.columns:
        try:
            # Ensure the 'Value' column is numeric
            datu_fails['Value'] = pd.to_numeric(datu_fails['Value'], errors='coerce')
            
            # Drop rows with missing or non-numeric values
            datu_fails = datu_fails.dropna(subset=['Value'])
            
            # Plot all values as a line plot
            plt.figure(figsize=(20, 8))
            plt.plot(datu_fails['Value'], marker='o', linestyle='-', alpha=0.7)
            plt.title("Line Chart of All Values")
            plt.xlabel("Index")
            plt.ylabel("Value")
            plt.grid()
            plt.show()
        except Exception as e:
            print(f"Error plotting data: {e}")
    else:
        print("No 'Value' column found to plot.")

# Use the provided file for analysis
plot_graph_and_heatmap('strukturas_24_25-main/masinmacasanas/annual-enterprise-survey-2023-financial-year-provisional.csv')
