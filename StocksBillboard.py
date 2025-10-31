import time
import sys
import os
import yfinance as yf
from datetime import datetime
from colorama import Fore, Style, init


init(autoreset=True) # Initialize colorama, and reset colors after each print

# Cache to store ticker data
cache = {
    'data': None,
    'last_update': None
}

# List of all tickers we want to monitor
TICKERS = ['^DJI', '^IXIC', '^GSPC', 'BTC-USD', 'VOO', 'VTI', 'ZB=F']
UPDATE_INTERVAL = 20  # seconds between screen updates
CACHE_INTERVAL = 60   # seconds between API calls


def main():
    # Main program loop that runs indefinitely
    # Controls the overall flow of the program by:
    # 1. Clearing the screen for fresh display
    # 2. Updating the cache with fresh stock data if needed
    # 3. Displaying values for each ticker in the TICKERS list
    # 4. Waiting for UPDATE_INTERVAL seconds before next refresh
    # 5. Handling any errors that occur during execution
    while True:
        try:
            clearScreen()
            update_cache()
            
            for ticker in TICKERS:
                DisplayVal(ticker)
            
            time.sleep(UPDATE_INTERVAL)
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(UPDATE_INTERVAL)

def update_cache():
    """Update the cache if needed"""
    # This function manages the caching mechanism for stock data to minimize API calls
    # It follows these steps:
    # 1. Gets current timestamp
    # 2. Checks if cache needs updating (either empty or older than CACHE_INTERVAL)
    # 3. If update needed, fetches all ticker data in a single API call
    # 4. Updates cache with new data and timestamp
    # 5. Handles any API errors with retry mechanism
    current_time = datetime.now()
    
    if (cache['last_update'] is None or 
        (current_time - cache['last_update']).seconds >= CACHE_INTERVAL):
        
        try:
            # Fetch all tickers in one call
            tickers = yf.Tickers(' '.join(TICKERS))
            cache['data'] = tickers
            cache['last_update'] = current_time
        except Exception as e:
            print(f"Failed to update cache: {e}")
            time.sleep(5)  # Wait before retrying

##Function that displays the current and on open price as well as the percent difference
def DisplayVal(value):
    
    ##Querry the information from yfinance
    info=GetPrice(value,1)
    onOpen=GetPrice(value,2)

    ##Check which color you need to display the value as
    
    if onOpen>=info:
        color='RED'
    else:
        color='GREEN'


    ##Figure out the percent difference and store it in a variable
    percent=round((((info*100)/onOpen)-100),2)
    
    ##Print the value and the associated information
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
def GetPrice(stock, time_type):
    """Get price from cache"""
    # Retrieves stock price information from the cache
    # Parameters:
    #   stock: ticker symbol to look up
    #   time_type: 1 for current price, 2 for opening price
    # Returns:
    #   - rounded price value to 2 decimal places
    #   - 0.0 if cache is empty or error occurs
    # Uses fast_info from yfinance for quick price lookups
    # Handles potential errors during price retrieval
    if cache['data'] is None:
        return 0.0
        
    try:
        ticker_data = cache['data'].tickers[stock].fast_info
        if time_type == 1:
            return round(ticker_data.last_price, 2)
        elif time_type == 2:
            return round(ticker_data.open, 2)
    except Exception as e:
        print(f"Error getting price for {stock}: {e}")
        return 0.0

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
