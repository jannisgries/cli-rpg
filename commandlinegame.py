import random
import pathlib
import csv
import sys
import os
import ast
import time 

########################################################################
# Functions for Game Functionalities
########################################################################
horizontal_line = "__________________________________________"

def save_game(player_name: str = "", player_state: str = "", player_returns: str = "", player_items: list = [], player_dead_enemies: list = []):
    """Save the current state of the game

    Args:
        player_name (str, optional): Name of the player. Defaults to "".
        player_state (str, optional): State of the game play. Defaults to "".
        player_returns (str, optional): Tracking, whether player goes down or up the track (return). Defaults to "".
        player_items (list, optional): Items which player collected. Defaults to [].
        player_dead_enemies (list, optional): Enemies the player defeated. Defaults to [].
    """
    game_path = pathlib.Path.home().joinpath(
        "Documents/codingnomads/projects/CLI-RPG/active-game.csv")
    with open(game_path, "w") as gamefile:
        row = [player_name, player_state, player_returns,
               player_items, player_dead_enemies]
        gamewriter = csv.writer(gamefile)
        gamewriter.writerow(row)

def open_game():  
    """Start game by start new session or opening up old one; initialization of values, if necessary

    Returns:
        All neccessary Information for gameplay
        str: name of player,
        str: state of player
        str: tracking var, whether player goes down or up (return)
        list: items player collected
        list: enemies player defeated
    """
    game_path = pathlib.Path.home().joinpath(
        "Documents/codingnomads/projects/CLI-RPG/active-game.csv")
    # Check if file exists
    if game_path.exists() == True:
        with open(game_path, "r") as gamefile:
            headers = ["player_name", "player_state", "player_returns",
                       "player_items", "player_dead_enemies"]
            reader = csv.DictReader(gamefile, fieldnames=headers)
            player_info = list(reader)[0]
            player_name = player_info["player_name"]
            player_state = player_info["player_state"]
            player_returns = player_info["player_returns"]
            player_items = ast.literal_eval(player_info["player_items"])
            player_dead_enemies = ast.literal_eval(player_info["player_dead_enemies"])
        # Workaround to handle corrupt file
        if player_name == "":
            player_name = input_and_validation("Tell me your name", ["any"])
            player_state = ""
            player_returns = ""
            player_items = []
            player_dead_enemies = []
        else:
            print("\nDo you want to start a new game or open your previous one?")
            start_new_game = input_and_validation(
                "Type in 'open' to open your game or 'new' to start a new one", {"open", "new"})
    # No file exists        
    else:
        start_new_game = "new"
    # Start new game
    if start_new_game == "new":
                player_name = input_and_validation(
                    "Tell me your name", ["any"])
                player_state = ""
                player_returns = ""
                player_items = []
                player_dead_enemies = []
    #Override the saved file with the current game   
    save_game(player_name, player_state, player_returns, player_items, player_dead_enemies)
    # Return all necessary items to start game
    return player_name, player_state, player_returns, player_items, player_dead_enemies

def exit_game(option: str = ""):
    """Function to end the game aka execution of script

    Args:
        option (str, optional): Possible arguments for the function are 'immediate' (Quit game w/out asking player if game should be save) 
        or 'restart' (Give player opportunity to restart the game). Defaults to "".
    """
    # Check if Player wants to restart the game
    if option == "restart":
        chosen_action = input_and_validation("Would you like to play again? \nType in 'restart' to restart, 'no' to end the game",{"no"})
        if chosen_action == "no":
            sys.exit("\nThanks for playing with us!\n")
    # Game is closed immediatly w/out asking to save
    elif option == "immediate":
        sys.exit("\nThanks for playing with us!\n")
    # Ask player to save the game and quit
    else:
        print(f"{horizontal_line}")
        print("\nDo you want to save your current state of the game ?")
        save_game_choice = input_and_validation(
            "Type in 'yes' to save your game or 'no' to just leave", {"yes", "no"})
        if save_game_choice == "yes":
            if "player_name" in globals():
                save_game(player_name, player_state, player_returns,
                        player_items, player_dead_enemies)
            else:
                print("\nSorry, but there is nothing to save.")
        sys.exit("\nThanks for playing with us!\n")

def input_and_validation(message: str, valid_options: set) -> str:
    """Ask user for input and validate his input based on the provided options. If not valid, ask again.

    Args:
        message (str): Message, which prompts user to input a value
        valid_options (set): Valid options, which the user may return as input

    Returns:
        str: User input as string, which has been validated
    """
    while True:
        # Ask for User Input
        user_input = input("\n" + message + ": ")
        # Check if User Input is a predefined keyword which gives player certain options
        ## Exit the game
        if user_input.lower() == "exit":
            exit_game()
        ## Save the current progress
        elif user_input.lower() == "save":
            print(f"{horizontal_line}")
            if "player_name" in globals():
                save_game(player_name, player_state, player_returns,
                          player_items, player_dead_enemies)
                print("\nYour progress has been saved.")
            else:
                print("\nSorry, but there is nothing to save.")
            print(f"{horizontal_line}")
        ## Display items, which the player currently has
        elif user_input.lower() == "items":
            print(f"{horizontal_line}")
            if player_items == []:
                print("\nYou currently have no items in your bag.")
            else:
                name_of_player_items = [x['name'] for x in player_items]
                print("\nThese are the current items in your bag: " +
                      ", ".join(name_of_player_items))
            print(f"{horizontal_line}")
        ## Display a game map
        elif user_input.lower() == "map":
            print(f"{horizontal_line}")
            basic_game_map = ("\n"
                "            ||             \n"
                "   left---middle----right  \n"
                "   ||       ||        ||   \n"
                )
            if player_state == "":
                game_map = basic_game_map
            elif player_state.startswith("_leftroom"):
                game_map = basic_game_map + "   You                     "
            elif player_state.startswith("_middleroom"):
                if player_state.startswith("_middleroom_go down_oldroom"):
                    game_map = basic_game_map + (
                        "            ||             \n"
                        "            /\\            \n"
                        "          old modern       \n"
                        "          ||               \n"
                        "          You              "
                        )
                elif player_state.startswith("_middleroom_go down_modernroom"):
                    game_map = basic_game_map + (
                        "            ||             \n"
                        "            /\\            \n"
                        "          old modern       \n"
                        "                ||         \n"
                        "                You        "
                        )
                elif player_state == "_middleroom_go down":
                    game_map = basic_game_map + (
                        "            ||             \n"
                        "            You            \n"
                        "            /\\            \n"
                        "          old modern       "
                        )
                else: 
                    game_map = basic_game_map + "            You            "           
            elif player_state.startswith("_rightroom"):
                game_map = basic_game_map + "                      You "
            print(game_map)
            print(f"{horizontal_line}")
        ## Display help message
        elif user_input.lower() == "help":
            print(f"{horizontal_line}")
            print("\nWelcome to a new Dungeons and Dreagons game.\nLet´s discuss some rules at the beginning. At any time, you can type 'exit' to quit the game, 'save' to save your current progress, 'items' to see your current items, 'map' to see a map of the game or 'help' to view this message again.")
            print(f"{horizontal_line}")
        ## Restart the game
        elif user_input.lower() == "restart":
            print(f"{horizontal_line}")
            restart_decision = input_and_validation("Are you sure? Type in 'yes' or 'no'",
                                                 {"yes", "no"})
            if restart_decision == "yes":
                os.execv(sys.executable, ['python'] + [sys.argv[0]])
        # Start Input-Validation
        ## User may provide anything (eg. his name)
        elif "any" in valid_options:
            print(f"{horizontal_line}")
            load_answer()
            break
        ## User may only provide certain valid options
        elif user_input not in valid_options:
            options = ""
            for option in valid_options:
                options += f"'{option}' or "
            options = options[:-4]
            print(f"{horizontal_line}")
            print(
                f"\nI am sorry, but you have to type either {options}.", end="\n")
            print(f"{horizontal_line}")
        ## User provided a valid option
        else:
            print(f"{horizontal_line}")
            load_answer()
            break
    return user_input

def load_answer(dots_per_second: float = 3):
    """Animation function to make the game look more interative. During a short amount of time, loading-dots are displayed.

    Args:
        dots_per_second (float, optional): Provide the ammount of dots, which are load per second. Defaults to 3.
    """
    # number of characters to print out per second
    loading_string = "." * 3 # characters to print out one by one (6 dots in this example)
    for n in range(0,1):
        #  track both the current character and its index for easier backtracking later
        for index, char in enumerate(loading_string):
            # you can check your loading status here
            # if the loading is done set `loading` to false and break
            sys.stdout.write(char)  # write the next char to STDOUT
            sys.stdout.flush()  # flush the output
            time.sleep(1.0 / dots_per_second)  # wait to match our speed
        index += 1  # lists are zero indexed, we need to increase by one for the accurate count
        # backtrack the written characters, overwrite them with space, backtrack again:
        sys.stdout.write("\b" * index + " " * index + "\b" * index)
        sys.stdout.flush()  # flush the output
    
########################################################################
# Functions for Game Interaction
########################################################################

def choose_doors(*args, can_return: bool = False):
    """Display given doors to the user and let him decide, which one he would like to go through. Takes current user state and adds user decision.

    Args:
        door_names (string): Name of the doors, the user may choose (have to be unique)
        can_return (bool, optional): Give user the option not only to go through the doors but return to the previous state. Defaults to False.

    Returns:
        string: new state of the player
        string: displays if user is going down or up (return)
    """
    player_returns = False
    number_of_doors = len(args)
    # Visualization of door options (flexible amount if doors) 
    vis_door_top = ""
    vis_door_middle = ""
    vis_door_bottom = ""
    vis_door_name = ""
    for door in args:
        if len(door) > 5:
            door_name = door[:6]
        else:
            door_name = door
        vis_door_top += "  ___  "
        vis_door_middle += " |   | "
        vis_door_bottom += "  ---  "
        vis_door_name += f"{door_name:^7}"
    vis_door_top += "\n"
    vis_door_middle += "\n"
    vis_door_bottom += "\n"
    vis_door_name += "\n"
    door_visualization = vis_door_top + \
        (vis_door_middle * 3) + vis_door_bottom + vis_door_name
    # Generate string of doors for message, which is displayed to user
    doors = set(f"{door} door" for door in args)
    door_options = ""
    for door in doors:
        door_options += f"'{door}' or "
    door_options = door_options[:-4]
    # Display Message to user and take user input
    if can_return == False:
        print(
            (f"\nOk, {player_name}. I see, that you are standing in front of {number_of_doors} doors.\n"
            f"{door_visualization}"
            "Through which one would you like to go?"))
        chosen_action = input_and_validation(f"Write eithter {door_options} to select either of them", 
                                         doors)
    else:
        doors.add('return')
        door_visualization += "OR: Return to prev. room\n"
        print(
            (f"\nOk, {player_name}. I see, that you are standing in front of {number_of_doors} doors.\n"
            f"{door_visualization}"
            "Through which one would you like to go - or do you want to return?"))
        chosen_action = input_and_validation(f"Write eithter {door_options} to select either of them - you may also type 'return' to go back to the previous room", 
                                         doors)
    # Define new player state based on the given input
    chosen_action = chosen_action.split()[0]
    if chosen_action == "return":
        new_state = player_state.rsplit("_", 1)[0]
        player_returns = True
    else: 
        room_to_enter = chosen_action + "room"
        new_state = f"{player_state}_{room_to_enter}"
    return new_state, player_returns

def decide_options(options: set):
    """Display given options to the user and let him decide, which option to take

    Args:
        options (set): available options for user to choose

    Returns:
        string: new state of the player
        string: displays if user is going down or up (return)
    """
    player_returns = False
    # Generate string of options for message, which is displayed to user
    string_options = ""
    for opt in options:
        string_options += f"'{opt}' or "
    string_options = string_options[:-4]
    # Display Message to user and take user input
    chosen_action = input_and_validation(f"Write eithter {string_options} to select either of them",
                                                options)
    # Define new player state based on given input
    if chosen_action == "return":
        #Split the last decision-option to return to previous playing state
        new_state = player_state.rsplit("_", 1)[0]
        player_returns = True
    elif chosen_action == "stay":
        new_state = player_state
    else: 
        new_state = f"{player_state}_{chosen_action}" 
    return new_state, player_returns

def filter_room(items_to_find: list = [], enemies_to_find: list = []) -> dict:
    """Filter predefined room in order to exclude items, which user already has, as well as enemies, the user already defeated

    Args:
        items_to_find (list, optional): predefined items of the room. Defaults to [].
        enemies_to_find (list, optional): predefined enemies of the room. Defaults to [].

    Returns:
        dict: returns room dict, which contains both filtered items and enemies
    """
    # Example of Input
    ## items = [{"name": "sowird", "score" : 10, "type":"weapon"}}]
    ## enemies = [{"name"="dragon", "defeat_items":"", "defeat_condition": "", "loss_consequence": "death", "canHide": True}]
    filtered_room = {}
    list_of_enemies = []
    list_of_items = []
    #Filter enemies by comparing enemies with defeated enemies
    if enemies_to_find:
        for enemy in enemies_to_find:
            if enemy["name"] not in player_dead_enemies:
                list_of_enemies.append(enemy)
    # Filter items by comparing items with player_items
    elif items_to_find:
        for item in items_to_find:
            if item not in player_items:
                list_of_items.append(item)
    filtered_room.update({"items": list_of_items})
    filtered_room.update({"enemies": list_of_enemies})
    # return the filtered room
    return filtered_room

def take_item(item: dict = {}):
    # item = {"name": "", "type":"weapon/multiplier_item/discover_item/special_item/death_item", "score":"", "string_image":""}
    if item != {}:
        print(f"\nYou found a new item: {item['name']}! Do you want to take it ?")
        #Manually add drawings of items
        if item["string_image"] != "":
            print(item["string_image"])       
        chosen_action = input_and_validation("Write either 'take' or 'leave' to select either of them",
                                                        {"take", "leave"})
        if chosen_action == "take":
            if item["type"] == "death_item":
                print(f"\nUf, to take this {item['name']} wasn´t a good choice. As your gaze beginns to rotate, you realize this wasn´t a good idea.")
                print(f"The {item['name']} was toxic - you die and loose the game.")
                print(f"{horizontal_line}")
                exit_game("restart")
            else:
                player_items.append(item)

def fight_enemy(enemy: dict = {}):
    """Process of player fighting a predefined enemy

    Args:
        enemy (dict, optional): Predefined enemy. Defaults to {}.

    Returns:
        As fight may has consequences on user items or enemies defeated by the player, theses variables have to be updates
        list: items of player
        list: enemies the player has defeated
    """
    # Example of enemy
    ## enemies = [{"name"="dragon", "defeat_items":"", "defeat_condition": "", "loss_consequence": "death", "canHide": True}]
    if enemy != {}:
        print(f"\nOh boy, you have encountered a {enemy['name']}. Would you like to fight it or hide and back off ?")
        # When encountering an enemy, user may decide to fight or hide
        chosen_action = input_and_validation("Write eithter 'fight' or 'hide' to select either of them",
                                                 {"fight", "hide"}) 
        outcome = "loss"
        ## User decides to fight
        if chosen_action == "fight":
            # The fight outcome depends on two variables: Items and Condition
            # 1. User need to have all the necessary items to win the fight
            if set(enemy['defeat_items']).issubset(set([x['name'] for x in player_items])):
                print("\nLuckily, you have all the necessary weapons: " + ", ".join(enemy['defeat_items']))
                # 2. Furthermore, each enemy has an individual defeat condition
                ## There are different kinds of conditions: random, dice, damage, none
                ### Random: The outcome is decided by random choice
                if enemy["defeat_condition"] == "random":
                    num = random.randint(0,1)
                    if num == 1:
                        outcome = "win"
                ### Dice: The outcome depends on a user´s virtual dice throw
                elif enemy["defeat_condition"].startswith("dice"):
                    # Predefined condition may be: bigger, smaller or equal to dice number
                    ## example: dice +6
                    # Let the user dice
                    print("\nThe outcome of the fight depends on your dice throw! Are you ready?", end="")
                    chosen_action = input_and_validation("Type in 'dice' to throw the dices",
                                                 {"dice"})
                    num = random.randint(1,6)
                    print(f"\nYou rolled a {num}")
                    # Try dice throw with condition
                    condition = enemy["defeat_condition"].split()[1]
                    condition_number = int(condition[-1])
                    ## Dice-Throw-Number bigger than defined number
                    if condition.startswith("+"):
                        if num > condition_number:
                            outcome = "win"
                    ## Dice-Throw-Number smaller than defined number
                    elif condition.startswith("-"):
                        if num < condition_number:
                            outcome = "win"
                     ## Dice-Throw-Number euql to defined number
                    elif condition.startswith("="):
                        if num == condition_number:
                            outcome = "win"            
                #### Damage: The outcome depends on the damage, the user can inflict on enemy
                elif enemy["defeat_condition"].startswith("damage"):
                    # Predifend condition contains treshhold of damage and (optional) mulitplier condition (dice / none)
                    ## Example: damage>10&multiplier 
                    condition = enemy["defeat_condition"].split(">")[1]
                    condition_number = int(condition.split("&")[0])
                    condition_muliplier = condition.split("&")[1]
                    # Find the user fight-score = damage he inflicts
                    ## 1. Multiplyier Items
                    ### Check if user has muliplying items, which multiply the damage of weapons
                    multiplier_items = [x["score"] for x in player_items if x["type"] == "multiplier_item"]
                    muliplier = 1
                    for num in multiplier_items:
                        muliplier *= num
                    ### Help user with a hint, if he has no such items
                    if muliplier == 1:
                        print("\nBut I noticed, you have no items which amplify the strength of your weapon - this is a pitty.")
                    ## 2. Weapons
                    ### Find score of the weapons, which can be used for the concrete enemy
                    weapon_score = 0
                    useable_weapon_items = [x["score"] for x in player_items if x["type"] == "weapon" and x["name"] in enemy["defeat_items"]]
                    for num in useable_weapon_items:
                            weapon_score += num
                    ## 3. Combine multiplying items and weapons to fight score = damage
                    user_fight_score = weapon_score * muliplier
                    # Apply (external) multiplier if in predefined condition of enemy
                    ## no external multiplier
                    if condition_muliplier == "":
                        if user_fight_score > condition_number:
                            outcome = "win"
                    ## external muliplier == dice
                    elif condition_muliplier == "dice":
                        # let user throw dices          
                        print("\nThe outcome of the fight depends on your dice throw! Are you ready?", end="")
                        chosen_action = input_and_validation("Type in 'dice' to throw the dices",
                                                    {"dice"})
                        num = random.randint(1,6)
                        print(f"\nYou rolled a {num}")
                        # multiply user fight score with multiplier
                        user_fight_score *= num
                        if user_fight_score > condition_number:
                            outcome = "win"                        
                else:
                    outcome = "win"            
            else: 
                print(f"\nUf, fighting a {enemy['name']} without the right kind of weapons – this was hopeless.", end=" ")
        ## User decides to hide
        elif chosen_action == "hide":
            # Player can´t hide of all enemies
            ## If player cant hide but does, he looses the fight
            if enemy['canHide'] == False:
                print(f"\nUps, you can´t hide from a {enemy['name']}")
                outcome = "loss"
            else: 
                outcome = "hidden"
        # Determine consequences of win / loss
        updated_player_items = player_items
        updated_player_dead_enemies = player_dead_enemies
        ## Player lost the fight
        if outcome == "loss":
            # Different, predefined consequences
            ## Death
            if enemy['loss_consequence'] == "death":
                print(f"You got eaten by the {enemy['name']} and lost the game. I am sorry.")
                exit_game("restart")
            ## Loss of all items, but no death
            elif enemy['loss_consequence'] == "loose_items":
                print(f"Whoa, this did not end up lucky for you - you have lost all your items.")
                updated_player_items = []
        ## Player won the fight
        elif outcome == "win":
            print(f"\nCongratulations, {player_name}! You defeated the {enemy['name']}!")
            # Add enemy to list of defeated enemies
            updated_player_dead_enemies.append(enemy["name"])
            # Check if user has won the game
            check_win()
    return updated_player_items, updated_player_dead_enemies

def check_win():
    """Check if user has won the game. Check user against winning condition and display message.
    """
    # Winning Condition
    if set(["dragon","leprechaun"]).issubset(set(player_dead_enemies)):
        print(f"{horizontal_line}")
        print(("\n"
            "#                     #  #  #       #\n"
            " #         #         #   #  # #     #\n"
            "  #       # #       #    #  #  #    #\n"
            "   #     #   #     #     #  #   #   #\n"
            "    #   #     #   #      #  #    #  #\n"
            "     # #       # #       #  #     # #\n"
            "      #         #        #  #       #"    
        ))
        print(f"{horizontal_line}")
        print("\nCongratulations, you have found all the enemies in this place. You may now run around this place for as long as you want - or exit the game.")
        print(f"{horizontal_line}")
        input_and_validation("Write 'continue' to continue the game or 'exit' to exit the game",
                                                     {"continue"})

########################################################################
# Game Introduction
########################################################################
# Introduction
print(f"\n{horizontal_line}")
print((
    "####         ###       ####   \n"
    "#   #       #   #      #   #  \n"
    "#    #     #     #     #    #   \n"   
    "#     #   #       #    #     #    \n"
    "#     #   #       #    #     #    \n"
    "#    #    # # # # #    #    #  \n"  
    "#   #     #       #    #   #   \n"
    "####      #       #    ####   "
))
print(f"{horizontal_line}")
print("\nWelcome to a new Dungeons and Dreagons game.\nLet´s discuss some rules at the beginning. At any time, you can type 'exit' to quit the game, 'save' to save your current progress, 'items' to see your current items, 'map' to see a map of the game or 'help' to view this message again.")
print(f"{horizontal_line}")
# Load current game or initiallize a new game
player_name, player_state, player_returns, player_items, player_dead_enemies = open_game()
# Display a message that greets them and introduces them to the game world.
print((f"""\nHello, {player_name}! I am so happy, that you joined our game world. Let´s start a new Dungeons and Dreagons game.\n"""
      f"""In order to play, you will have to talk to me and take some decisions. Are you ready? \nGreat! Lets Go…"""))
print(f"{horizontal_line}")
load_answer(1)

########################################################################
# Start of the game logic
########################################################################
while True:
    # Logic depends on Player states rather than Rooms - To have a logical structure in the code, the if statements are grouped by .startwith()
    # Each decision-situation may have to deverging messages, depending on the player going down or up (return way) > player_returns
    ########################################################################
    # Start-Room
    if player_state == "":
        player_state, player_returns = choose_doors("left", "middle", "right")

    ########################################################################
    # Left-Room 
    elif player_state.startswith("_leftroom") == True:
        # Left Room - Start
        if player_state == "_leftroom":
            if player_returns == False:
                print("\nAs you walk into the room behind the left door, you see that the room is empty. You may now decide to return to the previous room or inspect the room further.")
            else: 
                print("\nYou are standing on the edge of the seemingless empty room on the left side again - You may now decide to return to the previous room or inspect the room again.")
            player_state, player_returns = decide_options({"return", "inspect"})
       # Left Room - Decision: Inspect
        elif player_state == "_leftroom_inspect":
            if player_returns == False:
            # As this is the end of this room-branch, there is no possible return
                sword_image = ("\n"
                            "  /\  \n"
                            " |  | \n"
                            " |  | \n"
                            " |  | \n"
                            " |  | \n"
                            "-    -\n"
                            "-    -\n"
                            " |  | \n"
                            )
                sword_item = {"name": "sword", "type":"weapon", "score": 10, "string_image": sword_image}
                room = filter_room(items_to_find=[sword_item])
                if room["items"] != []:
                    print("\nYou start to closely inspect the seemingless empty room - oh what is this:", end=" ")
                    for item in room["items"]:
                        take_item(item)
                else: 
                    print("\nThere is nothing more to find in this room")
                print("\nWould you like to stay in the room or return ?")
                player_state, player_returns = decide_options({"return", "stay"})
                
    ########################################################################
    # Middle-Room 
    elif player_state.startswith("_middleroom") == True:
        # Middle-Room-Start
        if player_state == "_middleroom":
            if player_returns == False:
                print("\nOh, this room seems to just be hallway for further adventures. It is a very long and narrow corridor with some light at the end.\nDo you want to go down the hallway or return ?", end="\n")
            else:
                print("\nHere you are, back at the beginning of the narrow corridor behind the middle door. Would you like to return through the middle door or head back down the hallway?", end="\n")
            player_state, player_returns = decide_options({"go down", "return"})

        #Middle-Room-Go Down
        elif player_state.startswith("_middleroom_go down"):
            if player_state == "_middleroom_go down":
                if player_returns == False:
                    print("\nSo, the light at the end of the corridor is a torch stuck between two doors.")
                else:
                    print("\nYou are now standing in front of the two doors again, which are seperated by a torch.")
                player_state, player_returns = choose_doors("old", "modern", can_return=True)
            elif player_state.startswith("_middleroom_go down_oldroom"):
                if player_state == "_middleroom_go down_oldroom":
                    if player_returns == False:
                        print("\nThe oak door creaks heavily as you push it, but with some effort you manage to open it. You look into a dusty and mysterious room - where you can´t see anything.")
                        print("\nWould you like to inspect the dark room or return?")
                    else: 
                        print("\nYou stand at the edge of room and extinguish your torch again. You may go back and inspect the room again or return through the old door.")
                    player_state, player_returns = decide_options({"inspect", "return"})
                if player_state == "_middleroom_go down_oldroom_inspect":
                    if "torch" in [x['name'] for x in player_items]:
                        print("\nWhen you are already about to go into the room, you remeber, that you have picked up a torch before.\nYou light up your torch and look into the room:")
                        load_answer(1)
                        print("\nThat was close: You are literally standing on the edge of a cliff. But with the light of the torch you manage to circumvent the danger - and head straight to an old box, which stands right behind the cliff.")
                        print("\nYou open up the box, and:")
                        load_answer(1)
                        ring_image = (
                        "   __  \n"
                        " /    \ \n"
                        "|      |\n"
                        " \\    /\n"
                        "   -- \n"                
                        )
                        ring_item = {"name": "ring", "type":"multiplier_item", "score": 2, "string_image": ring_image}
                        room = filter_room(items_to_find=[ring_item])
                        if room["items"] != []:
                            for item in room["items"]:
                                take_item(item)
                        else: 
                            print("\nThere is nothing more to find here.")
                        if "sword" in [x['name'] for x in player_items]:
                            print("\nThis is a pretty ring - actually, did you realize, that your sword started shining once you took the ring ?")
                        else: 
                            print("\nThis is a pretty ring - actually, did you realize, there is a sword engraved on the side of the ring?")
                        print("\nWould you like to stay here or return ?")
                        player_state, player_returns = decide_options({"return", "stay"})

                    else:
                        print("\nIt is super dark in this room - what were you thinking? You carefully take your first leap...")
                        load_answer(1)
                        print("and step into the void. You lose your balance and fall into the depths of a cliff. Sorry, you have died and lost the game.")
                        exit_game("restart")
            elif player_state.startswith("_middleroom_go down_modernroom"):
                room = filter_room(enemies_to_find=[{"name" : "leprechaun", "defeat_items": ["sword"], "defeat_condition":"dice -5", "loss_consequence": "loose_items", "canHide": False}])
                for enemy in room["enemies"]:
                    player_items, player_dead_enemies = fight_enemy(enemy) 
                room = filter_room(enemies_to_find=[{"name" : "leprechaun", "defeat_items": ["sword"], "defeat_condition":"dice -5", "loss_consequence": "loose_items", "canHide": False}])
                if room["enemies"] == []:                    
                    torch_image = ("\n"
                        "    \\\\||||||//  \n"
                        "      \\||||/     \n"    
                        "       |  |     \n"
                        "       |  |     \n"
                        "       |  |     \n"
                        "       |  |     \n"
                        )
                    torch_item = {"name": "torch", "type":"discover_item", "score": 0, "string_image": torch_image}

                    berry_image = ("\n"
                        "   |       \n"
                        "  / \\     \n"
                        "  \\ /     \n"
                        )
                    berry_item = {"name": "suspicious berry", "type":"death_item", "score": 0, "string_image": berry_image}
                    room_items = [
                        torch_item,
                        berry_item
                    ]
                    room = filter_room(items_to_find=room_items)
                    print("\nWithout the leprechaun standing in the way you are able to analyze the nest, in which he was collecting his prey.")
                    for item in room["items"]:
                        take_item(item)

                print("\nWould you like to stay or return?")
                player_state, player_returns = decide_options({"stay", "return"})

    ########################################################################
    # Right-Room
    elif player_state.startswith("_rightroom"):
        room = filter_room(enemies_to_find=[{"name" : "dragon", "defeat_items": ["sword"], "defeat_condition":"damage>41&dice", "loss_consequence": "death", "canHide": True}])
        for enemy in room["enemies"]:
            player_items, player_dead_enemies = fight_enemy(enemy) 
        print("\nThere is nothing more to find in this room")
        print("Would you like to stay in the room or return ?")
        player_state, player_returns = decide_options({"return", "stay"})
