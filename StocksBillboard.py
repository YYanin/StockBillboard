import time
import sys
import os
import yfinance as yf

from colorama import Fore, Style, init
init(autoreset=True) # Initialize colorama, and reset colors after each print

def main():
    clearScreen()
    
    value='VOO'
    info=GetPrice(value,1)
    onOpen=GetPrice(value,2)
    
    print(value,':')

    print('On Open: ',value,' = ',onOpen, '$')
    print('Latest:',value,' = ',info, '$')

    return 0


##Function to return the current value of a given ticker
##if time is 1, then return the latest price, if 2 then return price on open
def GetPrice(stock,time):

    ##Pull the Price from the yahoo library
    val=yf.Ticker(stock)
    info=val.fast_info
    
    if time==1:
        price=round(info.last_price,2)
    elif time==2:
        price=round(info.open,2)
    
    return price


##Clears the screen
def clearScreen():
    # clear the console screen
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__=='__main__':
    main()
