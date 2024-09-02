import streamlit as st
import numpy as np
import time

# Game settings
GRID_SIZE = 20
INITIAL_SNAKE_LENGTH = 3
SPEED = 0.2  # seconds between movements

# Direction constants
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

# Initialize the game state
if 'snake' not in st.session_state:
    st.session_state.snake = [(0, i) for i in range(INITIAL_SNAKE_LENGTH)]
    st.session_state.direction = RIGHT
    st.session_state.food = (np.random.randint(0, GRID_SIZE), np.random.randint(0, GRID_SIZE))
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.last_update = time.time()

# Function to move the snake
def move_snake():
    new_head = (st.session_state.snake[0][0] + st.session_state.direction[0],
                st.session_state.snake[0][1] + st.session_state.direction[1])

    # Check for collisions with walls
    if (new_head[0] < 0 or new_head[0] >= GRID_SIZE or
        new_head[1] < 0 or new_head[1] >= GRID_SIZE):
        st.session_state.game_over = True
        return

    # Check for collisions with itself
    if new_head in st.session_state.snake:
        st.session_state.game_over = True
        return

    # Move snake
    st.session_state.snake = [new_head] + st.session_state.snake[:-1]

    # Check if food is eaten
    if new_head == st.session_state.food:
        st.session_state.snake.append(st.session_state.snake[-1])  # Grow the snake
        st.session_state.food = (np.random.randint(0, GRID_SIZE), np.random.randint(0, GRID_SIZE))
        st.session_state.score += 1

# Function to draw the grid
def draw_grid():
    grid = np.zeros((GRID_SIZE, GRID_SIZE, 3), dtype=int)

    # Draw the snake (green color, fully opaque)
    for segment in st.session_state.snake:
        grid[segment] = [0, 255, 0]  # RGB Green

    # Draw the food (red color, fully opaque)
    grid[st.session_state.food] = [255, 0, 0]  # RGB Red

    return grid

# Streamlit UI
st.title("Snake Game")
st.text(f"Score: {st.session_state.score}")

# Capture user input for direction
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Left"):
        if st.session_state.direction != RIGHT:  # Prevent moving in the opposite direction
            st.session_state.direction = LEFT
with col2:
    if st.button("Up"):
        if st.session_state.direction != DOWN:  # Prevent moving in the opposite direction
            st.session_state.direction = UP
with col3:
    if st.button("Right"):
        if st.session_state.direction != LEFT:  # Prevent moving in the opposite direction
            st.session_state.direction = RIGHT
if st.button("Down"):
    if st.session_state.direction != UP:  # Prevent moving in the opposite direction
        st.session_state.direction = DOWN

# Game loop
if not st.session_state.game_over:
    current_time = time.time()

    # Update only if enough time has passed (for the speed control)
    if current_time - st.session_state.last_update >= SPEED:
        move_snake()
        st.session_state.last_update = current_time

    grid = draw_grid()
    st.image(grid, width=300)

    # Simulate a delay for the game loop
    time.sleep(SPEED)

    # Add an empty placeholder to trigger a rerun without st.experimental_rerun()
    st.empty()

else:
    st.error("Game Over! Refresh the page to restart.")
