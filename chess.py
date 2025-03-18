class Piece:
    """
    Базовый класс для всех шахматных фигур.
    
    Атрибуты:
        color (str): Цвет фигуры ('white' или 'black').
    """
    def __init__(self, color):
        self.color = color  # Инициализация цвета фигуры
        self.has_moved = False  # Флаг для отслеживания, двигалась ли фигура

    def __str__(self):
        """
        Возвращает:
            str: Символ фигуры.
        """
        # Возвращаем символ в верхнем регистре для белых фигур и в нижнем для черных
        return self.symbol.upper() if self.color == 'white' else self.symbol.lower()


class King(Piece):
    """
    Класс, представляющий короля.
    
    Атрибуты:
        symbol (str): Символ короля ('k').
    """
    symbol = 'k'  # Символ короля (в нижнем регистре для черных)
    
    def is_valid_move(self, board, start, end):
        """
        Проверяет, является ли ход короля допустимым.
        
        Король может двигаться на одну клетку в любом направлении.
        """
        dx = abs(start[0] - end[0])  # Разница по строкам
        dy = abs(start[1] - end[1])  # Разница по столбцам
        
        # Король может двигаться на одну клетку в любом направлении
        if max(dx, dy) == 1:
            return True
        
        return False  # Если ход не соответствует правилам, возвращаем False


class Queen(Piece):
    """
    Класс, представляющий ферзя.
    
    Атрибуты:
        symbol (str): Символ ферзя ('q').
    """
    symbol = 'q'  # Символ ферзя (в нижнем регистре для черных)
    
    def is_valid_move(self, board, start, end):
        """
        Проверяет, является ли ход ферзя допустимым.
        
        Ферзь может двигаться как ладья или слон.
        """
        # Проверяем ход как ладья или слон
        return Rook(self.color).is_valid_move(board, start, end) or Bishop(self.color).is_valid_move(board, start, end)


class Rook(Piece):
    """
    Класс, представляющий ладью.
    
    Атрибуты:
        symbol (str): Символ ладьи ('r').
    """
    symbol = 'r'  # Символ ладьи (в нижнем регистре для черных)
    
    def is_valid_move(self, board, start, end):
        """
        Проверяет, является ли ход ладьи допустимым.
        
        Ладья может двигаться по горизонтали или вертикали.
        """
        if start[0] == end[0]:  # Горизонтальное движение
            step = 1 if end[1] > start[1] else -1  # Направление движения
            for y in range(start[1] + step, end[1], step):
                if board[start[0]][y] is not None:
                    return False  # Если путь не свободен, ход недопустим
        elif start[1] == end[1]:  # Вертикальное движение
            step = 1 if end[0] > start[0] else -1  # Направление движения
            for x in range(start[0] + step, end[0], step):
                if board[x][start[1]] is not None:
                    return False  # Если путь не свободен, ход недопустим
        else:
            return False  # Если движение не по горизонтали или вертикали, ход недопустим
        return True  # Ход допустим


class Bishop(Piece):
    """
    Класс, представляющий слона.
    
    Атрибуты:
        symbol (str): Символ слона ('b').
    """
    symbol = 'b'  # Символ слона (в нижнем регистре для черных)
    
    def is_valid_move(self, board, start, end):
        """
        Проверяет, является ли ход слона допустимым.
        
        Слон может двигаться по диагонали.
        """
        dx = end[0] - start[0]  # Разница по строкам
        dy = end[1] - start[1]  # Разница по столбцам
        if abs(dx) != abs(dy):  # Если движение не по диагонали
            return False
        step_x = 1 if dx > 0 else -1  # Направление по строкам
        step_y = 1 if dy > 0 else -1  # Направление по столбцам
        x, y = start[0] + step_x, start[1] + step_y
        while x != end[0] and y != end[1]:
            if board[x][y] is not None:
                return False  # Если путь не свободен, ход недопустим
            x += step_x
            y += step_y
        return True  # Ход допустим


class Knight(Piece):
    """
    Класс, представляющий коня.
    
    Атрибуты:
        symbol (str): Символ коня ('n').
    """
    symbol = 'n'  # Символ коня (в нижнем регистре для черных)
    
    def is_valid_move(self, board, start, end):
        """
        Проверяет, является ли ход коня допустимым.
        
        Конь может двигаться буквой "Г".
        """
        dx = abs(start[0] - end[0])  # Разница по строкам
        dy = abs(start[1] - end[1])  # Разница по столбцам
        return (dx, dy) in [(2, 1), (1, 2)]  # Ход допустим, если соответствует правилам коня


class Pawn(Piece):
    """
    Класс, представляющий пешку.
    
    Атрибуты:
        symbol (str): Символ пешки ('p').
    """
    symbol = 'p'  # Символ пешки (в нижнем регистре для черных)
    
    def is_valid_move(self, board, start, end):
        """
        Проверяет, является ли ход пешки допустимым.
        
        Пешка может двигаться вперед на одну или две клетки (с начальной позиции)
        и бить по диагонали.
        """
        direction = 1 if self.color == 'white' else -1  # Направление движения пешки
        dx, dy = end[0] - start[0], end[1] - start[1]  # Разница по строкам и столбцам

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
        return False  # Если ход не соответствует правилам, возвращаем False

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
        self.history = []  # история ходов
        self.setup_pieces()  # раставление фигур на доске

    def setup_pieces(self):
        """
        Расставляет фигуры на доске в начальной позиции.
        """
        for i in range(8):
            self.board[1][i] = Pawn('white')  # белые пешки на второй строке
            self.board[6][i] = Pawn('black')  # черные пешки на седьмой строке
        
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]  # Порядок фигур
        for i, piece in enumerate(piece_order):
            self.board[0][i] = piece('white')  # белые фигуры на первой строке
            self.board[7][i] = piece('black')  # черные фигуры на восьмой строке

    def print_board(self):
        """
        Выводит текущее состояние доски в консоль.
        """
        print('  A B C D E F G H')  
        for i in range(8):
            row = [str(self.board[i][j]) if self.board[i][j] else '.' for j in range(8)]  # Формируем строку доски
            print(f'{8 - i} ' + ' '.join(row) + f' {8 - i}')  # Выводим строку с номерами строк
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
        piece = self.board[start[0]][start[1]]  # Получаем фигуру из начальной позиции
        if piece is None:
            return False  # Если фигуры нет, ход невозможен
        target_piece = self.board[end[0]][end[1]]  # Получаем фигуру в конечной позиции
        if target_piece is not None and target_piece.color == piece.color:
            return False  # Если в конечной позиции фигура того же цвета, ход невозможен
        if not piece.is_valid_move(self.board, start, end):
            return False  # Если ход недопустим, возвращаем False

        # Обычный ход
        self.board[end[0]][end[1]] = piece  # Перемещаем фигуру на конечную позицию
        self.board[start[0]][start[1]] = None  # Убираем фигуру с начальной позиции
        piece.has_moved = True  # Отмечаем, что фигура двигалась
        # Добавляем ход в историю
        self.history.append(Move(start, end, piece, target_piece))
        return True  # Ход выполнен успешно

    def undo_move(self):
        """
        Откатывает последний ход.
        
        Возвращает:
            bool: True, если откат выполнен успешно, иначе False.
        """
        if not self.history:
            return False  # Если история пуста, откат невозможен
        
        last_move = self.history.pop()  # Получаем последний ход из истории
        start, end, piece, captured_piece = last_move.start, last_move.end, last_move.piece, last_move.captured_piece
        
        # Возвращаем фигуру на начальную позицию
        self.board[start[0]][start[1]] = piece
        self.board[end[0]][end[1]] = captured_piece
        
        # Отмечаем, что фигура больше не двигалась (если это был первый ход)
        if not self.history:
            piece.has_moved = False
        
        return True  # Откат выполнен успешно


def parse_input(input_str):
    """
    Преобразует строку ввода (например, "E2") в координаты доски (строка, столбец).
    
    Аргументы:
        input_str (str): Строка ввода (например, "E2").
    
    Возвращает:
        tuple: Координаты (строка, столбец) или None, если ввод некорректен.
    """
    try:
        x = 8 - int(input_str[1])  # Преобразуем номер строки в индекс (от 0 до 7)
        y = ord(input_str[0].upper()) - ord('A')  # Преобразуем букву в индекс (от 0 до 7)
        return (x, y)  # Возвращаем координаты
    except (IndexError, ValueError):
        return None  # Если ввод некорректен, возвращаем None


def play_game():
    """
    Основной цикл игры. Позволяет двум игрокам поочередно делать ходы.
    """
    board = Board()  # Создаем доску
    current_player = 'white'  # Начинает белый игрок
    
    while True:
        board.print_board()  # Выводим доску
        print(f"Ход игрока {current_player}.")  # Указываем, чей ход
        move = input("Введите ход (например, A7 A5) или 'undo' для шага назад: ").strip().split()  # Получаем ввод от игрока
        
        if len(move) == 1 and move[0].lower() == 'undo':
            # Откат хода
            if not board.undo_move():
                print("Невозможно откатить ход.")
            else:
                current_player = 'black' if current_player == 'white' else 'white'  # Передаем ход другому игроку
            continue
        
        # Обычный ход
        if len(move) != 2:
            print("Неверный формат хода.")
            continue
        start = parse_input(move[0])  # Преобразуем начальную позицию
        end = parse_input(move[1])  # Преобразуем конечную позицию
        if start is None or end is None:
            print("Неверные координаты.")
            continue
        if not board.move_piece(start, end):
            print("Недопустимый ход.")
            continue
        
        current_player = 'black' if current_player == 'white' else 'white' 

play_game() 