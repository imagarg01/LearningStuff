## Useful Commands

### Cursor Movement

#### One step

- h -> move cursor left one by one
- j -> move cursor down one by one
- k -> move cursor up one by one
- l -> move cursor right one by one

#### Page movement

- H -> move to top of screen
- M -> move to middle of screen
- L -> move to bottom of screen

- gg -> go the first line of document, if you want to move on a particular line for example
  '15gg' will move to 15th line upward movement.

- G -> go to the last line of document, if you want to move on a particualr line downwards for
  example '7G' will move to 7th line from top.

- } -> jump to next paragraph
- { -> jump to previous paragraph
- ctrl+e -> move screen down one line
- ctrl+y -> move screen up one line
- ctrl+b -> move back one full screen
- ctrl+f -> move forward one full screen

#### Line movement

- 0 -> jump to start of the line
- $ -> jump to end of the line

#### Word movement

- w -> move the cursor forward one word at a time. Prefix with number if you want to move
  multiple word at a time i.e. "3w" move 3 word at a time.
- b -> move the cursor backward one word at a time. Prefix with number if you want to move
  multiple word backward at a time i.e. "3b" move 3 word backward at a time.

#### Editing

- i -> insert mode before the cursor
- a -> insert mode after the cursor
- o -> insert mode on the next line
- O -> insert mode on the previous line
- x -> delete character under the cursor
- dd -> delete the line
- D -> delete from cursor to end of the line
- dw -> delete the word under the cursor
- d$ -> delete from cursor to end of the line
- d0 -> delete from cursor to start of the line
- u -> undo the last operation
- ctrl+r -> redo the last operation
- p -> paste the deleted text after the cursor
- P -> paste the deleted text before the cursor
- r -> replace the character under the cursor
- R -> replace the character under the cursor and keep replacing until you press 'esc'
- c -> change the character under the cursor
- cw -> change the word under the cursor
- c$ -> change from cursor to end of the line
- c0 -> change from cursor to start of the Line
- ctrl+g -> show the current line number and file name

#### Developers->Moving between parenthesis

While writing program we have to use () and {}. For Example if your cursor on a '{' and you
want to search where it has been closing press '%' it will take on closing '}'

```cmd
public class Factorial {
    public static void main(String[] args) {
        int num = 10;
        long factorial = 1;
        for(int i = 1; i <= num; ++i){
            // factorial = factorial * i;
            factorial *= i;
        }
        System.out.printf("Factorial of %d = %d", num, factorial);
    }
}
```

## Search

- /pattern -> search for pattern
- ?pattern -> search for pattern backward
- n -> repeat search in same direction
- N -> repeat search in opposite direction
