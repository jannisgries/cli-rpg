# Ask the player for their name.
player_name = input("\n\n\nTell me your name: ")
chosen_door = ""
has_sword = False

# Display a message that greets them and introduces them to the game world.
print(f"Hello, {player_name}! I am so happy, that you joined our game world. Let´s start a new Dungeons and Dreagons game.\n\nIn order to play, you will have to talk to me and take some decisions. Are you ready? \nGreat! Lets Go…", end="\n\n")

while True:
    # Present them with a choice between two doors.
    print(
        (f"Ok, {player_name}. I see, that you are standing in front of two doors.\n"
         " ___    ___\n"
         "|   |  |   |\n"
         "|   |  |   |\n"
         " ---    ---\n"
         "Through which one would you like to go?"),
        end="\n\n")

    # Add input validation
    while True:
        chosen_door = input(
            "Write eithter 'left door' or 'right door' to select either of them: ")
        if chosen_door != "left door" and chosen_door != "right door":
            print("\n\nI am sorry, but you have to type 'left door' or 'right door'", end="\n\n")
        else:
            break

    # If they choose the left door, they'll see an empty room.
    if chosen_door == "left door":
        # When in the seemingly empty room, they can choose to look around. If they do so, they will find a sword. They can choose to take it or leave it.
        print("\n\nAs you walk into the room behind the left door, you see that the room is empty. You may now decide to return to the previous room or inspect the room further.", end="\n\n")
        while True:
            chosen_action = input(
            "Write eithter 'return' or 'inspect' to select either of them: ")
            if chosen_action != "return" and chosen_action != "inspect":
                print("\n\nI am sorry, but you have to type 'return' or 'inspect'", end="\n\n")
            else:
                break
        if chosen_action == "inspect":
            if has_sword == False:
                print("\n\nAh, after you were closely inspecting the seemingless empty room, you found a sword. \nDo you want to take it ?.", end="\n")
                print(
                    (
                    "  /\  \n"
                    " |  | \n"
                    " |  | \n"
                    " |  | \n"
                    " |  | \n"
                    "-    -\n"
                    "-    -\n"
                    " |  | \n"
                    ),
                end="\n\n")
                while True:
                    chosen_action = input(
                        "Write either 'take' or 'leave' to select either of them: ")
                    if chosen_action != "take" and chosen_action != "leave":
                        print(
                            "\n\nI am sorry, but you have to type 'take' or 'leave'", end="\n\n")
                    else:
                        break
                if chosen_action == "take":
                    has_sword = True
            print("\n\nAfter a close investigation you notice, there is nothing else than the sword in this room\nWould you like to return ?", end="\n\n")
            while True:
                chosen_action = input(
                    "Write either 'return' or 'stay' to select either of them: ")
                if chosen_action != "return" and chosen_action != "stay":
                    print("\n\nI am sorry, but you have to type 'return' or 'stay'", end="\n\n")
                else:
                    break
            while chosen_action == "stay":
                print("After yet another search you realize, there is for Sure nothing else than the sword in this room\nWould you like to return ?", end="\n\n")
                chosen_action = input(
                    "Write either 'return' or 'stay' to select either of them: ")
                while True:
                    chosen_action = input(
                        "Write either 'return' or 'stay' to select either of them: ")
                    if chosen_action != "return" and chosen_action != "stay":
                        print(
                            "\n\nI am sorry, but you have to type 'return' or 'stay'", end="\n\n")
                    else:
                        break

    # If they choose the right door, then they encounter a dragon.
    elif chosen_door == "right door":
        print("Oh boy, you are encountering a dragon. Would you like to fight the dragon or return to the previous room ?", end="\n\n")
        # When encountering the dragon, they have the choice to fight it.
        # If they have the sword from the other room, then they will be able to defeat it and win the game.
        # If they don't have the sword, then they will be eaten by the dragon and lose the game.
        while True:
            chosen_action = input(
                "Write eithter 'fight' or 'return' to select either of them: ")
            if chosen_action != "fight" and chosen_action != "return":
                print("\n\nI am sorry, but you have to type 'fighth' or 'return'", end="\n\n")
            else:
                break
        if chosen_action == "fight":
            if has_sword == True:
                print(
                    f"\n\nCongratulations, {player_name}! You defeated the dragon and won the game!", end="\n\n")
            else:
                print(f"\n\nUf, fighting a dragon without any kind of weapon – this was hopeless. You got eaten by the dragon and lost the game. I am sorry.", end="\n\n")
            break
