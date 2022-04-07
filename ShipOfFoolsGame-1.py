from random import randint

class Die:

    """this class is responsible for handling randomly generated integer values between 1 and 6."""

    def __init__(self):
        self._value=0
        self.roll()

    def roll(self):
        """rolls the dices."""
        self._value=randint(1,6)

    def get_value(self):
        """returns the value after rolling the dice."""
        return self._value
    
class DiceCup:

    """this class banks and releases the dices, also rolls the dices that are not banked."""

    def __init__(self):
        self._dice=[]
        self._bank=[0,0,0,0,0]
        for i in range(5):
            self._dice.append(Die())

    def value(self,index):
        """this method takes the value of the dice based on the index."""
        return self._dice[index].get_value()

    def bank(self,index):
        """this method holds a specific dice based on the index."""
        self._bank[index]=1

    def is_banked(self,index):
        """this method  checks waether a specific index is banked or not"""
        if self._bank[index]==1:
            return True
        else:
            return False

    def release(self,index):
        """this method releases a banked dice off a specific index """
        self._bank[index]=0

    def release_all(self):
        """this method releases all the banked dice"""
        self._bank=[0,0,0,0,0]

    def roll(self):
        """rolls objects of die class"""
        for obj in range(5):
            if self._bank[obj]==0:
                self._dice[obj].roll()

class PlayRoom:

    """this class handles the number of players and lets each player play every 
       also checks if a player has reached the winning score"""

    def __init__(self):
        self._players=[]
        self._score=[]

    def set_game(self, game_obj):
        """this method is used to set the game i.e ShipOfFoolsGame"""
        self._game=game_obj

    def add_player(self,game_obj):
        """this method adds the players"""
        self._players.append(game_obj)


    def reset_scores(self):
        """this method resets the scores"""
        for obj in self._players:
            obj.reset_score()

    def play_round(self):
        """'this method is similar to the play_round in Player class"""
        for obj in self._players:
            print("\n \n Player : ", obj._name)
            obj.play_round(self._game)

    def game_finished(self):
        """this method checks if each player has reached a winning score of 21 or more"""
        listt=[]
        i=0
        length=len(self._players)
        while i<len(self._players):
            if self._players[i].current_score()>=21:
                listt.append(True)
                i=i+1
            else:
                listt.append(False)
                i=i+1
        return any(listt)

    def print_scores(self):
        """prints the current score of each player"""
        for obj in self._players:
            print("\n Score of ", obj._name, " is : ", obj.current_score())
            if obj.current_score()>=21:
                self._score.append(obj.current_score())
       
        
    def print_winner(self):
        """this method checks the indvidual scores of the players and prints the winner"""
        maximum=max(self._score)
        for obj in self._players:
            if  obj.current_score()==maximum:
                print("\n Winner is ",obj._name)      

class ShipOfFoolsGame:

    """this class contains the logic of the game"""

    def __init__(self):
        self._cup=DiceCup()
        self.winning_score=21

    def round(self): 
        """allows every player to play a round"""
        print("***dices rolling***")
        print("The results after rolling \n")
        self._cup.release_all()
        crew=0
        self._cup.roll()
        has_ship = False
        has_captain = False
        has_crew = False
        for round in range(3):
            ls=[]
            inc=0
            while inc<5:
                ls.append(self._cup._dice[inc].get_value())
                inc=inc+1
            print(ls)
            if not (has_ship) and (6 in ls):
                for a in range(5):
                    if ls[a]==6:
                        self._cup.bank(a)
                        break
                has_ship = True
            else:
                if has_ship:
                    pass
                else:
                    self._cup.roll()
            if (has_ship) and not (has_captain) and (5 in ls):
                for a in range(5):
                    if ls[a]==5:
                        self._cup.bank(a)
                        break
                has_captain = True
            else:
                if has_captain:
                    pass
                else:
                    self._cup.roll()
            if (has_captain) and not (has_crew) and (4 in ls):
                for a in range(5):
                    if ls[a]==4:
                        self._cup.bank(a)   
                        break
                has_crew = True
            else:
                if has_crew:
                    pass
                else:
                    self._cup.roll()
            if has_ship and has_captain and has_crew:
                if round<2:
                        for a in range(5):
                            if self._cup._dice[a].get_value()>3:
                                self._cup.bank(a)
                            else:
                                self._cup.roll()
                elif round==2:
                    for a in range(5):
                        if self._cup.is_banked(a):
                            pass
                        else:
                            self._cup.bank(a)
        if (has_ship) and (has_captain) and (has_crew):
            crew = sum(ls) - 15
            print("The Score for current round : ",crew)
            return crew
        else:
            print("The Score for current round : ",crew)
            return crew

class Player:

    """generates the score of an individual player and the score gained is accumulated"""

    def __init__(self,player_name):
        self._name=self.set_name(player_name)
        self._score=0

    def set_name(self,name):
        """this mmethod sets the name of the player"""
        return name

    def current_score(self):
        """this method updates the score of each player and stores it"""
        return self._score

    def reset_score(self):
        """this method resets the score to zero"""
        self._score=0

    def play_round(self,game_round):
        """this method allows to play rounds"""
        roundA=game_round
        self._score=self._score + roundA.round()

if __name__ == "__main__":
    room = PlayRoom()
    room.set_game(ShipOfFoolsGame())
    room.add_player(Player("A"))
    room.add_player(Player("B"))
    room.reset_scores()
    while not room.game_finished():
        room.play_round()
        room.print_scores()
    room.print_winner()