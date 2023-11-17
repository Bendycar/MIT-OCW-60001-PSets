# %load ps3.py
# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    
    word1 = word.lower()
    points = 0
    for i in word1:
        if i == '*':
            points += 0
        else:
            points += SCRABBLE_LETTER_VALUES[i]
    if ((7 * len(word)) - (3 * (n - len(word)))) >= 1:
        score = ((7 * len(word)) - (3 * (n - len(word)))) * points
    else:
        score = points

    return score

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3)) - 1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, (n - 1)):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
        
    hand['*'] = hand.get('*', 0) + 1

    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    new_hand = hand.copy()
    word1 = word.lower()
    for i in word1:
        if i in hand.keys():
            new_hand[i] -= 1

    for i in list(new_hand.keys()): #Converted keys to a list to prevent RuntimeError
        if new_hand[i] <= 0:
            del new_hand[i]

    return new_hand
#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    
    VOWELS = 'aeiou'
    word1 = word.lower()
    
    if word1 in word_list:
        
        for i in word1:
            if i not in hand.keys() or word1.count(i) > hand[i]:
                return False

        return True
    else:
        for i in word1:
            if i == '*':
                for i in VOWELS:
                    word2 = word1.replace('*', i)
                    if word2 in word_list:
                        for i in word1:
                            if i not in hand.keys() or word1.count(i) > hand[i]:
                                return False
                        
                        return True

                       
#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    
    length = 0
    for i in hand.keys():
        length += hand[i]

    return length

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    
    current_score = 0 # Keep track of the total score
    #hand = deal_hand(HAND_SIZE)
    handlen = calculate_handlen(hand)
    
    while handlen > 0:# As long as there are still letters left in the hand:
    
        print("Letters in hand:")
        display_hand(hand)# Display the hand
        
        request = input("Play a valid word from your hand: ")# Ask user for input
        
        if request == '!!':# If the input is two exclamation points:
        
            break# End the game (break out of the loop)

            
        else:# Otherwise (the input is not two exclamation points):

            if is_valid_word(request, hand, word_list):# If the word is valid:

                word_score = get_word_score(request, handlen)
                current_score += word_score
                print("That word was worth", word_score, "points")# Tell the user how many points the word earned,
                print("This hand's current score is", current_score)# and the updated total score

            else:# Otherwise (the word is not valid):
                print("Please play a valid word")# Reject invalid word (print a message)
                
            hand = update_hand(hand, request)# update the user's hand by removing the letters of their inputted word
            handlen = calculate_handlen(hand)

    # Game is over (user entered '!!' or ran out of letters),
    print("End of hand! This hand's score was", current_score)# so tell user the total score

    return current_score# Return the total score as result of function



#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    #Ask the user if they would like to sub a letter
        #If no, break
    #Else:
    hand_clone = hand.copy() #Clone hand
    all_letters = VOWELS + CONSONANTS #Create new set of all letters by combining vowels and consonents
    for i in hand:
        all_letters = all_letters.replace(i, "") #Remove from this set all letters currently in hand
    num_of_letters = hand_clone[letter]
    for i in range(num_of_letters):    #For loop in range equal to number of instances of that letter
        x = random.choice(all_letters)    
        hand_clone[x] = hand_clone.get(x, 0) + 1 #Add to hand clone a randomly chosen letter
    del hand_clone[letter] #Delete all instances of subbed letter
    
    return hand_clone #Return hand clone
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    num_hands = int(input("How many hands would you like to play? "))# Asks for number of hands
    total_score = 0 # Create total score variable
    sub_counter = 0 # Create sub counter
    hand_counter = 0 # Create hand counter
    replay_counter = 0 #Create replay counter
    while hand_counter < num_hands: #While hand counter less than number of hands
       hand = deal_hand(HAND_SIZE) #Define hand
       print("Letters in hand:")
       display_hand(hand)# Display the hand
       if sub_counter == 0: #Check sub counter, Ask if they want to sub
           ask = input("Would you like to substitute a letter from your hand? ")
           ask = ask.lower()
           if ask == "yes":
               letter = input("Which letter? ")
               letter = letter.lower()
               sub_counter += 1#If yes: sub counter += 1
               hand = substitute_hand(hand, letter)#Perform sub code
       current_score = play_hand(hand, word_list)#Play hand
       if replay_counter == 0: #Ask if they want to replay
           replay = input("Would you like to replay that same hand? ") #If yes, play another hand with no sub check
           replay = replay.lower()
           if replay == "yes":
               replay_counter += 1
               extra_game = play_hand(hand, word_list)
               best = max(current_score, extra_game)
               current_score = best
       total_score += current_score #Increment score
       hand_counter += 1
   
    print("Game over! Your total score was", total_score)


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
