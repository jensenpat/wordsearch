#!/usr/local/bin/python3

import os
import sys
import random
from copy import deepcopy
import curses

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


def svg_preamble(fo, width, height):
    """Output the SVG preamble, with styles, to open file object fo."""

    print("""<?xml version="1.0" encoding="utf-8"?>
    <svg xmlns="http://www.w3.org/2000/svg"
         xmlns:xlink="http://www.w3.org/1999/xlink" width="{}" height="{}" >
    <defs>
    <style type="text/css"><![CDATA[
    line, path {{
      stroke: black;
      stroke-width: 4;
      stroke-linecap: square;
    }}
    path {{
      fill: none;
    }}

    text {{
      font: bold 24px Verdana, Helvetica, Arial, sans-serif;
    }}

    ]]>
    </style>
    </defs>
    """.format(width, height), file=fo)

def grid_as_svg(grid, width, height):
    """Return the wordsearch grid as a sequence of SVG <text> elements."""

    # A bit of padding at the top.
    YPAD = 20
    # There is some (not much) wiggle room to squeeze in wider grids by
    # reducing the letter spacing.
    letter_width = min(32, width / ncols)
    grid_width = letter_width * ncols
    # The grid is centred; this is the padding either side of it.
    XPAD = (width - grid_width) / 2
    letter_height = letter_width
    grid_height = letter_height * nrows
    s = []

    # Output the grid, one letter at a time, keeping track of the y-coord.
    y = YPAD + letter_height / 2
    for irow in range(nrows):
        x = XPAD + letter_width / 2
        for icol in range(ncols):
            letter = grid[irow][icol]
            if letter != ' ':
                s.append('<text x="{}" y="{}" text-anchor="middle">{}</text>'
                                .format(x, y, letter))
            x += letter_width
        y += letter_height

    # We return the last y-coord used, to decide where to put the word list.
    return y, '\n'.join(s)

def wordlist_svg(wordlist, width, height, y0):
    """Return a list of the words to find as a sequence of <text> elements."""

    # Use two columns of words to save (some) space.
    n = len(wordlist)
    col1, col2 = wordlist[:n//2], wordlist[n//2:]

    def word_at(x, y, word):
        """The SVG element for word centred at (x, y)."""
        return ( '<text x="{}" y="{}" text-anchor="middle" class="wordlist">'
                 '{}</text>'.format(x, y, word) )

    s = []
    x = width * 0.25
    # Build the list of <text> elements for each column of words.
    y0 += 25
    for i, word in enumerate(col1):
       s.append(word_at(x, y0 + 25*i, word))
    x = width * 0.75
    for i, word in enumerate(col2):
       s.append(word_at(x, y0 + 25*i, word))
    return '\n'.join(s)

def write_wordsearch_svg(filename, grid, wordlist):
    """Save the wordsearch grid as an SVG file to filename."""

    width, height = 1000, 1414
    with open(filename, 'w') as fo:
        svg_preamble(fo, width, height)
        y0, svg_grid = grid_as_svg(grid, width, height)
        print(svg_grid, file=fo)
        # If there's room print the word list.
        if y0 + 25 * len(wordlist) // 2 < height:
            print(wordlist_svg(wordlist, width, height, y0), file=fo)
        print('</svg>', file=fo)


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

# Read the wordlist filename and grid dimensions (nrows, ncols) from the
# command line.
#wordlist_filename = sys.argv[1]
#nrows, ncols = int(sys.argv[2]), int(sys.argv[3])

def Main(window):
  mask = None
  wordlist = sorted(get_wordlist(wordlist_filename), key=lambda w: len(w),
                  reverse=True)
  max_word_len = max(nrows, ncols)
  if max(len(word) for word in wordlist) > max_word_len:
    raise ValueError('Word list contains a word with too many letters.'
                     'The maximum is {}'.format(max(nrows, ncols)))

  allow_backwards_words = False
  grid, solution = make_wordsearch(nrows, ncols, wordlist, allow_backwards_words,
                                 mask)
  
  height, width = window.getmaxyx()
  startrow = 12 
  startcol = 32

  for irow in range(nrows):
      puzrow = ' '.join(grid[irow])
      window.addstr(startrow, startcol, puzrow);
      startrow = startrow + 1
 
      #print(' '.join(grid[irow]))
  #show_grid_text(grid)
  window.addstr(22, 0, "WORD LIST GOES HERE")
  window.addstr(24, 0, "Controls: Press a key")
  key = window.getch()

curses.wrapper(Main)
print("got end")
