#!/usr/local/bin/python3

# Wordsearch
# By Pat Jensen
# License: BSD-2-Clause

import os
import sys
import random
import curses
from copy import deepcopy
from curses.textpad import rectangle

# Maximum number of rows and columns.
NMAX = 32
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
nrows = 15
ncols = 15
wordlist_filename = "planets.txt"

def circle_mask(grid):
    """A circular mask to shape the grid."""
    r2 = min(ncols, nrows)**2 // 4
    cx, cy = ncols//2, nrows // 2
    for irow in range(nrows):
        for icol in range(ncols):
            if (irow - cy)**2 + (icol - cx)**2 > r2:
                grid[irow][icol] = '*'

def squares_mask(grid):
    """A mask of overlapping squares to shape the grid."""
    a = int(0.38 * min(ncols, nrows))
    cy = nrows // 2
    cx = ncols // 2
    for irow in range(nrows):
        for icol in range(ncols):
            if a <= icol < ncols-a:
                if irow < cy-a or irow > cy+a:
                    grid[irow][icol] = '*'
            if a <= irow < nrows-a:
                if icol < cx-a or icol > cx+a:
                    grid[irow][icol] = '*'

def no_mask(grid):
    """The default, no mask."""
    pass

# A dictionary of masking functions, keyed by their name.
apply_mask = {
              None: no_mask,
              'circle': circle_mask,
              'squares': squares_mask,
             }

def make_grid(mask=None):
    """Make the grid and apply a mask (locations a letter cannot be placed)."""
    grid = [[' ']*ncols for _ in range(nrows)]
    apply_mask[mask](grid)
    return grid

def _make_wordsearch(nrows, ncols, wordlist, allow_backwards_words=True,
                    mask=None):
    """Attempt to make a word search with the given parameters."""

    grid = make_grid(mask)

    def fill_grid_randomly(grid):
        """Fill up the empty, unmasked positions with random letters."""
        for irow in range(nrows):
            for icol in range(ncols):
                if grid[irow][icol] == ' ':
                    grid[irow][icol] = random.choice(alphabet)

    def remove_mask(grid):
        """Remove the mask, for text output, by replacing with whitespace."""
        for irow in range(nrows):
            for icol in range(ncols):
                if grid[irow][icol] == '*':
                    grid[irow][icol] = ' '


    def test_candidate(irow, icol, dx, dy, word):
        """Test the candidate location (icol, irow) for word in orientation
           dx, dy)."""
        for j in range(len(word)):
            if grid[irow][icol] not in (' ', word[j]):
                return False
            irow += dy
            icol += dx
        return True

    def place_word(word):
        """Place word randomly in the grid and return True, if possible."""

        # Left, down, and the diagonals.
        dxdy_choices = [(0,1), (1,0), (1,1), (1,-1)]
        random.shuffle(dxdy_choices)
        for (dx, dy) in dxdy_choices:
            if allow_backwards_words and random.choice([True, False]):
                    # If backwards words are allowed, simply reverse word.
                    word = word[::-1]
            # Work out the minimum and maximum column and row indexes, given
            # the word length.
            n = len(word)
            colmin = 0
            colmax = ncols - n if dx else ncols - 1
            rowmin = 0 if dy >= 0 else n - 1
            rowmax = nrows - n if dy >= 0 else nrows - 1
            if colmax - colmin < 0 or rowmax - rowmin < 0:
                # No possible place for the word in this orientation.
                continue
            # Build a list of candidate locations for the word.
            candidates = []
            for irow in range(rowmin, rowmax+1):
                for icol in range(colmin, colmax+1):
                    if test_candidate(irow, icol, dx, dy, word):
                        candidates.append((irow, icol))
            # If we don't have any candidates, try the next orientation.
            if not candidates:
                continue
            # Pick a random candidate location and place the word in this
            # orientation.
            loc = irow, icol = random.choice(candidates)
            for j in range(n):
                grid[irow][icol] = word[j]
                irow += dy
                icol += dx
            # We're done: no need to try any more orientations.
            break
        else:
            # If we're here, it's because we tried all orientations but
            # couldn't find anywhere to place the word. Oh dear.
            return False
        # will use this later for scoring
        # print(word, loc, (dx, dy))
        return True

    # Iterate over the word list and try to place each word (without spaces).
    for word in wordlist:
        word = word.replace(' ', '')
        if not place_word(word):
            # We failed to place word, so bail.
            return None, None

    # grid is a list of lists, so we need to deepcopy here for an independent
    # copy to keep as the solution (without random letters in unfilled spots).
    solution = deepcopy(grid)
    fill_grid_randomly(grid)
    remove_mask(grid)
    remove_mask(solution)

    return grid, solution


def make_wordsearch(*args, **kwargs):
    """Make a word search, attempting to fit words into the specified grid."""

    # We try NATTEMPTS times (with random orientations) before giving up.
    NATTEMPTS = 10
    for i in range(NATTEMPTS):
        grid, solution = _make_wordsearch(*args, **kwargs)
        if grid:
            # print('Fitted the words in {} attempt(s)'.format(i+1))
            return grid, solution
    print('I failed to place all the words after {} attempts.'
          .format(NATTEMPTS))
    return None, None

def show_grid_text(grid):
    """Output a text version of the filled grid wordsearch."""
    for irow in range(nrows):
        print(' '.join(grid[irow]))

def show_wordlist_text(wordlist):
    """Output a text version of the list of the words to find."""
    for word in wordlist:
        print(word)

def show_wordsearch_text(grid, wordlist):
    """Output the wordsearch grid and list of words to find."""
    show_grid_text(grid)
    print()
    show_wordlist_text(wordlist)

def get_wordlist(wordlist_filename):
    """Read in the word list from wordlist_filename."""
    wordlist = []
    with open(wordlist_filename) as fi:
        for line in fi:
            # The word is upper-cased and comments and blank lines are ignored.
            line = line.strip().upper()
            if not line or line.startswith('#'):
                continue
            wordlist.append(line)
    return wordlist

def listToString(s): 
    str1 = " " 
    return (str1.join(s))

def Main(window):
  mask = None
  wordlist = sorted(get_wordlist(wordlist_filename), key=lambda w: len(w),
                  reverse=True)
  max_word_len = max(nrows, ncols)
  scoreword = ''
  score = 0
 
  if max(len(word) for word in wordlist) > max_word_len:
    raise ValueError('Word list contains a word with too many letters.'
                     'The maximum is {}'.format(max(nrows, ncols)))

  allow_backwards_words = False
  grid, solution = make_wordsearch(nrows, ncols, wordlist, allow_backwards_words,
                                 mask)
  
  #height, width = window.getmaxyx()
  width = 80
  height = 24

  # Set up coordinates to track completed words
  co1 = set()

  curses.curs_set(2)
  curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
  window.bkgd(' ', curses.color_pair(1))

  window.hline(0, 0, " ", width, curses.A_REVERSE)

  category = wordlist_filename.replace(".txt", "")
  window.addstr(0, 0, category.center(width, ' '), curses.A_REVERSE)
  window.addstr(0, 0, " wordsearch", curses.A_REVERSE)
  window.addstr(0, 70, "Score: 0", curses.A_REVERSE)

  # Draw search box
  rectangle(window, 2, 24, 18, 54)
 
  # Render word search surface
  startrow = 3
  startcol = 25

  for irow in range(nrows):
    puzrow = ' '.join(grid[irow])
    window.addstr(startrow, startcol, puzrow);
    startrow = startrow + 1
 
  # Render word hint list
  wordlistdisp = listToString(wordlist)
  window.addstr(20, 0, wordlistdisp.center(width, ' '))

  # Render navigational directions
  window.addstr(23, 0, "Arrow keys to navigate. Space: Select, Return: Clear, Q: Quit")

  # Move on to puzzle surface
  window.move(10, 37)
 
  # Main event loop 
  key = window.getch()
  while key != ord('q') and key != 27:
    if key == curses.KEY_UP:
      cy, cx = curses.getsyx()
      if not cy < 4:
        try:
          window.move(cy-1, cx)
        except:
          curses.beep()
          window.refresh()
    elif key == curses.KEY_DOWN:
      cy, cx = curses.getsyx()
      if not cy > 16:
        try:
          window.move(cy+1, cx)
        except:
          curses.beep()
          window.refresh()
    elif key == curses.KEY_LEFT:
      cy, cx = curses.getsyx()
      if not cx < 27:
        try:
          window.move(cy, cx-2)
        except:
          curses.beep()
          window.refresh()
    elif key == curses.KEY_RIGHT:
      cy, cx = curses.getsyx()
      if not cx > 52:
        try:
          window.move(cy, cx+2)
        except:
          curses.beep()
          window.refresh()
    elif key == curses.KEY_RESIZE:
      window.refresh()

    # Return to wipe
    elif key == 10:
      cy, cx = curses.getsyx()
      for cord in co1:
        wipechar = window.instr(cord[0], cord[1], 1)
        window.addch(cord[0], cord[1], wipechar)
      # FIXME: dont we need to delete the solved coords too?
      window.addstr(10, 60, "                 ")
      scoreword = ''
      window.move(cy, cx)  

    # Space to score
    elif key == ord(' '):    # space bar
      cy, cx = curses.getsyx()			# get y/x

      # Add coords for each letter we are adding
      co1.add((cy, cx))
      # window.addstr(11, 60, str(co1))

      # Find cursor and see if we have character match
      scorechar = window.instr(cy, cx, 1)		# get char under cursor
      scoredecode = scorechar.decode("utf-8")
      scoreword = ''.join([scoreword, scoredecode])
      window.addstr(10, 60, scoreword)

      # Now let's check for a word match
      for word in wordlist:
        if (word == scoreword):
          # Increase score based on number of chars
          score = score + len(word)	

          # Render new score
          scoretext = "Score: " + str(score)
          sx = width - 9
          sx = sx - len(str(score))
          window.addstr(0, sx, scoretext, curses.A_REVERSE)

          # Reset settings for next word and clear buffer
          window.addstr(10, 60, "                 ") 
          scoreword = ''
          
          # Clear word from word list and redraw word list 
          wordlist.remove(word)
          wordlistdisp = listToString(wordlist)
          window.addstr(20, 0, wordlistdisp.center(width, ' '))

      window.addch(cy, cx, scorechar, curses.A_REVERSE)	 # highlight char 
      window.move(cy, cx)			# move back on board
      curses.beep()				# beep
      
    key = window.getch()

curses.wrapper(Main)

print("Thank you for playing wordsearch.")
