# AI Project 3 - Tic Tac Toe
Generalized Tic Tac Toe - an n by n board game where each player chooses one of the parts X or O, and then playsin an alternate order to placehischoice on the board. A player wins when they are able to place m consecutive symbols (0s or Xs) in a contiguous sequence (row, column or diagonal). The game may end in a draw when no one wins. 

## Implementation
The following program is written in Python programming language. The reasons behind this choice were **faster execution** ,**variety of libraries.** Two .py files were created: tic_tac_toe.py comprises of the overall tic tac toe game logic, requester.py comprises of the API requests used within the tic_tac_toe file to run the game on the API.
Libraries used:

- copy
- time
- numpy
- collections


## Requirements
- [Python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [Minimax](https://en.wikipedia.org/wiki/Minimax)


## How to run
First of all make sure you have Python installed on your computer. Then access the folder where you store both **.py** files from cmd. Next step you have to run the **tic_tac_toe.py file** and write down the inputs accordingly:

```bash
tic_tac_toe.py

Enter Game ID if joining another game. To create your own, enter 0:

Enter n and m for an n x n game with target m:

Please enter opponent team id:

Play as X (if entering someone's game) or O (if game is your own)?
```
