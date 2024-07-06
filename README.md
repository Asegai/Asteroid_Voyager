# Asteroid Voyager

Welcome to **Asteroid Voyager**, a thrilling space adventure game built with Python and the Kivy framework.

## Features

- **Main Menu**:
  - Adjustable Difficulty Slider with Real-Time Feedback

- **Gameplay**:
  - **Player**: Control a spaceship using mouse movements. The spaceship gains various power-ups upon colliding with special asteroids.
  - **Enemies**: UFO enemies that move towards the player.
  - **Asteroids**: Various types of asteroids with unique effects:
    - Regular Asteroids: Cause the player to become invincible temporarily.
    - Exploding Asteroids: Clear all enemies upon collision.
    - Freeze Asteroids: Freeze the game for a few seconds upon collision, giving you time to orient yourself.
    - Radioactive Asteroids: Remove nearby enemies for a short duration.
  - **Boss Enemies**: Special enemy that spawns periodically.
  - **Score and High Score**: Track your score and your high score which is saved in a json file.

- **Background Music and Sound Effects**:
  - Background music during gameplay.
  - Sound effects for various actions, like asteroid and boss spawns.

- **Pause and Resume**: Pause the game with a pause button or by pressing 'P' on the keyboard.

## How to Play

1. **Download the Game**:
   - Download the entire game folder from the repository.

2. **Run the Game**:
   - Navigate to the downloaded folder.
   - Run the provided `start_game.cmd` file as an administrator. This file sets up the environment and ensures all dependencies are installed.
   - After running the `start_game.cmd`, execute the game with Python:
     ```sh
     python main.py
     ```
