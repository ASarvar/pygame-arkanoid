import pygame
import random
import math

# !!! PHASE 9: Font for power-up labels - will be initialized when needed
POWERUP_FONT = None

def get_powerup_font():
    global POWERUP_FONT
    if POWERUP_FONT is None:
        POWERUP_FONT = pygame.font.Font(None, 24)
    return POWERUP_FONT

class Paddle:
    def __init__(self, screen_width, screen_height):
        """
        !!! PHASE 2: Adding the Paddle class
        Initializes the Paddle object.
        - screen_width, screen_height: Dimensions of the game window to handle boundaries.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Define paddle properties
        self.original_width = 100
        self.width = self.original_width
        self.height = 10
        self.speed = 7
        self.color = (200, 200, 200)

        # !!! PHASE 7: Power-up related attributes
        self.power_up_active = False
        self.power_up_timer = 0
        
        # !!! PHASE 9: More power-up attributes
        self.power_up_timers = {
            'grow': 0,
            'laser': 0,
            'glue': 0,
            'slow': 0,
            'multi': 0,
            'fast': 0,
            'wide': 0,
            'shield': 0
        }
        self.has_laser = False
        self.has_glue = False
        self.has_shield = False

        # Create the paddle's rectangle object (self.rect)
        # It's placed at the bottom-center of the screen.
        self.rect = pygame.Rect(
            self.screen_width // 2 - self.width // 2,
            self.screen_height - 30,
            self.width,
            self.height
        )

    def update(self):
        """
        !!! PHASE 2: Paddle movement and boundary checking
        Updates the paddle's position based on keyboard input and handles boundaries.
        This method is called once every frame from the main loop.
        """
        # Get all the keys currently being pressed
        keys = pygame.key.get_pressed()

        # Move left if the left arrow key is pressed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        # Move right if the right arrow key is pressed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Boundary checking to keep the paddle on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
            
        # !!! PHASE 7: Handle power-up timer
        if self.power_up_active:
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                # Power-up wears off, reset paddle size
                self.width = self.original_width
                self.rect.width = self.width
                # Center the paddle after resizing
                self.rect.x += (150 - self.original_width) // 2
                self.power_up_active = False
                
        # !!! PHASE 9: Update all power-up timers
        self._update_power_ups()

    def draw(self, screen):
        """
        !!! PHASE 2: Paddle drawing
        Draws the paddle onto the provided screen surface.
        - screen: The main pygame screen object to draw on.
        """
        pygame.draw.rect(screen, self.color, self.rect)

    # !!! PHASE 5: Add reset method for paddle
    def reset(self):
        """ 
        !!! PHASE 5: Resets the paddle to its starting position.
        """
        self.rect.x = self.screen_width // 2 - self.width // 2
        # !!! PHASE 7: Reset power-up effects
        self.width = self.original_width
        self.rect.width = self.width
        self.power_up_active = False
        self.power_up_timer = 0
        # !!! PHASE 9: Reset all power-ups
        self.has_laser = False
        self.has_glue = False
        self.has_shield = False
        for power_up in self.power_up_timers:
            self.power_up_timers[power_up] = 0

    # !!! PHASE 7: Add power-up activation method
    def activate_power_up(self, type, duration=600):
        """ 
        !!! PHASE 7&9: Activates a power-up effect on the paddle.
        """
        if type == 'grow':
            if self.power_up_timers['grow'] <= 0: # Only grow if not already grown
                current_center = self.rect.centerx
                self.width = 150
                self.rect.width = self.width
                self.rect.centerx = current_center
            self.power_up_timers['grow'] = duration
        elif type == 'laser':
            self.has_laser = True
            self.power_up_timers['laser'] = duration
        elif type == 'glue':
            self.has_glue = True
            self.power_up_timers['glue'] = duration
        elif type == 'slow':
            # !!! NEW: Slow power-up
            self.power_up_timers['slow'] = duration
        elif type == 'multi':
            # !!! NEW: Multi-ball power-up (not fully implemented)
            self.power_up_timers['multi'] = duration
        elif type == 'fast':
            # !!! NEW: Fast ball power-up (not fully implemented)
            self.power_up_timers['fast'] = duration
        elif type == 'wide':
            # Even wider paddle than grow
            if self.power_up_timers['wide'] <= 0:
                current_center = self.rect.centerx
                self.width = 200  # Extra wide
                self.rect.width = self.width
                self.rect.centerx = current_center
            self.power_up_timers['wide'] = duration
        elif type == 'shield':
            # Shield gives extra protection
            self.has_shield = True
            self.power_up_timers['shield'] = duration
            
    def _update_power_ups(self):
        """ 
        !!! PHASE 9: Internal method to handle countdowns and deactivation of power-ups.
        """
        # Grow
        if self.power_up_timers['grow'] > 0:
            self.power_up_timers['grow'] -= 1
            if self.power_up_timers['grow'] <= 0:
                current_center = self.rect.centerx
                self.width = self.original_width
                self.rect.width = self.width
                self.rect.centerx = current_center
        # Laser
        if self.power_up_timers['laser'] > 0:
            self.power_up_timers['laser'] -= 1
            if self.power_up_timers['laser'] <= 0:
                self.has_laser = False
        # Glue
        if self.power_up_timers['glue'] > 0:
            self.power_up_timers['glue'] -= 1
            if self.power_up_timers['glue'] <= 0:
                self.has_glue = False
        # Slow
        if self.power_up_timers['slow'] > 0:
            self.power_up_timers['slow'] -= 1
            if self.power_up_timers['slow'] <= 0:
                pass # Slow effect ends, but not implemented
        # Multi
        if self.power_up_timers['multi'] > 0:
            self.power_up_timers['multi'] -= 1
            if self.power_up_timers['multi'] <= 0:
                pass # Multi-ball effect ends, but not implemented
        # Fast
        if self.power_up_timers['fast'] > 0:
            self.power_up_timers['fast'] -= 1
            if self.power_up_timers['fast'] <= 0:
                pass # Fast ball effect ends, but not fully implemented
        # Wide
        if self.power_up_timers['wide'] > 0:
            self.power_up_timers['wide'] -= 1
            if self.power_up_timers['wide'] <= 0:
                # Revert to normal size when wide power-up ends
                current_center = self.rect.centerx
                self.width = self.original_width
                self.rect.width = self.width
                self.rect.centerx = current_center
        # Shield
        if self.power_up_timers['shield'] > 0:
            self.power_up_timers['shield'] -= 1
            if self.power_up_timers['shield'] <= 0:
                self.has_shield = False

# !!! PHASE 3: Add Ball class
class Ball:
    def __init__(self, screen_width, screen_height):
        """
        !!! PHASE 3: Adding the Ball class
        Initializes the Ball object.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Define ball properties
        self.radius = 10
        self.color = (200, 200, 200)
        
        # The rect will be used for position and collision.
        # We will draw a circle at the center of this rect.
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)

        # !!! PHASE 9: Ball states for power-ups
        self.is_glued = False
        self.is_slowed = False
        self.slow_timer = 0
        self.base_speed = 6

        # !!! NEW: Enhanced ball attributes for new power-ups
        self.is_fast = False
        self.fast_timer = 0
        self.fast_speed_multiplier = 1.5

        # Call reset to set the initial position and speed
        self.reset()

    def reset(self):
        """
        !!! PHASE 3: Ball reset functionality
        Resets the ball to the center of the screen with a random initial velocity.
        """
        self.rect.center = (self.screen_width // 2, self.screen_height // 2)
        # Give the ball a random horizontal direction to start
        self.speed_x = self.base_speed * random.choice((1, -1))
        self.speed_y = -self.base_speed # Start moving upwards
        # !!! PHASE 9: Reset ball states
        self.is_glued = False
        self.is_slowed = False
        self.slow_timer = 0

    def update(self, paddle, bounce_sound=None, launch_ball=False):
        """
        !!! PHASE 3&9: Ball movement and collision detection
        Updates the ball's position and handles all collisions.
        Returns 'lost' if the ball goes off the bottom of the screen.
        - paddle: The player's paddle object, needed for collision checks.
        - bounce_sound: Sound to play when bouncing (Phase 8)
        - launch_ball: Whether to launch the ball if it's glued (Phase 9)
        """
        collision_object = None
        
        # !!! PHASE 9: Handle Glue State
        if self.is_glued:
            self.rect.centerx = paddle.rect.centerx
            self.rect.bottom = paddle.rect.top
            if launch_ball:
                self.is_glued = False
                self.speed_x = self.base_speed * random.choice((1, -1))
                self.speed_y = -self.base_speed
            return 'playing', None # Don't move further if glued

        # !!! PHASE 9: Handle Slow State
        if self.is_slowed:
            self.slow_timer -= 1
            if self.slow_timer <= 0:
                self.speed_x = self.speed_x * 2
                self.speed_y = self.speed_y * 2
                self.is_slowed = False
        
        # Move the ball
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off the top, left, and right walls
        if self.rect.top <= 0:
            self.speed_y *= -1
            collision_object = 'wall'
            # !!! PHASE 8: Play bounce sound
            if bounce_sound:
                bounce_sound.play()
        if self.rect.left <= 0 or self.rect.right >= self.screen_width:
            self.speed_x *= -1
            collision_object = 'wall'
            # !!! PHASE 8: Play bounce sound
            if bounce_sound:
                bounce_sound.play()

        # Check for collision with the paddle
        if self.rect.colliderect(paddle.rect):
            # To prevent the ball from getting "stuck" in the paddle,
            # ensure we only register the bounce when the ball is moving downwards.
            if self.speed_y > 0:
                # !!! PHASE 9: Glue Power-Up Logic
                if paddle.has_glue:
                    self.is_glued = True
                    collision_object = 'paddle_glue'
                else:
                    self.speed_y *= -1
                    collision_object = 'paddle'
                # !!! PHASE 8: Play bounce sound
                if bounce_sound:
                    bounce_sound.play()
        
        # !!! PHASE 5: Check if the ball has fallen off the bottom of the screen (loss condition)
        if self.rect.top > self.screen_height:
            # Instead of resetting here, we signal that the ball was lost.
            return 'lost', None
            
        return 'playing', collision_object
    
    # !!! PHASE 9: Add slow power-up effect to ball
    def apply_slow(self):
        """Apply slow effect to the ball."""
        if not self.is_slowed:
            self.speed_x = self.speed_x // 2
            self.speed_y = self.speed_y // 2
            self.is_slowed = True
            self.slow_timer = 600  # 10 seconds at 60 FPS

    # !!! PHASE 9: Add fast power-up effect to ball
    def apply_fast(self):
        """Apply fast effect to the ball."""
        if not self.is_fast:
            self.speed_x = int(self.speed_x * self.fast_speed_multiplier)
            self.speed_y = int(self.speed_y * self.fast_speed_multiplier)
            self.is_fast = True
            self.fast_timer = 600  # 10 seconds at 60 FPS

    def draw(self, screen):
        """
        !!! PHASE 3: Ball drawing
        Draws the ball on the screen as a circle.
        """
        pygame.draw.ellipse(screen, self.color, self.rect)

# !!! PHASE 4: Add Brick class
class Brick:
    def __init__(self, x, y, width, height, color):
        """
        !!! PHASE 4: Adding the Brick class
        Initializes the Brick object.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        """
        !!! PHASE 4: Brick drawing
        Draws the brick onto the screen.
        """
        pygame.draw.rect(screen, self.color, self.rect)

# !!! PHASE 7&9: Add PowerUp class
class PowerUp:
    # !!! PHASE 9&10: Power-up properties for different types
    # !!! NEW: Extended power-up types
    PROPERTIES = {
        'grow': {'color': (60, 60, 255), 'char': 'G', 'message': 'PADDLE GROW'},
        'laser': {'color': (255, 60, 60), 'char': 'L', 'message': 'LASER CANNONS'},
        'glue': {'color': (60, 255, 60), 'char': 'C', 'message': 'CATCH PADDLE'},
        'slow': {'color': (255, 165, 0), 'char': 'S', 'message': 'SLOW BALL'},
        'multi': {'color': (255, 0, 255), 'char': 'M', 'message': 'MULTI BALL'},
        'fast': {'color': (255, 255, 0), 'char': 'F', 'message': 'FAST BALL'},
        'wide': {'color': (0, 255, 255), 'char': 'W', 'message': 'WIDE PADDLE'},
        'shield': {'color': (128, 128, 128), 'char': 'D', 'message': 'SHIELD UP'},
    }
    
    def __init__(self, x, y, type='grow'):
        """
        !!! PHASE 7&9: Adding the PowerUp class with multiple types
        Initializes the PowerUp object.
        """
        self.width = 30
        self.height = 15
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed_y = 3
        self.type = type
        # !!! PHASE 9: Set color and character based on type
        self.color = self.PROPERTIES[type]['color']
        self.char = self.PROPERTIES[type]['char']

    def update(self):
        """ 
        !!! PHASE 7: Power-up movement
        Moves the power-up downwards.
        """
        self.rect.y += self.speed_y

    def draw(self, screen):
        """ 
        !!! PHASE 7&9: Power-up drawing with type indication
        Draws the power-up with identifying letter.
        """
        # Draw the power-up box
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw the identifying letter
        text_surf = get_powerup_font().render(self.char, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

# !!! PHASE 9: Add Laser class
class Laser:
    def __init__(self, x, y):
        """ 
        !!! PHASE 9: Initializes the Laser object fired from the paddle.
        """
        self.width = 5
        self.height = 15
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = (255, 255, 0) # Yellow laser
        self.speed_y = -8

    def update(self):
        """ 
        !!! PHASE 9: Moves the laser upwards.
        """
        self.rect.y += self.speed_y

    def draw(self, screen):
        """ 
        !!! PHASE 9: Draws the laser.
        """
        pygame.draw.rect(screen, self.color, self.rect)

# !!! PHASE 11: Add visual effects classes
class Particle:
    def __init__(self, x, y, color, min_size, max_size, min_speed, max_speed, gravity):
        """
        !!! PHASE 11: Particle system for explosions
        """
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(min_size, max_size)
        self.gravity = gravity
        angle = random.uniform(0, 360)
        speed = random.uniform(min_speed, max_speed)
        self.vx = speed * math.cos(math.radians(angle))
        self.vy = speed * math.sin(math.radians(angle))

    def update(self):
        """Update particle position and size."""
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.size -= 0.1 # Particles shrink over time

    def draw(self, screen):
        """Draw the particle if it's still visible."""
        if self.size > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

class Firework:
    def __init__(self, screen_width, screen_height):
        """
        !!! PHASE 11: Firework system for victory celebration
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = random.randint(0, screen_width)
        self.y = screen_height
        self.vy = -random.uniform(8, 12) # Speed of the rocket
        self.color = (255, 255, 255) # White rocket
        self.exploded = False
        self.particles = []
        self.explosion_y = random.uniform(screen_height * 0.2, screen_height * 0.5)

    def update(self):
        """Update firework rocket and explosion."""
        if not self.exploded:
            self.y += self.vy
            if self.y <= self.explosion_y:
                self.exploded = True
                explosion_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                for _ in range(50): # Create 50 particles on explosion
                    self.particles.append(Particle(self.x, self.y, explosion_color, 2, 4, 1, 4, 0.1))
        else:
            for particle in self.particles[:]:
                particle.update()
                if particle.size <= 0:
                    self.particles.remove(particle)

    def draw(self, screen):
        """Draw the firework rocket or explosion particles."""
        if not self.exploded:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)
        else:
            for particle in self.particles:
                particle.draw(screen)

    def is_dead(self):
        """Check if the firework is done displaying."""
        return self.exploded and not self.particles
