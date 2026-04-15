import random
import time
from functools import reduce

MONSTER_NAMES= ["Blackbane, The Blood Canine", "Nightlisk, The Howling Vampling",
                "Blackbeast, The Monstrous Creeper", "Plagueeyes, The Vicious Slasher",
                "Rottingwing, The Muted Creeper", "Blackmoth, The Monstrous Controller",
                "Cursefreak, The Feral Revenant", "Taintsome, The Vengeful Raven"]
LOOTABLES = ["Sword", "Shield", "Potion", "Scroll"]

def colorize(text: str, color: str):
    colorset = {
        "red": "\033[0;31m",
        "green": "\033[0;32m",
        "yellow": "\033[0;33m",
        "blue": "\033[0;34m",
        "light_red": "\033[1;31m",
        "light_green": "\033[1;32m",
        "light_blue": "\033[1;34m",
        "bold": "\033[1m",
        "crossed": "\033[9m",
        "underline": "\033[4m"
    }

    return f"{colorset[color]}{text}\033[0m"

class GameOverError(Exception):
    pass

def game_over():
    time.sleep(2)
    print(colorize(colorize("GAME OVER!", "bold"), "red"))
    raise GameOverError

def combat(func):
    def wrapper(*args, **kwargs):
        print("\nACTION HAS BEEN TAKEN!")
        print("----------------------")
        time.sleep(2)
        func(*args, **kwargs)
        print("----------------------\n")
        time.sleep(2)
    return wrapper

class Entity:
    def __init__(self, name: str, hp: int, is_alive: bool = True):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.is_alive = is_alive

    def take_damage(self, amount: int):
        self.hp -= amount
        if self.hp <= 0:
            self.die()

    def die(self):
        print(f"{colorize(colorize(self.name, 'crossed'), 'bold')} has {colorize("died", "red")}!")
        self.is_alive = False
        if isinstance(self, Hero):
            game_over()

class Hero(Entity):
    def __init__(self, name: str, hp: int = 100, mana: int = 100, level: int = 1, experience: int = 0, loot=None, rpg_stats=None):
        super().__init__(name, hp)
        if loot is None:
            loot = {}
        if rpg_stats is None:
            rpg_stats = {'STR': 10, 'DEX': 10, 'CON': 10, 'INT': 10, 'WIS': 10, 'CHA': 10}
        self.mana = mana
        self.max_mana = mana
        self.level = level
        self.experience = experience
        self.loot = loot
        self.rpg_stats = rpg_stats

    @combat
    def attack(self, e: "Enemy", is_strong: bool = False):
        power = self.rpg_stats["STR"]//5
        if "Sword" in self.loot:
            power += self.loot["Sword"]
        if is_strong:
            power += 2
            self.mana -= 20
        damage = random.randint(power, power*5)
        print(f"{colorize(self.name, "green")} {colorize("ATTACKS", "bold")} {colorize(e.name, "red")} for {colorize(str(damage), "light_red")} {colorize("HP", "light_red")} damage!")
        if self.mana + 10 >  self.max_mana:
            self.mana = self.max_mana
        else:
            self.mana += 10
        e.take_damage(damage)

    @combat
    def heal(self):
        self.mana -= 40
        heal_power = self.rpg_stats["CON"]//5
        if "Potion" in self.loot:
            heal_power += self.loot["Potion"]
        heal_amount = random.randint(heal_power, heal_power*3)
        if self.hp + heal_amount > self.max_hp:
            heal_amount = self.max_hp - self.hp
        print(f"{colorize(self.name, "green")} {colorize("HEALS", "bold")} for {colorize(str(heal_amount) + " HP!", "light_green")}")
        self.hp += heal_amount

    def level_up(self):
        self.level += 1
        print(f"You have {colorize("LEVELED UP", "bold")} to Lv. {colorize(str(self.level), "blue")}!")
        for stat in self.rpg_stats:
            self.rpg_stats[stat] += 5
        self.hp = self.max_hp
        print(f"{colorize(self.name, "green")} is now at {colorize(f"{self.max_hp} HP", "light_green")}!")

    def gain_exp(self, exp: int):
        if "Scroll" in self.loot:
            exp += self.loot["Scroll"]
        self.experience += exp
        while self.experience >= 2 ** (self.level+2):
            self.experience -= 2 ** (self.level+2)
            self.level_up()

    def show_stats(self):
        print("================================")
        print(f"{colorize(self.name, "green")} has {colorize(str(self.hp) + f"/{self.max_hp} HP", "light_green")} has {colorize(str(self.mana) + f"/{self.max_mana} Mana", "light_blue")} and is level {colorize(str(self.level), "blue")}")
        print(f"They have {colorize(str(self.experience), "blue")}/{colorize(str(2**(self.level+2)), "blue")} exp.")
        print(f"They have the following {colorize("loot", "yellow")}:")
        if not self.loot:
            print("Nothing Yet!")
        else:
            for item, power in self.loot.items():
                print(f"{colorize(item, "yellow")} with {colorize(str(power), "bold")} power!")
            if len(self.loot) > 1:
                total_power = reduce(lambda x, y: x + y, self.loot.values())
                print(f"Total gear power: {colorize(str(total_power), 'bold')}")
        print("================================")

    def show_rpg_stats(self):
        print(f"{colorize(self.name, 'green')} has the following stats:")
        for stat, value in self.rpg_stats.items():
            print(f"{colorize(stat, 'yellow')} {colorize('=', 'bold')} {colorize(str(value), 'bold')}")

    def blacksmith_event(self):
        print("\n\n\n\nYou have found yourself in a strange place...")
        time.sleep(2)
        print("You see a blacksmith standing in front of you...")
        time.sleep(2)
        print("He looks like he has some experience in the art of smithing...")
        time.sleep(2)
        print("He looks at you almost to see if you have any gear...")
        time.sleep(2)
        if not self.loot:
            print("He sees that you don't have any gear and says:")
            time.sleep(2)
            print(f"'Here, take this {colorize("Sword", "yellow")}. You'll need it.'")
            time.sleep(2)
            self.loot["Sword"] = 1
            print(f"He gives you a {colorize("Sword", "yellow")} with {colorize("1", "bold")} power.")
            time.sleep(2)
            print("You leave the blacksmith.")
            time.sleep(2)
            return
        num1, num2 = random.randint(10, 20), random.randint(10, 20)
        ans = 0
        while True:
            try:
                print("He asks you a math question...")
                time.sleep(2)
                print(f"{num1} * {num2} = ?")
                ans = int(input("Enter your answer: "))
                break
            except ValueError:
                print(colorize("Invalid input. Please enter a number.", "red"))
                continue
        if ans == num1 * num2:
            print(f"{colorize("Correct!", "green")} Blacksmith sharpens your gear for {colorize("free", "light_green")}!")
            self.loot = dict(map(lambda item: (item[0], item[1] + 1), self.loot.items()))
            time.sleep(2)
        else:
            print(f"You have {colorize("lost", "red")} the {colorize("prize", "yellow")}!")
            time.sleep(2)
        print("You leave the blacksmith.")
        time.sleep(2)

class Warrior(Hero):
    def __init__(self, name: str, hp: int = 150, mana: int = 100, level: int = 1, experience: int = 0, loot=None, rpg_stats=None):
        if loot is None:
            loot = {'Shield': 1}
        if rpg_stats is None:
            rpg_stats = {'STR': 5, 'DEX': 15, 'CON': 10, 'INT': 10, 'WIS': 10, 'CHA': 5}
        super().__init__(name, hp, mana, level, experience, loot, rpg_stats)

    def spec_skill(self):
        # TODO Will be implemented later
        pass

class Rouge(Hero):
    def __init__(self, name: str, hp: int = 75, mana: int = 75, level: int = 1, experience: int = 0, loot = None, rpg_stats = None):
        if rpg_stats is None:
            rpg_stats = {'STR': 15, 'DEX': 5, 'CON': 10, 'INT': 10, 'WIS': 5, 'CHA': 10}
        super().__init__(name, hp, mana, level, experience, loot, rpg_stats)

    @combat
    def attack(self, e: "Enemy", is_strong: bool = False):
        power = self.rpg_stats["STR"]//5
        if "Sword" in self.loot:
            power += self.loot["Sword"]
        if is_strong:
            power += 2
            self.mana -= 20
        damage = random.randint(power, power*5)
        if random.randint(1, 10) <= 3:
            damage *= 2
            print(colorize("Critical Hit!", "red"))
        print(f"{colorize(self.name, 'green')} {colorize('ATTACKS', 'bold')} {colorize(e.name, 'red')} for {colorize(str(damage), 'light_red')} {colorize('HP', 'light_red')} damage!")
        if self.mana + 10 >  self.max_mana:
            self.mana = self.max_mana
        else:
            self.mana += 10
        e.take_damage(damage)

    def spec_skill(self):
        # TODO Will be implemented later
        pass

class Wizard(Hero):
    def __init__(self, name: str, hp: int = 50, mana: int = 150, level: int = 1, experience: int = 0, loot = None, rpg_stats = None):
        if rpg_stats is None:
            rpg_stats = {'STR': 20, 'DEX': 5, 'CON': 15, 'INT': 10, 'WIS': 15, 'CHA': 5}
        super().__init__(name, hp, mana, level, experience, loot, rpg_stats)

    def spec_skill(self):
        # TODO Will be implemented later
        pass


class Enemy(Entity):
    def __init__(self, name: str, hp: int, difficulty: int = 1, choices=None):
        super().__init__(name, hp)
        if choices is None:
            choices = ["ATTACK", "ATTACK", "ATTACK", "HEAL"]
        self.difficulty = difficulty
        self.choices = choices

    @combat
    def attack(self, h: Hero):
        power = self.difficulty + 1
        if "Shield" in h.loot:
            power = int(power - h.loot["Shield"]/2)
        if power < 1:
            power = 1
        damage = random.randint(power, power * 5)
        print(f"{colorize(self.name, 'red')} {colorize("ATTACKS", "bold")} {colorize(h.name, "green")} for {colorize(f"{damage} HP", "light_red")} damage!")
        h.take_damage(damage)

    @combat
    def heal(self):
        heal_amount = random.randint(1, self.difficulty * 3)
        if self.hp + heal_amount > self.max_hp:
            heal_amount = self.max_hp - self.hp
        print(f"{colorize(self.name, 'red')} {colorize("HEALS", "bold")} for {colorize(f"{heal_amount} HP", 'light_green')}!")
        self.hp += heal_amount

    def take_action(self):
        if self.hp < self.max_hp/2:
            self.choices.append("HEAL")
        action = random.choice(self.choices) if self.hp != self.max_hp else "ATTACK"
        return action

    def reset_choices(self):
        self.choices = ["ATTACK", "ATTACK", "ATTACK", "HEAL"]


def enemy_spawner():
    lvl = 1
    while True:
        e_max_hp = 5 * (lvl + 2)
        e_name = random.choice(MONSTER_NAMES)
        yield Enemy(e_name, e_max_hp, lvl)
        lvl += 1


def main(top_scores: int = 0, countdown: int = 3):

    print(f"Welcome to the Dungeon! You have {colorize(str(countdown), 'bold')} chances left!")
    h_name = input("Enter your name: ")
    while True:
        h_class = input("Enter your class (Warrior/Rouge/Wizard): ").lower()

        if h_class == "warrior":
            hero = Warrior(h_name)
        elif h_class == "rouge":
            hero = Rouge(h_name)
        elif h_class == "wizard":
            hero = Wizard(h_name)
        else:
            print(colorize("Invalid class. Please enter Warrior/Rouge/Wizard.", "red"))
            continue
        break
    countdown -= 1
    print("Welcome to the Dungeon!")
    spawner = enemy_spawner()
    try:
        while True:
            enemy = next(spawner)
            print(f"\nA new {colorize('enemy', 'red')} has appeared!")
            time.sleep(1)
            while enemy.is_alive:
                hero.show_stats()
                print(f"Enemy: {colorize(enemy.name, 'red')} with {colorize(f'{enemy.hp} HP', 'light_red')}")
                print("Choose an action:")
                print("1) Attack (+10 Mana)")
                print("2) Strong Attack (-20 Mana)")
                print("3) Heal (-40 Mana)")
                print("4) Special Skill (Not Implemented Yet!)")
                print("5) Check Stats")
                print("6) Exit")
                try:
                    inp = int(input("Enter your choice: "))
                    if not 0 < inp < 7:
                        raise ValueError
                except ValueError:
                    print(colorize("Invalid input. Please enter a valid number.", "red"))
                    time.sleep(3)
                    continue
                if inp == 1:
                    hero.attack(enemy)
                elif inp == 2:
                    if hero.mana < 20:
                        print(colorize("Not enough mana!", "red"))
                        time.sleep(2)
                        continue
                    else:
                        hero.attack(enemy, True)
                elif inp == 3:
                    if hero.mana < 40:
                        print(colorize("Not enough mana!", "red"))
                        time.sleep(2)
                        continue
                    else:
                        hero.heal()
                elif inp == 4:
                    hero.spec_skill()
                elif inp == 5:
                    hero.show_rpg_stats()
                    continue
                else:
                    print("Exiting...")
                    exit(0)
                if not enemy.is_alive:
                    hero.gain_exp(enemy.difficulty * 10)
                    continue
                e_act = enemy.take_action()
                if e_act == "HEAL":
                    enemy.heal()
                    enemy.choices.append("ATTACK")
                else:
                    enemy.attack(hero)
            if random.randint(1, 5) == 1:
                print(f"\n\n\nYou have found something {colorize("useful", "blue")}!")
                time.sleep(2)
                new_loot = random.choice(LOOTABLES)
                loot_power = random.randint(1, 5)

                if new_loot in hero.loot:
                    hero.loot[new_loot] += loot_power
                    print(f"You found another {colorize(new_loot, "yellow")} with {colorize(str(loot_power), "bold")} power!")
                else:
                    hero.loot[new_loot] = loot_power
                    print(f"You found a {colorize(new_loot, "yellow")} with {colorize(str(loot_power), "bold")} power!")
                time.sleep(2)
            if random.randint(1, 5) == 5 or enemy.difficulty == 1:
                hero.blacksmith_event()
    except GameOverError:
        hero.show_stats()
        print(f"Your score is {colorize(colorize(str(enemy.difficulty), 'bold'), 'underline')}")
        top_scores = max(top_scores, enemy.difficulty)
        print(f"Your top score is {colorize(colorize(str(top_scores), 'bold'), 'underline')}")
        print(f"You have {colorize(colorize(str(countdown), 'bold'), 'light_red')} chances left.")
        print("Better luck next time!")
        if countdown > 0:
            print(f"Would you like to play again? ({colorize(colorize("y", "bold"), "green")}/{colorize(colorize("n", "bold"), "red")})")
            inp = input()
            if inp.lower() == "y":
                del hero, spawner, enemy
                main(top_scores, countdown)
        print("Exiting...")
        exit(0)

if __name__ == "__main__":
    top_score = 0
    main()


