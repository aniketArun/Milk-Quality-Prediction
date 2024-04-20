import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style
# %matplotlib inline
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from tkinter import messagebox

def rForestClassfication(f_name, file_path):
    """Load the dataset"""

    df = pd.read_csv(file_path)

    data_cp = df.copy()

    # Rename columns
    data_cp = data_cp.rename(columns={'Temprature':'Temperature'})

    # Remove any empty spaces in header col
    data_cp.columns = data_cp.columns.str.replace(' ', '')

    """<h1>Train & Evaluate the Model</h1>
    Metrics such as accuracy, precision, and recall can be used measure the performance of the model.
    """

    # Split the dataset into features(to use to predict) and target variable(to predict)
    X = data_cp.drop(['Grade'], axis=1)
    y = data_cp['Grade']



    # Scale numerical variables
    scaler = StandardScaler()

    # Transform col-values to have zero mean and variance
    X[['pH', 'Temperature', 'Fat', 'Turbidity']] = scaler.fit_transform(X[['pH', 'Temperature', 'Fat', 'Turbidity']])

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Perform random classifier classification
    rf = RandomForestClassifier(random_state=42)
    rf.fit(X_train, y_train)

    y_pred_rf = rf.predict(X_test)
    accuracy_rf = accuracy_score(y_test, y_pred_rf)
    messagebox.showinfo(title='Gomata Milk Man', message="Accuracy of Random Forest classifier: {:.2f}%".format(accuracy_rf * 100))
    plot_predicted_values_in_tkinter_frame(y_test,y_pred_rf, f_name)
    # print("Accuracy of Random Forest classifier: {:.2f}%".format(accuracy_rf * 100))
    # print('------------------------------------------------------------------')
    # print(classification_report(y_test, y_pred_rf))





def plot_predicted_values_in_tkinter_frame(y_test, y_pred_rf, frame_):
    
    # Create a frame to hold the plots
    frame = ttk.Frame(frame_)
    frame.pack(fill=tk.BOTH, expand=True)

    # Create a figure to hold the plots
    fig = Figure(figsize=(14, 6))

    # Create two subplots in the figure
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    # Plot the confusion matrix in the first subplot
    cm = confusion_matrix(y_test, y_pred_rf)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=['Predicted Negative', 'Predicted Positive'],
                yticklabels=['Actual Negative', 'Actual Positive'],
                ax=ax1)
    ax1.set_title('Confusion Matrix')
    ax1.set_xlabel('Predicted')
    ax1.set_ylabel('Actual')

    # Plot the distribution of predicted and actual values in the second subplot
    labels, counts_pred = np.unique(y_pred_rf, return_counts=True)
    ax2.bar(labels, counts_pred, alpha=0.6, label='Predicted', color='blue')
    
    labels, counts_actual = np.unique(y_test, return_counts=True)
    ax2.bar(labels, counts_actual, alpha=0.6, label='Actual', color='orange')
    
    ax2.set_title('Distribution of Predicted and Actual Values')
    ax2.set_xlabel('Class')
    ax2.set_ylabel('Count')
    ax2.legend()
    
    # Create a FigureCanvasTkAgg to embed the Matplotlib figure in the Tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
