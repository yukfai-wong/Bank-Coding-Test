import numpy as np
from typing import List, Tuple, Set, Any

def reverse_list(l: List[Any]) -> List[Any]:
    """
    Reverses the input list in-place.
    
    Parameters:
        l (List[Any]): The list to reverse.
        
    Returns:
        List[Any]: The reversed list.
    """
    length = len(l)          # Get the length of the list.
    mid = length // 2        # Only need to iterate halfway.
    last_idx = length - 1    # Calculate the last index of the list.
    for i in range(mid):
        # Swap the elements at the current index and its corresponding index from the end.
        l[i], l[last_idx - i] = l[last_idx - i], l[i]
    return l

def idx_prob(matrix: np.ndarray, idx: Tuple[int, int]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    For a given cell index in the sudoku matrix, extract its row, column, and corresponding 3x3 box.
    
    Parameters:
        matrix (np.ndarray): The sudoku board as a NumPy array.
        idx (Tuple[int, int]): A tuple representing the (row, column) index of the cell.
        
    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray]: Three arrays containing the values from the row, column, and 3x3 box.
    """
    r = matrix[idx[0], :]  # Get the entire row corresponding to the index.
    c = matrix[:, idx[1]]  # Get the entire column corresponding to the index.
    # Calculate the starting indices (top-left corner) of the 3x3 box.
    box_r = (idx[0] // 3) * 3  
    box_c = (idx[1] // 3) * 3
    # Extract the 3x3 box and flatten it to a one-dimensional array.
    box = matrix[box_r:box_r+3, box_c:box_c+3].flatten()
    return r, c, box

def is_valid_sudoku(matrix: np.ndarray) -> bool:
    """
    Checks if the provided sudoku board is valid.
    
    It validates the rows, columns, and 3x3 boxes by ensuring that there are no duplicate numbers 
    (ignoring zeros, which represent empty cells).
    
    Parameters:
        matrix (np.ndarray): The sudoku board as a NumPy array.
        
    Returns:
        bool: True if the board is valid, otherwise False.
    """
    # Check each row for duplicates (ignoring zeros)
    for row in matrix:
        non_zero = row[row != 0]  # Filter out zeros.
        if len(non_zero) != len(np.unique(non_zero)):
            return False  # Duplicate found in row.
            
    # Check each column for duplicates (ignoring zeros)
    for col in range(9):
        current_col = matrix[:, col]
        non_zero = current_col[current_col != 0]
        if len(non_zero) != len(np.unique(non_zero)):
            return False  # Duplicate found in column.
            
    # Check each 3x3 box for duplicates (ignoring zeros)
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box = matrix[box_row:box_row+3, box_col:box_col+3].flatten()
            non_zero = box[box != 0]
            if len(non_zero) != len(np.unique(non_zero)):
                return False  # Duplicate found in 3x3 box.
                
    return True  # All checks passed.

# Set of possible numbers for sudoku (1 to 9).
possible_int: Set[int] = set(range(1, 10))
def sudoku_ans_advise(matrix: np.ndarray, idx: Tuple[int, int]) -> Set[int]:
    """
    Suggests possible numbers for a given empty cell in the sudoku board.
    
    It calculates the possible numbers by excluding those already present in the cell's row, column, and 3x3 box.
    
    Parameters:
        matrix (np.ndarray): The sudoku board as a NumPy array.
        idx (Tuple[int, int]): A tuple representing the (row, column) index of the empty cell.
        
    Returns:
        Set[int]: A set of possible numbers that can be placed in the given cell.
    """
    # Get the row, column, and box values for the given index.
    r, c, box = idx_prob(matrix, idx)
    # Subtract numbers already present in row, column, and box from the set of all possible numbers.
    possible_ans = possible_int - set(r) - set(c) - set(box)
    return possible_ans

def solve_sudoku_attemp(matrix: np.ndarray, empty_index: List[Tuple[int, int]], empty_index_position: int) -> bool:
    """
    Recursively attempts to solve the sudoku puzzle using backtracking.
    
    Parameters:
        matrix (np.ndarray): The sudoku board as a NumPy array.
        empty_index (List[Tuple[int, int]]): A list of tuples where each tuple represents the (row, column) of an empty cell.
        empty_index_position (int): The current position in the empty_index list being attempted.
        
    Returns:
        bool: True if the sudoku can be solved, False otherwise.
    """
    # If all empty cells have been filled successfully, return True.
    if empty_index_position == len(empty_index):
        return True
        
    # Get possible answers for the current empty cell.
    step_answer = sudoku_ans_advise(matrix, empty_index[empty_index_position])
    for ans in step_answer:
        # Try a possible number in the current empty cell.
        matrix[empty_index[empty_index_position]] = ans
        # Recursively attempt to solve the rest of the sudoku.
        if solve_sudoku_attemp(matrix, empty_index, empty_index_position + 1):
            return True
    # Backtrack: reset the cell to 0 if no number leads to a solution.
    matrix[empty_index[empty_index_position]] = 0
    return False

def solve_sudoku(matrix: List[List[int]]) -> np.ndarray:
    """
    Solves the sudoku puzzle.
    
    It first converts the provided board into a NumPy array, validates the board, finds empty cells,
    and then uses backtracking to attempt to solve the puzzle.
    
    Parameters:
        matrix (List[List[int]]): The sudoku board represented as a 2D list.
        
    Returns:
        np.ndarray: The solved sudoku board as a NumPy array if solvable.
        
    Raises:
        ValueError: If the sudoku puzzle is unsolvable.
    """
    matrix_np = np.array(matrix)
    # Validate initial sudoku board.
    if not is_valid_sudoku(matrix_np):
        raise ValueError("Sudoku unsolveable")
        
    # Find indices of all empty cells (cells with value 0).
    empty_indices = np.where(matrix_np == 0)
    empty_index = list(zip(empty_indices[0], empty_indices[1]))
    
    # Attempt to solve the sudoku using backtracking.
    if solve_sudoku_attemp(matrix_np, empty_index, 0):
        return matrix_np
    raise ValueError("Sudoku unsolveable")
