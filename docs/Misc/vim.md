## Changing Vim mode

i - Enter insert mode

a - Enter insert mode after the cursor

A - Enter insert mode at the end of the line

o - Open a new line below the current line and enter insert mode

O - Open a new line above the current line and enter insert mode

v - Enter visual mode

Ctrl+v - Enter visual-block mode

: - Enter command mode

R - Enter replace mode

ESC - Go back to Normal mode from any mode

## Exiting Vim

:w - Write (save) the file, but don't exit

:wa - Write (save) all files, but don't exit

:q - Quit (fails if there are unsaved changes)

:q! - Quit and throw away unsaved changes

:wq - Write (save) the file and exit

:x - Write (save) the file and exit (same as :wq)

:wqa - Write (save) all files and exit

## Moving around in Vim

h - Move cursor left

j - Move cursor down

k - Move cursor up

l - Move cursor right

you can prefix these with a number to move multiple times, e.g., "5j" moves down 5 lines.

## Movements within a line

$ - Move to the end of the line

0 - Move to the beginning of the line

^ - Move cursor to first non-blank character of the line

fx - Find next occurrence of character 'x'

Fx - Find previous occurrence of character 'x'

tx - Move towards next occurrence of character 'x' (stops before it)

Tx - Move towards previous occurrence of character 'x' (stops before it)

; - Repeat the last f, t, F or T movement

, - Repeat the last f, t, F or T movement, backwards

## Word movements

w - Move to the beginning of the next word. Stops at punctuation marks, spaces, tabs, and newlines. More granual movement can be achieved with a prefix number, e.g., "3w" moves 3 words forward.

W - Move to the beginning of the next WORD. Only stops at spaces, tabs, and newlines. Ignores punctuation. More granual movement can be achieved with a prefix number, e.g., "3W" moves 3 WORDs forward.

b - Move cursor to the beginning of the current or previous word. More granual movement can be achieved with a prefix number, e.g., "3b" moves 3 words backward.

B - Move cursor backwards to start of WORD. Ignores punctuation. More granual movement can be achieved with a prefix number, e.g., "3B" moves 3 WORDs backward.

e - Move cursor to the end of the current or next word. More granual movement can be achieved with a prefix number, e.g., "3e" moves 3 words forward.

E - Move cursor forward to end of WORD. More granual movement can be achieved with a prefix number, e.g., "3E" moves 3 WORDs forward.

ge - Move cursor to the end of the current or previous word.

gE - Move cursor backwards to end of WORD.

## Sentence movements

) - Move cursor to the beginning of the current or next sentence.

( - Move cursor to the beginning of the current or previous sentence.

## Paragraph movements

{ - Move cursor to the beginning of the current or previous paragraph.

} - Move cursor to the beginning of the next paragraph.

## Moving to specific lines

gg - Move to the first line of the file

G - Move to the last line of the file

{number}G - Move to line {number}

{numbger}j - Move down {number} lines

{number}k - Move up {number} lines

H - Move cursor to line at the top of the window

M - Move cursor to middle line of the window

L - Move cursor to line at the bottom of the window

## Parenthesis, Brackets, Braces, and Method Navigation

% - Find next pararenthesis, bracket, or brace that matches the one under the cursor. This works for (), [], {}, and <>.

[( - Go to previous opening parenthesis **(**

]) - Go to next closing parenthesis **)**

[{ - Go to previous opening parenthesis **{**

]} - Go to next closing parenthesis **}**

]m - Go to next start of method or function

]M - Go to next end of method or function

[m - Go to previous start of method or function

[M - Go to previous end of method or function

## Screen related movements

Ctrl+f - Scroll down one screen

Ctrl+b - Scroll up one screen

Ctrl+d - Scroll down half a screen

Ctrl+u - Scroll up half a screen

## Scrolling While Leaving Cursor In Place

zz - Place current cursor line in the center of the screen

zt - Place current cursor line at the top of the screen

zb - Place current cursor line at the bottom of the screen

Ctrl+E - Scroll down one line, keeping cursor in place

Ctrl+Y - Scroll up one line, keeping cursor in place

## Search Movements

/pattern - Search forward for the next occurrence of "pattern"

?pattern - Search backward for the next occurrence of "pattern"

starkey - Search forward for the next occurrence of the word under the cursor with \*

# - Search backward for the next occurrence of the word under the cursor

n - Repeat the last search in the same direction

N - Repeat the last search in the opposite direction

## Deletion

dw - Delete from the cursor to the start of the next word

de - Delete from the cursor to the end of the current word

dG - Delete from the cursor to the end of the file

d]} - Delete from the cursor to the next closing parenthesis, bracket, or brace

2dd - Delete the current line and the line below it (2 lines total)

## Undo and Redo

u - Undo the last action

Ctrl+r - Redo the last undone action

## Replacing & Deleting Characters

r{characters} - Replace the character under the cursor with {characters}

R - Enter replace mode, allowing you to overwrite existing text

x - Delete the character under the cursor

## Yanking (Copying) and Pasting

y{motion} - Yank (copy) text defined by {motion}. For example, "yw" yanks from the cursor to the start of the next word.

yy - Yank (copy) the current line

Y - Yank (copy) from the cursor to the end of the line

p - Paste the yanked text after the cursor

P - Paste the yanked text before the cursor

## Search/Replace

:%s/old/new/g - Replace all occurrences of "old" with "new" in the entire file

:%s/old/new/gc - Replace all occurrences of "old" with "new" in the entire file, with confirmation for each replacement

:%s/old/new/gi - Replace all occurrences of "old" with "new" in the entire file, ignoring case
