import pygame
import sys

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40
FONT_SIZE_LARGE = 60
FONT_SIZE_MEDIUM = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (66, 135, 245)
RED = (245, 66, 66)
TOWER_BG = (230, 230, 230)
TOWER_BORDER = (180, 180, 180)
TEXT_COLOR = (50, 50, 50)
GREEN = (77, 201, 80)

# Numbers to add
NUMBER_1 = 5
NUMBER_2 = 7

# --- Block Class ---
class Block:
    """Represents a single draggable block."""
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.color = color
        self.original_pos = (x, y)
        self.is_dragging = False
        self.in_tower = False

    def draw(self, screen):
        """Draws the block on the screen with a border."""
        pygame.draw.rect(screen, self.color, self.rect, border_radius=6)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=6)

    def move_to(self, pos):
        """Moves the center of the block to a new position."""
        self.rect.center = pos

    def return_to_start(self):
        """Resets the block to its original position."""
        self.rect.topleft = self.original_pos

# --- Main Game Setup ---
def main():
    """The main function to run the game."""
    pygame.init()

    # Create the screen and clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Adding Blocks!")
    clock = pygame.time.Clock()

    # Create fonts
    large_font = pygame.font.Font(None, FONT_SIZE_LARGE)
    medium_font = pygame.font.Font(None, FONT_SIZE_MEDIUM)

    # Define the reset button area
    reset_button_rect = pygame.Rect(20, SCREEN_HEIGHT - 65, 100, 40)

    # --- Game Objects and Areas ---
    
    # Define the tower area in the center of the screen
    tower_rect = pygame.Rect((SCREEN_WIDTH / 2) - 75, 50, 150, SCREEN_HEIGHT - 100)

    # Create the lists to hold all blocks and tower blocks
    all_blocks = []
    tower_blocks = []

    # Create blue blocks for the first number
    for i in range(NUMBER_1):
        x = 50 + (i % 3) * (BLOCK_SIZE + 10)
        y = 150 + (i // 3) * (BLOCK_SIZE + 10)
        all_blocks.append(Block(x, y, BLUE))

    # Create red blocks for the second number
    for i in range(NUMBER_2):
        x = SCREEN_WIDTH - 200 + (i % 3) * (BLOCK_SIZE + 10)
        y = 150 + (i // 3) * (BLOCK_SIZE + 10)
        all_blocks.append(Block(x, y, RED))

    # Variable to keep track of the currently dragged block
    dragged_block = None

    # --- Game Loop ---
    running = True
    while running:
        # Calculate counts of blocks in the tower for display
        blue_in_tower = sum(1 for block in tower_blocks if block.color == BLUE)
        red_in_tower = sum(1 for block in tower_blocks if block.color == RED)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- Mouse Down Event ---
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button
                    # Check if the reset button was clicked
                    if reset_button_rect.collidepoint(event.pos):
                        # Clear the tower and reset all blocks
                        for block in all_blocks:
                            if block.in_tower:
                                block.return_to_start()
                                block.in_tower = False
                        tower_blocks.clear()
                        dragged_block = None # Make sure we aren't dragging anything
                        continue # Skip checking blocks on this click

                    # Check if a block was clicked that is not already in the tower
                    for block in all_blocks:
                        if block.rect.collidepoint(event.pos) and not block.in_tower:
                            block.is_dragging = True
                            dragged_block = block
                            break # Only drag one block at a time

            # --- Mouse Up Event ---
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and dragged_block:
                    dragged_block.is_dragging = False
                    # Check if the block was dropped inside the tower
                    if tower_rect.colliderect(dragged_block.rect):
                        dragged_block.in_tower = True
                        tower_blocks.append(dragged_block)
                        
                        # Stack the blocks neatly from the bottom of the tower
                        stack_pos = len(tower_blocks)
                        new_x = tower_rect.centerx
                        new_y = tower_rect.bottom - (stack_pos * BLOCK_SIZE) + (BLOCK_SIZE / 2)
                        dragged_block.move_to((new_x, new_y))
                    else:
                        # If not in the tower, send it back to its starting spot
                        dragged_block.return_to_start()
                    
                    dragged_block = None

            # --- Mouse Motion Event ---
            elif event.type == pygame.MOUSEMOTION:
                if dragged_block:
                    dragged_block.move_to(event.pos)

        # --- Drawing ---
        screen.fill(WHITE)

        # Draw the tower area
        pygame.draw.rect(screen, TOWER_BG, tower_rect, border_radius=10)
        pygame.draw.rect(screen, TOWER_BORDER, tower_rect, 3, border_radius=10)

        # Draw labels
        title_text = medium_font.render("Drag the blocks to the tower!", True, TEXT_COLOR)
        screen.blit(title_text, (SCREEN_WIDTH / 2 - title_text.get_width() / 2, 15))

        num1_text = large_font.render(str(blue_in_tower), True, BLUE)
        screen.blit(num1_text, (110, 80))

        plus_text = large_font.render("+", True, BLACK)
        screen.blit(plus_text, (SCREEN_WIDTH / 2 - plus_text.get_width() / 2, 80))

        num2_text = large_font.render(str(red_in_tower), True, RED)
        screen.blit(num2_text, (SCREEN_WIDTH - 150, 80))
        
        # Draw all the blocks
        for block in all_blocks:
            block.draw(screen)
        
        # Draw the count of blocks in the tower
        count_text = large_font.render(str(len(tower_blocks)), True, TEXT_COLOR)
        pygame.draw.rect(screen, WHITE, (tower_rect.centerx - 40, tower_rect.bottom + 5, 80, 50))
        screen.blit(count_text, (tower_rect.centerx - count_text.get_width() / 2, tower_rect.bottom + 10))

        # Draw the reset button
        pygame.draw.rect(screen, GREEN, reset_button_rect, border_radius=10)
        reset_text = medium_font.render("Reset", True, WHITE)
        reset_text_rect = reset_text.get_rect(center=reset_button_rect.center)
        screen.blit(reset_text, reset_text_rect)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


