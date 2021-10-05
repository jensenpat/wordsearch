wordsearch(6)

# NAME
*wordsearch* - Classic word search game that you can play in your terminal

# SYNOPSIS
*/usr/games/wordsearch*

# DESCRIPTION
The object of *wordsearch* is to find and solve a set of words that belong to a particular category.

The player will navigate using arrow keys to find the letters that make up each word. Using the space bar, the player can select individual letters for each word. 

Once each word has been completed, the player will receive a score equal to the number of letters of each word. With all words completed, the player wins the game for the named category.

After finishing a category, the player will be prompted to begin a new category, or the player can choose to exit the game.

*wordsearch* supports the following command line arguments to customize gameplay:

	*-t <color>*    Set a curses color theme for game play: red, blue, green and black

	*-h*            Show wordsearch command line arguments

	*-v*            Show wordsearch version

# COMMANDS
Help is available on screen during gameplay. A description of available commands are below:

_Arrow keys:_ Move the cursor around the screen

_Space bar:_ Select a letter to score against the word list

_Return key:_ Clear the current letters being scored

_Q or Escape key:_ Exit to the shell prompt

# CONVENTIONS
Each word search puzzle generally features up to 9 words that make up that category. 

Puzzles are available as word lists and can be placed in any of the following directories:

_puzzles/_
_/usr/local/share/wordsearch/_
_/usr/pkg/share/wordsearch/_

Puzzles can be edited in your text editor. When *wordsearch* is started, it will select a random word list for each category during gameplay. 

Word lists should be optimized for display on an 80-column text terminal. Ideally, the entire set of words in a category should be less then 80 characters.

# SEE ALSO
hangman(6), boggle(6), quiz(6), tetris(6), wump(6)

# AUTHORS
Pat Jensen (patj@passpackets.com)

Based on a printable word search page generator by Christian Hill (https://scipython.com)
