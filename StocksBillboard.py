import time
import sys
import os
import yfinance as yf

from colorama import Fore, Style, init
init(autoreset=True) # Initialize colorama, and reset colors after each print

def main():

    while True:

        clearScreen()
    
        value='^DJI'
        DisplayVal(value)
    
    
        value2='^IXIC'
        DisplayVal(value2)
 
        value3='^GSPC'
        DisplayVal(value3)
        
        time.sleep(20)

##Function that displays the value in the terminal
def DisplayVal(value):

    info=GetPrice(value,1)
    onOpen=GetPrice(value,2)
    color=GetColor(onOpen,info)
    
    percent=round((((info*100)/onOpen)-100),2)

    print(value)

    if color=='RED':
        print('Open: ',value,' = ',onOpen)
        print('Latest:',value,' = ',Fore.RED + str(info))
        print('Loss ', Fore.RED + str(percent),'%', '\n')
    else:
        print('On Open: ',value,' = ',onOpen)
        print('Latest:',value,' = ',Fore.GREEN + str(info))
        print('Gain ', Fore.GREEN + str(percent),'%', '\n')

    return


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

def GetColor(StartVal,CurrentVal):
    

    if StartVal>=CurrentVal:
        color='RED'
        return color
    else:
        color='GREEN'
        return color

##Clears the screen
def clearScreen():
    # clear the console screen
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__=='__main__':
    main()
