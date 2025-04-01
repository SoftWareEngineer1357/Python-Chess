class Basic:
    """
    Базовый класс для всех шахматных фигур.
    
    Атрибуты:
        color (str): Цвет фигуры ('white' или 'black').
    """
    def __init__(self, color):
        self.color = color  # цвет фигуры
        self.has_moved = False  #отметка для отслеживания, двигалась ли фигура

    def __str__(self):
        """
        Возвращает:
            str: Символ фигуры.
        """
        return self.symbol.upper() if self.color == 'white' else self.symbol.lower()


class King(Basic):
    """
    Класс, представляющий короля.
    
    Атрибуты:
        symbol (str): Символ короля ('k').
    """
    symbol = 'k'
    
    def is_valid_move(self, start, end):
        """
        Проверяет, является ли ход короля допустимым.
        
        Король может двигаться на одну клетку в любом направлении.
        """
        dx = abs(start[0] - end[0])  # Разница по строкам
        dy = abs(start[1] - end[1])  # Разница по столбцам
        
        # Король может двигаться на одну клетку в любом направлении
        if max(dx, dy) == 1:
            return True
        return False


class Queen(Basic):
    """
    Класс, представляющий ферзя.
    
    Атрибуты:
        symbol (str): Символ ферзя ('q').
    """
    symbol = 'q'
    
    def is_valid_move(self, board, start, end):
        """
        Проверяет, является ли ход ферзя допустимым.
        
        Ферзь может двигаться как ладья или слон.
        """
        # Проверяем ход как ладья или слон
        return Rook(self.color).is_valid_move(board, start, end) or Bishop(self.color).is_valid_move(board, start, end)


class Rook(Basic):
    """
    Класс, представляющий ладью.
    
    Атрибуты:
        symbol (str): Символ ладьи ('r').
    """
    symbol = 'r' 
    
    def is_valid_move(self, board, start, end):
        """
        Проверяет, является ли ход ладьи допустимым.
        
        Ладья может двигаться по горизонтали или вертикали.
        """
        if start[0] == end[0]:
            step = 1 if end[1] > start[1] else -1  # направление движения
            for y in range(start[1] + step, end[1], step):
                if board[start[0]][y] is not None:
                    return False  # если путь не свободен, ход недопустим
        elif start[1] == end[1]:  # вертикальное движение
            step = 1 if end[0] > start[0] else -1  # направление движения
            for x in range(start[0] + step, end[0], step):
                if board[x][start[1]] is not None:
                    return False  # если путь не свободен, ход недопустим
        else:
            return False  # если движение не по горизонтали или вертикали, ход недопустим
        return True  # ход допустим


class Bishop(Basic):
    """
    Класс, представляющий слона.
    
    Атрибуты:
        symbol (str): Символ слона ('b').
    """
    symbol = 'b'
    
    def is_valid_move(self, board, start, end):
        """
        Проверяет, является ли ход слона допустимым.
        
        Слон может двигаться по диагонали.
        """
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        if abs(dx) != abs(dy):  # движение не по диагонали
            return False
        step_x = 1 if dx > 0 else - 1  # направление по строкам
        step_y = 1 if dy > 0 else - 1  # направление по столбцам
        x, y = start[0] + step_x, start[1] + step_y
        while x != end[0] and y != end[1]:
            if board[x][y] is not None:
                return False  # если путь не свободен, ход недопустим
            x += step_x
            y += step_y
        return True


class Knight(Basic):
    """
    Класс, представляющий коня.
    
    Атрибуты:
        symbol (str): Символ коня ('n').
    """
    symbol = 'n'
    
    def is_valid_move(self, board, start, end):
        """
        Проверяет, является ли ход коня допустимым.
        
        Конь может двигаться буквой "Г".
        """
        dx = abs(start[0] - end[0])
        dy = abs(start[1] - end[1])
        return (dx, dy) in [(2, 1), (1, 2)] 


class Pawn(Basic):
    """
    Класс, представляющий пешку.
    
    Атрибуты:
        symbol (str): Символ пешки ('p').
    """
    symbol = 'p'
    
    def is_valid_move(self, board, start, end):
        """
        Проверяет, является ли ход пешки допустимым.
        
        Пешка может двигаться вперед на одну или две клетки (с начальной позиции)
        и бить по диагонали.
        """
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        direction = 1 if self.color == 'white' else -1

        # ход пешки на одну клетку вперед
        if dx == direction and dy == 0 and board[end[0]][end[1]] is None:
            return True
        # ход пешки на две клетки вперед в начале игры
        if dx == 2 * direction and dy == 0 and start[0] == (1 if self.color == 'white' else 6) and board[end[0]][end[1]] is None:
            if board[start[0] + direction][start[1]] is None:
                return True
        # ход по диагонали
        if dx == direction and abs(dy) == 1 and board[end[0]][end[1]] is not None and board[end[0]][end[1]].color != self.color:
            return True
        return False  #если ход неправильный то, код вернет False

class Move:
    """
    Класс для хранения информации о ходе.
    
    Атрибуты:
        start (tuple): Начальная позиция (строка, столбец).
        end (tuple): Конечная позиция (строка, столбец).
        piece (Piece): Фигура, которая совершила ход.
        captured_piece (Piece): Фигура, которая была взята (если есть).
    """
    def __init__(self, start, end, piece, captured_piece=None):
        self.start = start
        self.end = end
        self.piece = piece
        self.captured_piece = captured_piece


class Board:
    """
    Класс, представляющий шахматную доску.
    
    Атрибуты:
        board (list): Двумерный список, представляющий доску.
        history (list): Список ходов, совершенных в партии.
    """
    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)] 
        self.history = []
        self.white_moves = 0 
        self.black_moves = 0
        self.setup_pieces()  # расстановка фигур на доске

    def setup_pieces(self):
        """
        Расставляет фигуры на доске в начальной позиции.
        """
        for i in range(8):
            self.board[1][i] = Pawn('white') 
            self.board[6][i] = Pawn('black') 
        
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i, piece in enumerate(piece_order):
            self.board[0][i] = piece('white')  # белые фигуры на первой строке
            self.board[7][i] = piece('black')  # черные фигуры на восьмой строке

    def print_board(self):
        """
        Выводит текущее состояние доски в консоль.
        """
        print("  A B C D E F G H")
        for i in range(8):
            print(8 - i, ' '.join([str(p) if p else '.' for p in self.board[i]]), 8 - i)
        print("  A B C D E F G H")

    def move_piece(self, start, end):
        """
        Выполняет ход фигуры с начальной позиции на конечную.
        
        Аргументы:
            start (tuple): Начальная позиция (строка, столбец).
            end (tuple): Конечная позиция (строка, столбец).
        
        Возвращает:
            bool: True, если ход выполнен успешно, иначе False.
        """
        piece = self.board[start[0]][start[1]]
        if piece is None:
            return False
        target_piece = self.board[end[0]][end[1]]
        if target_piece is not None and target_piece.color == piece.color:
            return False
        if not piece.is_valid_move(self.board, start, end):
            return False

        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = None
        piece.has_moved = True
        
        if piece.color == 'white':
            self.white_moves += 1
        else:
            self.black_moves += 1
            
        self.history.append(Move(start, end, piece, target_piece))
        return True

    def undo_move(self):
        """
        Откатывает последний ход и уменьшает счетчик ходов.
        """
        if not self.history:
            return False
        
        last_move = self.history.pop()
        start = last_move.start
        end = last_move.end
        piece = last_move.piece
        captured_piece = last_move.captured_piece
        
        self.board[start[0]][start[1]] = piece
        self.board[end[0]][end[1]] = captured_piece
        
        if piece.color == 'white':
            self.white_moves -= 1
        else:
            self.black_moves -= 1
            
        if not self.history:
            piece.has_moved = False
        
        return True


def parse_input(input_str):
    """
    Преобразует строку ввода (например, "E2") в координаты доски (строка, столбец).
    
    Аргументы:
        input_str (str): Строка ввода (например, "E2").
    
    Возвращает:
        tuple: Координаты (строка, столбец) или None, если ввод некорректен.
    """
    try:
        x = 8 - int(input_str[1])
        y = ord(input_str[0].upper()) - ord('A')  # Преобразуем букву в индекс (от 0 до 7)
        return (x, y)  # Возвращаем координаты
    except (IndexError, ValueError):
        return None  # Если ввод некорректен, возвращаем None


def play_game():
    """
    Основной цикл игры с отображением количества ходов.
    """
    board = Board()
    current_player = 'white'
    
    while True:
        board.print_board()
        print(f"\nХод игрока {current_player}.")
        print(f"Ходов белых: {board.white_moves} | Ходов черных: {board.black_moves}")
        
        move = input("Введите ход (например, A7 A5) или 'undo' для шага назад: ").strip().split()
        
        if len(move) == 1 and move[0].lower() == 'undo':
            if not board.undo_move():
                print("Невозможно откатить ход.")
            else:
                current_player = 'black' if current_player == 'white' else 'white'
            continue
            
        if len(move) != 2:
            print("Неверный формат хода.")
            continue
            
        start = parse_input(move[0])
        end = parse_input(move[1])
        if start is None or end is None:
            print("Неверные координаты.")
            continue
            
        if not board.move_piece(start, end):
            print("Недопустимый ход.")
            continue
            
        current_player = 'black' if current_player == 'white' else 'white'

play_game()