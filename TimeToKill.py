def create_DECK():
    SUITS = ["♠", "♡", "♣", "♢"]
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    DECK = set()

    for suit in SUITS:
        suit_cards = {f'{rank} {suit}' for rank in RANKS}
        DECK.update(suit_cards)
        
        # Remove the 'A ♡'
        DECK.discard('A ♡')
    
    return DECK


def ace_hearts_location(game_length):
    # Determine where the 'A ♡' is "shuffled" to
    import random
    match game_length:
        case '1':
            print ('\nPlaying a short game of Time To Kill.')
            location = random.randint(1,13)
        case '2':
            print ('\nPlaying a normal game of Time To Kill.')
            location = random.randint(1,26)
        case '3':
            print ('\nPlaying a long game of Time To Kill.')
            location = random.randint(27,52)
        case '4':
            print ('\nPlaying a random game of Time To Kill.')  
            location = random.randint(1,52)
    return location
  

def d6_roll():
    import random
    roll = random.randint(1,6)
    return roll


def draw_cards(roll, cards_drawn, target_location, DECK):
    DRAWN_CARDS = []

    for i in range(roll):
        cards_drawn += 1
        if cards_drawn <= 52:
            if cards_drawn == target_location:
                DRAWN_CARDS.append('A ♡ - Time To Kill')
            else:
                card = DECK.pop()
                DRAWN_CARDS.append(card)
        else:
            return cards_drawn, DRAWN_CARDS, DECK
    
    return cards_drawn, DRAWN_CARDS, DECK


def sort_cards(DRAWN_CARDS):
    SUIT_ORDER = {
    '♢': 0,
    '♣': 1,
    '♡': 2,
    '♠': 3,
    }

    RANK_ORDER = {str(r):r for r in range(2,11)}
    RANK_ORDER.update(
        J = 11,
        Q = 12,
        K = 13,
        A = 14,
    )

    def helper(card):
        suit = SUIT_ORDER.get(card[-1:], 20)
        rank = RANK_ORDER.get(card[:-2], 20)
        return (rank, suit)

    DRAWN_CARDS.sort(key=helper, reverse = True)
    return


def sort_kept_cards(KEPT_CARDS):
    SUIT_ORDER = {
    '♠': 0,
    '♡': 1,
    '♣': 2,
    '♢': 3,
    }

    RANK_ORDER = {str(r):r for r in range(2,11)}
    RANK_ORDER.update(
        J = 11,
        Q = 12,
        K = 13,
        A = 14,
    )

    def helper(card):
        suit = SUIT_ORDER.get(card[-1:], 20)
        rank = RANK_ORDER.get(card[:-2], 20)
        return (suit, rank)

    KEPT_CARDS.sort(key=helper)
    return


def keep_card(DRAWN_CARDS, KEPT_CARDS):
    KEEPING_CARD=[]

    # sort the drawn cards
    sort_cards(DRAWN_CARDS)

    # find the highest card
    highest_card = DRAWN_CARDS[0]
    KEEPING_CARD.append(highest_card)
    DRAWN_CARDS.remove(highest_card)

    for card in DRAWN_CARDS:
        if card[:-2] == highest_card[:-2]:
            KEEPING_CARD.append(card)
        else:
            break
    
    # Remove specific card if King kept
    for card in KEEPING_CARD:
        if card[:-2] == 'K':
            match card[-1:]:
                case '♠':
                    # remove highest valued heart
                    for kept_card in reversed(KEPT_CARDS):
                        if kept_card[-1:] == '♡':
                            KEPT_CARDS.remove(kept_card)
                            break
                case '♡':
                    # remove highest valued spade
                    for kept_card in reversed(KEPT_CARDS):
                        if kept_card[-1:] == '♠':
                            KEPT_CARDS.remove(kept_card)
                            break
                case '♣':
                    # remove highest valued diamond
                    for kept_card in reversed(KEPT_CARDS):
                        if kept_card[-1:] == '♢':
                            KEPT_CARDS.remove(kept_card)
                            break
                case '♢':
                    # remove highest valued club
                    for kept_card in reversed(KEPT_CARDS):
                        if kept_card[-1:] == '♣':
                            KEPT_CARDS.remove(kept_card)
                            break

        KEPT_CARDS.append(card)

    return KEPT_CARDS


def find_instinct(KEPT_CARDS):
    FACES = {'J', 'Q', 'K'}
    instincts = {
        'Cold': 0,
        'Hesitant': 0,
        'Paranoid': 0,
        'Clear-Minded': 0
    }

    for card in KEPT_CARDS:
        # find point value
        if card[:-2] == 'A':
            points = 3
        elif card[:-2] in FACES:
            points = 2
        else:
            points = 1
        
        # give points to suit
        match card[-1:]:
            case '♠':
                instincts['Cold'] += points
            case '♡':
                instincts['Hesitant'] += points
            case '♣':
                instincts['Paranoid'] += points
            case '♢':
                instincts['Clear-Minded'] += points
        
    # determine dominant instinct
    max_instinct = max(instincts.items(), key=lambda x : x[1])
    max_key = max_instinct[0]
    max_value = max_instinct[1]
    dominant_instinct = max_key

    # find other with same point value
    for key, value in instincts.items():
        if value == max_value and key != max_key:
            dominant_instinct += f' / {key}'

    return dominant_instinct


def moment(moment_num, cards_drawn, KEPT_CARDS, target_location, DECK):
    print(f'\n----- Moment {moment_num} -----')

    # Don't do these for the first moment
    if moment_num > 1:
        # Sort and display the kept cards
        sort_kept_cards(KEPT_CARDS)
        kept_cards_out = ' | '.join(KEPT_CARDS)
        print('Kept Cards: | ' + kept_cards_out + ' |')

        # Determine and display the Instinct
        instinct = find_instinct(KEPT_CARDS)
        print(f'Instinct: {instinct}')

    # Roll a D6
    roll = d6_roll()
    print(f'D6 Roll: {roll}')

    # Draw that number of cards
    cards_drawn, DRAWN_CARDS, DECK = draw_cards(roll, cards_drawn, target_location, DECK)
    print('Cards: ')
    for card in DRAWN_CARDS:
        print(f'       {card}')
    
    # Determine the new kept cards
    KEPT_CARDS = keep_card(DRAWN_CARDS, KEPT_CARDS)
    
    return cards_drawn, KEPT_CARDS, DECK
    
    
def main():
    DECK = create_DECK()
    moment_num = 1
    cards_drawn = 0
    KEPT_CARDS = []
    
    # Determine the length of game user wants
    print('\nWhat length of game do you want?')
    print('[1] Short')
    print('[2] Normal')
    print('[3] Long')
    print('[4] Random')
    game_length = input('\nEnter the value of your selection: ')

    # Make sure the input is valid
    if int(game_length) > 4:
        print('\nInvalid input. Please try again.\n')
        return
    
    # "Shuffle" the 'A ♡' into the correct location
    target_location = ace_hearts_location(game_length)

    # Start the game
    ready = input('Are you ready? [y/n]: ')
    if ready != 'n':
        cards_drawn, KEPT_CARDS, DECK = moment(moment_num, cards_drawn, KEPT_CARDS, target_location, DECK)
    else:
        print('\nGame aborted\n')
        return

    # Continue the game until the 'A ♡' is found
    while cards_drawn < target_location:
        continue_game = input('\nContinue? [y/n]: ')
        if continue_game != 'n':
            moment_num += 1
            cards_drawn, KEPT_CARDS, DECK = moment(moment_num, cards_drawn, KEPT_CARDS, target_location, DECK)
        elif continue_game == 'n':
            break

    if cards_drawn >= target_location:
        print('\nMake the call\n')
    else:
        print('\nGame aborted\n')

    return
    

if __name__ == '__main__':
    main()