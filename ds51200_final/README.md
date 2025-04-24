**Metadata** 
- Name: Haejin Son 
- Project Name: Monte Carlo Simulator 

**Synopsis** 
This is a brief demo code of how the classes are used. 

from Montecarlo.monte_carlo import Die 
die=Die(np.array([1,2,3,4,5,6]))
die.change_weight(2,5.0)
die.roll(10) 

from Montecarlo.monte_carlo import Die 
game=Game([die1,die2])
game.play(100)
game.show(form='wide') 

from Montecarlo.monte_carlo import Die 
analyzer=Analyzer(game) 
analyzer.jackpot()
analyzer.combo()

**API description**
This list includes all classes and methods in the project.

Die class: 
    __init__(self,faces)
    change_weight(self,face,new_weight)
    roll(self,num_roll=1)
    show(self) 
    
Game class:
    __init__(self,dice) 
    play(self,roll_times)
    show(self,form='wide')
    
Analyzer class: 
    __init__(self,game)
    jackpot(self)
    face_counts_per_roll(self)
    combo(self)
    permutation(self)