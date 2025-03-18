# Chess Game in Python

## Description
This is a simple command-line chess game implemented in Python. It allows two players to take turns making moves on an 8x8 chessboard, following the standard rules of chess. The game supports move validation for all pieces, move history tracking, and the ability to undo the last move.

## Features
- Fully functional chessboard with correct piece placement
- Move validation for all chess pieces
- Move history tracking
- Ability to undo the last move
- Console-based user interface

## Installation
To run this chess game, you need Python installed on your system. Follow these steps:

1. Clone the repository or download the source code:
   ```sh
   git clone <repository-url>
   ```
   or manually download the Python script.

2. Navigate to the project directory:
   ```sh
   cd chess-game
   ```

3. Run the game:
   ```sh
   python chess.py
   ```

## How to Play
1. The game starts with the standard chess piece setup.
2. Players take turns moving their pieces by entering coordinates in the format `A2 A3`.
3. The game checks if the move is valid and updates the board.
4. Players can type `undo` to revert the last move.
5. The game continues until checkmate, stalemate, or manual termination.

## Input Format
- Moves should be entered in algebraic notation, e.g., `E2 E4`.
- To undo a move, type `undo`.

## Example Game
```
  A B C D E F G H
8 r n b q k b n r 8
7 p p p p p p p p 7
6 . . . . . . . . 6
5 . . . . . . . . 5
4 . . . . . . . . 4
3 . . . . . . . . 3
2 P P P P P P P P 2
1 R N B Q K B N R 1
  A B C D E F G H

White to move: E2 E4
```

## License
This project is licensed under the MIT License.

## Author
[Your Name]

