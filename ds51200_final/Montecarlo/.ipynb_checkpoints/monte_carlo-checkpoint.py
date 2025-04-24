import numpy as np
import pandas as pd

class Die:
    def __init__(self, faces):
        """
        Initialize Die object with unique faces and weights.
        
        Parameters: faces 
            NumPy array. 
            Values must be distinct. 
            Data Type can be strings or numbers. 
            
        Raises: TypeError, ValueError 
            TypeError: if 'faces' is not a NumPy array. 
            ValueError: if the face values are not distinct.
        """
        
        if not isinstance(faces, np.ndarray):
            raise TypeError("faces must be a Numpy array") 
            
        if len(faces) != len(np.unique(faces)):
            raise ValueError("Faces must contain unique values") 
        
        """
        Create a private dataframe to store faces and the corresponding weights.
        Face values are used as the index. 
        Weights are initialized to 1.0 for each face. 
        """
        
        self._die_df = pd.DataFrame({
            'faces': faces, 
            'weights': np.ones(len(faces))
        }).set_index('faces')
    
    def change_weight(self, face, new_weight): 
        """
        This method changes the weight of a single side.
        
        Parameters: face, new_weight 
            face: face is to be changed. must be found in the die array. 
            new_weight: new weight assigned to the face. must be positive numbers (integer, float of string castable to float) 
    
        Raises: IndexError, TypeError
            IndexError: if the face passed is in the die array. 
            TypeError: if the new weight is numeric (integer or float) or castable as numeric.
        """
        
        if face not in self._die_df.index:
            raise IndexError("The face value is not found in the die array")
        
        try: 
            numeric_weight = float(new_weight)
        except (TypeError, ValueError):
            raise TypeError("The weights must be positive numbers (integers or floats, including 0, or castable as numeric)")
        
        self._die_df.at[face, 'weights'] = numeric_weight
        
    def roll(self, num_roll=1): 
        """
        This method rolls the die one or more times.
        
        Parameters: num_rolls 
            the number of times the die is to be rolled. 
            defaults to 1. 
        Returns: list 
            a list of outcomes 
        """
        outcomes = np.random.choice(
            self._die_df.index,
            size=num_roll,
            replace=True,
            p=self._die_df['weights'] / self._die_df['weights'].sum()
        )
        return outcomes.tolist()
    
    def show(self):
        """
        This method shows the die's current state. 
        
        Returns: 
            copy of the private die data frame with face and corresponding weights
        """
        return self._die_df.copy()

class Game:
    def __init__(self, dice): 
        """
        Initializes the class called Game that consists of rolling one or more Die objects. 
        
        Parameters: dice 
            a list of already instantiated dice objects. 
        """
        self.dice = dice
        self._play_results = None  # only keeps the result of the most recent play.
            
    def play(self, roll_times):
        """
        This method specifies how many times the dice should be rolled.
        
        Parameters: roll_times
            the number of times to roll the dice. 
        """
        results = {}  # dictionary 
        
        for i, die in enumerate(self.dice):  # roll the die
            results[i] = die.roll(roll_times)  # stores the outcome in results dictionary
            
        # creates a private data frame in wide format, saves the result of the play 
        self._play_results = pd.DataFrame(results)
        # make sure the data frame names the index 
        self._play_results.index.name = "roll_number"
            
    def show(self, form='wide'):
        """
        This method shows the user the results of the most recent play. 
        
        Parameters: the form of the data frame. 
            'wide': default.  
            'narrow': has a 'MultiIndex' with index names, roll_number and die_number 
        
        Returns: pd.DataFrame
            a copy of the private play data frame to the user. 
        
        Raises: ValueError 
            if the user passes an invalid option for narrow or wide. 
        """
        if self._play_results is None:
            return None 
            
        if form == 'wide':
            return self._play_results.copy()
        
        if form == 'narrow': 
            narrow_df = self._play_results.stack().to_frame(name='outcome')  # new single column called 'outcome' 
            narrow_df.index.names = ['roll_number', 'die_number']  # MultiIndex comprises of the roll number and the die number 
            return narrow_df
        
        raise ValueError("This is an invalid option. Please choose 'narrow' or 'wide'")

class Analyzer:
    def __init__(self, game):
        """
        Takes a game object as input and calculates descriptive statistics.
        
        Parameters:
            game (Game): The Game object to analyze
        
        Raises:
            ValueError: if the passed value is not a Game object
        """
        if not isinstance(game, Game):
            raise ValueError("Input must be a Game object.")
        self.results = game._play_results
    
    def jackpot(self):
        """
        Computes how many times the game resulted in a jackpot (all faces are the same).
        
        Returns:
            int: Number of jackpots
        """
        return int((self.results.nunique(axis=1) == 1).sum())

    def face_counts_per_roll(self):
        """
        Computes how many times a given face is rolled in each event.
        
        Returns:
            pd.DataFrame: A data frame with the roll number as the index and face values as columns
        """
        face_counts_df = self.results.apply(pd.Series.value_counts, axis=1)
        face_counts_df.index.name = 'roll_number'
        return face_counts_df

    def combo(self):
        """
        Computes the distinct combinations of faces rolled and their counts.
        
        Returns:
            pd.DataFrame: A data frame with combinations as a MultiIndex and counts as the column
        """
        combo = self.results.apply(lambda row: tuple(sorted(row)), axis=1)
        combo_count = combo.value_counts().to_frame(name='count')
        combo_count.index = pd.MultiIndex.from_tuples(combo_count.index)
        return combo_count

    def permutation(self):
        """
        Computes the distinct permutations of faces rolled and their counts.
        
        Returns:
            pd.DataFrame: A data frame with permutations as a MultiIndex and counts as the column
        """
        from itertools import permutations
        perms = self.results.apply(lambda row: tuple(row), axis=1).apply(lambda x: list(permutations(x)))
        perm_counts = perms.explode().value_counts().to_frame(name='count')
        perm_counts.index = pd.MultiIndex.from_tuples(perm_counts.index)
        return perm_counts
