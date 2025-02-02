"""
Test script for module a1

When run as a script, this module invokes several procedures that 
test the various functions in the module a1.

Author: Geoffrey Miller gom6
Date:   9/15/2022
"""
from xml.dom import UserDataHandler
import introcs
import a1


def testA():
    """

    Test procedure for Part A
    
    Tests whether space is present
    
    Precondition: Needs Space(s) present

    """

    #Testing to see if python can print my first name properly
    print('Testing whether "before_space" is working')

    input_beforespace = 'Geoffrey Miller'

    outcome_beforespace = a1.before_space(input_beforespace)

    introcs.assert_equals('Geoffrey',outcome_beforespace)


    input_beforespace = 'Geoffrey  Miller'

    outcome_beforespace = a1.before_space(input_beforespace)

    introcs.assert_equals('Geoffrey',outcome_beforespace) #tesing with two spaces


    input_beforespace = ' Geoffrey Miller'

    outcome_beforespace = a1.before_space(input_beforespace)

    introcs.assert_equals('',outcome_beforespace)#testing with one space before words


    input_beforespace = 'Geoffrey   '

    outcome_beforespace = a1.before_space(input_beforespace)

    introcs.assert_equals('Geoffrey',outcome_beforespace)#Testing wit 3 spaces after


    input_beforespace = '  Geoffrey    '

    outcome_beforespace = a1.before_space(input_beforespace)

    introcs.assert_equals('',outcome_beforespace)
    #testing with two space before and three after
    """

    """
    #Testing to see if python can print my last name properly
    print('Testing whether "after_space" is working')

    input_afterspace = 'Geoffrey Miller'

    outcome_afterspace = a1.after_space(input_afterspace)
    
    introcs.assert_equals('Miller',outcome_afterspace)#normal text


    input_afterspace = 'Geoffrey Owen Miller'

    outcome_afterspace = a1.after_space(input_afterspace)
    
    introcs.assert_equals('Owen Miller',outcome_afterspace)#with two words


    input_afterspace = 'Geoffrey Owen Owen Miller'

    outcome_afterspace = a1.after_space(input_afterspace)
    
    introcs.assert_equals('Owen Owen Miller',outcome_afterspace)#With three words  


    input_afterspace = 'Geoffrey Owen Owen Owen Owen Miller'

    outcome_afterspace = a1.after_space(input_afterspace)
    
    introcs.assert_equals('Owen Owen Owen Owen Miller',outcome_afterspace) 
#with four words

    input_afterspace = ' Geoffrey Owen Owen Owen Owen Miller'

    outcome_afterspace = a1.after_space(input_afterspace)
    
    introcs.assert_equals('Geoffrey Owen Owen Owen Owen Miller',outcome_afterspace)
#with a space before

    input_afterspace = 'GeoffreyOwenOwenOwen  Owen Miller'

    outcome_afterspace = a1.after_space(input_afterspace)
    
    introcs.assert_equals(' Owen Miller',outcome_afterspace)
#with one big word and two spaces

def testB():
    """
    Test procedure for Part B

    Finding the values after "lhs" and "rhs"
    """
    print('Testing to see if having an valid answer works of after "rhs" ')
    
    binput = 'A "B C" D'

    boutcome = a1.first_inside_quotes(binput)

    introcs.assert_equals('B C',boutcome) 
    #testing with one space and two words
    
    binput = 'A "L D B C" D'

    boutcome = a1.first_inside_quotes(binput)

    introcs.assert_equals('L D B C',boutcome)
#Testing with four words

    binput = ' A " B C " D'

    boutcome = a1.first_inside_quotes(binput)

    introcs.assert_equals(' B C ',boutcome)
#testing with spaces at the start and end of the quotes

    print('Testing to see whether printing bitcoin works properly')
    
    bput = '{ "lhs" : "1 Bitcoin", "rhs" : "19995.85429186 Euros", "err" : "" }' 

    boutcom = a1.get_lhs(bput)

    introcs.assert_equals('1 Bitcoin',boutcom)
#Testing with one single number bitcoin

    bpu = '{ "lhs" : "900 Bitcoin", "rhs" : "19995.85429186 Euros", "err" : "" }' 

    boutco = a1.get_lhs(bpu)

    introcs.assert_equals('900 Bitcoin',boutco)
#Testing with with three digit bitcoin

    print('Testing to see whether printing Euros works properly')
        
    bpu = '{ "lhs" : "1 Bitcoin", "rhs" : "19995.85429186 Euros", "err" : "" }'

    boutco = a1.get_rhs(bpu)

    introcs.assert_equals('19995.85429186 Euros',boutco)
#Testing with big number of euros

    bpu = '{ "lhs" : "1 Bitcoin", "rhs" : "19995 Euros", "err" : "" }'

    boutco = a1.get_rhs(bpu)

    introcs.assert_equals('19995 Euros',boutco)
#Testing with less numbers

    print('Test to see whether there is a error present')

    errora = '{ "lhs" : "", "rhs" : "", "err" : "Currency amount is invalid." }'

    errorb = a1.has_error(errora)

    introcs.assert_equals(True,errorb)
#Testing with an invaild statement

    errorb = '{ "lhs" : "1 Bitcoin", "rhs" : "19995.85429186 Euros", "err" : "" }'

    errora = a1.has_error(errorb)

    introcs.assert_equals(False,errora)
#Testing with a correct statement


def testC():
    """
    Test procedure for Part C
    """
    print('Testing the web service')
    

    result = a1.query_website('USD', 'CUP', 2.5) #json string

    introcs.assert_equals('{ "lhs" : "2.5 United States Dollars", "rhs" : "64.375 Cuban \
Pesos", "err" : "" }', result)


    result = a1.query_website('CUC', 'CRC', 2.5) #json string

    introcs.assert_equals('{ "lhs" : "2.5 Cuban Convertible Pesos", "rhs" : "1638.7180325\
 Costa Rican ColÃ³nes", "err" : "" }', result)


    result = a1.query_website('CZK', 'DJF', 2.5) #json string

    introcs.assert_equals('{ "lhs" : "2.5 Czech Republic Koruny", "rhs" : "18.062668782522 \
Djiboutian Francs", "err" : "" }', result)
    

    result = a1.query_website('CZE', 'DJF', 2.5) #json string

    introcs.assert_equals('{ "lhs" : "", "rhs" : "", "err" : "Source currency code is \
invalid." }', result)


    result = a1.query_website('CUC', 'DJF', 10) #json string

    introcs.assert_equals('{ "lhs" : "10 Cuban Convertible Pesos", "rhs" : "1790 \
Djiboutian Francs", "err" : "" }', result)


def testD():
    """
    Test procedure for Part D
    """
    result = a1.query_website('CUC', 'DJF', 10) #Test to see if website works

    introcs.assert_equals('{ "lhs" : "10 Cuban Convertible Pesos", "rhs" : "1790 \
Djiboutian Francs", "err" : "" }', result)


    result = a1.query_website('USD', 'EUR', 10) #Testing diffrent currencies

    introcs.assert_equals('{ "lhs" : "10 United States Dollars", "rhs" : "10.07098 \
Euros", "err" : "" }', result)


    result = a1.query_website('DJF', 'USD', 10.00001) #Testing diffrent currencies

    introcs.assert_equals('{ "lhs" : "10.00001 Djiboutian Francs", "rhs" \
: "0.055865977653631 United States Dollars", "err" : "" }', result)


    result = a1.currency('DJF')#Testing diffrent currencies

    introcs.assert_equals(1, result)


    result = a1.currency('USD')#testing to see if three letters work

    introcs.assert_equals(1, result)


    result = a1.currency('JFNJFN')#Testing error with many letters

    introcs.assert_equals(0, result)


    result = a1.currency('OOO')#Testing error with three letters

    introcs.assert_equals(0, result)

testA()
testB()
testC()
testD()
print('Module a1 passed all tests.')