import checkers
import gamebot
import pygame
import os
from time import sleep

##COLORS##
WHITE = (255, 255, 255)
BLUE = (0,   0, 255)
RED = (255,   0,   0)
BLACK = (0,   0,   0)
GOLD = (255, 215,   0)
HIGH = (160, 190, 255)

##DIRECTIONS##
NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"

# Game modes
HUMAN_VS_AI = 0
AI_VS_AI = 1

def create_bot(game, color, difficulty):
    """Create a bot with the specified difficulty level
    
    difficulty levels:
    1 - Random moves only
    2 - MiniMax strategy with depth 1
    3 - Alpha-Beta pruning with depth 2
    4 - Standard Alpha-Beta with depth 3
    5 - Advanced Alpha-Beta with depth 5
    """
    if difficulty == 1:
        # Level 1: Random moves
        return gamebot.Bot(game, color, mid_eval='piece2val', method='random', depth=1)
    elif difficulty == 2:
        # Level 2: MiniMax with depth 1
        return gamebot.Bot(game, color, mid_eval='piece_and_board', method='minmax', depth=1)
    elif difficulty == 3:
        # Level 3: Alpha-Beta with depth 2
        return gamebot.Bot(game, color, mid_eval='piece_and_board', 
                           method='minmax', depth=2, end_eval='sum_of_dist')
    elif difficulty == 4:
        # Level 4: Current standard implementation
        return gamebot.Bot(game, color, mid_eval='piece_and_row',
                          end_eval='farthest_piece', method='alpha_beta', depth=3)
    else:
        # Level 5: Advanced Alpha-Beta with deeper search
        return gamebot.Bot(game, color, mid_eval='piece_and_board_pov',
                          end_eval='farthest_piece', method='alpha_beta', depth=4)

def select_difficulty():
    """Display a menu to select AI difficulty and return the selected difficulty level"""
    screen_width = 400
    screen_height = 300
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Checkers - Select Difficulty")
    
    font = pygame.font.SysFont(None, 30)
    title_font = pygame.font.SysFont(None, 40)
    
    # Create buttons for each difficulty level
    level1_button = pygame.Rect(100, 80, 200, 30)
    level2_button = pygame.Rect(100, 120, 200, 30)
    level3_button = pygame.Rect(100, 160, 200, 30)
    level4_button = pygame.Rect(100, 200, 200, 30)
    level5_button = pygame.Rect(100, 240, 200, 30)
    
    selected_difficulty = None
    while selected_difficulty is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 4  # Default to level 4
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if level1_button.collidepoint(mouse_pos):
                    selected_difficulty = 1
                elif level2_button.collidepoint(mouse_pos):
                    selected_difficulty = 2
                elif level3_button.collidepoint(mouse_pos):
                    selected_difficulty = 3
                elif level4_button.collidepoint(mouse_pos):
                    selected_difficulty = 4
                elif level5_button.collidepoint(mouse_pos):
                    selected_difficulty = 5
        
        screen.fill(WHITE)
        title = title_font.render("Select Difficulty", True, BLACK)
        screen.blit(title, (100, 30))
        
        # Draw buttons
        pygame.draw.rect(screen, HIGH, level1_button)
        pygame.draw.rect(screen, HIGH, level2_button)
        pygame.draw.rect(screen, HIGH, level3_button)
        pygame.draw.rect(screen, HIGH, level4_button)
        pygame.draw.rect(screen, HIGH, level5_button)
        
        # Button text
        level1_text = font.render("Level 1 - Beginner", True, BLACK)
        level2_text = font.render("Level 2 - Easy", True, BLACK)
        level3_text = font.render("Level 3 - Medium", True, BLACK)
        level4_text = font.render("Level 4 - Hard", True, BLACK)
        level5_text = font.render("Level 5 - Expert", True, BLACK)
        
        screen.blit(level1_text, (level1_button.x + 20, level1_button.y + 5))
        screen.blit(level2_text, (level2_button.x + 20, level2_button.y + 5))
        screen.blit(level3_text, (level3_button.x + 20, level3_button.y + 5))
        screen.blit(level4_text, (level4_button.x + 20, level4_button.y + 5))
        screen.blit(level5_text, (level5_button.x + 20, level5_button.y + 5))
        
        pygame.display.flip()
    
    return selected_difficulty

def select_game_mode():
    """Display a menu to select game mode and return the selected mode"""
    screen_width = 400
    screen_height = 200
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Checkers - Select Game Mode")
    
    font = pygame.font.SysFont(None, 30)
    title_font = pygame.font.SysFont(None, 40)
    
    human_vs_ai_button = pygame.Rect(120, 80, 180, 40)
    ai_vs_ai_button = pygame.Rect(120, 130, 180, 40)
    
    selected_mode = None
    while selected_mode is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return AI_VS_AI
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if human_vs_ai_button.collidepoint(mouse_pos):
                    selected_mode = HUMAN_VS_AI
                elif ai_vs_ai_button.collidepoint(mouse_pos):
                    selected_mode = AI_VS_AI
        
        screen.fill(WHITE)
        title = title_font.render("Select Game Mode", True, BLACK)
        screen.blit(title, (80, 30))
        pygame.draw.rect(screen, HIGH, human_vs_ai_button)
        pygame.draw.rect(screen, HIGH, ai_vs_ai_button)
        human_ai_text = font.render("Player vs Bot", True, BLACK)
        ai_ai_text = font.render("Bot vs Bot", True, BLACK)
        screen.blit(human_ai_text, (human_vs_ai_button.x + 25, human_vs_ai_button.y + 10))
        screen.blit(ai_ai_text, (ai_vs_ai_button.x + 40, ai_vs_ai_button.y + 10))
        pygame.display.flip()
    
    return selected_mode

def select_ai_difficulties():
    """Display a menu to select separate difficulty levels for Red and Blue Bot"""
    screen_width = 550  # Wider to accommodate two columns
    screen_height = 350
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Select Bot Difficulties")
    
    font = pygame.font.SysFont(None, 30)
    title_font = pygame.font.SysFont(None, 40)
    
    # Create buttons for each difficulty level for Red AI
    red_level1_button = pygame.Rect(50, 80, 200, 30)
    red_level2_button = pygame.Rect(50, 120, 200, 30)
    red_level3_button = pygame.Rect(50, 160, 200, 30)
    red_level4_button = pygame.Rect(50, 200, 200, 30)
    red_level5_button = pygame.Rect(50, 240, 200, 30)
    
    # Create buttons for each difficulty level for Blue AI
    blue_level1_button = pygame.Rect(320, 80, 200, 30)
    blue_level2_button = pygame.Rect(320, 120, 200, 30)
    blue_level3_button = pygame.Rect(320, 160, 200, 30)
    blue_level4_button = pygame.Rect(320, 200, 200, 30)
    blue_level5_button = pygame.Rect(320, 240, 200, 30)
    
    red_difficulty = None
    blue_difficulty = None
    
    while red_difficulty is None or blue_difficulty is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 4, 4  # Default to level 4 for both
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check Red AI buttons
                if red_difficulty is None:  # Only check if not already selected
                    if red_level1_button.collidepoint(mouse_pos):
                        red_difficulty = 1
                    elif red_level2_button.collidepoint(mouse_pos):
                        red_difficulty = 2
                    elif red_level3_button.collidepoint(mouse_pos):
                        red_difficulty = 3
                    elif red_level4_button.collidepoint(mouse_pos):
                        red_difficulty = 4
                    elif red_level5_button.collidepoint(mouse_pos):
                        red_difficulty = 5
                
                # Check Blue AI buttons
                if blue_difficulty is None:  # Only check if not already selected
                    if blue_level1_button.collidepoint(mouse_pos):
                        blue_difficulty = 1
                    elif blue_level2_button.collidepoint(mouse_pos):
                        blue_difficulty = 2
                    elif blue_level3_button.collidepoint(mouse_pos):
                        blue_difficulty = 3
                    elif blue_level4_button.collidepoint(mouse_pos):
                        blue_difficulty = 4
                    elif blue_level5_button.collidepoint(mouse_pos):
                        blue_difficulty = 5
        
        screen.fill(WHITE)
        title = title_font.render("Select Bot Difficulties", True, BLACK)
        screen.blit(title, (130, 10))
        
        # Draw labels for the two AIs
        red_label = font.render("Red", True, RED)
        blue_label = font.render("Blue", True, BLUE)
        screen.blit(red_label, (120, 50))
        screen.blit(blue_label, (390, 50))
        
        # Draw Red AI buttons - only highlight the selected button
        pygame.draw.rect(screen, RED if red_difficulty == 1 else HIGH, red_level1_button)
        pygame.draw.rect(screen, RED if red_difficulty == 2 else HIGH, red_level2_button)
        pygame.draw.rect(screen, RED if red_difficulty == 3 else HIGH, red_level3_button)
        pygame.draw.rect(screen, RED if red_difficulty == 4 else HIGH, red_level4_button)
        pygame.draw.rect(screen, RED if red_difficulty == 5 else HIGH, red_level5_button)
        
        # Draw Blue AI buttons - only highlight the selected button
        pygame.draw.rect(screen, BLUE if blue_difficulty == 1 else HIGH, blue_level1_button)
        pygame.draw.rect(screen, BLUE if blue_difficulty == 2 else HIGH, blue_level2_button)
        pygame.draw.rect(screen, BLUE if blue_difficulty == 3 else HIGH, blue_level3_button)
        pygame.draw.rect(screen, BLUE if blue_difficulty == 4 else HIGH, blue_level4_button)
        pygame.draw.rect(screen, BLUE if blue_difficulty == 5 else HIGH, blue_level5_button)
        
        # Button text
        for level, button in zip(range(1, 6), [red_level1_button, red_level2_button, red_level3_button, red_level4_button, red_level5_button]):
            text_color = WHITE if red_difficulty == level else BLACK
            level_text = [
                "Level 1 - Beginner",
                "Level 2 - Easy",
                "Level 3 - Medium",
                "Level 4 - Hard",
                "Level 5 - Expert"
            ][level-1]
            level_text = font.render(level_text, True, text_color)
            screen.blit(level_text, (button.x + 10, button.y + 5))
        
        # Do the same for blue buttons
        for level, button in zip(range(1, 6), [blue_level1_button, blue_level2_button, blue_level3_button, blue_level4_button, blue_level5_button]):
            text_color = WHITE if blue_difficulty == level else BLACK
            level_text = [
                "Level 1 - Beginner",
                "Level 2 - Easy",
                "Level 3 - Medium",
                "Level 4 - Hard",
                "Level 5 - Expert"
            ][level-1]
            level_text = font.render(level_text, True, text_color)
            screen.blit(level_text, (button.x + 10, button.y + 5))
        
        pygame.display.flip()
    
    return red_difficulty, blue_difficulty

def select_player_color():
    """Display a menu for the player to select whether to play as Blue or Red"""
    screen_width = 400
    screen_height = 200
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Select Your Color")
    
    font = pygame.font.SysFont(None, 30)
    title_font = pygame.font.SysFont(None, 40)
    
    # Create buttons
    play_as_blue_button = pygame.Rect(100, 80, 220, 40)  # Blue = go first
    play_as_red_button = pygame.Rect(100, 130, 220, 40)  # Red = go second
    
    selected_color = None
    while selected_color is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return BLUE  # Default to Blue
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_as_blue_button.collidepoint(mouse_pos):
                    selected_color = BLUE
                elif play_as_red_button.collidepoint(mouse_pos):
                    selected_color = RED
        
        screen.fill(WHITE)
        title = title_font.render("Select Your Color", True, BLACK)
        screen.blit(title, (90, 30))
        
        pygame.draw.rect(screen, HIGH, play_as_blue_button)
        pygame.draw.rect(screen, HIGH, play_as_red_button)
        
        blue_text = font.render("Play as Blue (First)", True, BLUE)
        red_text = font.render("Play as Red (Second)", True, RED)
        
        screen.blit(blue_text, (play_as_blue_button.x + 15, play_as_blue_button.y + 10))
        screen.blit(red_text, (play_as_red_button.x + 15, play_as_red_button.y + 10))
        
        pygame.display.flip()
    
    return selected_color

def show_winner(screen, winner):
    """Display who won the game with options to play again or quit"""
    # Create a semi-transparent overlay
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Semi-transparent black background
    
    # Create a modal dialog box
    modal_width, modal_height = 400, 300
    modal_rect = pygame.Rect(
        (screen.get_width() - modal_width) // 2,
        (screen.get_height() - modal_height) // 2,
        modal_width, modal_height
    )
    
    # Determine winner and set colors/text
    if winner == RED:
        title_text = "Red Wins!"
        title_color = RED
    elif winner == BLUE:
        title_text = "Blue Wins!"
        title_color = BLUE
    else:
        title_text = "Draw!"
        title_color = GOLD
    
    # Create fonts
    title_font = pygame.font.SysFont(None, 64)
    button_font = pygame.font.SysFont(None, 32)
    
    # Create text surfaces
    title_surface = title_font.render(title_text, True, title_color)
    
    # Create buttons
    play_again_button = pygame.Rect(
        modal_rect.centerx - 120,
        modal_rect.bottom - 100,
        240, 40
    )
    quit_button = pygame.Rect(
        modal_rect.centerx - 120,
        modal_rect.bottom - 50,
        240, 40
    )
    
    play_again_text = button_font.render("Play Again", True, BLACK)
    quit_text = button_font.render("Quit Game", True, BLACK)
    
    # Animation variables
    clock = pygame.time.Clock()
    alpha = 0
    
    # Fade in animation
    while alpha < 255:
        alpha = min(255, alpha + 10)
        overlay.set_alpha(alpha)
        
        screen.blit(overlay, (0, 0))
        
        # Draw modal background with border
        pygame.draw.rect(screen, WHITE, modal_rect, border_radius=15)
        pygame.draw.rect(screen, title_color, modal_rect, width=5, border_radius=15)
        
        # Draw title
        title_rect = title_surface.get_rect(centerx=modal_rect.centerx, top=modal_rect.top + 30)
        screen.blit(title_surface, title_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Draw buttons
    pygame.draw.rect(screen, HIGH, play_again_button, border_radius=8)
    pygame.draw.rect(screen, title_color, play_again_button, width=2, border_radius=8)
    pygame.draw.rect(screen, HIGH, quit_button, border_radius=8)
    pygame.draw.rect(screen, title_color, quit_button, width=2, border_radius=8)
    
    # Draw button text
    play_text_rect = play_again_text.get_rect(center=play_again_button.center)
    quit_text_rect = quit_text.get_rect(center=quit_button.center)
    screen.blit(play_again_text, play_text_rect)
    screen.blit(quit_text, quit_text_rect)
    
    pygame.display.flip()
    
    # Wait for user choice
    waiting = True
    play_again = False
    
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Don't play again
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_button.collidepoint(mouse_pos):
                    play_again = True
                    waiting = False
                elif quit_button.collidepoint(mouse_pos):
                    play_again = False
                    waiting = False
        
        # Add subtle animation to buttons
        highlight = (200 + (pygame.time.get_ticks() % 1000) // 20)
        highlight = min(255, highlight)
        
        # Redraw the buttons with animation
        pygame.draw.rect(screen, (highlight, highlight, highlight), play_again_button, border_radius=8)
        pygame.draw.rect(screen, title_color, play_again_button, width=2, border_radius=8)
        pygame.draw.rect(screen, (highlight, highlight, highlight), quit_button, border_radius=8)
        pygame.draw.rect(screen, title_color, quit_button, width=2, border_radius=8)
        
        screen.blit(play_again_text, play_text_rect)
        screen.blit(quit_text, quit_text_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Fade out
    for alpha in range(255, -1, -15):
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        clock.tick(60)
    
    return play_again

def main():
    pygame.init()
    
    # Open the log file for results
    log_file = open("result.txt", "w")
    log_file.write("CHECKERS GAME LOGS\n")
    log_file.write("=================\n\n")
    
    while True:
        # Select game mode first
        game_mode = select_game_mode()
        
        # Get difficulty and player color
        red_difficulty = 4  # Default difficulty
        blue_difficulty = 4  # Default difficulty
        player_color = BLUE  # Default player color
        
        if game_mode == HUMAN_VS_AI:
            # Let player choose their color
            player_color = select_player_color()
            
            # If player is Red, we need AI difficulty for Blue
            # If player is Blue, we need AI difficulty for Red
            if player_color == BLUE:
                red_difficulty = select_difficulty()  # AI plays as Red
            else:  # player is RED
                blue_difficulty = select_difficulty()  # AI plays as Blue
                
        else:  # AI_VS_AI mode
            red_difficulty, blue_difficulty = select_ai_difficulties()
        
        # Set up game
        game = checkers.Game(loop_mode=False)
        game.setup()
        
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        screen = pygame.display.set_mode((630, 600))
        
        # Set appropriate window title
        if game_mode == HUMAN_VS_AI:
            ai_color = RED if player_color == BLUE else BLUE
            ai_difficulty = red_difficulty if ai_color == RED else blue_difficulty
            player_color_name = "Blue" if player_color == BLUE else "Red"
            pygame.display.set_caption(f"Checkers - {player_color_name} (Human) vs Level {ai_difficulty} AI")
            
            # Log game start
            log_file.write(f"\nNew Game: {player_color_name} (Human) vs Level {ai_difficulty} AI\n")
            log_file.write("-----------------------------------------\n")
        else:
            pygame.display.set_caption(f"Checkers - Red Bot (Lvl {red_difficulty}) vs Blue Bot (Lvl {blue_difficulty})")
            
            # Log game start
            log_file.write(f"\nNew Game: Red Bot (Level {red_difficulty}) vs Blue Bot (Level {blue_difficulty})\n")
            log_file.write("-----------------------------------------\n")
        
        # Create AI bots based on selected difficulties
        red_bot = create_bot(game, RED, red_difficulty)
        
        if game_mode == AI_VS_AI or player_color == RED:
            blue_bot = create_bot(game, BLUE, blue_difficulty)
        
        move_count = 0
        # Main game loop
        while True:
            # Handle Blue's turn
            if game.turn == BLUE:
                if game_mode == HUMAN_VS_AI and player_color == BLUE:
                    # Human plays as Blue
                    game.player_turn()
                    game.update()
                else:
                    # AI plays as Blue
                    move_count += 1
                    count_nodes = blue_bot.step(game.board, True)
                    log_message = f'Move {move_count}: Blue Bot (Level {blue_difficulty}) explored {count_nodes} nodes\n'
                    log_file.write(log_message)
                    log_file.flush()  # Ensure it's written immediately
                    game.update()
            # Handle Red's turn
            else:
                if game_mode == HUMAN_VS_AI and player_color == RED:
                    # Human plays as Red
                    game.player_turn()
                    game.update()
                else:
                    # AI plays as Red
                    move_count += 1
                    count_nodes = red_bot.step(game.board, True)
                    log_message = f'Move {move_count}: Red Bot (Level {red_difficulty}) explored {count_nodes} nodes\n'
                    log_file.write(log_message)
                    log_file.flush()  # Ensure it's written immediately
                    game.update()
            
            # Check if game is over
            if game.endit:
                # Log game end
                winner = getattr(game, 'winner', None)
                if winner is None:
                    red_pieces = sum(row.count(RED) for row in game.board)
                    blue_pieces = sum(row.count(BLUE) for row in game.board)
                    if red_pieces > blue_pieces:
                        winner = RED
                    elif blue_pieces > red_pieces:
                        winner = BLUE
                    else:
                        winner = None
                        
                # Log the winner
                if winner == RED:
                    log_file.write("\nGame Result: RED WINS!\n\n")
                elif winner == BLUE:
                    log_file.write("\nGame Result: BLUE WINS!\n\n")
                else:
                    log_file.write("\nGame Result: DRAW!\n\n")
                    
                log_file.write("=================\n\n")
                log_file.flush()
                
                show_winner(screen, winner)
                break
    
    # Close the log file when application exits
    log_file.close()
    pygame.quit()

if __name__ == "__main__":
    main()