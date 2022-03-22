from calendar import c
import random
import numpy


row = int(input('Enter the Number of rows for the board: '))
col = int(input('Enter the Number of columns for the board: '))

pcletter = input('Enter computer letter: ')
userletter = input('Enter your letter: ')

horizontal_wins = [0, 0]        # [user wins, computer wins]
vertical_wins = [0, 0]          
# Draws the board for the game
def playSpace(row, col):
    if row < 3 and col < 3:
        print('row and col cannot be both less than 3')
        return
    rows = row*2;   cols = col
    frame = []
    # setup unit cells
    horizonatal = ['+', '-']
    vertical = ['|', ' ']
    # populate frame
    
    for r_index in range(rows+1):
        # Define a unit
        if r_index % 2 == 0:
            unit = horizonatal
        else:
            unit = vertical
        # Define the final
        end = [unit[0]]
        # Create table
        frame_row = unit*cols + end
        frame.append(frame_row)
    return frame
frame = playSpace(row, col)
for value in frame:
    print(''.join(value))        

# Creates row and coll representation for each space        
def cells(row, col):
    rows = row*2; cols = col*2
    # Represent all row spaces
    row_choices = []
    col_choice = []
    col_choices = []
    for index in range(col):
        col_choice.append(index*2+1)
    for index in range(row):
        row_choices.append(index*2+1)
        col_choices.append(col_choice.copy())

    return [row_choices, col_choices]
[row_choices, col_choices] = cells(row, col)
# Plays for the computer            
def computerPlay(letter):
    Row = 0; Col = 0
    while Row == 0:
        Row = random.choice(row_choices)
        if Row != 0:
            break
    while Col == 0:
        Col = random.choice(col_choices[int((Row-1)/2)])
        if Col != 0:
            frame[Row][Col] = letter
            col_choices[int((Row-1)/2)][int((Col-1)/2)] = 0
                
            Ans = 'yes'          # are there all zeros?
            for value in col_choices[int((Row-1)/2)]:
                if value != 0:
                    Ans = 'no'
                    break
            if Ans == 'yes':
                row_choices[int((Row-1)/2)] = 0
            break
# Plays for the human
def userPlay(R, C, letter):
    table_row = row_choices[R]
    if table_row == 0:
        while table_row == 0:
            R = int(input('Re-enter row: ')) - 1
            table_row = row_choices[R]
            if table_row != 0:
                break
    table_col = col_choices[R][C]
    if table_col == 0:
        while table_col == 0:
            C = int(input('Re-enter the column: ')) - 1
            table_col = col_choices[R][C]
            if table_col != 0:
                break
    col_choices[R][C] = 0
                
    Ans = 'yes'          # are there all zeros?
    for value in col_choices[R]:
        if value != 0:
            Ans = 'no'
            break
    if Ans == 'yes':
        row_choices[R] = 0
    frame[table_row][table_col] = letter
    return
    
def checkHorizontal():
    index_col = 1; index_row = 1
    rows = row*2 
    cols = col*2
    while index_row < rows:                 # for every row
        while index_col < (cols-4):         # for every column
            clue = frame[index_row][index_col]      # Gets the symbol in a cell
            if clue == userletter or clue == 'u':                  # Checks if it is the user symbol
                winner = 'u'                        # Sets to user winning symbol
                Hwins = horizontal_wins[0]           # Gets number of user wins
                horizontal_wins[0] = checkH(index_row, index_col, clue, winner, Hwins)    # Determines if user has a horizontal gain and updates mumber of wins
                
                if horizontal_wins[0] > Hwins:
                    index_col += 6
                else:
                    index_col += 2                       
            elif clue == pcletter or clue == 'c':
                winner = 'c'
                Hwins = horizontal_wins[1]
                horizontal_wins[1] = checkH(index_row, index_col, clue, winner, Hwins)
                
                if horizontal_wins[1] > Hwins:
                    index_col += 6
                else:
                    index_col += 2
            else:
                index_col += 2
        index_row += 2
        index_col = 1

def checkVertical():
    index_col = 1; index_row = 1
    rows = row*2 + 1
    cols = col*2 + 1
    while index_col < cols:
        while index_row < (rows-5):
            clue = frame[index_row][index_col]      # Gets the symbol in a cell
            if clue == userletter or clue == 'u':                  # Checks if it is the user symbol
                winner = 'u'                        # Sets to user winning symbol
                Vwins = vertical_wins[0]           # Gets number of user wins
                vertical_wins[0] = checkV(index_row, index_col, clue, winner, Vwins)    # Determines if user has a horizontal gain and updates mumber of wins
                
                if vertical_wins[0] > Vwins:
                    index_row += 6
                else:
                    index_row += 2                       
            elif clue == pcletter or clue == 'c':
                winner = 'c'
                Vwins = vertical_wins[1]
                vertical_wins[1] = checkV(index_row, index_col, clue, winner, Vwins)
                
                if vertical_wins[1] > Vwins:
                    index_row += 6
                else:
                    index_row += 2
            elif clue != ' ':
                index_row += 6
            else:
                index_row += 2
        index_col += 2
        index_row = 1

def checkH(x, y, c, l, w):
    Ans = 'yes'     # Is there a complete triad?
    same = 0
    
    if c != l:
        for next_columns in range(y+2, y+5, 2):
            if frame[x][next_columns] != c and frame[x][next_columns] != l:
                Ans = 'no'
                break
            elif frame[x][next_columns] == l:
                same += 1
        print('same: ', same)
    else:
        for next_columns in range(y+2, y+5, 2):
            if frame[x][next_columns] != l:
                Ans = 'no'
                break
            else:
                same += 1
        print('same: ', same)        
    if Ans == 'yes' and same < 2:
        for next_columns in range(y, y+5, 2):
            frame[x][next_columns] = l
        same = 0
        return w + 1
    same = 0
    return w

def checkV(x, y, c, l, w):
    Ans = 'yes'
    same = 0

    if c != l:
        for next_row in range(x+2, x+5, 2):
            if frame[next_row][y] != c and frame[next_row][y] != l:
                Ans = 'no'
                break
            elif frame[next_row][y] == l:
                same+=1
    else:
        for next_row in range(x+2, x+5, 2):
            if frame[next_row][y] != l:
                Ans = 'no'
                break
            else:
                same+=1            
    print('same:', same)
    if Ans == 'yes' and same < 2:
        for next_row in range(x, x+5, 2):
            frame[next_row][y] = l
        same = 0
        return w + 1
    same = 0
    return w

                            
                
# Runs the game
for k in range(40):
    Row = int(input('Enter row: '))
    Column = int(input('Enter column: '))
    
    userPlay(Row-1, Column-1, userletter)
    
    for value in frame:
        print(''.join(value))
    print('\n')
    computerPlay(pcletter)
    checkVertical()
    checkHorizontal()
    for value in frame:
        print(''.join(value))
    print(horizontal_wins, vertical_wins)
        
    