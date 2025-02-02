"""
User interface for module currency

When run as a script, this module prompts the user for two currencies and 
an amount. It prints out the result of converting the first currency to 
the second.

Author: Geoffrey Miller gom6
Date:   9/15/2022
"""
import a1
#I was confused with the error in this code and how to fix it
first = str(input("Enter original currency: ")) 
second = str(input("Enter desired currency: "))
third = str(input("Enter original amount: "))
fourth = str(a1.exchange(first, second, float(third)))

print('You can exchange ' + third + ' ' + first + ' for ' + fourth + ' ' +second + '.')