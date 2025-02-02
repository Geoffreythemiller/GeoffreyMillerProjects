"""
Module for currency exchange

This module provides several string parsing functions to implement a 
simple currency exchange routine using an online currency service. 
The primary function in this module is exchange.

Author: Geoffrey Miller gom6
Date:   9/15/2022
"""
import introcs

from locale import currency
from operator import index


def before_space(s):
    """Returns a copy of s up to, but not including, the first space

    Parameter s: the string to slice
    Precondition: s is a string with at least one space"""
    space = s.index(' ')
    outcome = s[:space]
    return outcome


def after_space(s):
    """Returns a copy of s after the first space
    Parameter s: the string to slice
    Precondition: s is a string with at least one space"""
    space = s.index(' ')
    outcome = s[space +1: ]
    return outcome



def first_inside_quotes(s):
    """Returns the first substring of s between two (double) quotes

    A quote character is one that is inside a string, not one that 
    delimits it.  We typically use single quotes (') to delimit a 
    string if want to use a double quote character (") inside of it.

    Examples:
    first_inside_quotes('A "B C" D') returns 'B C'
    first_inside_quotes('A "B C" D "E F" G') returns 'B C', 
    because it only picks the first such substring

    Parameter s: a string to search
    Precondition: s is a string containing at least two double quotes"""
    bquotes = s.index('"')
    bquotesr = s.find('"',bquotes + 1)
    boutcome = s[bquotes + 1:bquotesr]
    return boutcome    


def get_lhs(json):
    """Returns the lhs value in the response to a currency query

    Given a JSON response to a currency query, this returns the 
    string inside double quotes (") immediately following the keyword
    "lhs". For example, if the JSON is
        
    '{ "lhs" : "1 Bitcoin", "rhs" : "19995.85429186 Euros", "err" : "" }'

    then this function returns '1 Bitcoin' (not '"1 Bitcoin"').  

    This function returns the empty string if the JSON response
    contains an error message.

    Parameter json: a json string to parse
    Precondition: json is the response to a currency query"""

    ajson = json.find('lhs')
    outjson = first_inside_quotes(json[ajson +5: ])
    return outjson


def get_rhs(json):
    """Returns the rhs value in the response to a currency query

    Given a JSON response to a currency query, this returns the 
    string inside double quotes (") immediately following the keyword
    "rhs". For example, if the JSON is

    '{ "lhs" : "1 Bitcoin", "rhs" : "19995.85429186 Euros", "err" : "" }'

    then this function returns '19995.85429186 Euros' (not 
    '"38781.518240835 Euros"').  

    This function returns the empty string if the JSON response
    contains an error message.

    Parameter json: a json string to parse
    Precondition: json is the response to a currency query"""

    ajson = json.find('rhs')
    outjson = first_inside_quotes(json[ajson +5: ])
    return outjson  


def has_error(json):
    """Returns True if the query has an error; False otherwise.

    Given a JSON response to a currency query, this returns True if there
    is an error message. For example, if the JSON is 

    '{ "lhs" : "", "rhs" : "", "err" : "Currency amount is invalid." }'

    then the query is not valid, so this function returns True (It 
    does NOT return the message 'Currency amount is invalid.').

    Parameter json: a json string to parse
    Precondition: json is the response to a currency query"""

    error = json.find('invalid')
    
    return not (error == -1)
    

def query_website(old, new, amt):
    """
    Returns a JSON string that is a response to a currency query.

    A currency query converts amt money in currency old to the 
    currency new. The response should be a string of the form    

    '{ "lhs":"<old-amt>", "rhs":"<new-amt>", "err":"" }'

    where the values old-amount and new-amount contain the value 
    and name for the old and new currencies. If the query is 
    invalid, both old-amount and new-amount will be empty, while 
    "err" will have an error message.

    Parameter old: the currency on hand
    Precondition: old is a string with no spaces or non-letters
        
    Parameter new: the currency to convert to
    Precondition: new is a string with no spaces or non-letters
        
    Parameter amt: amount of currency to convert
    Precondition: amt is a float
    """
    
    return introcs.urlread('http://cs1110.cs.cornell.edu/2022fa/a1?old=' + old + \
    '&new=' + new + '&amt=' + str(amt))


def is_currency(code):
    """
    Returns: True if code is a valid (3 letter code for a) currency
    It returns False otherwise.

    Parameter code: the currency code to verify
    Precondition: code is a string with no spaces or non-letters.
    """
    json = query_website(code, 'USD', 1)
    valid = has_error(json)
    return not(valid)


def exchange(old, new, amt):
    """
    Returns the amount of currency received in the given exchange.

    In this exchange, the user is changing amt money in currency 
    old to the currency new. The value returned represents the 
    amount in currency new.

    The value returned has type float.

    Parameter old: the currency on hand
    Precondition: old is a string for a valid currency code
        
    Parameter new: the currency to convert to
    Precondition: new is a string for a valid currency code
        
    Parameter amt: amount of currency to convert
    Precondition: amt is a float
    """
    exchangedJason = query_website(old, new, amt)
    ajso = get_rhs(exchangedJason)
    jason = before_space(ajso)
    return float(jason)