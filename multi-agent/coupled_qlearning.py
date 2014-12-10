#hier de pseudocode van coupled q-learning
#staat niet in slides, was in de les gegeven

#het algoritme gebruikt joints/vectoren/arrays voor bepaalde values.
#In de les zijn die gegeven door een pijl erop. Ik heb het hier met
#een underscore gedaan.

init Q_(s,a_)
repeat for each episode
    initialise s
        repeat for each step
            choose a_ using equilibrium concept C or Q_(s,a_)
            s',r_ <- do a_ and observe next state and rewards (can be a'_)
            do for all i
                Qi(s,a_) <- (1-alpha)Qi(s,a_) + alpha(ri + gamma C(Q1(s',a'_), ..., Qn(s'a'_)))
            s <- s'
            until s is terminal
            
#dunno wat die equilibrium concept C is. De C is een fancy C. Kunnen we woensdag navragen.