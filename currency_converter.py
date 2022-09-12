# Azure ttk theme from https://github.com/rdbende/Azure-ttk-theme


import socket
from forex_python.converter import CurrencyRates
from forex_python.converter import CurrencyCodes
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from pip._vendor import requests
import datetime as dt
import json;
import tkinter.scrolledtext as st


##############################
#
#   class CurrencyConverter
#   
#   API & CALL MICROSERVICE
#
###############################
# 
class CurrencyConverter:

    def __init__(self, url):
        url = 'https://api.exchangerate.host/latest'
        response = requests.get(url)
        data = response.json()
        self.rates = data.get('rates')
        
     
    def reqMicroService(message):
        Host = 'localhost'
        Port = 1234

        s = socket.socket()                  
        name = "Currency Converter App"
        s.connect((Host, Port))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        
        s_name = s.recv(1024)                
        s_name = s_name.decode()             
        s.send(name.encode()) 
        

        s.send(message.encode())

        message = s.recv(1024)          
        message = message.decode()

        s.close()
        return message


######################
## End of Class CurrencyConverter
##




##############################
#
#
#   INITIALIZE GUI/ROOT
#   GLOBAL VARIABLES
#
###############################

root = Tk()
converter = CurrencyConverter('https://api.exchangerate.host/latest')
c = CurrencyCodes()
root.tk.call('lappend', 'auto_path', '/awthemes-10.4.0/pkgIndex')
root.title('Currency Converter')
root.geometry('1000x750')
content = ttk.Frame(root, padding=(10,10,12,12))
title_label = Label(content, text="Currency Converter", font=('franklin gothic medium', 20), anchor= 'center')


currency_names = ['USD', 'EUR', 'GBP', 'CAD', 'JPY', 'MXN', 'CHF', 'AMD', 'AUD', 'BRL']

rates = converter.rates

user_amount = StringVar()
theme_mode_check = StringVar()
currency_variable1 = StringVar()
currency_variable2 = StringVar()
currency_variable1.set('Select Currency')
currency_variable2.set('Select Currency')
theme_mode_check.set('Swtich to dark mode')


root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "light")



##############################
#
#
#   FUNCTIONS
#
#
###############################

def changeCurrInfo(event, which_text_area):
    currency_variable = StringVar()
    currency_variable = event.widget
    currInfo = CurrencyConverter.reqMicroService(currency_variable.get())
    
    place_text = which_text_area
    
    if place_text == 1 :
        text_area.delete('1.0', float(len(currInfo)))
        text_area.insert(tk.INSERT, str(currInfo))
        
    else:
        text_area2.delete('1.0', float(len(currInfo)))
        text_area2.insert(tk.INSERT, str(currInfo))
        
        
        
        
def convert(amount, base_currency, des_currency):
        
    if base_currency != 'AED':
        amount = amount/rates[base_currency]

    # Limiting the result to 2 decimal places
    amount = round(amount*rates[des_currency], 2)
    # Add comma every 3 numbers
    amount = '{:,}'.format(amount)
    return amount
    
        
        
def processed(*args):
    try:
        given_amount = float(amount_entry.get())
        given_base_currency = currency_variable1.get()
        given_des_currency = currency_variable2.get()
        converted_amount = convert(given_amount, given_base_currency, given_des_currency)
        # Add comma every 3 numbers
        given_amount = '{:,}'.format(given_amount)

        final_result.config(text=f'{given_amount} {given_base_currency} = {converted_amount} {given_des_currency}')

    # Create warning message box
    except ValueError:
        convert_error = messagebox.showwarning('WARNING!', 'Please only enter integers in the Input Amount field')
        return convert_error

    
def clear():
    clear_entry = amount_entry.delete(0, END)
    clear_result = final_result.config(text='')
    currency_variable1.set('Select Currency')
    currency_variable2.set('Select Currency')
    clear_curr_info1 = text_area.delete('1.0', END)
    clear_curr_info2 = text_area2.delete('1.0', END)
    return clear_entry, clear_result, 


def switch():
    
    given_base_currency = currency_variable1.get()
    given_des_currency = currency_variable2.get()

    currency_variable1.set(given_des_currency)
    currency_variable2.set(given_base_currency)
    
    currInfo = CurrencyConverter.reqMicroService(currency_variable1.get())
    text_area.delete('1.0', float(len(currInfo)))
    text_area.insert(tk.INSERT, str(currInfo))

    currInfo2 = CurrencyConverter.reqMicroService(currency_variable2.get())
    text_area2.delete('1.0', float(len(currInfo2)))
    text_area2.insert(tk.INSERT, str(currInfo2))


def printData():
    print_warning = messagebox.askokcancel(title = 'Requires PDF reader', message= 'Okay to print?')
    return print_warning


def change_theme():
    # NOTE: The theme's real name is azure-<mode>
    if root.tk.call("ttk::style", "theme", "use") == "azure-dark":
        # Set light theme
        root.tk.call("set_theme", "light")
        theme_mode_check.set('Swtich to dark mode')
    else:
        # Set dark theme
        root.tk.call("set_theme", "dark")
        theme_mode_check.set('Swtich to light mode')


##############################
#
#
#   LAYOUT
#
#
###############################

amount_label = Label(content, text='Enter the amount to convert here: ', font=('franklin gothic book', 15), anchor='center')


amount_entry = Entry(content, relief= SUNKEN, bd = 3, textvariable= user_amount)
amount_entry.config(width=25)
amount_entry.focus()

base_currency_label = Label(content, text='From: ', font=('franklin gothic book', 15))

destination_currency_label = Label(content, text='To: ', font=('franklin gothic book', 15))

switch_button = Button(content, text='Switch', command=switch)


currency_combobox1 = ttk.Combobox(content, width=20, values = currency_names, textvariable=currency_variable1, state='readonly', justify='center')
currency_combobox1.bind('<<ComboboxSelected>>', lambda event: changeCurrInfo(event, 1))

currency_combobox2 = ttk.Combobox(content, width=20, values = currency_names, textvariable=currency_variable2, state='readonly', justify='center')
currency_combobox2.bind('<<ComboboxSelected>>', lambda event: changeCurrInfo(event, 2))


clear_button = Button(content, text='Reset to Default', width=15, command=clear)
convert_button = Button(content, text='Convert', command=processed)

final_result = Label(content, font=('calibri', 16), relief='sunken', width=25, height =2)

text_area = st.ScrolledText(content, width = 25, height = 8, font = ("Times New Roman",12))
text_area2 = st.ScrolledText(content, width = 25, height = 8, font = ("Times New Roman",12))

print_button = Button(content, text='Print',  command=printData)
print_label = Label(content, text='*Requires PDF Reader', font=('calibri', 8))

mode_change_button = Button(content, text= 'Swtich to dark mode', textvariable = theme_mode_check , command=change_theme)



##############################
#
#
#   GRID
#
#
###############################


root.bind("<Return>", processed)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

content.grid(column=0, row=0,  sticky=(N, S, E, W))
title_label.grid(column=2, row=0, sticky=(N), padx=5)

amount_label.grid(column=2, row=1, padx=5)
amount_entry.grid(column=2, row=2, padx=5)

base_currency_label.grid(column=1, row=3, sticky=(N, S, E, W))
destination_currency_label.grid(column=3, row=3, sticky=(N, S, E, W))

currency_combobox1.grid(column=1, row=4,  pady=5, padx=5)
currency_combobox2.grid(column=3, row=4, sticky=(W),  pady=5, padx=20)

switch_button.grid(column=2, row=4,)
convert_button.grid(column=2, row=5, pady=5, padx=5,)
clear_button.grid(column=2, row=5, pady=5, padx=1, sticky=(E))

final_result.grid(column=2, row=6, padx=5)

text_area.grid(column=1, row=7, pady=10, padx=10)
text_area2.grid(column=3, row=7, pady=5, padx=5)

print_button.grid(column=3, row=8)
print_label.grid(column=3, row=9, sticky=(N,E))

mode_change_button.grid(column=2, row=9)





root.mainloop()