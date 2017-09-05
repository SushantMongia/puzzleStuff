#////////////////////////////////////////////////////////////////////////////////#
# Puzzle Solution                                                                #
# Sushant Mongia                                                                 #
#                                                                                #
# Description: This program calculates a subset of costs from a priceList.       #
#              The summation of all the elements of the new subset = TargetPrice #
#                                                                                #
# Assumption:  Data is given in this format                                      #
#              [Target Price],[$xx.xx]                                           #
#              [Items List], [Cost]                                              #
#              [Dish],[$xx.xx]                                                   #
#               .... , $....                                                     #
#                                                                                #
#////////////////////////////////////////////////////////////////////////////////#

# Stuff to import
import csv
import numpy as np

ival=[]

# Function for finding all possible subsets and to see if we have a solution in there
def combinations(priceList, index, targetPrice, memory):

  # Calculate value for a subset; Solution Possible -> 1 ; Otherwise -> 0
  if index >= len(priceList):
      return 1 if targetPrice == 0 else 0

  # Track if we missed a calculation/ Track what we calculated
  if (index, targetPrice) not in memory:  
    counter = combinations(priceList, index + 1, targetPrice, memory)
    counter += combinations(priceList, index + 1, targetPrice - priceList[index], memory)
   
    # Store Calculated result in memory
    memory[(index, targetPrice)] = counter 

  # Return value from Value
  return memory[(index, targetPrice)]   


# Function for finding all possible subsets and to see if we have a solution in there
def solutions(priceList, targetPrice, memory):
  priceCombo = []
  
  # Run through the priceList
  for index, value in enumerate(priceList):

    # For the given price from the priceList, see if we can get a solution by including more values from priceList
    if combinations(priceList, index + 1, targetPrice - value, memory) > 0:

      # Append selected price to the subset
      priceCombo.append(value)
      targetPrice -= value
      ival.append(index)

  # Return the priceCombo calculated
  return priceCombo



# The main function starts here!    
if __name__ == "__main__":

    #Declartions
    mydict          = [] # Extracted Names from the file
    avals           = [] # Extracted Price from the file
    pvals           = [] # Temp Price Vals List
    answer          = [] # Final PriceCombo Names stored here! 
    priceCombo      = [] # Final priceCombo here
    # Headers for the .csv file
    HEADERS = ["Name", "Price"]

    # Input fileName from the user 
    print "Enter file name (must be a .csv file):"
    fileName = raw_input()

    #fileName = "data.csv"

    dataFile = open(fileName)

    # In python the DictReader reads the cols out of order, (cont...A)
    data = csv.DictReader(dataFile, HEADERS)
    for value in data:
        # Check if we have a missing value/ corrupted value
        if any(val in (None, "","$ ") for val in value.itervalues()):
            print "Missing Value in %s" %value
        else:
            #(cont...A) so fetching values by Header Name
            mydict += [value.get('Name')]

            avals += [value.get('Price')]
            
    dataFile.close()

    # Trim the values in avals from $xx.xx down to xx.xx
    for price in avals:
        pvals.append(price[price.index('$') + len('$'):])
            
    targetPrice = float(pvals[0])
    priceList = np.array(pvals[1:])

    memory = dict()

    # Checking for Possible priceCombo that adds upto the targetPrice
    if combinations(priceList.astype(float), 0, targetPrice, memory) == 0:
        print "There is no combination of dishes that is equal to the target price!"
    else:
        #print memory
        ans = (solutions(priceList.astype(float), targetPrice, memory))
        for vals in ival:
          answer.append(mydict[vals+1])
            #answer.append(round(vals,2))
        print answer
        print targetPrice
        for vals in ans:
          priceCombo.append(round(vals,2))
        print priceCombo
            
