#!/usr/bin/env python3

#Natural Language Processing Assignment 1
#Title: Random Sentence Generator
#Description: It uses grammar.gr and generates random sentenes. It takes grammar file as its first argument and number of sentences as second. If the second argument is not provided, it defaults to generating a single sentence.
#Author: Nafisa Ali Amir, Abhinav Singh
#Last Modified: 08/31/2018

import sys
from collections import defaultdict
import random
import bisect
from optparse import OptionParser

#Global Variables
Max_Non_Terminals = 500                     #The maximum number of non terminal expansions allowed
sentence = ""                               #Placeholder for generated sentence. It is overwritten each time the generator is called
non_terminals_counter = Max_Non_Terminals   #counter to limit the number of non terminal expansions
verboseOption = False                       #flag for verbose option '-t'
lessVerboseOption = False                   #flag for a less verbose option '-b'

#The function parse_args parses the command line arguments and returns the grammar file path and the number of sentences to be generated
def parse_args():
	
    num_rand_sentences = 1                      #default number of sentences is 1        
   
    parser = OptionParser()
    parser.add_option('-t', action = 'store_true', dest = 'verbose')
    parser.add_option('-b', action = 'store_true', dest = 'less_verbose')
    (options, args) = parser.parse_args()
    
    if options.verbose:
        global verboseOption
        verboseOption = True
    if options.less_verbose:
        global lessVerboseOption
        lessVerboseOption = True


    if len(args) > 1:                           #check for the second argument and update the number of sentences to generate
        num_rand_sentences = args[1]

    return int(num_rand_sentences), args[0]     #Returns the number of sentences to generate and the grammar to read from


#The function get_hash_table reads the grammar file and returns the hash table of the terminals and non-terminals
def get_hash_table(grammar_filename):

    hash_table = defaultdict(list)              #Using the python's defaultdict for creating hash tables

    cum_freq = defaultdict(list)

    grammar_file = open(grammar_filename, 'r')
        
    for line in grammar_file:
    	line = line.partition('#')[0]           #Remove all comments
    	line = line.partition('\n')[0]          #Remove all empty lines
    	if line and (('(' or ')') not in line):
            tokens = line.split()
            freq = float(tokens[0])  
            tokens.pop(0)
            non_terminals = tokens[0]
            tokens.pop(0)
            terminals = tokens
            hash_table[non_terminals].append(terminals)  #Updating the hash table for each entry
            if cum_freq[non_terminals]:         
                freq = freq + cum_freq[non_terminals][-1]   
            cum_freq[non_terminals].append(freq)        #Creating a cumulative frequency hash table for considering the freq/number on the leftmost side of the grammar
    
    grammar_file.close()                        #Done with the grammar file

    return hash_table, cum_freq

#The function rand_sentence_generator will generate a random sentence using hash table containing grammar rules and a start place which is hardcoded as ROOT
def rand_sentence_generator(hash_table, cum_freq, key):

    symbols = hash_table[key]                   #Get the values from the hash table for the key 'start'
       
    global sentence
    if verboseOption and symbols:               
        sentence = sentence + "(" + key + " "        #Print necessary brackets and symbols for the verbose option
    if lessVerboseOption:
        if key == 'S' or key == 's':            #Print { at the beginning of S (capital letter or not)
            sentence = sentence + "{"
        if key == 'NP' or key == 'np':          #Print [ at the beginning of noun phrase NP (capital letters or not)        
            sentence = sentence + "["

    global non_terminals_counter
    if symbols and non_terminals_counter > 0:   #Check for the non-terminal expansion counter and proceed if the limit is not reached yet
        non_terminals_counter = non_terminals_counter - 1   #update the counter for the latest expansion
        v = random.uniform(0.01, cum_freq[key][-1])         #choose a floating point number from the cumulative frequency list 
        
        symbols = symbols[bisect.bisect_left(cum_freq[key], v)] #selects the symbol with value less than the number v

        for symbol in symbols:
            rand_sentence_generator(hash_table, cum_freq, symbol)     #Recursively call the function to parse further keys until you hit a terminal
        if verboseOption:
            sentence = sentence.strip()       #Remove any previous newline and tab characters trailing in the sentence for verbose printing
            sentence = sentence + ")\n"             #Add a closing bracket and add newline for verbose printing
        if lessVerboseOption:
            if key == 'NP' or key == 'np':          #Print closing brackets for less verbose option '-b'
                sentence = sentence + "]"
            if key == 'S' or key == 's':
                sentence = sentence + "}"

    elif non_terminals_counter > 0:                 #When you hit a terminal
        #sentence = sentence + " " + key + " "             #Update sentence with the terminal word
        sentence = sentence + key + " "             #Update sentence with the terminal word


    if non_terminals_counter == 0:                  #If the non terminal expansions reach max limit, print "..."
        sentence = sentence + "..."
        return
 
#Main Part of the Program 

#1. Parse the command line arguments
num_rand_sentences, grammar_filename = parse_args()     

#2. Read the grammar file and return a hash table of rules
hash_table, cum_freq = get_hash_table(grammar_filename)

#3. Call the generator and create sentences
for _ in range(num_rand_sentences):             #Call the generator x times, look up the function parse_args to find where x came from
    
    #Initialise the variables before calling the generator
    sentence = ""
    non_terminals_counter = Max_Non_Terminals

    rand_sentence_generator(hash_table, cum_freq, 'ROOT') #Call generator with ROOT as the starting point

    if "..." in sentence:
        sentence = sentence.split("...")[0] + "..."

    print(sentence.strip())   #Print the generated sentence on the console






