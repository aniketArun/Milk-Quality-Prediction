import tkinter as tk
from tkinter import PhotoImage
import pandas as pd
from tkinter import ttk
from datetime import datetime
from demoModule1 import *
from view import *
# function to get farmer name from CSV
def get_farmer_name(id):
    df = pd.read_csv('farmers.csv')
    row = df.loc[df['id'] == id]
    farmer_name = row.iloc[0]['name']
    return farmer_name
    
# function to update the display
def update_table():
    df = pd.read_csv('milk_collection.csv')
    for index, row in df.iterrows():
        farmer_id = row['ID']
        farmer_name = get_farmer_name(farmer_id)
        fat = row['Fat']
        weight = row['Weight']
        rate = row['Rate']
        amount = row['Amount']
        tree.insert("", tk.END, values=(farmer_id, farmer_name, fat, weight, rate, amount))


def showId():
    update_table()
    global farmer_name
    farmer_id = int(id_entry.get())
    farmer_name = get_farmer_name(farmer_id)
    name_entry.config(text=farmer_name)
    if(id_entry.get() and fat_entry.get() and weight_entry.get()):                     
        root.destroy()
        calculate_rate()
        showFile()     
    else:  
        showFile()
        

# function to calculate the rate and amount
def calculate_rate():
    global fat,weight,rate,amount,farmer_id
    fat = float(fat_entry.get())
    weight = float(weight_entry.get())

    rates_df = pd.read_csv('rate.csv')
    # calculate amount based on fat content
    rate = rates_df.loc[rates_df['fat'] == fat]['rate'].iloc[0]

    amount = rate * weight
    farmer_id = int(id_entry.get())
    farmer_name = get_farmer_name(farmer_id)
    
    data = {'ID': farmer_id, 'Name': farmer_name, 'Fat': fat, 'Weight': weight, 'Rate': rate, 'Amount': amount}
    df = pd.DataFrame(data, index=[0])
    df.to_csv('milk_collection.csv', mode='a', header=False, index=False)
    tree.delete(*tree.get_children())
    update_table()
    add_data()
    id_entry.delete(0,'end')
    fat_entry.delete(0,'end')
    weight_entry.delete(0,'end')

def add_data():
    # get current date and time
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    
    # write data to file
    with open(farmer_name+'.csv', 'a') as f: 
        f.write(f'{dt_string},{fat},{weight},{rate},{amount}\n')

    #show message on succeeds
    messagebox.showinfo(title="Milker-write bill",message="Bill written !")

main()
# create tkinter window
window = tk.Tk()
menubar = tk.Menu(window)

#adding icon to Window
p1 = tk.PhotoImage(file = 'cow.png') 
# Setting icon of master window
window.iconphoto(False, p1) 
# Adding File Menu and commands
file = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='File', menu = file)
file.add_command(label ='Edit Rates', command = editRate)
file.add_command(label ='Open...', command = None)
file.add_command(label ='Save', command = None)
file.add_separator()
file.add_command(label ='Exit', command = window.destroy)

Function = tk.Menu(menubar, tearoff = 0)
# icon = PhotoImage(file='farmer.png')
menubar.add_cascade(label ='Farmer', menu = Function)
Function.add_command(label ='Add Farmer', command = add_farmer_window)
Function.add_command(label ='Edit Farmer', command = editFarmer)
Function.add_command(label ='Delete Farmer', command = delete_Farmer)
Function.add_command(label ='Remove Duplicates', command = removeDuplicte)
Function.add_separator()
Function.add_command(label ='Analytics...', command = analyt)
Function.add_command(label ='Find again', command = None)

help_ = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='Help', menu = help_)
help_.add_command(label ='Tk Help', command = None)
help_.add_command(label ='Demo', command = None)
help_.add_separator()
help_.add_command(label ='About Tk', command = None)
  
window.config(menu = menubar)

# create frames
input_frame = tk.Frame(window)
output_frame = tk.Frame(window)

# create labels and entry fields
id_label = tk.Label(input_frame, text="Enter Farmer ID:")
id_entry = tk.Entry(input_frame)
name_label = tk.Label(input_frame,text='Name:')
name_entry = tk.Label(input_frame,text='',padx=60)
fat_label = tk.Label(input_frame, text="Enter Fat %:")
fat_entry = tk.Entry(input_frame)
weight_label = tk.Label(input_frame, text="Enter Weight:")
weight_entry = tk.Entry(input_frame)

# bind enter key to calculate_rate function
window.bind('<Return>', lambda event=None: showId())

# create treeview for displaying data
tree = tk.ttk.Treeview(output_frame, columns=("ID", "Name", "Fat", "Weight", "Rate", "Amount"), show='headings')
tree.heading("#1", text="ID",anchor='center')
tree.heading("#2", text="Name",anchor='center')
tree.heading("#3", text="Fat",anchor='center')
tree.heading("#4", text="Weight",anchor='center')
tree.heading("#5", text="Rate",anchor='center')
tree.heading("#6", text="Amount",anchor='center')

#adjust the size of table/tree
tree.column('ID',width=50)

# create scrollbar for treeview
scrollbar = tk.Scrollbar(output_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

# pack widgets
id_label.pack(side=tk.LEFT)
id_entry.pack(side=tk.LEFT)
name_label.pack(side=tk.LEFT)
name_entry.pack(side=tk.LEFT)
fat_label.pack(side=tk.LEFT)
fat_entry.pack(side=tk.LEFT)
weight_label.pack(side=tk.LEFT)
weight_entry.pack(side=tk.LEFT)
input_frame.pack(padx=10, pady=10)
tree.pack(side=tk.LEFT)
scrollbar.pack(side=tk.RIGHT, fill="y")
output_frame.pack(padx=1, pady=10)


def showFile():
    global root
    root = tk.Tk()
    root.title(farmer_name+'-Collection File')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Define the size of the window
    window_height = 200
    # Calculate the position of the window
    y_pos = screen_height - window_height-100
    # Set the position of the window
    root.geometry('{}x{}+{}+{}'.format(screen_width, window_height, 0, y_pos))
    # create a Treeview widget
    tree = ttk.Treeview(root)
    tree.pack(side='bottom')
    # add columns to the Treeview widget
    tree['columns'] = ('date', 'fat', 'weight', 'rate', 'amount')
    tree.heading('date', text='Date',anchor='center')
    tree.heading('fat', text='Fat',anchor='center')
    tree.heading('weight', text='Weight',anchor='center')
    tree.heading('rate', text='Rate',anchor='center')
    tree.heading('amount', text='Amount',anchor='center')
    tree.column('fat',width=30)
    try:
        with open(farmer_name+'.csv', 'r') as f:
            reader = csv.DictReader(f)        
            # loop through the rows in the file and insert them into the Treeview widget
            for row in reader:
                
                tree.insert('', 'end', values=(row['date'], row['fat'], row['weight'], row['rate'], row['amount']))
        # open the name.csv file and read its contents
    except FileNotFoundError:
        with open(farmer_name+'.csv','w') as f:
            f.write('date,fat,weight,rate,amount')
    root.mainloop()
    
# start tkinter event loop
window.mainloop()
