class Piece:
    """
    Базовый класс для всех шахматных фигур.
    
    Атрибуты:
        color (str): Цвет фигуры ('white' или 'black').
    """
    def __init__(self, color):
        self.color = color
        self.has_moved = False  # Добавляем флаг для отслеживания движения фигуры
    
    def is_valid_move(self, board, start, end):
        """
        Проверяет, является ли ход фигуры допустимым.
        
        Аргументы:
            board (list): Шахматная доска (двумерный список).
            start (tuple): Начальная позиция фигуры (строка, столбец).
            end (tuple): Конечная позиция фигуры (строка, столбец).
        
        Возвращает:
            bool: True, если ход допустим, иначе False.
        """
        raise NotImplementedError

    def __str__(self):
        """
        Возвращает символ фигуры.
        
        Возвращает:
            str: Символ фигуры.
        """
        return self.symbol

class King(Piece):
    """
    Класс, представляющий короля.
    
    Атрибуты:
        symbol (str): Символ короля ('K').
    """
    symbol = 'K'
    
    def is_valid_move(self, board, start, end):
        """
        Проверяет, является ли ход короля допустимым.
        
        Король может двигаться на одну клетку в любом направлении или выполнять рокировку.
        """
        dx = abs(start[0] - end[0])
        dy = abs(start[1] - end[1])
        
        # Обычный ход короля
        if max(dx, dy) == 1:
            return True
        
        # Рокировка
        if dx == 0 and abs(dy) == 2:
            # Проверяем, что король и ладья не двигались
            if self.has_moved:
                return False
            # Определяем направление рокировки
            direction = 1 if dy > 0 else -1
            # Проверяем, что путь свободен
            for y in range(start[1] + direction, end[1], direction):
                if board[start[0]][y] is not None:
                    return False
            # Проверяем, что ладья на месте и не двигалась
            rook_y = 7 if direction == 1 else 0
            rook = board[start[0]][rook_y]
            if not isinstance(rook, Rook) or rook.has_moved:
                return False
            return True
        
        return False

class Queen(Piece):
    """
    Класс, представляющий ферзя.
    
    Атрибуты:
        symbol (str): Символ ферзя ('Q').
    """
    symbol = 'Q'
    
    def is_valid_move(self, board, start, end):
        """
        Проверяет, является ли ход ферзя допустимым.
        
        Ферзь может двигаться как ладья или слон.
        """
        return Rook(self.color).is_valid_move(board, start, end) or Bishop(self.color).is_valid_move(board, start, end)

class Rook(Piece):
    """
    Класс, представляющий ладью.
    
    Атрибуты:
        symbol (str): Символ ладьи ('R').
    """
    symbol = 'R'
    
    def is_valid_move(self, board, start, end):
        """
        Проверяет, является ли ход ладьи допустимым.
        
        Ладья может двигаться по горизонтали или вертикали.
        """
        if start[0] == end[0]:  # Горизонтальное движение
            step = 1 if end[1] > start[1] else -1
            for y in range(start[1] + step, end[1], step):
                if board[start[0]][y] is not None:
                    return False
        elif start[1] == end[1]:  # Вертикальное движение
            step = 1 if end[0] > start[0] else -1
            for x in range(start[0] + step, end[0], step):
                if board[x][start[1]] is not None:
                    return False
        else:
            return False
        return True

class Bishop(Piece):
    """
    Класс, представляющий слона.
    
    Атрибуты:
        symbol (str): Символ слона ('B').
    """
    symbol = 'B'
    
    def is_valid_move(self, board, start, end):
        """
        Проверяет, является ли ход слона допустимым.
        
        Слон может двигаться по диагонали.
        """
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        if abs(dx) != abs(dy):
            return False
        step_x = 1 if dx > 0 else -1
        step_y = 1 if dy > 0 else -1
        x, y = start[0] + step_x, start[1] + step_y
        while x != end[0] and y != end[1]:
            if board[x][y] is not None:
                return False
            x += step_x
            y += step_y
        return True

class Knight(Piece):
    """
    Класс, представляющий коня.
    
    Атрибуты:
        symbol (str): Символ коня ('N').
    """
    symbol = 'N'
    
    def is_valid_move(self, board, start, end):
        """
        Проверяет, является ли ход коня допустимым.
        
        Конь может двигаться буквой "Г".
        """
        dx = abs(start[0] - end[0])
        dy = abs(start[1] - end[1])
        return (dx, dy) in [(2, 1), (1, 2)]

class Pawn(Piece):
    """
    Класс, представляющий пешку.
    
    Атрибуты:
        symbol (str): Символ пешки ('P').
    """
    symbol = 'P'
    
    def is_valid_move(self, board, start, end):
        """
        Проверяет, является ли ход пешки допустимым.
        
        Пешка может двигаться вперед на одну или две клетки (с начальной позиции)
        и бить по диагонали.
        """
        direction = 1 if self.color == 'white' else -1
        dx, dy = end[0] - start[0], end[1] - start[1]

        # Движение вперед на одну клетку
        if dx == direction and dy == 0 and board[end[0]][end[1]] is None:
            return True
        # Движение вперед на две клетки (только с начальной позиции)
        if dx == 2 * direction and dy == 0 and start[0] == (1 if self.color == 'white' else 6) and board[end[0]][end[1]] is None:
            # Проверяем, что путь свободен
            if board[start[0] + direction][start[1]] is None:
                return True
        # Бить по диагонали
        if dx == direction and abs(dy) == 1 and board[end[0]][end[1]] is not None and board[end[0]][end[1]].color != self.color:
            return True
        return False

class Board:
    """
    Класс, представляющий шахматную доску.
    
    Атрибуты:
        board (list): Двумерный список, представляющий доску.
    """
    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]
        self.setup_pieces()
    
    def setup_pieces(self):
        """
        Расставляет фигуры на доске в начальной позиции.
        """
        for i in range(8):
            self.board[1][i] = Pawn('white')
            self.board[6][i] = Pawn('black')
        
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i, piece in enumerate(piece_order):
            self.board[0][i] = piece('white')
            self.board[7][i] = piece('black')
    
    def print_board(self):
        """
        Выводит текущее состояние доски в консоль.
        """
        print('  A B C D E F G H')
        for i in range(8):
            row = [str(self.board[i][j]) if self.board[i][j] else '.' for j in range(8)]
            print(f'{8 - i} ' + ' '.join(row) + f' {8 - i}')
        print('  A B C D E F G H')
    
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
        
        # Рокировка
        if isinstance(piece, King) and abs(start[1] - end[1]) == 2:
            direction = 1 if end[1] > start[1] else -1
            rook_y = 7 if direction == 1 else 0
            rook = self.board[start[0]][rook_y]
            # Перемещаем короля
            self.board[end[0]][end[1]] = piece
            self.board[start[0]][start[1]] = None
            # Перемещаем ладью
            self.board[start[0]][start[1] + direction] = rook
            self.board[start[0]][rook_y] = None
            # Отмечаем, что король и ладья двигались
            piece.has_moved = True
            rook.has_moved = True
            return True
        
        # Обычный ход
        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = None
        piece.has_moved = True
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
        x = 8 - int(input_str[1])  # Преобразуем номер строки в индекс
        y = ord(input_str[0].upper()) - ord('A')  # Преобразуем букву в индекс
        return (x, y)
    except (IndexError, ValueError):
        return None

def play_game():
    """
    Основной цикл игры. Позволяет двум игрокам поочередно делать ходы.
    """
    board = Board()
    current_player = 'white'
    
    while True:
        board.print_board()
        print(f"Ход игрока {current_player}.")
        move = input("Введите ход (например, E2 E4 или O-O/O-O-O): ").strip().split()
        
        if len(move) == 1 and move[0].upper() in ['O-O', 'O-O-O']:
            # Обработка рокировки
            king_row = 0 if current_player == 'white' else 7
            king_start = (king_row, 4)
            if move[0].upper() == 'O-O':
                king_end = (king_row, 6)
            else:
                king_end = (king_row, 2)
            if not board.move_piece(king_start, king_end):
                print("Недопустимая рокировка. Попробуйте снова.")
                continue
        else:
            # Обычный ход
            if len(move) != 2:
                print("Неверный формат хода. Попробуйте снова.")
                continue
            start = parse_input(move[0])
            end = parse_input(move[1])
            if start is None or end is None:
                print("Неверные координаты. Попробуйте снова.")
                continue
            if not board.move_piece(start, end):
                print("Недопустимый ход. Попробуйте снова.")
                continue
        
        # Смена игрока
        current_player = 'black' if current_player == 'white' else 'white'

# Запуск игры
play_game()