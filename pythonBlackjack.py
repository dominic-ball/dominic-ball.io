import random # random for use in shuffling the deck.
import time #for delays between print statements.

discardPile = []  # List to store removed cards.

# Card class:
class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def __str__(self):
        return f"{self.rank} of {self.suit}"
#card class end.


# Deck class begin:
class Deck:
    def __init__(self):
        self.cards = self.create_deck()  # Initialize with a full deck of cards.

    #creates the deck, then all 6 decks
    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

        deck = []

        # Uses a full 6 decks
        for i in range(6):
            for suit in suits:
                for rank in ranks:
                    value = values[rank]
                    deck.append(Card(suit, rank, value))
        return deck
    
    #draws a card, then removes it from the deck
    def draw_card(self):
        return self.cards.pop(0)
    
    # Shuffle the deck
    def shuffle(self):
        random.shuffle(self.cards)

    # Method to check if deck needs reshuffling (below 150 cards)
    def check_deck_size(self):
        if len(self.cards) < 150:  # reshuffle at 150
            print("\nReshuffling deck...\n")
            self.cards = self.create_deck()  # Recreate the deck
            self.shuffle()  # Shuffle the combined deck

# Hand class
class Hand:
    def __init__(self):
        self.hand = []

    #gives the numerical value of a hand
    #10 - all face cards: 10
    #Ace is 1 or 11
    #everything else is numerical value
    def calculate_hand(self):
        totalValue = 0
        aces = 0

        for card in self.hand:
            totalValue += card.value
            if card.rank == 'Ace':
                aces += 1

        # Adjust for Aces if total value exceeds 21
        while totalValue > 21 and aces:
            totalValue -= 10
            aces -= 1
        
        return totalValue

    # Adds card to hand
    def add_card(self, card):
        self.hand.append(card)

    # Prints the hand
    def print_hand(self):
        if not self.hand:
            print("\nHand is empty")
        else:
            for card in self.hand:
                print(card)

    def print_card(self, index):
       # Prints a specific card from the hand by index
        if 0 <= index < len(self.hand):
            print(self.hand[index])
        else:
            print("Invalid card index")

#runs the actual game itself
class gameRunner:
    def __init__(self):
        self.deck = Deck()  # Create a new deck of cards
        self.player_hand = Hand()  # Create a hand for the player
        self.dealer_hand = Hand()  # Create a hand for the dealer
        self.deck.shuffle()  # Shuffle the deck
        self.bust = False  # Initialize the bust attribute
        self.dealer_showing_all_cards = False  # Flag to track if dealer's second card should be shown

        # Begin UI setup, menu screen
        print()
        print("*_*_*_*_*_*_*_Welcome to BlackJack_*_*_*_*_*_*_*")  # Logo of sorts
        for i in range(2):  # Double line break
            print()

        self.player_balance = self.get_player_balance()  # Player balance

    # Method to get player's balance
    def get_player_balance(self):
        while True:
            try:
                balance = float(input("How much would you like to deposit?: "))
                if balance <= 0:
                    print("Please enter a positive amount.")
                else:
                    return balance
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    # Method to deal initial cards
    def deal_initial_cards(self):
        print()

        # Handles for insufficient funds
        while True:
            try:
                self.bet_amount = float(input("Enter Bet Amount: "))
                if self.bet_amount > self.player_balance:
                    print("Not Enough remaining in balance. Try Again!")
                elif self.bet_amount <= 0:
                    print("Bet must be greater than 0.")
                else:
                    self.player_balance -= self.bet_amount
                    break
            except ValueError:
                print("Invalid input. Please enter a valid bet amount.")

        print("\nDealing cards...")
        time.sleep(1)

        # Deal initial cards to player
        for i in range(2):
            drawn_card = self.deck.draw_card()
            self.player_hand.add_card(drawn_card)
            print(f"\nYou draw: {drawn_card}")
            time.sleep(1)

        # Check for Natural Blackjack (Ace + 10-value card) for the player
        if self.player_hand.calculate_hand() == 21 and len(self.player_hand.hand) == 2:
            print("\nNatural Blackjack! You win with 3-2 odds.")
            self.player_balance += self.bet_amount + (self.bet_amount * 1.5)
            return True  # Player wins instantly, skip to next round

        # Deal initial card to dealer
        drawn_card = self.deck.draw_card()
        self.dealer_hand.add_card(drawn_card)
        print(f"\nDealer draws: {drawn_card}")
        time.sleep(1)

        # Dealer's second card is face down
        drawn_card = self.deck.draw_card()
        self.dealer_hand.add_card(drawn_card)
        print("Dealer's second card is face down.")
        time.sleep(1)
        print("Dealer is taking a peek...")
        time.sleep(2)

        # Check if dealer has a Blackjack
        dealer_total = self.dealer_hand.calculate_hand()
        if dealer_total == 21 and len(self.dealer_hand.hand) == 2:
            self.dealer_showing_all_cards = True  # Show dealer's cards if Blackjack
            self.show_hands()
            print("Dealer has Blackjack!")
            if self.player_hand.calculate_hand() == 21:
                print("It's a push (both have Blackjack).")
                self.player_balance += self.bet_amount  # Return the bet
            else:
             print("Dealer wins with Blackjack.")
            return True  # End the round
        else:
            return False  # Continue the game if no natural Blackjack for dealer


    def show_hands(self):
        print()
        print("\nPlayer's hand:")
        self.player_hand.print_hand()
    
        print("\nDealer's hand:")
        if self.dealer_showing_all_cards:
            self.dealer_hand.print_hand()  # Print all dealer's cards if the flag is True
        else:
            # Show only the dealer's first card and a placeholder for the second card
            self.dealer_hand.print_card(0)
            print(" [Hidden Card]")

    # Player input for hit or stand
    def hit_or_stand(self):
        # Initialize player_total with the current hand's value
        player_total = self.player_hand.calculate_hand()  
        player_turn = True
        while player_turn:
            print()

            choice = input("Hit or stand: ").lower()
            #input: hit
            #adds a card to player's deck, prints the value, etc.
            if choice == "hit":
                drawn_card = self.deck.draw_card()  # Draw a card from the deck
                self.player_hand.add_card(drawn_card)  # Add the card to the player's hand
                time.sleep(0.5)
                print(f"You drew a {drawn_card}")
        
                # Print player's hand after drawing
                print("\nYour hand:")
                self.player_hand.print_hand()

                # Immediately check if the player busts
                player_total = self.player_hand.calculate_hand()
                print(f"\nYou currently have a total value of: {player_total}")

                #game checking as a card is added, for player/dealer wins
                if player_total > 21:
                    time.sleep(0.5)
                    print("Over 21, Bust! You lose.")
                    player_turn = False
                    self.bust = True
                    return  # Return to avoid further actions
                
                elif player_total == 21:
                    time.sleep(0.5)
                    print("21, that's Blackjack! You win!")
                    player_turn = False
                    self.player_balance += 2 * self.bet_amount  # Award balance for Blackjack
                    return  # Return to avoid asking for input again

            #input: stand
            #end players turn, print some output letting user know their input is read
            elif choice == "stand":
                print("You chose to stand.")
                player_turn = False

            else: #user error management
                print("Please choose between 'hit' or 'stand'.")

    # Dealer's turn 
    def dealer_next_card(self):
        if self.bust:
            return  # Skip dealer's turn if the player busted

        # Reveal dealer's second card
        self.dealer_showing_all_cards = True
        print("\nDealer reveals second card:")
        self.show_hands()  # Reveal all dealer's cards
        dealer_total = self.dealer_hand.calculate_hand()
        print(f"Dealer's hand total: {dealer_total}")

        dealer_turn = True
        while dealer_turn:
            while dealer_total < 17:
                drawn_card = self.deck.draw_card()  # Draw a card from the deck
                self.dealer_hand.add_card(drawn_card)  # Add the card to the dealer's hand
                dealer_total = self.dealer_hand.calculate_hand()  # Update dealer's total
                print(f"Dealer draws a {drawn_card}")
                print("\nDealer's hand:")
                self.dealer_hand.print_hand()
                print(f"Dealer's hand total: {dealer_total}")

            # Check if the dealer busts or hits Blackjack
            if dealer_total > 21:
                print()
                print("Dealer Busts! You win!")
                self.player_balance += self.bet_amount * 2
                return  # Return immediately to avoid further checks

            elif dealer_total == 21:
                print()
                print("Dealer has Blackjack, you lose.")
                return  # Return immediately to avoid further checks

            dealer_turn = False
    
        # Only compare hands if the dealer hasn't busted
        if dealer_total < self.player_hand.calculate_hand():
            print("You Win!")
            self.player_balance += 2* self.bet_amount
        elif dealer_total == self.player_hand.calculate_hand():
            print("It's a push.")
            self.player_balance += self.bet_amount
        else:
            print("You lose.")

    # Main game loop
    def start_game(self):
        playing = True
        while playing:
            # Check if the deck needs reshuffling
            self.deck.check_deck_size()  
            print(f"Current balance: ${round(self.player_balance, 2)}")

            blackjack = self.deal_initial_cards()  # Deal initial cards
            if blackjack:
                continue  # Skip to next game if player or dealer has Blackjack

            self.show_hands()  # Show hands
            self.hit_or_stand()  # Player's turn
            #ensure player did not bust
            
            if not self.bust:
                self.dealer_next_card()  # Dealer's turn
            
            # User input to play again
            play_again = input("\nDo you want to play again? (yes/no): ").lower()
            if play_again == 'yes':
                self.reset_game()  
            else:
                playing = False  # Exit the loop if the player chooses not to play again

        print("Thanks for playing!")

    # Reset the game for replayability
    def reset_game(self):
        self.player_hand = Hand()  # Reset player hand
        self.dealer_hand = Hand()  # Reset dealer hand
        self.deck = Deck()  # Create a new deck of cards
        self.deck.shuffle()  # Shuffle the deck before the game starts
        self.bust = False
        self.dealer_showing_all_cards = False
# Run the game
game = gameRunner()
game.start_game()
