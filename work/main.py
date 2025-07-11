import pygame
import sys
import random
# !!! PHASE 2: Import the Paddle class from our new file.
# !!! PHASE 3: Import the Ball class as well.
# !!! PHASE 4: Import the Brick class as well.
# !!! PHASE 7: Import the PowerUp class as well.
# !!! PHASE 9: Import the Laser class as well.
# !!! PHASE 11: Import the Particle and Firework classes as well.
from game_objects import Paddle, Ball, Brick, PowerUp, Laser, Particle, Firework

# -- General Setup --
# This is the basic setup that initializes all the modules required for PyGame.
# We also need to set up a clock to control the frame rate of our game.
pygame.init()
# !!! PHASE 8: Initialize the mixer module for sound
pygame.mixer.init()
clock = pygame.time.Clock()

# -- Screen Setup --
# Here we define the dimensions of our game window.
# Using variables for width and height makes it easier to change them later.
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# We can set a caption for the window to give our game a title.
pygame.display.set_caption("PyGame Arkanoid")

# !!! PHASE 2: Colors --
BG_COLOR = pygame.Color('grey12')
# !!! PHASE 4: Brick colors
BRICK_COLORS = [(178, 34, 34), (255, 165, 0), (255, 215, 0), (50, 205, 50)] # Red, Orange, Yellow, Green

# !!! PHASE 5: Font Setup --
# We need a font to display messages on the screen.
game_font = pygame.font.Font(None, 40)
# !!! PHASE 10: Message font for power-up notifications
message_font = pygame.font.Font(None, 30)
# !!! PHASE 12: Title screen font
title_font = pygame.font.Font(None, 70)

# !!! NEW: Sound Management --
sound_enabled = True  # Global mute toggle

class SoundManager:
    """Manages all game sounds with mute functionality"""
    def __init__(self):
        self.enabled = True
        
    def play_sound(self, sound):
        """Play sound only if sound is enabled"""
        if self.enabled and sound_enabled:
            sound.play()
    
    def toggle_mute(self):
        """Toggle mute on/off"""
        global sound_enabled
        sound_enabled = not sound_enabled
        return sound_enabled

sound_manager = SoundManager()

# !!! PHASE 8: Sound Setup --
# Load your sound files here. Make sure they are in the same directory as your script.
try:
    bounce_sound = pygame.mixer.Sound('bounce.wav')
    brick_break_sound = pygame.mixer.Sound('brick_break.wav')
    game_over_sound = pygame.mixer.Sound('game_over.wav')
    laser_sound = pygame.mixer.Sound('laser.wav')
except pygame.error as e:
    print(f"Warning: Sound file not found. {e}")
    # Create dummy sound objects if files are not found, so the game doesn't crash
    class DummySound:
        def play(self): pass
    bounce_sound = DummySound()
    brick_break_sound = DummySound()
    game_over_sound = DummySound()
    laser_sound = DummySound()

# !!! PHASE 2: Game Objects --
# Now, instead of a simple Rect, we create an *instance* of our Paddle class.
paddle = Paddle(screen_width, screen_height)
# !!! PHASE 3: Create a Ball instance
ball = Ball(screen_width, screen_height)

# !!! NEW: Level Management --
current_level = 1
max_levels = 5

def create_brick_wall(level=1):
    """Create different brick patterns for each level"""
    bricks = []
    brick_width = 75
    brick_height = 20
    brick_padding = 5
    wall_start_y = 50
    
    if level == 1:
        # Level 1: Simple 4x10 grid
        brick_rows = 4
        brick_cols = 10
        for row in range(brick_rows):
            for col in range(brick_cols):
                x = col * (brick_width + brick_padding) + brick_padding
                y = row * (brick_height + brick_padding) + wall_start_y
                color = BRICK_COLORS[row % len(BRICK_COLORS)]
                bricks.append(Brick(x, y, brick_width, brick_height, color))
    
    elif level == 2:
        # Level 2: Diamond pattern
        brick_cols = 10
        pattern = [
            [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 0, 0]
        ]
        for row in range(len(pattern)):
            for col in range(len(pattern[row])):
                if pattern[row][col]:
                    x = col * (brick_width + brick_padding) + brick_padding
                    y = row * (brick_height + brick_padding) + wall_start_y
                    color = BRICK_COLORS[row % len(BRICK_COLORS)]
                    bricks.append(Brick(x, y, brick_width, brick_height, color))
    
    elif level == 3:
        # Level 3: Pyramid pattern
        brick_cols = 10
        for row in range(6):
            start_col = row
            end_col = brick_cols - row
            for col in range(start_col, end_col):
                x = col * (brick_width + brick_padding) + brick_padding
                y = row * (brick_height + brick_padding) + wall_start_y
                color = BRICK_COLORS[row % len(BRICK_COLORS)]
                bricks.append(Brick(x, y, brick_width, brick_height, color))
    
    elif level == 4:
        # Level 4: Checkerboard pattern
        brick_rows = 6
        brick_cols = 10
        for row in range(brick_rows):
            for col in range(brick_cols):
                if (row + col) % 2 == 0:  # Checkerboard pattern
                    x = col * (brick_width + brick_padding) + brick_padding
                    y = row * (brick_height + brick_padding) + wall_start_y
                    color = BRICK_COLORS[row % len(BRICK_COLORS)]
                    bricks.append(Brick(x, y, brick_width, brick_height, color))
    
    elif level == 5:
        # Level 5: Complex pattern with gaps
        brick_cols = 10
        pattern = [
            [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
            [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
            [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        for row in range(len(pattern)):
            for col in range(len(pattern[row])):
                if pattern[row][col]:
                    x = col * (brick_width + brick_padding) + brick_padding
                    y = row * (brick_height + brick_padding) + wall_start_y
                    color = BRICK_COLORS[row % len(BRICK_COLORS)]
                    bricks.append(Brick(x, y, brick_width, brick_height, color))
    
    return bricks

# !!! PHASE 5: Brick Wall Setup Function ---
# We put the brick creation logic into a function to easily rebuild the wall.
def create_brick_wall_legacy():
    """Legacy function - keeping for compatibility"""
    bricks = []
    brick_rows = 4
    brick_cols = 10
    brick_width = 75
    brick_height = 20
    brick_padding = 5
    wall_start_y = 50
    for row in range(brick_rows):
        for col in range(brick_cols):
            # Calculate the x and y position for each brick
            x = col * (brick_width + brick_padding) + brick_padding
            y = row * (brick_height + brick_padding) + wall_start_y
            # Get a color for the current row
            color = BRICK_COLORS[row % len(BRICK_COLORS)]
            # Create a Brick object and add it to our list
            bricks.append(Brick(x, y, brick_width, brick_height, color))
    return bricks

# Create the initial wall of bricks
bricks = create_brick_wall(current_level)

# !!! PHASE 5: Game State Variable ---
# !!! PHASE 12: The game now starts on the title screen
game_state = 'title_screen' # Can be 'title_screen', 'playing', 'game_over', or 'you_win'

# !!! PHASE 6: Game Variables - Score & Lives ---
score = 0
lives = 3

# !!! PHASE 7: Power-ups list ---
power_ups = []

# !!! PHASE 9: Lasers list ---
lasers = []

# !!! PHASE 9: Track if space was pressed this frame
space_pressed = False

# !!! PHASE 10: Message system
display_message = ""
message_timer = 0

# !!! PHASE 11: Visual effects
particles = []
fireworks = []

# -- Main Game Loop --
# The game loop is the heart of any PyGame program. It's a `while` loop that
# runs continuously, handling events, updating game state, and drawing to the screen.
while True:
    # --- Event Handling ---
    # This `for` loop checks for any events that have happened since the last frame.
    # Events can be key presses, mouse movements, or, in this case, closing the window.
    space_pressed = False  # Reset each frame
    for event in pygame.event.get():
        # The `pygame.QUIT` event is triggered when the user clicks the 'X' button
        # on the window.
        if event.type == pygame.QUIT:
            # If the QUIT event is detected, we first shut down PyGame cleanly.
            pygame.quit()
            # Then, we exit the program using `sys.exit()`.
            sys.exit()
        # !!! PHASE 5: Restart Logic ---
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            space_pressed = True
            # !!! PHASE 12: Title Screen Logic
            if game_state == 'title_screen':
                # Start the game from title screen
                game_state = 'playing'
            elif game_state != 'playing':
                # Reset the game objects to their starting state and return to title
                paddle.reset()
                ball.reset()
                current_level = 1  # Reset to level 1
                bricks = create_brick_wall(current_level)
                game_state = 'title_screen'
                # !!! PHASE 6: Reset score and lives
                score = 0
                lives = 3
                # !!! PHASE 7: Clear any lingering power-ups
                power_ups.clear()
                # !!! PHASE 9: Clear any lingering lasers
                lasers.clear()
                # !!! PHASE 11: Clear visual effects
                particles.clear()
                fireworks.clear()
            # !!! PHASE 9: Handle space key during gameplay
            elif game_state == 'playing':
                # Fire lasers if paddle has laser power-up
                if paddle.has_laser:
                    # Fire two lasers, one from each side of the paddle
                    lasers.append(Laser(paddle.rect.centerx - 30, paddle.rect.top))
                    lasers.append(Laser(paddle.rect.centerx + 30, paddle.rect.top))
                    sound_manager.play_sound(laser_sound)
        # !!! NEW: Mute button handling
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            is_muted = sound_manager.toggle_mute()
            display_message = "SOUND MUTED" if not is_muted else "SOUND ON"
            message_timer = 120

    # !!! PHASE 5: Updating Objects (only if the game is in the 'playing' state) ---
    if game_state == 'playing':
        # !!! PHASE 2: Updating Objects ---
        # The main loop no longer needs to know the details of how the paddle works.
        # It just tells the paddle to update itself.
        paddle.update()
        # !!! PHASE 3: Update the ball and pass the paddle for collision detection
        # !!! PHASE 9: Pass space_pressed to launch glued ball
        ball_status, collision_object = ball.update(paddle, bounce_sound, space_pressed)
        
        # !!! PHASE 11: Add particle effects for ball collisions
        if collision_object in ['wall', 'paddle', 'paddle_glue']:
            # Add a few yellow particles when ball bounces
            for _ in range(5):
                particles.append(Particle(ball.rect.centerx, ball.rect.centery, (255, 255, 0), 1, 3, 1, 3, 0))

        # !!! PHASE 6: Check for Loss of a Life ---
        if ball_status == 'lost':
            lives -= 1
            # !!! PHASE 8: Play game over sound when losing a life
            sound_manager.play_sound(game_over_sound)
            if lives <= 0:
                game_state = 'game_over'
            else:
                # Reset ball and paddle position for the next life
                ball.reset()
                paddle.reset()

        # !!! PHASE 4: Ball and Brick Collision ---
        # We iterate over a copy of the list (bricks[:]) because we might modify
        # the original list inside the loop, which can cause errors.
        for brick in bricks[:]:
            if ball.rect.colliderect(brick.rect):
                # Reverse the ball's vertical direction
                ball.speed_y *= -1
                # !!! PHASE 8: Play brick break sound
                sound_manager.play_sound(brick_break_sound)
                # !!! PHASE 6: Increase score when a brick is hit
                score += 10
                # !!! PHASE 7&9: 20% chance to drop a power-up
                # !!! NEW: Extended power-up types
                if random.random() < 0.2:
                    power_up_type = random.choice(['grow', 'laser', 'glue', 'slow', 'multi', 'fast', 'wide', 'shield'])
                    power_up = PowerUp(brick.rect.centerx, brick.rect.centery, power_up_type)
                    power_ups.append(power_up)
                # !!! PHASE 11: Add particle explosion when brick is destroyed
                for _ in range(15): # 15 particles
                    particles.append(Particle(brick.rect.centerx, brick.rect.centery, brick.color, 1, 4, 1, 4, 0.05))
                # Remove the brick from the list
                bricks.remove(brick)
                # Break the loop to prevent the ball from hitting multiple bricks in one frame
                break
        
        # !!! PHASE 7: Update and Check Power-Up Collisions ---
        for power_up in power_ups[:]:
            power_up.update()
            # Remove power-up if it goes off-screen
            if power_up.rect.top > screen_height:
                power_ups.remove(power_up)
            # Check for collision with paddle
            elif paddle.rect.colliderect(power_up.rect):
                # !!! PHASE 9: Apply different power-up effects
                # !!! NEW: Extended power-up handling
                if power_up.type == 'slow':
                    ball.apply_slow()
                elif power_up.type == 'fast':
                    ball.apply_fast()
                elif power_up.type == 'multi':
                    # TODO: Implement multi-ball in future update
                    display_message = "MULTI-BALL (Coming Soon!)"
                    message_timer = 120
                    power_ups.remove(power_up)
                    continue
                else:
                    paddle.activate_power_up(power_up.type)
                # !!! PHASE 10: Show power-up message
                display_message = power_up.PROPERTIES[power_up.type]['message']
                message_timer = 120 # Display for 2 seconds
                power_ups.remove(power_up)
        
        # !!! PHASE 9: Update and Check Laser Collisions ---
        for laser in lasers[:]:
            laser.update()
            # Remove laser if it goes off-screen
            if laser.rect.bottom < 0:
                lasers.remove(laser)
            else:
                # Check for collision with bricks
                for brick in bricks[:]:
                    if laser.rect.colliderect(brick.rect):
                        # !!! PHASE 8: Play brick break sound
                        sound_manager.play_sound(brick_break_sound)
                        # !!! PHASE 6: Increase score when a brick is hit
                        score += 10
                        # Remove the brick and laser
                        bricks.remove(brick)
                        # !!! PHASE 11: Add particle explosion for laser hits
                        for _ in range(10): # 10 particles for laser hits
                            particles.append(Particle(brick.rect.centerx, brick.rect.centery, brick.color, 1, 3, 1, 3, 0.05))
                        lasers.remove(laser)
                        break
        
        # !!! PHASE 5: Check for Win ---
        # !!! NEW: Level progression
        if not bricks:
            if current_level < max_levels:
                # Advance to next level
                current_level += 1
                bricks = create_brick_wall(current_level)
                ball.reset()
                paddle.reset()
                # Bonus score for completing level
                score += 100 * current_level
                display_message = f"LEVEL {current_level}!"
                message_timer = 180  # 3 seconds
                # Clear power-ups for fresh start
                power_ups.clear()
                lasers.clear()
            else:
                # All levels completed!
                game_state = 'you_win'
                # !!! PHASE 11: Create fireworks when winning
                if random.random() < 0.3: # 30% chance each frame to create a firework
                    fireworks.append(Firework(screen_width, screen_height))

    # !!! PHASE 10: Update message timer ---
    if message_timer > 0:
        message_timer -= 1

    # !!! PHASE 11: Update particles ---
    for particle in particles[:]:
        particle.update()
        if particle.size <= 0:
            particles.remove(particle)
    
    # !!! PHASE 11: Update fireworks ---
    for firework in fireworks[:]:
        firework.update()
        if firework.is_dead():
            fireworks.remove(firework)

    # --- Drawing ---
    # This is where all the rendering will happen in later steps.
    # For now, we'll just fill the screen with a solid color.
    # Colors are represented by RGB tuples (Red, Green, Blue).
    # (0, 0, 0) is black.
    screen.fill(BG_COLOR)
    
    # !!! PHASE 12: Title Screen Drawing ---
    # !!! NEW: Enhanced title screen with controls
    if game_state == 'title_screen':
        # Draw the title
        title_surface = title_font.render("ARKANOID", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width / 2, screen_height / 2 - 100))
        screen.blit(title_surface, title_rect)
        
        # Draw the start message
        start_surface = game_font.render("Press SPACE to Start", True, (255, 255, 255))
        start_rect = start_surface.get_rect(center=(screen_width / 2, screen_height / 2 - 20))
        screen.blit(start_surface, start_rect)
        
        # Controls information
        controls = [
            "Controls:",
            "Arrow Keys - Move Paddle",
            "SPACE - Launch Ball / Fire Lasers",
            "M - Toggle Mute",
            "",
            f"Complete {max_levels} Levels to Win!"
        ]
        
        for i, control in enumerate(controls):
            color = (255, 255, 0) if i == 0 else (200, 200, 200)  # Yellow for header
            control_surface = message_font.render(control, True, color)
            control_rect = control_surface.get_rect(center=(screen_width / 2, screen_height / 2 + 40 + i * 25))
            screen.blit(control_surface, control_rect)
    
    elif game_state == 'playing':
        # !!! PHASE 2: We tell the paddle to draw itself to the screen.
        paddle.draw(screen)
        # !!! PHASE 3: Draw the ball
        ball.draw(screen)
        # !!! PHASE 4: Draw all the bricks
        for brick in bricks:
            brick.draw(screen)
        
        # !!! PHASE 7: Draw all power-ups
        for power_up in power_ups:
            power_up.draw(screen)
        
        # !!! PHASE 9: Draw all lasers
        for laser in lasers:
            laser.draw(screen)

        # !!! PHASE 11: Draw particles and fireworks
        for particle in particles:
            particle.draw(screen)
        
        for firework in fireworks:
            firework.draw(screen)

        # !!! PHASE 6: Draw Score and Lives ---
        score_text = game_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        lives_text = game_font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (screen_width - lives_text.get_width() - 10, 10))

        # !!! NEW: Display current level and mute status
        level_text = game_font.render(f"Level: {current_level}", True, (255, 255, 255))
        screen.blit(level_text, (screen_width // 2 - level_text.get_width() // 2, 10))
        
        # Mute indicator
        if not sound_enabled:
            mute_text = message_font.render("MUTED", True, (255, 0, 0))
            screen.blit(mute_text, (10, 50))

        # !!! PHASE 10: Display Power-Up Message ---
        if message_timer > 0:
            message_surface = message_font.render(display_message, True, (255, 255, 255))
            message_rect = message_surface.get_rect(center=(screen_width / 2, 150))
            screen.blit(message_surface, message_rect)

    # !!! PHASE 5: Draw Game Over / You Win Screens ---
    # !!! NEW: Enhanced game over screen
    elif game_state == 'game_over':
        text_surface = game_font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(screen_width / 2, screen_height / 2 - 60))
        screen.blit(text_surface, text_rect)
        
        # Show final score and level reached
        final_score_text = message_font.render(f"Final Score: {score}", True, (255, 255, 255))
        final_score_rect = final_score_text.get_rect(center=(screen_width / 2, screen_height / 2 - 20))
        screen.blit(final_score_text, final_score_rect)
        
        level_reached_text = message_font.render(f"Level Reached: {current_level}", True, (255, 255, 255))
        level_reached_rect = level_reached_text.get_rect(center=(screen_width / 2, screen_height / 2 + 10))
        screen.blit(level_reached_text, level_reached_rect)
        
        # !!! PHASE 12: Updated restart message
        restart_surface = game_font.render("Press SPACE to return to Title", True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
        screen.blit(restart_surface, restart_rect)

    elif game_state == 'you_win':
        # !!! NEW: Enhanced victory screen
        text_surface = game_font.render("CONGRATULATIONS!", True, (255, 215, 0))  # Gold color
        text_rect = text_surface.get_rect(center=(screen_width / 2, screen_height / 2 - 60))
        screen.blit(text_surface, text_rect)
        
        complete_text = message_font.render("All Levels Completed!", True, (255, 255, 255))
        complete_rect = complete_text.get_rect(center=(screen_width / 2, screen_height / 2 - 20))
        screen.blit(complete_text, complete_rect)
        
        # Show final score
        final_score_text = message_font.render(f"Final Score: {score}", True, (255, 255, 255))
        final_score_rect = final_score_text.get_rect(center=(screen_width / 2, screen_height / 2 + 10))
        screen.blit(final_score_text, final_score_rect)

        # !!! PHASE 12: Updated restart message
        restart_surface = game_font.render("Press SPACE to return to Title", True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
        screen.blit(restart_surface, restart_rect)
        
        # !!! PHASE 11: Draw fireworks on win screen
        for firework in fireworks:
            firework.draw(screen)

    # --- Updating the Display ---
    # `pygame.display.flip()` updates the entire screen with everything we've drawn
    # in the current frame. This is what makes our drawings visible.
    pygame.display.flip()

    # --- Frame Rate Control ---
    # `clock.tick(60)` tells PyGame to pause for the right amount of time to ensure
    # our game runs at a maximum of 60 frames per second (FPS). This keeps the
    # game's speed consistent across different computers.
    clock.tick(60)

