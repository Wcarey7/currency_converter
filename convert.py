from forex_python.converter import CurrencyRates
from forex_python.converter import CurrencyCodes
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from pip._vendor import requests
import datetime as dt


class CurrencyConverter:

    def __init__(self, url):
        self.url = 'https://api.exchangerate.host/latest'
        self.response = requests.get(url)
        self.data = self.response.json()
        self.rates = self.data.get('rates')

    def convert(self, amount, base_currency, des_currency):
        if base_currency != 'AED':
            amount = amount/self.rates[base_currency]

        # Limiting the result to 2 decimal places
        amount = round(amount*self.rates[des_currency], 2)
        # Add comma every 3 numbers
        amount = '{:,}'.format(amount)
        return amount

# Main window
class Main(tk.Tk):

    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title('Currency Converter')
        self.geometry('1000x1000')
        self.config(bg='#cad3df')
        self.CurrencyConverter = converter
        c = CurrencyCodes()

        # Create title label
        self.title_label = Label(self, text='Currency Converter', bg='#e9edf2', fg='black', font=('franklin gothic medium', 20), )
        self.title_label.place(x=300, y=35, anchor='center')

        # Create amount label
        self.amount_label = Label(self, text='Enter the amount to convert here: ', bg='#e9edf2', fg='black', font=('franklin gothic book', 15))
        self.amount_label.place(x=300, y=80, anchor='center')

        # Create amount entry box
        self.amount_entry = Entry(self)
        self.amount_entry.config(width=25)
        self.amount_entry.place(x=300, y=110, anchor='center')

        # Create 'from' label
        self.base_currency_label = Label(self, text='From: ', bg='#e9edf2', fg='black', font=('franklin gothic book', 15))
        self.base_currency_label.place(x=200, y=140, anchor='center')

        # Create 'to' label
        self.destination_currency_label = Label(self, text='To: ', bg='#e9edf2', fg='black', font=('franklin gothic book', 15))
        self.destination_currency_label.place(x=400, y=140, anchor='center')

        # Create dropdown menus
        self.currency_variable1 = StringVar(self)
        self.currency_variable2 = StringVar(self)
        self.currency_variable1.set(c.get_currency_name('USD'))
        self.currency_variable2.set(c.get_currency_name('EUR'))

        self.currency_combobox1 = ttk.Combobox(self, width=20, textvariable=self.currency_variable1, values=list(self.CurrencyConverter.rates.keys()), state='readonly')
        self.currency_combobox1.place(x=200, y=170, anchor='center')

        self.currency_combobox2 = ttk.Combobox(self, width=20, textvariable=self.currency_variable2, values=list(self.CurrencyConverter.rates.keys()), state='readonly')
        self.currency_combobox2.place(x=400, y=170, anchor='center')

        # Create 'convert' button
        self.convert_button = Button(self, text='Convert', bg='#52595D', fg='white', command=self.processed)
        self.convert_button.place(x=275, y=270, anchor='center')

        # Create 'clear' button
        self.clear_button = Button(self, text='Clear', bg='red', fg='white', command=self.clear)
        self.clear_button.place(x=325, y=270, anchor='center')
        
        # Create 'invert' button
        self.clear_button = Button(self, text='Switch', bg='#52595D', fg='white', command=self.invert)
        self.clear_button.place(x=300, y=170, anchor='center')

        # Create converted result field
        self.final_result = Label(self, text='RESULTS HERE', bg='#52595D', fg='white', font=('calibri', 12), relief='sunken', width=40)
        self.final_result.place(x=300, y=310, anchor='center')
        
        # Historical Graph Placeholder
        self.title_label = Label(self, text='Historical Graph Placeholder', bg='#e9edf2', fg='black', font=('franklin gothic medium', 20), height=5)
        self.title_label.place(x=300, y=425, anchor='center')
        
        # Currency Info1
        self.title_label = Label(self, text='Currency Info 1', bg='#e9edf2', fg='black', font=('franklin gothic medium', 15))
        self.title_label.place(x=200, y=550, anchor='center')
        
        # Currency Info2
        self.title_label = Label(self, text='Currency Info 2', bg='#e9edf2', fg='black', font=('franklin gothic medium', 15))
        self.title_label.place(x=400, y=550, anchor='center')
        
        # Create 'print' button
        self.convert_button = Button(self, text='Print', bg='#52595D', fg='white', command=self.printData)
        self.convert_button.place(x=425, y=800, anchor='center')



    # Create clear function, to clear the amount field and final result field
    def clear(self):
        clear_entry = self.amount_entry.delete(0, END)
        clear_result = self.final_result.config(text='')
        return clear_entry, clear_result

    # Create a function to perform
    def processed(self):
        try:
            given_amount = float(self.amount_entry.get())
            given_base_currency = self.currency_variable1.get()
            given_des_currency = self.currency_variable2.get()
            converted_amount = self.CurrencyConverter.convert(given_amount, given_base_currency, given_des_currency)
            # Add comma every 3 numbers
            given_amount = '{:,}'.format(given_amount)

            self.final_result.config(text=f'{given_amount} {given_base_currency} = {converted_amount} {given_des_currency}')

        # Create warning message box
        except ValueError:
            convert_error = messagebox.showwarning('WARNING!', 'Please only enter integers in the Input Amount field')
            return convert_error
        
    def invert(self):
        return
    
    def printData(self):
        print_warning = messagebox.askokcancel(title = 'Requires PDF reader', message= 'Okay to print?')
        return print_warning


if __name__ == '__main__':
    converter = CurrencyConverter('https://api.exchangerate.host/latest')
    Main(converter)
    mainloop()