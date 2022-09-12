# Currency Information Generator

# This microservice communicates with the Currency Converter application. 
# The Currency Converter app sets up the socket connection and the microservice connects to the socket.
# The Currency Converter app will send an encoded request to the microservice.
# The microservice will respond, and the Currency Converter will receive the message.

import time, socket, sys

print("Initializing....\n")
time.sleep(1)

s = socket.socket()
shost = 'localhost'                             # specify publishing host (Currency Converter)
host = 'localhost'                              # specify subscribing host  (Currency Info Generator)
name = "Currency Info"
port = 1234                                     # specify port
#print("Trying to connect to ", host, "(", port, ")\n")
s.bind((host, port)) 
time.sleep(1)
s.listen()

                 # store name of app for ease of identification
#print("Type EXIT to quit")
#print("Enter message to send...")

# Currency Data
currency_info = {
    "USD": """The United States dollar (symbol: $; code: USD; also abbreviated US$ or U.S. Dollar,\
to distinguish it from other dollar-denominated currencies; referred to as the dollar, U.S. dollar, American dollar,\
or colloquially buck) is the official currency of the United States and several other countries. 
    """,
    "EUR": """The euro (symbol: €; code: EUR) is the official currency of 19 out of the 27 member states \
of the European Union. This group of states is known as the eurozone or, officially, the euro area, and \
includes about 349 million citizens as of 2019. The euro is divided into 100 cents. 
    """,
    "GBP": """The pound (sign: £) is the main unit of sterling, and the currency itself may be referred to by the \
compound noun pound sterling or the term British pound, although neither of these are official names of the \
currency. One pound is subdivided into 100 pence (singular: 'penny', abbreviated: 'p'). \
Sterling is the world's oldest currency that is still in use and that has been in continuous use since its inception. \
It is currently the fourth most-traded currency in the foreign exchange market, after the United States dollar, the euro, \
and the Japanese yen. Together with those three currencies and Renminbi, it forms the basket of currencies which calculate \
the value of IMF special drawing rights. As of mid-2021, sterling is also the fourth most-held reserve currency in global reserves. \
All these currencies are government-issued fiat currencies. 
    """,
    "CAD": """The Canadian dollar (symbol: $; code: CAD; French: dollar canadien) is the currency of Canada. \
It is abbreviated with the dollar sign $, or sometimes CA$, Can$ or C$ to distinguish it from other dollar-denominated \
currencies. It is divided into 100 cents (¢). 
    """,
    "JPY": """The yen (Japanese: 円, symbol: ¥; code: JPY; also abbreviated as JP¥) is the official currency of Japan. It is the \
third-most traded currency in the foreign exchange market, after the United States dollar (US$) and the euro. It is also widely \
used as a third reserve currency after the US dollar and the euro. 
    """,
    "MXN": """The Mexican peso (symbol: $; code: MXN) is the currency of Mexico. Modern peso and dollar \
currencies have a common origin in the 16th–19th century Spanish dollar, most continuing to use its sign, "$".
    """,
    "CHF": """The Swiss franc (German: Franken, French: franc, Italian: franco and Romansh: franc; sign: Fr. (in German language), \
fr. (in French, Italian, Romansh languages), or CHF in any other language, or internationally; code: CHF) is the currency and \
legal tender of Switzerland and Liechtenstein. It is also legal tender in the Italian exclave of Campione d'Italia. The Swiss National \
Bank (SNB) issues banknotes and the federal mint Swissmint issues coins. 
    """,
    "AMD": """The dram (Armenian: դրամ; sign: ֏; code: AMD) is the monetary unit of Armenia and the neighboring Republic of Artsakh. It was \
historically subdivided into 100 luma (Armenian: լումա). The word "dram" translates into English as "money" and is cognate with the Greek \
drachma and the Arabic dirham, as well as the English weight unit dram. The first instance of a dram currency was in the period from 1199 to 1375, \
when silver coins called dram were issued.
    """,
    "AUD": """The Australian dollar (sign: $; code: AUD) is the currency of Australia, including its external territories: Christmas Island, Cocos (Keeling) \
Islands, and Norfolk Island. It is officially used as currency by three independent Pacific Island states: Kiribati, Nauru, and Tuvalu. It is legal tender \
in Australia. Within Australia, it is almost always abbreviated with the dollar sign ($), with A$ or AU$ sometimes used to distinguish it from other \
dollar-denominated currencies. The $ symbol precedes the amount. It is subdivided into 100 cents. 
    """,
    "BRL": """The Brazilian real (pl. reais; sign: R$; code: BRL) is the official currency of Brazil. It is subdivided into 100 centavos. The Central Bank of Brazil \
is the central bank and the issuing authority. The real replaced the cruzeiro real in 1994. \
As of April 2019, the real was the twentieth most traded currency.
    """
}

# Continuous Communication Pipeline
while True:
    #s.connect((host, port))
    sock, addr = s.accept() 
    print("Connected...\n")

    sock.send(name.encode())                           # send microservice name
    s_name = sock.recv(1024)                           # receive app name (Currency Converter)
    s_name = s_name.decode()       

    message = sock.recv(1024)                      # receive message from app (Currency Converter)
    message = message.decode()
    print(s_name + ":", message)                # display message from app (Currency Converter)
    if message == "EXIT":                       # exit if the entered message is EXIT
        print("Exiting...")
        break
    if message not in currency_info.keys():     # respond if no currency info is available
        message = "No information available"
        s.send(message.encode())
    for k in currency_info.keys():              # respond with appropriate currency
        if message == k:
            message = currency_info[k]
            sock.send(message.encode())
            print(name + ":", message)           