import random

card_dict = {
    "A": 1, "2": 2, "3": 3, "4": 4, "5": 5, 
    "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, 
    "J": 10, "Q": 10, "K": 10
}

def score(cards):
    score1 = sum(card_dict[card] for card in cards)
    if "A" in cards and score1 + 10 <= 21:
        score2 = score1 + 10
    else:
        score2 = score1
    return score1, score2

# 1. Setup Deck & Players
base_deck = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"] * 4
random.shuffle(base_deck)

players = ["Player 1", "Player 2", "Player 3"]
dealer = "Player 4 (Dealer)"
all_participants = players + [dealer]

hands = {p: [] for p in all_participants}

# 2. Initial Deal (2 cards each)
for _ in range(2):
    for p in all_participants:
        hands[p].append(base_deck.pop())

print("--- Initial Deal ---")
for p in all_participants:
    _, s2 = score(hands[p])
    print(f"{p} has {hands[p]} (Score: {s2})")
print("-" * 30)

# 3. Human Players' Turns
for p in players:
    print(f"\n== {p}'s Turn ==")
    while True:
        _, current_score = score(hands[p])
        print(f"Your hand: {hands[p]} (Current Best Score: {current_score})")
        
        if current_score > 21:
            print("💥 Bust! You went over 21.")
            break
        elif current_score == 21:
            print("🎉 Blackjack / 21!")
            break
            
        choice = input("Do you want to take a card? (y/n): ").strip().lower()
        if choice == 'y':
            new_card = base_deck.pop()
            hands[p].append(new_card)
            print(f"You drew: {new_card}")
        else:
            print(f"{p} decides to Stand.")
            break

# 4. Dealer's Turn (Player 4 rules)
print(f"\n== {dealer}'s Turn ==")
while True:
    _, dealer_score = score(hands[dealer])
    print(f"Dealer hand: {hands[dealer]} (Score: {dealer_score})")
    
    if dealer_score > 21:
        print("💥 Dealer Busts!")
        break
    elif dealer_score >= 17:
        print(f"Dealer score is {dealer_score} (>= 17). Dealer must Stand.")
        break
    else:
        print(f"Dealer score is {dealer_score} (< 17). Dealer draws a card...")
        hands[dealer].append(base_deck.pop())

# 5. Final Results
print("\n" + "="*10 + " FINAL RESULTS " + "="*10)
_, d_final = score(hands[dealer])

for p in players:
    _, p_final = score(hands[p])
    print(f"\n{p}: Final Hand {hands[p]} | Score: {p_final}")
    
    if p_final > 21:
        print("❌ Result: Player Bust (Lost)")
    elif d_final > 21:
        print("🏆 Result: Player Wins (Dealer Bust)")
    elif p_final > d_final:
        print("🏆 Result: Player Wins!")
    elif p_final < d_final:
        print("❌ Result: Player Loses to Dealer")
    else:
        print("🤝 Result: Push (Tie)")

print(f"\n{dealer}: Final Hand {hands[dealer]} | Score: {d_final}")
