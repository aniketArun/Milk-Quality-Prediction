import tkinter as tk
from tkinter import ttk
import time
import pandas as pd
from tkinter import messagebox
import csv

def main():
    root = tk.Tk()
    root.title("Preparing...")
    root.geometry("400x350")
    # Setting icon of master window
    image = tk.PhotoImage(file="cow.png")
    root.iconphoto(False, image)
    label = tk.Label(root, image=image)
    label.pack()
    # Create progress bar widget
    progress = ttk.Progressbar(root, orient=tk.HORIZONTAL,
                               length=250, mode='indeterminate')
    progress.pack(pady=10)

    # Start progress bar
    progress.start(10)

    # Destroy window after 5 seconds
    root.after(5000, root.destroy)

    root.mainloop()

def add_farmer():
    id_val = int(idEntry.get())
    name_val = nameEntry.get()
    
    df = pd.read_csv("farmers.csv")
    if id_val in df['id'].values:
        messagebox.showerror("Error", "ID already exists")
    else:
        df.loc[len(df)] = [id_val, name_val]
        df.to_csv("farmers.csv", index=False)
        messagebox.showinfo("Success", "Farmer added successfully")
    idEntry.delete(0,'end')
    nameEntry.delete(0,'end')

def add_farmer_window():
    add_farmer_window = tk.Tk()
    # setting icon
    # p1 = tk.PhotoImage(file = 'add.png') 
    # add_farmer_window.iconphoto(False, p1)
    
    add_farmer_window.title("Add Farmer")
    add_farmer_window.geometry("300x200")
    add_farmer_window.resizable(False, False)
       
    idLabel = tk.Label(add_farmer_window, text="ID: ")
    idLabel.pack(pady=5)
    global idEntry
    idEntry = tk.Entry(add_farmer_window)
    idEntry.pack(pady=5)
    global nameEntry
    nameLabel = tk.Label(add_farmer_window, text="Name: ")
    nameLabel.pack(pady=5)
    nameEntry = tk.Entry(add_farmer_window)
    nameEntry.pack(pady=5)

    addBtn = tk.Button(add_farmer_window, text="Add Farmer", command=add_farmer)
    addBtn.pack(pady=10)
    add_farmer_window.mainloop()

def delete_Farmer():   
    # create main window
    root = tk.Tk()
    root.geometry('350x250')
    root.resizable(width=False, height=False)
    # p1 = tk.PhotoImage(file = 'cow.png') 
    # Setting icon of master window
    # root.iconphoto(False, p1)
    # photoFile = tk.PhotoImage('delete.jfif')
    # read the farmer.csv file into a pandas dataframe
    global farmer_data
    farmer_data = pd.read_csv('farmers.csv')

    # create GUI elements
    titleLabel = tk.Label(root, text='Delete Farmer', font=('Arial', 24))
    titleLabel.pack(pady=10)

    idLabel = tk.Label(root, text='Enter Farmer ID:', font=('Arial', 14))
    idLabel.pack(pady=5)
    global idEntry
    idEntry = tk.Entry(root, font=('Arial', 14))
    idEntry.pack(pady=5)

    deleteButton = tk.Button(root, text='Delete', font=('Arial', 14), command=delete_farmer)
    deleteButton.pack(pady=10)
    global resultLabel
    resultLabel = tk.Label(root, text='', font=('Arial', 14))
    resultLabel.pack(pady=5)
    
    root.mainloop()

# define function to delete a farmer from the farmer.csv file
def delete_farmer():
    id_val = int(idEntry.get())
    farmer_data.drop(farmer_data[farmer_data['id'] == id_val].index, inplace=True)
    farmer_data.to_csv('farmers.csv', index=False)
    resultLabel.config(text=f"Farmer with ID {id_val} has been deleted.")



def update_farmer():
    farmer_id = int(id_entry.get())
    farmer_name = name_entry.get()

    with open('farmers.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    with open('farmers.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for farmer in rows:
            if farmer[0] == 'id':  # skip the header row
                writer.writerow(farmer)
                continue
            if int(farmer[0]) == farmer_id:
                farmer[1] = farmer_name
            writer.writerow(farmer)
    id_entry.delete(0,'end')
    name_entry.delete(0,'end')
    messagebox.showinfo(title="Milker-Edit Farmer",message = f"Farmer with ID {farmer_id} updated successfully!")

def editFarmer():
    # Create the main window and a frame inside it
    window = tk.Tk()
    window.geometry('400x200')
    frame = tk.Frame(window)
    frame.pack(pady=20)

    # p1 = tk.PhotoImage(file = 'cow.png') 
    # # Setting icon of master window
    # window.iconphoto(False, p1)
    # file_photo = tk.PhotoImage(file='edit.png')

    global id_entry,name_entry
    # Add labels and entry widgets to the frame
    id_label = tk.Label(frame, text='Enter farmer ID:')
    id_label.grid(row=0, column=0, padx=10, pady=10)
    id_entry = tk.Entry(frame)
    id_entry.grid(row=0, column=1, padx=10, pady=10)

    name_label = tk.Label(frame, text='Enter new name:')
    name_label.grid(row=1, column=0, padx=10, pady=10)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=1, column=1, padx=10, pady=10)

    button = tk.Button(frame, text='Update', command=update_farmer)
    button.grid(row=2, column=1, padx=10, pady=10)

    result_label = tk.Label(window, text='')
    result_label.pack()

    window.mainloop()

def removeDuplicte():
    # Load csv file into a dataframe
    df = pd.read_csv('milk_collection.csv')

    # Remove duplicates based on the "ID" column
    df.drop_duplicates(subset=['ID'], keep='first', inplace=True)

    # Save cleaned dataframe back to the csv file
    df.to_csv('filename_cleaned.csv', index=False)
    import os
    os.remove('milk_collection.csv')
    os.rename('filename_cleaned.csv','milk_collection.csv')
    messagebox.showinfo(message='File Edited !')

def update_rate():
    fat = float(fat_entryU.get())
    rate = float(rate_EntryU.get())

    with open('rate.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    with open('rate.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for values in rows:
            if values[0] == 'fat':  # skip the header row
                writer.writerow(values)
                continue
            if float(values[0]) == fat:
                values[1] = rate
            writer.writerow(values)
    fat_entryU.delete(0,'end')
    rate_EntryU.delete(0,'end')
    messagebox.showinfo(title="Milker-Edit rate",message = f"rate with  {fat} updated successfully!")

def editRate():
    # Create the main window and a frame inside it
    window = tk.Tk()
    window.geometry('400x200')
    window.title("Edit Rate")
    frame = tk.Frame(window)
    frame.pack(pady=20)

    # p1 = tk.PhotoImage(file = 'cow.png') 
    # # Setting icon of master window
    # window.iconphoto(False, p1)
    # file_photo = tk.PhotoImage(file='edit.png')
    global fat_entryU
    global rate_EntryU
    # Add labels and entry widgets to the frame
    fat_label = tk.Label(frame, text='Enter FAt:')
    fat_label.grid(row=0, column=0, padx=10, pady=10)
    fat_entryU = tk.Entry(frame)
    fat_entryU.grid(row=0, column=1, padx=10, pady=10)

    rate_label = tk.Label(frame, text='Enter new Rate:')
    rate_label.grid(row=1, column=0, padx=10, pady=10)
    rate_EntryU = tk.Entry(frame)
    rate_EntryU.grid(row=1, column=1, padx=10, pady=10)

    button = tk.Button(frame, text='Update', command=update_rate)
    button.grid(row=2, column=1, padx=10, pady=10)

    result_label = tk.Label(window, text='')
    result_label.pack()

    window.mainloop()






