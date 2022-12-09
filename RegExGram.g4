grammar RegExGram;

s : 'a' s | 'b' t ;
t : 'c' t |EOF ;
