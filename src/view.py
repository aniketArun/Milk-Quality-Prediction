import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import csv
from tkinter import filedialog
from plot import *

File = None

def display_csv_in_treeview(csv_frame):
    # Create a Treeview widget
    tree = ttk.Treeview(csv_frame)
    tree["show"] = "headings"  # Show only the headings
    
    # Function to load CSV file
    def load_csv():
        # Prompt the user to select a CSV file
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        global File
        File = file_path
        # Read the CSV file and populate the Treeview widget
        with open(file_path, "r") as csvfile:
            reader = csv.reader(csvfile)
            
            # Get the column names from the first row of the CSV file
            column_names = next(reader)
            tree["columns"] = column_names
            
            # Set the column headings
            for col in column_names:
                tree.heading(col, text=col)
            
            # Insert data from the CSV file into the Treeview
            for row in reader:
                tree.insert("", "end", values=row)
    
    # Create a button to load the CSV file
    load_button = tk.Button(csv_frame, text="Load CSV", command=load_csv)
    load_button.pack(pady=10)
    
    # Pack the Treeview widget to the main window
    tree.pack(fill=tk.BOTH, expand=True)

def analyt():
    # Sample dataset
    data = {
        'pH': [6.7, 6.8, 6.9, 6.7, 6.8, 6.9, 6.7, 6.8, 6.9, 6.7],
        'Temperature': [4, 5, 6, 4, 5, 6, 4, 5, 6, 4],
        'Fat_Content': [3.5, 3.4, 3.6, 3.3, 3.2, 3.7, 3.1, 3.5, 3.6, 3.4],
        'Turbidity': [10, 12, 11, 9, 13, 11, 10, 12, 9, 11],
        'Grade': ['A', 'B', 'A', 'B', 'A', 'C', 'B', 'A', 'C', 'A']
    }

    df = pd.DataFrame(data)

    def create_scatter_plot():
        fig = plt.Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.scatter(df['pH'], df['Fat_Content'])
        ax.set_xlabel('pH')
        ax.set_ylabel('Fat Content')
        ax.set_title('pH vs Fat Content')
        canvas = FigureCanvasTkAgg(fig, master=scatter_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def create_box_plot():
        fig = plt.Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.boxplot([df['Turbidity'], df['Temperature']])
        ax.set_xticklabels(['Turbidity', 'Temperature'])
        ax.set_ylabel('Values')
        ax.set_title('Box Plot: Turbidity vs Temperature')
        canvas = FigureCanvasTkAgg(fig, master=boxplot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def create_linear_regression_plot():
        X = df[['pH']]
        y = df['Fat_Content']
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)

        fig = plt.Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.scatter(df['pH'], df['Fat_Content'], label='Actual Data')
        ax.plot(df['pH'], y_pred, color='red', label='Linear Regression')
        ax.set_xlabel('pH')
        ax.set_ylabel('Fat Content')
        ax.set_title('pH vs Fat Content (Linear Regression)')
        ax.legend()
        canvas = FigureCanvasTkAgg(fig, master=linear_regression_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    # Create main window
    root = tk.Tk()
    root.title("Data Visualization")

    # Create tabs
    tab_control = ttk.Notebook(root)
    scatter_frame = ttk.Frame(tab_control)
    boxplot_frame = ttk.Frame(tab_control)
    csv_frame = ttk.Frame(tab_control)
    linear_regression_frame = ttk.Frame(tab_control)
    rforest_frame = ttk.Frame(tab_control)
    tab_control.add(csv_frame, text='Dataset')
    tab_control.add(scatter_frame, text='Scatter Plot')
    tab_control.add(boxplot_frame, text='Box Plot')
    tab_control.add(linear_regression_frame, text='Linear Regression')
    tab_control.add(rforest_frame, text='Random Forest Prediction')
    tab_control.pack(expand=1, fill="both")
    
    csv_button = ttk.Button(csv_frame, text='Choose File', command= lambda: display_csv_in_treeview(csv_frame))
    csv_button.pack(pady=10)
    # Create buttons
    scatter_button = ttk.Button(scatter_frame, text='Create Scatter Plot', command=create_scatter_plot)
    scatter_button.pack(pady=10)

    boxplot_button = ttk.Button(boxplot_frame, text='Create Box Plot', command=create_box_plot)
    boxplot_button.pack(pady=10)

    linear_regression_button = ttk.Button(linear_regression_frame, text='Create Linear Regression Plot', command=create_linear_regression_plot)
    linear_regression_button.pack(pady=10)

    rforest_button = ttk.Button(rforest_frame, text='Predict the Values', command=lambda : rForestClassfication(rforest_frame,File))
    rforest_button.pack(pady=10)

    root.mainloop()
