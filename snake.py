import streamlit as st
import numpy as np

def initialize_game():
    board_size = 20
    initial_position = (board_size // 2, board_size // 2)
    st.session_state.snake = [initial_position]
    st.session_state.direction = 'right'
    st.session_state.food = (np.random.randint(0, board_size), np.random.randint(0, board_size))
    st.session_state.game_over = False
    st.session_state.board_size = board_size

def move_snake():
    head_x, head_y = st.session_state.snake[-1]
    direction = st.session_state.direction
    if direction == 'right':
        head_y += 1
    elif direction == 'left':
        head_y -= 1
    elif direction == 'up':
        head_x -= 1
    elif direction == 'down':
        head_x += 1

    new_head = (head_x, head_y)
    if new_head in st.session_state.snake or head_x < 0 or head_y < 0 or        head_x >= st.session_state.board_size or head_y >= st.session_state.board_size:
        st.session_state.game_over = True
    else:
        st.session_state.snake.append(new_head)
        if new_head == st.session_state.food:
            while new_head in st.session_state.snake:
                new_food = (np.random.randint(0, st.session_state.board_size), np.random.randint(0, st.session_state.board_size))
            st.session_state.food = new_food
        else:
            st.session_state.snake.pop(0)

def render_board():
    board = np.full((st.session_state.board_size, st.session_state.board_size), fill_value=' ')
    food_x, food_y = st.session_state.food
    board[food_x][food_y] = 'F'
    for (x, y) in st.session_state.snake:
        board[x][y] = 'S'
    board_display = '\n'.join([''.join(row) for row in board])
    st.text(board_display)

def handle_input(direction):
    opposite = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
    if direction != opposite[st.session_state.direction]:
        st.session_state.direction = direction

if 'snake' not in st.session_state:
    initialize_game()

st.title("Streamlit Snake Game")
if st.session_state.game_over:
    st.error("Game Over! Score: " + str(len(st.session_state.snake) - 1))
    if st.button("Restart Game"):
        initialize_game()
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Left", on_click=handle_input, args=('left',))
    with col2:
        st.button("Up", on_click=handle_input, args=('up',))
        st.button("Down", on_click=handle_input, args=('down',))
    with col3:
        st.button("Right", on_click=handle_input, args=('right',))
    move_snake()
    render_board()
