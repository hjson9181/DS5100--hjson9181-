import unittest
import numpy as np
import pandas as pd
from Montecarlo.monte_carlo import Die, Game, Analyzer

class TestDie(unittest.TestCase):

    def setUp(self):
        # Set up die instances
        self.die1=Die(np.array([1, 2, 3, 4, 5, 6]))
        self.die2=Die(np.array(['H', 'T']))

    def test_initialization(self):
        """
        Tests if Die initializes correctly with faces and weights.
        """
        # Test die1 with 6 numeric faces
        self.assertEqual(len(self.die1._die_df), 6)
        self.assertTrue(np.all(self.die1._die_df['weights']==1.0))
        
        # Test die2 with 2 string faces
        self.assertEqual(self.die2._die_df.index.tolist(), ['H', 'T'])
        self.assertTrue(np.all(self.die2._die_df['weights']==1.0))

    def test_change_weight(self):
        """
        Tests if change_weight method correctly changes the weight. 
        """
        self.die1.change_weight(1,4.0)
        weight_changed=self.die1._die_df.loc[1,'weights']
        self.assertEqual(weight_changed,4.0)
    
    def test_roll(self):
        """
        Tests if the roll method correctly returns a list of outcomes.
        """
        outcomes=self.die1.roll(5)
        self.assertEqual(len(outcomes),5)
            
    def test_show(self):
        """
        Tests if the show method correclty returns a dataframe with face and corresponding weights.
        """
        df=self.die1.show()
        self.assertTrue(isinstance(df, type(self.die1._die_df)))
        self.assertTrue((df.columns==['weights']).all())
        self.assertTrue((df.index==self.die1._die_df.index).all())   

class TestGame(unittest.TestCase):
    def setUp(self):
        #create Game instnace using the dice instances previously set up in class Die
        self.die1=Die(np.array([1, 2, 3, 4, 5, 6]))
        self.die2=Die(np.array(['H', 'T']))
        self.game=Game([self.die1, self.die2])
        
    def test_initialization(self):
        """
        Tests if the Game class initializes with faces and weights correctly.
        """
        self.assertEqual(len(self.game.dice),2)
        self.assertTrue(isinstance(self.game.dice[0],Die))
        self.assertTrue(isinstance(self.game.dice[1],Die))

    def test_play(self):
        """
        Tests if the play method generates a dataframe.
        """
        self.game.play(5)  #roll the dice 5 times
        self.assertTrue(isinstance(self.game._play_results, pd.DataFrame)) #checks if _play_results exists and is a dataframe
        self.assertEqual(self.game._play_results.shape, (5, 2)) #the dataframe has 5 rows (num_rolls) and 2 columns (dice1, dice2)
        self.assertEqual(self.game._play_results.index.name, 'roll_number') #checks if the dataframe index is 'roll_number'
    
    def test_show_wide(self):
        """
        Tests if the show method correctly returns the wide format.
        """
        self.game.play(3)
        result=self.game.show(form='wide')
        
        self.assertTrue(isinstance(result,pd.DataFrame))
        self.assertEqual(result.shape,(3,2))
        
    def test_show_narrow(self):
        """
        Tests if the show method correctly returns the narrow format.
        """
        self.game.play(3)
        result=self.game.show(form='narrow')

        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(result.index.names, ['roll_number', 'die_number'])
        self.assertEqual(result.columns.tolist(), ['outcome'])
        
class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        die1=Die(np.array([2,5]))
        die2=Die(np.array([2,5])) #two identical dice
        
        self.game=Game([die1,die2])
        self.game.play(3) #roll 3 times
        self.analyzer=Analyzer(self.game)
        
    def test_jackpot(self):
        """
        Tests if the jackpot method correctly functions and counts all matching rolls.
        """
        jackpot_count = self.analyzer.jackpot()
        self.assertTrue(isinstance(jackpot_count, int))
        self.assertTrue(0<=jackpot_count<=3) #all 3 rolls should be identical, jackpot
        
    def test_face_counts_per_roll(self):
        """
        Tests if the face_counts_per_roll method correclty returns a dataframe of outputs 
        """
        face_counts=self.analyzer.face_counts_per_roll()
        self.assertTrue(isinstance(face_counts, pd.DataFrame))
        self.assertIn(2, face_counts.columns)
        self.assertTrue(set(face_counts.columns).issubset({2,5}))
    
    def test_combo(self):
        """
        Tests if the combo method correctly returns a dataframe of distinct combinations as a MultiIndex with faces rolled and their counts.
        """
        combos = self.analyzer.combo()
        self.assertTrue(isinstance(combos, pd.DataFrame)) #checks the output is dataframe
        self.assertEqual(combos.index.names, [None, None]) #checks the names of index
        self.assertEqual(combos['count'].sum(), 3) #checks the first row has combination of 3 rolls
                        
    def test_permutation(self):
        """
        Tests if the permutation methods correctly returns a dataframe of faces rolls and their counts with a correct structure, MultiIndex. 
        """
        perms = self.analyzer.permutation()
        self.assertTrue(isinstance(perms, pd.DataFrame))
        self.assertEqual(perms.index.names, [None, None])
        self.assertEqual(perms['count'].sum(), 6)  
                        
if __name__ == '__main__':
    unittest.main()