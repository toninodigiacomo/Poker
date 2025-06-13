# The script of the game goes in this file.

## Ren'Py Screen Definitions
define config.screen_width = 2560
define config.screen_height = 1440

# The game starts here.

label start:

    # Initialize the game
    $ game = GameState()
    $ game.create_deck()
    $ game.players = [Player(name="Player 1", is_human=True), Player(name="AI Player", is_human=False)]
    $ game.deal_hands()  # Deal initial cards to players

    # Display the poker game screen
    show screen poker_game

    # Loop to handle the game logic
    while True:
        # Wait for the player to interact (e.g., press buttons)
        $ result = ui.interact()

        # Check the result of the player's action and handle accordingly
        if result == "bet":
            $ game.pot += game.players[0].bet(10)  # Example: player bets 10 chips
        elif result == "call":
            $ game.pot += 10  # Example: calling the opponent's bet
        elif result == "fold":
            return  # End the current game loop if the player folds
        elif result == "next_round":
            $ game.community_cards = []
            $ start_new_round()  # Appelle la fonction start_new_round

    # This ends the game.
    return
