# currency_converter
CS361
[UML Diagram.pdf](https://github.com/Wcarey7/currency_converter/files/9174507/UML.Diagram.pdf)



# Required Python imports:

   import socket
   
   import json



# How to package data:

    data = json.dumps({"base_currency": curr1, "des_currency": curr2, "amount_to_convert": amount})

    *Note: {"key": value} are always of type string. Key is required in quotes with names exactly as written above.




# Example send data from client to microservice:

    client.send(data.encode())




# Microservice returns to client:

    converted_amount is a single number in the format of "11.7"
