from pyparsing import Word, alphas, alphanums, Literal, Forward, Group, ZeroOrMore, Optional, Keyword
import os
import pygame

# Map
OBJECT_SIZE = 50
COLOR_EMPTY = (255, 255, 255)  # White

os.environ['SDL_VIDEO_CENTERED'] = '1'

def resize_image(image):
    return pygame.transform.scale(image, (OBJECT_SIZE-1, OBJECT_SIZE-1))

def createGameMap(level):
    with open('assets\\Map\\maps.txt') as map_file:
        while level > 0:
            line = map_file.readline()
            if line == '---------------\n':
                level = level - 1

        lines = []
        for line in map_file:
            if line == '---------------\n':
                break
            lines.append(line)

        symbols = (' ', '#', '*', '.')
        height = len(lines)
        width = max(map(len, lines)) - 1
        boxes = []
        walls = []
        targets = []
        matrix = [[0 for _ in range(width)] for _ in range(height)]

        for row in range(height):
            for col in range(width):
                if col < len(lines[row])-1:
                    if lines[row][col] == '@':
                        player = [row, col]
                    elif lines[row][col] == '$' or lines[row][col] == '*':
                        if lines[row][col] == '$':
                            boxes.append([row, col])
                        else:
                            boxes.append([row, col])
                            targets.append([row, col])
                    else:
                        matrix[row][col] = symbols.index(lines[row][col])
                        if lines[row][col] == '#':
                            walls.append([row, col])
                        elif lines[row][col] == '.':
                            targets.append([row, col])

        return player, boxes, matrix, walls, targets 

def loadMapLevel(level):
    global current_level, player_position, boxes_positions, game_map_matrix, screen, wall_positions, target_positions, screen_width, screen_height, split_width, right_surface, left_surface
    game_map_matrix = []
    current_level = level

    player_position, boxes_positions, game_map_matrix, wall_positions, target_positions = createGameMap(current_level)

    command_surface_width = (6 * OBJECT_SIZE)
    screen_width = (len(game_map_matrix[0]) * OBJECT_SIZE) + command_surface_width
    screen_height = (len(game_map_matrix) * OBJECT_SIZE)
    split_width = int(command_surface_width)

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Coduban Game")

    left_surface = pygame.Surface((split_width, screen_height))
    right_surface = pygame.Surface((screen_width - split_width, screen_height))

def parser(user_text):
    identifier = Word(alphas+"_") + ZeroOrMore(alphanums+"_")

    # Define the EBNF for a print statement
    expression = Forward()
    punctuations = ",.;:-_?!/ "
    number = Word("0123456789")
    letter = Word(alphas)
    boolean_literal = Literal("true") | Literal("false")
    string = (Literal('"') + Word(alphanums + punctuations) + Literal('"')) | (Literal("'") + Word(alphanums + punctuations) + Literal("'"))

    factor = number | string | "(" + expression + ")" | identifier | letter
    term = factor + ZeroOrMore((Literal("*") | Literal("/")) + factor)
    expression << term + ZeroOrMore((Literal("+") | Literal("-")) + term)

    # Define the EBNF for an assignment statement
    assignment_statement = identifier + "=" + expression

    # Define the EBNF for a function
    function_call = expression
    function_declaration = Literal("def ") + function_call
    function_statement = function_declaration | function_call

    range_statement = expression + ',' + Optional(" ") + expression

    # Define the EBNF for a Python print statement
    move_statement = expression

    # Define the EBNF for conditional statement
    condition_statement = Keyword('if') + Optional(" ") + "(" + expression + ")" + Optional(" ") + Keyword(':') + Optional(" ") + (move_statement | function_statement)

    loop_statement = Keyword('for') + Optional(" ") + expression + Optional(" ") +  Keyword('in') + Optional(" ") + Keyword('range') + '(' + range_statement + ')'  ':' + Optional(" ") + (move_statement | function_statement)

    # All Python statements
    python_statements = (loop_statement | condition_statement | move_statement | assignment_statement | function_statement | function_call)

    # Test the parser
    text = user_text
    result = python_statements.parseString(user_text)
    words = text.split()
    if result[len(result)-1] == words[len(words) - 1]:
        return result
    
def moveleft():
    movePlayer("left")
def moveright():
    movePlayer("right")
def moveup():
    movePlayer("up")
def movedown():
    movePlayer("down")
def stop():
    if (prev_move == player_position):
        return True
    return False

def movePlayer(direction):
    global score
    if direction == "left":
        move = True
        # Check if hitting a wall
        if [player_position[0], player_position[1] - 1] in wall_positions:
            move = False
        # Check if pushing a box
        elif [player_position[0], player_position[1] - 1] in boxes_positions:
            for box_pos in boxes_positions:
                if box_pos == [player_position[0], player_position[1] - 1]:
                    box = box_pos
            if [box[0], box[1] - 1] in wall_positions or [box[0], box[1] - 1] in boxes_positions:
                move = False
            else:
                box[1] -= 1
                move = True
        if move:
            player_position[1] -= 1
            score += 1
    elif direction == "right":
        move = True
        if [player_position[0], player_position[1] + 1] in wall_positions:
            move = False
        elif [player_position[0], player_position[1] + 1] in boxes_positions:
            for box_pos in boxes_positions:
                if box_pos == [player_position[0], player_position[1] + 1]:
                    box = box_pos
            if [box[0], box[1] + 1] in wall_positions or [box[0], box[1] + 1] in boxes_positions:
                move = False
            else:
                box[1] += 1
                move = True
        if move:
            player_position[1] += 1
            score += 1
    elif direction == "up":
        move = True
        if [player_position[0] - 1, player_position[1]] in wall_positions:
            move = False
        elif [player_position[0] - 1, player_position[1]] in boxes_positions:
            for box_pos in boxes_positions:
                if box_pos == [player_position[0] - 1, player_position[1]]:
                    box = box_pos
            if [box[0] - 1, box[1]] in wall_positions or [box[0] - 1, box[1]] in boxes_positions:
                move = False
            else:
                box[0] -= 1
                move = True
        if move:
            player_position[0] -= 1
            score += 1
    elif direction == "down":
        move = True
        if [player_position[0] + 1, player_position[1]] in wall_positions:
            move = False
        elif [player_position[0] + 1, player_position[1]] in boxes_positions:
            for box_pos in boxes_positions:
                if box_pos == [player_position[0] + 1, player_position[1]]:
                    box = box_pos
            if [box[0] + 1, box[1]] in wall_positions or [box[0] + 1, box[1]] in boxes_positions:
                move = False
            else:
                box[0] += 1
                move = True
        if move:
            player_position[0] += 1
            score += 1
    prev_move = player_position
    print(score)

def checkPlayerDirection(direction):
    if direction == "left":
        return pygame.image.load("player_22.png")
    elif direction == "right":
        return pygame.image.load("player_19.png")
    elif direction == "up":
        return pygame.image.load("player_08.png")
    elif direction == "down":
        return pygame.image.load("player_05.png")

def showCompletedScreen():
    screen = pygame.display.set_mode((612, 382))
    bg = pygame.image.load("completed.jpg")
    screen.blit(bg, (0, 0))
    pygame.display.update()
    pygame.time.delay(1000)

def drawGameSurface(right_surface):
    wall_image = pygame.image.load("block_02.png")
    crate_image = pygame.image.load("crate_02.png")
    crate_target_image = pygame.image.load("crate_12.png")
    target_image = pygame.image.load("crate_27.png")

    right_surface.fill((255, 255, 255))
     
    for index_row, row in enumerate(game_map_matrix):
        for index_col, col in enumerate(row):
            tile = game_map_matrix[index_row][index_col]
            tile_rect = pygame.Rect(index_col * OBJECT_SIZE, index_row * OBJECT_SIZE, OBJECT_SIZE, OBJECT_SIZE)

            if tile == 1:
                right_surface.blit(resize_image(wall_image), tile_rect.topleft)
            elif tile == 3:
                right_surface.blit(resize_image(target_image), tile_rect.topleft)

    for box_pos in boxes_positions:
        y_coordinate, x_coordinate = box_pos
        box_rect = pygame.Rect(x_coordinate * OBJECT_SIZE, y_coordinate * OBJECT_SIZE, OBJECT_SIZE, OBJECT_SIZE)
        if box_pos in target_positions:
            right_surface.blit(resize_image(crate_target_image), box_rect.topleft)
            game_map_matrix[y_coordinate][x_coordinate] = 3
        else:
            right_surface.blit(resize_image(crate_image), box_rect.topleft)

    y_coordinate, x_coordinate = player_position
    player_rect = pygame.Rect(x_coordinate * OBJECT_SIZE, y_coordinate * OBJECT_SIZE, OBJECT_SIZE, OBJECT_SIZE)
    right_surface.blit(resize_image(player_image), player_rect.topleft)

    screen.blit(right_surface, (split_width, 0))

def drawCompilerSurface(left_surface):
    global user_text, base_font
    left_surface.fill((0, 0, 0))

    base_font = pygame.font.Font(None, 30)
    text_surface = base_font.render("Command Line:", True, (255, 255, 255))
    left_surface.blit(text_surface, (8, 10))

    base_font = pygame.font.Font(None, 35)
    text_surface = base_font.render("> ", True, (255, 255, 255))
    left_surface.blit(text_surface, (8, 30))

    position = 1.4*OBJECT_SIZE + 30
    base_font = pygame.font.Font(None, 25)
    text_surface = base_font.render(user_text, True, (255, 255, 255))
    left_surface.blit(text_surface, (30, 36))

    base_font = pygame.font.Font(None, 30)
    text_surface = base_font.render("Command List:", True, (255, 255, 255))
    left_surface.blit(text_surface, (8, 1.4*OBJECT_SIZE))

    for command in commands:
        text = str(command)
        base_font = pygame.font.Font(None, 23)
        text_surface = base_font.render(text, True, (255, 255, 255))
        left_surface.blit(text_surface, (8, position))
        position = position + 25

    screen.blit(left_surface, (0, 0))

def checkUserInput(user_text):
    movedown_control = ['movedown', 'movedown()', 'md']
    moveup_control = ['moveup', 'moveup()', 'mu']
    moveleft_control = ['moveleft','moveleft()','ml']
    moveright_control = ['moveright', 'moveright()', 'mr']

    if user_text in movedown_control:
        return 'movedown()'
    elif user_text in moveup_control:
        return 'moveup()'
    elif user_text in moveleft_control:
        return 'moveleft()'
    elif user_text in moveright_control :
        return 'moveright()'
    else:
        parsed = parser(user_text)
        try:
            if len(parsed) > 0:
                if 'for' in user_text:
                    if 'mr' in user_text:
                        user_text = user_text.replace('mr', checkUserInput('mr'))
                    elif 'ml' in user_text:
                        user_text = user_text.replace('ml', checkUserInput('ml'))
                    elif 'md' in user_text:
                        user_text = user_text.replace('md', checkUserInput('md'))
                    elif 'mu' in user_text:
                        user_text = user_text.replace('mu', checkUserInput('mu'))
                    return user_text
                else:
                    return 'pass'
        except Exception as e:
            return 'pass'

def main():
    global level, screen, score, boxes_positions, screen_width, screen_height, split_height, direction, player_image, user_text, commands, prev_move

    level = 0
    score = 0

    direction = "down"
    loadMapLevel(level)

    initial_player_position = player_position.copy()

    user_text = ''
    commands = []
    
    # Game loop
    game_running = True

    while game_running:
        player_image = checkPlayerDirection(direction)

        # Draw compiler surface
        drawCompilerSurface(left_surface)

        # Draw the game on top surface
        drawGameSurface(right_surface)

        # Update the display
        pygame.display.update()

        event = pygame.event.wait()
        if event.type == pygame.QUIT:
                game_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                print("User submitted text:", user_text)
                for command in commands:
                    exec(command)
                user_text = ""
                commands = []
            elif event.key == pygame.K_END:
                # Cheat code: end level
                boxes_positions = target_positions
            elif event.key == pygame.K_ESCAPE:
                if initial_player_position == player_position:
                    quit_game = True
                else:
                    commands = []
                    user_text = ""
                    loadMapLevel(level)
                    initial_player_position = player_position.copy()
            elif event.key == pygame.K_RETURN:
                    # User pressed Enter, do something with the input
                    print(checkUserInput(user_text))
                    commands.append(checkUserInput(user_text))
                    user_text = ""
            elif event.key == pygame.K_BACKSPACE:
                # User pressed Backspace, remove the last character
                user_text = user_text[:-1]
            elif event.key == pygame.K_DELETE:
                # User pressed Backspace, remove the last character
                user_text = ""    
            else:
                # Other key press, append the character to the input
                user_text += event.unicode

            boxes_positions.sort()
            target_positions.sort()

            ## If the player wins, do the following:
            if boxes_positions == target_positions:
                if level < 89:
                    level += 1
                else:
                    quit_game = True
                showCompletedScreen()
                loadMapLevel(level)
                initial_player_position = player_position.copy()

pygame.init()

main()

pygame.quit()