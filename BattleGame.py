import random
import csv

# Function that prints all character names and their classes from the given file, and then returns a list of names
def character_display(file):
    charas = open(file, "r")
    reader = csv.reader(charas, delimiter = ",")
    d = {"name": "", "class": "", "special_attack_min": 0, "special_attack_max": 0, "health": 100, "cooldown": 0, "turns_since": 0}
    d_list = list(d)
    names = []
    for line in reader:
        i = 0
        name = True
        for value in line:
            if name == True:
                names.append(value)
                name = False
            d[d_list[i]] = value
            i += 1
        print(("{}, who is a{}.").format(d["name"], d["class"]))
    charas.close()
    return names

# Function that gets the data for the two chosen characters and puts them in dictionaries within a list
def player_opponent(file, player, opponent):
    charas = open(file, "r")
    reader = csv.reader(charas, delimiter = ",")
    l = [{"name": "", "class": "", "special_attack_min": 0, "special_attack_max": 0, "health": 100, "cooldown": 0, "turns_since": 0}
, {"name": "", "class": "", "special_attack_min": 0, "special_attack_max": 0, "health": 100, "cooldown": 0, "turns_since": 0}]
    player_l = list(l[0])
    opponent_l = list(l[1])
    player_d = l[0]
    opponent_d = l[1]
    for line in reader:
        i = 0
        if line[0].lower() == player.lower():
            for value in line:
                player_d[player_l[i]] = value
                i += 1
        elif line[0].lower() == opponent.lower():
            for value in line:
                opponent_d[opponent_l[i]] = value
                i += 1
    charas.close()
    return l

# Function that takes player lists, determines whether a special attack can be used, and calculates and displays damage and health points
def player_turn(attacker, attackee, attack_special):
    init_damage = 0
    damage = 0
    block = False
    heal = False
    blocked_dam = 0
    special_chance = random.randint(1,9)
    if attack_special == True:
        print("Special Attack Attempted.")
        if attacker["turns_since"] >= attacker["cooldown"]:
            attacker["turns_since"] = 0
            print("Special Attack Used")
            if special_chance <= 2:
                heal = True
            else:
                damage = random.randrange(attacker["special_attack_min"], (attacker["special_attack_max"]+1))
        else:
            print("Basic Attack Used")
            if attacker["weapon"]["ideal"].lower() == attacker["class"].lower():
                damage = random.randrange(attacker["weapon"]["damage"][0],attacker["weapon"]["damage"][1]+1)
            else:
                damage = (random.randrange(attacker["weapon"]["damage"][0],attacker["weapon"]["damage"][1]+1)) - 1
                attacker["turns_since"] += 1
    else:
        print("Basic Attack Used")
        if attacker["weapon"]["ideal"].lower() == attacker["class"].lower():
            damage = random.randrange(attacker["weapon"]["damage"][0],attacker["weapon"]["damage"][1]+1)
        else:
            damage = (random.randrange(attacker["weapon"]["damage"][0],attacker["weapon"]["damage"][1]+1)) - 1
        attacker["turns_since"] += 1
#       Rolls chance to see if attackee will block, and subtracts from damage if they do
    if random.uniform(0,1) <= attackee["armor"]["blocking_chance"]:
        block = True
        blocked_dam = random.randrange(attackee["armor"]["block_range"][0], attackee["armor"]["block_range"][1]+1)
        init_damage = damage
        damage -= blocked_dam
#       Makes sure there's no negative damage
    if damage <= 0:
        damage = 0
    if init_damage <= 0:
        init_damage = 0
#       Calculates attackee's health after damage dealt and displays health. Changes display if attackee blocked or if special healed instead of attacked
    if heal == False:
        if block == False:
            print(attacker["name"] + " did " + str(damage) + " damage this round!")
            attackee["health"] -= damage
            if attackee["health"] < 0:
                attackee["health"] = 0
            print(attackee["name"] + " has " + str(attackee["health"]) + " health points left.\n")
        else:
            print(attacker["name"] + " dealt " + str(init_damage) + " damage, but " + attackee["name"] + " blocked " + str(blocked_dam) + " damage!")
            print(attacker["name"] + " did " + str(damage) + " damage this round!")
            attackee["health"] -= damage
            if attackee["health"] < 0:
                attackee["health"] = 0
            print(attackee["name"] + " has " + str(attackee["health"]) + " health points left.\n")
    else:
        print(("{} healed {} by 2 points and did no damage this round!").format(attacker["name"],attackee["name"]))
        attackee["health"] += 2
        if attackee["health"] < 0:
            attackee["health"] = 0
        print(attackee["name"] + " has " + str(attackee["health"]) + " health points left.\n")


# Function that gets user's desired attack
def user_attack():
    attack = input("Do you want to use your basic attack or your special attack? ")
    while attack.lower() != "basic" and attack.lower() != "special":
        attack = input("Please enter a valid answer. Basic or special? ")
    if attack.lower() == "special":
        attack = True
    else:
        attack = False
    print("\n")
    return attack

# Function that randonly generates computer's desired attack
def comp_attack():
    choice = ["basic", "special"]
    attack = random.choice(choice)
    if attack == "special":
        attack = True
    else:
        attack = False
    print
    return attack

# Function that checks if one of the players died
def still_alive(user, comp):
    death_message = ["Oh no, you're dead, ", "Oh no, better luck next time, ", "Git gud, ", "Oof, you died, ", "Looks like you've reached your demise, ", "Too bad, "]
    if user["health"] <= 0:
        print(random.choice(death_message) + user["name"])
        print("Sorry, the Other Player won...")
        return False
    elif comp["health"] <= 0:
        print(random.choice(death_message) + comp["name"])
        print("You win!")
        return False
    else:
        return True


# Weapons and armor dictionaries within a list
weapons = [{"name":"Cleaver","damage": [10,20], "ideal": "barbarian"},{"name":"Sword","damage": [5,10], "ideal": "warrior"},{"name":"Wand","damage": [1,5], "ideal": "mage"},{"name":"Magic Orb","damage": [5,15], "ideal": "shapeshifter"},{"name":"Royal Bow","damage": [5,6], "ideal": "hunter"},{"name":"Dagger","damage": [1,5], "ideal": "hunter"},{"name":"Broadsword","damage": [10,13], "ideal": "warrior"},{"name":"Glowing necklace","damage": [0,2], "ideal": "shapeshifter"},{"name":"Staff","damage": [4,8], "ideal": "mage"},{"name":"Spiked Club","damage": [13,18], "ideal": "barbarian"}]
armor = [{"name":"Pot lid","block_range": [0,60], "blocking_chance": 0.1},{"name":"Bowtie","block_range": [5,30], "blocking_chance": 0.2},{"name":"Dapper hat","block_range": [10,50], "blocking_chance": 0.2},{"name":"Greaves","block_range": [15,20], "blocking_chance": 0.4},{"name":"Chainmail","block_range": [30,32], "blocking_chance": 0.5},{"name":"Tunic","block_range": [20,22], "blocking_chance": 0.6},{"name":"Toilet paper armor","block_range": [1,5], "blocking_chance": 0.9},{"name":"Green screen","block_range": [1,10], "blocking_chance": 0.7},{"name":"Exoskeleton","block_range": [15,25], "blocking_chance": 0.4},{"name":"Oversized shield","block_range": [10,20], "blocking_chance": 0.8}]
w_names = []
a_names = []
for d in weapons:
    w_names.append(d["name"].lower())
for d in armor:
    a_names.append(d["name"].lower())


# Welcome message, then display of all character options
print("Welcome!\nYour options are: ")
names = character_display("character_data.csv")
player_choice = input("Who would you like to play? ")

# Gets user input and checks if input is valid
lower_names = [n.lower() for n in names]
while player_choice.lower() not in lower_names:
    player_choice = input("Enter a valid name.\nWho would you like to play? ")
lower_names.remove(player_choice.lower())
o = lower_names[random.randrange(0, len(lower_names))]

# Calls function to grab the data about the two chosen characters and stores the data in two dictionaries
main_charas = player_opponent("character_data.csv", player_choice, o)
player_d = main_charas[0]
opponent_d = main_charas[1]

print(("Your opponent is {}, who is a{}.").format(opponent_d["name"], opponent_d["class"]))


# Prints list of weapons, takes user input, makes sure input is valid, then randomly chooses weapon for computer
print("Here are your weapon options: ")
for d in weapons:
    print(("{}, which does between {} and {} damage and is ideal for a {}").format(d["name"],d["damage"][0],d["damage"][1],d["ideal"]))
weapon_choice = input("\nWhich would you like to choose? ")
while weapon_choice.lower() not in w_names:
    weapon_choice = input("Enter a valid name.\nWhich would you like to choose? ")
opponent_weapon = w_names[random.randrange(0, len(w_names))]
print(("{} is using {}").format(opponent_d["name"], opponent_weapon.capitalize()))
# Adds the weapons to player and opponent's dictionaries
for d in weapons:
    if d["name"].lower() == weapon_choice.lower():
        player_d["weapon"] = d
    if d["name"].lower() == opponent_weapon.lower():
        opponent_d["weapon"] = d

# Prints list of armor, takes user input, makes sure input is valid, then randomly chooses armor for computer
print("Here are your armor options: ")
for d in armor:
    print(("{}, which can block between {} and {} damage {}% of the time").format(d["name"],d["block_range"][0],d["block_range"][1],(d["blocking_chance"]*100)))
armor_choice = input("\nWhich would you like to choose? ")
while armor_choice.lower() not in a_names:
    armor_choice = input("Enter a valid name.\nWhich would you like to choose? ")
opponent_armor = a_names[random.randrange(0, len(a_names))]
print(("{} is using {}").format(opponent_d["name"], opponent_armor.capitalize()))
# Adds the armor to player and opponent's dictionaries
for d in armor:
    if d["name"].lower() == armor_choice.lower():
        player_d["armor"] = d
    if d["name"].lower() == opponent_armor.lower():
        opponent_d["armor"] = d

#Converts all integer values in player dictionaries to integers
player_d["special_attack_min"] = int(player_d["special_attack_min"])
player_d["special_attack_max"] = int(player_d["special_attack_max"])
player_d["health"] = int(player_d["health"])
player_d["cooldown"] = int(player_d["cooldown"])
player_d["turns_since"] = int(player_d["turns_since"])
opponent_d["health"] = int(opponent_d["health"])
opponent_d["cooldown"] = int(opponent_d["cooldown"])
opponent_d["turns_since"] = int(opponent_d["turns_since"])
opponent_d["special_attack_min"] = int(opponent_d["special_attack_min"])
opponent_d["special_attack_max"] = int(opponent_d["special_attack_max"])

# Loops through game rounds until someone dies
round = 1

while still_alive(player_d, opponent_d) == True:
    print("ROUND " + str(round) + " ------------------------------")
    player_turn(player_d, opponent_d, user_attack())
    if still_alive(player_d, opponent_d) == False:
        break
    player_turn(opponent_d, player_d, comp_attack())
    if still_alive(player_d, opponent_d) == False:
        break
    round += 1
