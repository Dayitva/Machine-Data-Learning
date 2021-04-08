import random as rand

policy = {
("N",0,0,"D",0):"NONE",
("N",0,0,"R",0):"NONE",
("N",1,0,"D",0):"NONE",
("N",1,0,"R",0):"NONE",
("N",2,0,"D",0):"NONE",
("N",2,0,"R",0):"NONE",
("N",0,1,"D",0):"NONE",
("N",0,1,"R",0):"NONE",
("N",1,1,"D",0):"NONE",
("N",1,1,"R",0):"NONE",
("N",2,1,"D",0):"NONE",
("N",2,1,"R",0):"NONE",
("N",0,2,"D",0):"NONE",
("N",0,2,"R",0):"NONE",
("N",1,2,"D",0):"NONE",
("N",1,2,"R",0):"NONE",
("N",2,2,"D",0):"NONE",
("N",2,2,"R",0):"NONE",
("N",0,3,"D",0):"NONE",
("N",0,3,"R",0):"NONE",
("N",1,3,"D",0):"NONE",
("N",1,3,"R",0):"NONE",
("N",2,3,"D",0):"NONE",
("N",2,3,"R",0):"NONE",
("N",0,0,"D",25):"DOWN",
("N",0,0,"R",25):"STAY",
("N",1,0,"D",25):"CRAFT",
("N",1,0,"R",25):"CRAFT",
("N",2,0,"D",25):"CRAFT",
("N",2,0,"R",25):"CRAFT",
("N",0,1,"D",25):"DOWN",
("N",0,1,"R",25):"STAY",
("N",1,1,"D",25):"DOWN",
("N",1,1,"R",25):"CRAFT",
("N",2,1,"D",25):"DOWN",
("N",2,1,"R",25):"CRAFT",
("N",0,2,"D",25):"DOWN",
("N",0,2,"R",25):"STAY",
("N",1,2,"D",25):"DOWN",
("N",1,2,"R",25):"STAY",
("N",2,2,"D",25):"DOWN",
("N",2,2,"R",25):"STAY",
("N",0,3,"D",25):"DOWN",
("N",0,3,"R",25):"STAY",
("N",1,3,"D",25):"DOWN",
("N",1,3,"R",25):"STAY",
("N",2,3,"D",25):"DOWN",
("N",2,3,"R",25):"STAY",
("N",0,0,"D",50):"DOWN",
("N",0,0,"R",50):"DOWN",
("N",1,0,"D",50):"CRAFT",
("N",1,0,"R",50):"CRAFT",
("N",2,0,"D",50):"CRAFT",
("N",2,0,"R",50):"CRAFT",
("N",0,1,"D",50):"DOWN",
("N",0,1,"R",50):"STAY",
("N",1,1,"D",50):"CRAFT",
("N",1,1,"R",50):"CRAFT",
("N",2,1,"D",50):"CRAFT",
("N",2,1,"R",50):"CRAFT",
("N",0,2,"D",50):"DOWN",
("N",0,2,"R",50):"STAY",
("N",1,2,"D",50):"DOWN",
("N",1,2,"R",50):"CRAFT",
("N",2,2,"D",50):"DOWN",
("N",2,2,"R",50):"CRAFT",
("N",0,3,"D",50):"DOWN",
("N",0,3,"R",50):"STAY",
("N",1,3,"D",50):"DOWN",
("N",1,3,"R",50):"STAY",
("N",2,3,"D",50):"DOWN",
("N",2,3,"R",50):"STAY",
("N",0,0,"D",75):"DOWN",
("N",0,0,"R",75):"DOWN",
("N",1,0,"D",75):"CRAFT",
("N",1,0,"R",75):"CRAFT",
("N",2,0,"D",75):"CRAFT",
("N",2,0,"R",75):"CRAFT",
("N",0,1,"D",75):"DOWN",
("N",0,1,"R",75):"STAY",
("N",1,1,"D",75):"CRAFT",
("N",1,1,"R",75):"CRAFT",
("N",2,1,"D",75):"CRAFT",
("N",2,1,"R",75):"CRAFT",
("N",0,2,"D",75):"DOWN",
("N",0,2,"R",75):"STAY",
("N",1,2,"D",75):"CRAFT",
("N",1,2,"R",75):"CRAFT",
("N",2,2,"D",75):"CRAFT",
("N",2,2,"R",75):"CRAFT",
("N",0,3,"D",75):"DOWN",
("N",0,3,"R",75):"STAY",
("N",1,3,"D",75):"DOWN",
("N",1,3,"R",75):"STAY",
("N",2,3,"D",75):"DOWN",
("N",2,3,"R",75):"STAY",
("N",0,0,"D",100):"DOWN",
("N",0,0,"R",100):"DOWN",
("N",1,0,"D",100):"CRAFT",
("N",1,0,"R",100):"CRAFT",
("N",2,0,"D",100):"CRAFT",
("N",2,0,"R",100):"CRAFT",
("N",0,1,"D",100):"DOWN",
("N",0,1,"R",100):"DOWN",
("N",1,1,"D",100):"CRAFT",
("N",1,1,"R",100):"CRAFT",
("N",2,1,"D",100):"CRAFT",
("N",2,1,"R",100):"CRAFT",
("N",0,2,"D",100):"DOWN",
("N",0,2,"R",100):"DOWN",
("N",1,2,"D",100):"DOWN",
("N",1,2,"R",100):"CRAFT",
("N",2,2,"D",100):"DOWN",
("N",2,2,"R",100):"CRAFT",
("N",0,3,"D",100):"DOWN",
("N",0,3,"R",100):"DOWN",
("N",1,3,"D",100):"DOWN",
("N",1,3,"R",100):"DOWN",
("N",2,3,"D",100):"DOWN",
("N",2,3,"R",100):"DOWN",
("E",0,0,"D",0):"NONE",
("E",0,0,"R",0):"NONE",
("E",1,0,"D",0):"NONE",
("E",1,0,"R",0):"NONE",
("E",2,0,"D",0):"NONE",
("E",2,0,"R",0):"NONE",
("E",0,1,"D",0):"NONE",
("E",0,1,"R",0):"NONE",
("E",1,1,"D",0):"NONE",
("E",1,1,"R",0):"NONE",
("E",2,1,"D",0):"NONE",
("E",2,1,"R",0):"NONE",
("E",0,2,"D",0):"NONE",
("E",0,2,"R",0):"NONE",
("E",1,2,"D",0):"NONE",
("E",1,2,"R",0):"NONE",
("E",2,2,"D",0):"NONE",
("E",2,2,"R",0):"NONE",
("E",0,3,"D",0):"NONE",
("E",0,3,"R",0):"NONE",
("E",1,3,"D",0):"NONE",
("E",1,3,"R",0):"NONE",
("E",2,3,"D",0):"NONE",
("E",2,3,"R",0):"NONE",
("E",0,0,"D",25):"HIT",
("E",0,0,"R",25):"HIT",
("E",1,0,"D",25):"HIT",
("E",1,0,"R",25):"HIT",
("E",2,0,"D",25):"HIT",
("E",2,0,"R",25):"HIT",
("E",0,1,"D",25):"SHOOT",
("E",0,1,"R",25):"SHOOT",
("E",1,1,"D",25):"SHOOT",
("E",1,1,"R",25):"SHOOT",
("E",2,1,"D",25):"SHOOT",
("E",2,1,"R",25):"SHOOT",
("E",0,2,"D",25):"SHOOT",
("E",0,2,"R",25):"SHOOT",
("E",1,2,"D",25):"SHOOT",
("E",1,2,"R",25):"SHOOT",
("E",2,2,"D",25):"SHOOT",
("E",2,2,"R",25):"SHOOT",
("E",0,3,"D",25):"SHOOT",
("E",0,3,"R",25):"SHOOT",
("E",1,3,"D",25):"SHOOT",
("E",1,3,"R",25):"SHOOT",
("E",2,3,"D",25):"SHOOT",
("E",2,3,"R",25):"SHOOT",
("E",0,0,"D",50):"HIT",
("E",0,0,"R",50):"HIT",
("E",1,0,"D",50):"HIT",
("E",1,0,"R",50):"HIT",
("E",2,0,"D",50):"HIT",
("E",2,0,"R",50):"HIT",
("E",0,1,"D",50):"HIT",
("E",0,1,"R",50):"SHOOT",
("E",1,1,"D",50):"HIT",
("E",1,1,"R",50):"SHOOT",
("E",2,1,"D",50):"HIT",
("E",2,1,"R",50):"SHOOT",
("E",0,2,"D",50):"SHOOT",
("E",0,2,"R",50):"SHOOT",
("E",1,2,"D",50):"SHOOT",
("E",1,2,"R",50):"SHOOT",
("E",2,2,"D",50):"SHOOT",
("E",2,2,"R",50):"SHOOT",
("E",0,3,"D",50):"SHOOT",
("E",0,3,"R",50):"SHOOT",
("E",1,3,"D",50):"SHOOT",
("E",1,3,"R",50):"SHOOT",
("E",2,3,"D",50):"SHOOT",
("E",2,3,"R",50):"SHOOT",
("E",0,0,"D",75):"HIT",
("E",0,0,"R",75):"HIT",
("E",1,0,"D",75):"HIT",
("E",1,0,"R",75):"HIT",
("E",2,0,"D",75):"HIT",
("E",2,0,"R",75):"HIT",
("E",0,1,"D",75):"HIT",
("E",0,1,"R",75):"SHOOT",
("E",1,1,"D",75):"HIT",
("E",1,1,"R",75):"SHOOT",
("E",2,1,"D",75):"HIT",
("E",2,1,"R",75):"SHOOT",
("E",0,2,"D",75):"SHOOT",
("E",0,2,"R",75):"SHOOT",
("E",1,2,"D",75):"SHOOT",
("E",1,2,"R",75):"SHOOT",
("E",2,2,"D",75):"SHOOT",
("E",2,2,"R",75):"SHOOT",
("E",0,3,"D",75):"SHOOT",
("E",0,3,"R",75):"SHOOT",
("E",1,3,"D",75):"SHOOT",
("E",1,3,"R",75):"SHOOT",
("E",2,3,"D",75):"SHOOT",
("E",2,3,"R",75):"SHOOT",
("E",0,0,"D",100):"HIT",
("E",0,0,"R",100):"HIT",
("E",1,0,"D",100):"HIT",
("E",1,0,"R",100):"HIT",
("E",2,0,"D",100):"HIT",
("E",2,0,"R",100):"HIT",
("E",0,1,"D",100):"HIT",
("E",0,1,"R",100):"HIT",
("E",1,1,"D",100):"HIT",
("E",1,1,"R",100):"HIT",
("E",2,1,"D",100):"HIT",
("E",2,1,"R",100):"HIT",
("E",0,2,"D",100):"HIT",
("E",0,2,"R",100):"HIT",
("E",1,2,"D",100):"HIT",
("E",1,2,"R",100):"HIT",
("E",2,2,"D",100):"HIT",
("E",2,2,"R",100):"HIT",
("E",0,3,"D",100):"SHOOT",
("E",0,3,"R",100):"SHOOT",
("E",1,3,"D",100):"SHOOT",
("E",1,3,"R",100):"SHOOT",
("E",2,3,"D",100):"SHOOT",
("E",2,3,"R",100):"SHOOT",
("S",0,0,"D",0):"NONE",
("S",0,0,"R",0):"NONE",
("S",1,0,"D",0):"NONE",
("S",1,0,"R",0):"NONE",
("S",2,0,"D",0):"NONE",
("S",2,0,"R",0):"NONE",
("S",0,1,"D",0):"NONE",
("S",0,1,"R",0):"NONE",
("S",1,1,"D",0):"NONE",
("S",1,1,"R",0):"NONE",
("S",2,1,"D",0):"NONE",
("S",2,1,"R",0):"NONE",
("S",0,2,"D",0):"NONE",
("S",0,2,"R",0):"NONE",
("S",1,2,"D",0):"NONE",
("S",1,2,"R",0):"NONE",
("S",2,2,"D",0):"NONE",
("S",2,2,"R",0):"NONE",
("S",0,3,"D",0):"NONE",
("S",0,3,"R",0):"NONE",
("S",1,3,"D",0):"NONE",
("S",1,3,"R",0):"NONE",
("S",2,3,"D",0):"NONE",
("S",2,3,"R",0):"NONE",
("S",0,0,"D",25):"GATHER",
("S",0,0,"R",25):"GATHER",
("S",1,0,"D",25):"UP",
("S",1,0,"R",25):"GATHER",
("S",2,0,"D",25):"UP",
("S",2,0,"R",25):"UP",
("S",0,1,"D",25):"UP",
("S",0,1,"R",25):"GATHER",
("S",1,1,"D",25):"UP",
("S",1,1,"R",25):"GATHER",
("S",2,1,"D",25):"UP",
("S",2,1,"R",25):"STAY",
("S",0,2,"D",25):"UP",
("S",0,2,"R",25):"STAY",
("S",1,2,"D",25):"UP",
("S",1,2,"R",25):"STAY",
("S",2,2,"D",25):"UP",
("S",2,2,"R",25):"STAY",
("S",0,3,"D",25):"UP",
("S",0,3,"R",25):"STAY",
("S",1,3,"D",25):"UP",
("S",1,3,"R",25):"GATHER",
("S",2,3,"D",25):"UP",
("S",2,3,"R",25):"STAY",
("S",0,0,"D",50):"GATHER",
("S",0,0,"R",50):"GATHER",
("S",1,0,"D",50):"GATHER",
("S",1,0,"R",50):"GATHER",
("S",2,0,"D",50):"UP",
("S",2,0,"R",50):"UP",
("S",0,1,"D",50):"UP",
("S",0,1,"R",50):"GATHER",
("S",1,1,"D",50):"UP",
("S",1,1,"R",50):"GATHER",
("S",2,1,"D",50):"UP",
("S",2,1,"R",50):"UP",
("S",0,2,"D",50):"UP",
("S",0,2,"R",50):"GATHER",
("S",1,2,"D",50):"UP",
("S",1,2,"R",50):"GATHER",
("S",2,2,"D",50):"UP",
("S",2,2,"R",50):"STAY",
("S",0,3,"D",50):"UP",
("S",0,3,"R",50):"GATHER",
("S",1,3,"D",50):"UP",
("S",1,3,"R",50):"GATHER",
("S",2,3,"D",50):"UP",
("S",2,3,"R",50):"STAY",
("S",0,0,"D",75):"GATHER",
("S",0,0,"R",75):"GATHER",
("S",1,0,"D",75):"UP",
("S",1,0,"R",75):"GATHER",
("S",2,0,"D",75):"UP",
("S",2,0,"R",75):"UP",
("S",0,1,"D",75):"UP",
("S",0,1,"R",75):"GATHER",
("S",1,1,"D",75):"UP",
("S",1,1,"R",75):"GATHER",
("S",2,1,"D",75):"UP",
("S",2,1,"R",75):"UP",
("S",0,2,"D",75):"UP",
("S",0,2,"R",75):"GATHER",
("S",1,2,"D",75):"UP",
("S",1,2,"R",75):"GATHER",
("S",2,2,"D",75):"UP",
("S",2,2,"R",75):"UP",
("S",0,3,"D",75):"UP",
("S",0,3,"R",75):"GATHER",
("S",1,3,"D",75):"UP",
("S",1,3,"R",75):"GATHER",
("S",2,3,"D",75):"UP",
("S",2,3,"R",75):"STAY",
("S",0,0,"D",100):"GATHER",
("S",0,0,"R",100):"GATHER",
("S",1,0,"D",100):"UP",
("S",1,0,"R",100):"GATHER",
("S",2,0,"D",100):"UP",
("S",2,0,"R",100):"UP",
("S",0,1,"D",100):"UP",
("S",0,1,"R",100):"GATHER",
("S",1,1,"D",100):"UP",
("S",1,1,"R",100):"GATHER",
("S",2,1,"D",100):"UP",
("S",2,1,"R",100):"UP",
("S",0,2,"D",100):"UP",
("S",0,2,"R",100):"GATHER",
("S",1,2,"D",100):"UP",
("S",1,2,"R",100):"GATHER",
("S",2,2,"D",100):"UP",
("S",2,2,"R",100):"UP",
("S",0,3,"D",100):"UP",
("S",0,3,"R",100):"GATHER",
("S",1,3,"D",100):"UP",
("S",1,3,"R",100):"GATHER",
("S",2,3,"D",100):"UP",
("S",2,3,"R",100):"UP",
("W",0,0,"D",0):"NONE",
("W",0,0,"R",0):"NONE",
("W",1,0,"D",0):"NONE",
("W",1,0,"R",0):"NONE",
("W",2,0,"D",0):"NONE",
("W",2,0,"R",0):"NONE",
("W",0,1,"D",0):"NONE",
("W",0,1,"R",0):"NONE",
("W",1,1,"D",0):"NONE",
("W",1,1,"R",0):"NONE",
("W",2,1,"D",0):"NONE",
("W",2,1,"R",0):"NONE",
("W",0,2,"D",0):"NONE",
("W",0,2,"R",0):"NONE",
("W",1,2,"D",0):"NONE",
("W",1,2,"R",0):"NONE",
("W",2,2,"D",0):"NONE",
("W",2,2,"R",0):"NONE",
("W",0,3,"D",0):"NONE",
("W",0,3,"R",0):"NONE",
("W",1,3,"D",0):"NONE",
("W",1,3,"R",0):"NONE",
("W",2,3,"D",0):"NONE",
("W",2,3,"R",0):"NONE",
("W",0,0,"D",25):"RIGHT",
("W",0,0,"R",25):"STAY",
("W",1,0,"D",25):"RIGHT",
("W",1,0,"R",25):"STAY",
("W",2,0,"D",25):"RIGHT",
("W",2,0,"R",25):"RIGHT",
("W",0,1,"D",25):"RIGHT",
("W",0,1,"R",25):"STAY",
("W",1,1,"D",25):"RIGHT",
("W",1,1,"R",25):"STAY",
("W",2,1,"D",25):"RIGHT",
("W",2,1,"R",25):"STAY",
("W",0,2,"D",25):"SHOOT",
("W",0,2,"R",25):"SHOOT",
("W",1,2,"D",25):"SHOOT",
("W",1,2,"R",25):"SHOOT",
("W",2,2,"D",25):"SHOOT",
("W",2,2,"R",25):"SHOOT",
("W",0,3,"D",25):"SHOOT",
("W",0,3,"R",25):"SHOOT",
("W",1,3,"D",25):"SHOOT",
("W",1,3,"R",25):"SHOOT",
("W",2,3,"D",25):"SHOOT",
("W",2,3,"R",25):"SHOOT",
("W",0,0,"D",50):"RIGHT",
("W",0,0,"R",50):"STAY",
("W",1,0,"D",50):"RIGHT",
("W",1,0,"R",50):"RIGHT",
("W",2,0,"D",50):"RIGHT",
("W",2,0,"R",50):"RIGHT",
("W",0,1,"D",50):"RIGHT",
("W",0,1,"R",50):"STAY",
("W",1,1,"D",50):"RIGHT",
("W",1,1,"R",50):"STAY",
("W",2,1,"D",50):"RIGHT",
("W",2,1,"R",50):"STAY",
("W",0,2,"D",50):"RIGHT",
("W",0,2,"R",50):"STAY",
("W",1,2,"D",50):"RIGHT",
("W",1,2,"R",50):"STAY",
("W",2,2,"D",50):"RIGHT",
("W",2,2,"R",50):"STAY",
("W",0,3,"D",50):"RIGHT",
("W",0,3,"R",50):"SHOOT",
("W",1,3,"D",50):"RIGHT",
("W",1,3,"R",50):"SHOOT",
("W",2,3,"D",50):"RIGHT",
("W",2,3,"R",50):"SHOOT",
("W",0,0,"D",75):"RIGHT",
("W",0,0,"R",75):"RIGHT",
("W",1,0,"D",75):"RIGHT",
("W",1,0,"R",75):"RIGHT",
("W",2,0,"D",75):"RIGHT",
("W",2,0,"R",75):"RIGHT",
("W",0,1,"D",75):"RIGHT",
("W",0,1,"R",75):"STAY",
("W",1,1,"D",75):"RIGHT",
("W",1,1,"R",75):"STAY",
("W",2,1,"D",75):"RIGHT",
("W",2,1,"R",75):"STAY",
("W",0,2,"D",75):"RIGHT",
("W",0,2,"R",75):"SHOOT",
("W",1,2,"D",75):"RIGHT",
("W",1,2,"R",75):"SHOOT",
("W",2,2,"D",75):"RIGHT",
("W",2,2,"R",75):"SHOOT",
("W",0,3,"D",75):"RIGHT",
("W",0,3,"R",75):"STAY",
("W",1,3,"D",75):"RIGHT",
("W",1,3,"R",75):"STAY",
("W",2,3,"D",75):"RIGHT",
("W",2,3,"R",75):"STAY",
("W",0,0,"D",100):"RIGHT",
("W",0,0,"R",100):"RIGHT",
("W",1,0,"D",100):"RIGHT",
("W",1,0,"R",100):"RIGHT",
("W",2,0,"D",100):"RIGHT",
("W",2,0,"R",100):"RIGHT",
("W",0,1,"D",100):"RIGHT",
("W",0,1,"R",100):"STAY",
("W",1,1,"D",100):"RIGHT",
("W",1,1,"R",100):"RIGHT",
("W",2,1,"D",100):"RIGHT",
("W",2,1,"R",100):"RIGHT",
("W",0,2,"D",100):"RIGHT",
("W",0,2,"R",100):"STAY",
("W",1,2,"D",100):"RIGHT",
("W",1,2,"R",100):"STAY",
("W",2,2,"D",100):"RIGHT",
("W",2,2,"R",100):"STAY",
("W",0,3,"D",100):"RIGHT",
("W",0,3,"R",100):"SHOOT",
("W",1,3,"D",100):"RIGHT",
("W",1,3,"R",100):"SHOOT",
("W",2,3,"D",100):"RIGHT",
("W",2,3,"R",100):"SHOOT",
("C",0,0,"D",0):"NONE",
("C",0,0,"R",0):"NONE",
("C",1,0,"D",0):"NONE",
("C",1,0,"R",0):"NONE",
("C",2,0,"D",0):"NONE",
("C",2,0,"R",0):"NONE",
("C",0,1,"D",0):"NONE",
("C",0,1,"R",0):"NONE",
("C",1,1,"D",0):"NONE",
("C",1,1,"R",0):"NONE",
("C",2,1,"D",0):"NONE",
("C",2,1,"R",0):"NONE",
("C",0,2,"D",0):"NONE",
("C",0,2,"R",0):"NONE",
("C",1,2,"D",0):"NONE",
("C",1,2,"R",0):"NONE",
("C",2,2,"D",0):"NONE",
("C",2,2,"R",0):"NONE",
("C",0,3,"D",0):"NONE",
("C",0,3,"R",0):"NONE",
("C",1,3,"D",0):"NONE",
("C",1,3,"R",0):"NONE",
("C",2,3,"D",0):"NONE",
("C",2,3,"R",0):"NONE",
("C",0,0,"D",25):"RIGHT",
("C",0,0,"R",25):"LEFT",
("C",1,0,"D",25):"UP",
("C",1,0,"R",25):"UP",
("C",2,0,"D",25):"UP",
("C",2,0,"R",25):"UP",
("C",0,1,"D",25):"RIGHT",
("C",0,1,"R",25):"UP",
("C",1,1,"D",25):"RIGHT",
("C",1,1,"R",25):"SHOOT",
("C",2,1,"D",25):"RIGHT",
("C",2,1,"R",25):"SHOOT",
("C",0,2,"D",25):"RIGHT",
("C",0,2,"R",25):"LEFT",
("C",1,2,"D",25):"RIGHT",
("C",1,2,"R",25):"LEFT",
("C",2,2,"D",25):"RIGHT",
("C",2,2,"R",25):"LEFT",
("C",0,3,"D",25):"RIGHT",
("C",0,3,"R",25):"LEFT",
("C",1,3,"D",25):"SHOOT",
("C",1,3,"R",25):"LEFT",
("C",2,3,"D",25):"SHOOT",
("C",2,3,"R",25):"LEFT",
("C",0,0,"D",50):"RIGHT",
("C",0,0,"R",50):"RIGHT",
("C",1,0,"D",50):"UP",
("C",1,0,"R",50):"UP",
("C",2,0,"D",50):"UP",
("C",2,0,"R",50):"UP",
("C",0,1,"D",50):"RIGHT",
("C",0,1,"R",50):"LEFT",
("C",1,1,"D",50):"UP",
("C",1,1,"R",50):"UP",
("C",2,1,"D",50):"UP",
("C",2,1,"R",50):"UP",
("C",0,2,"D",50):"RIGHT",
("C",0,2,"R",50):"LEFT",
("C",1,2,"D",50):"RIGHT",
("C",1,2,"R",50):"LEFT",
("C",2,2,"D",50):"RIGHT",
("C",2,2,"R",50):"LEFT",
("C",0,3,"D",50):"RIGHT",
("C",0,3,"R",50):"LEFT",
("C",1,3,"D",50):"RIGHT",
("C",1,3,"R",50):"LEFT",
("C",2,3,"D",50):"RIGHT",
("C",2,3,"R",50):"LEFT",
("C",0,0,"D",75):"RIGHT",
("C",0,0,"R",75):"RIGHT",
("C",1,0,"D",75):"UP",
("C",1,0,"R",75):"UP",
("C",2,0,"D",75):"UP",
("C",2,0,"R",75):"UP",
("C",0,1,"D",75):"RIGHT",
("C",0,1,"R",75):"LEFT",
("C",1,1,"D",75):"RIGHT",
("C",1,1,"R",75):"UP",
("C",2,1,"D",75):"RIGHT",
("C",2,1,"R",75):"UP",
("C",0,2,"D",75):"RIGHT",
("C",0,2,"R",75):"LEFT",
("C",1,2,"D",75):"RIGHT",
("C",1,2,"R",75):"UP",
("C",2,2,"D",75):"RIGHT",
("C",2,2,"R",75):"UP",
("C",0,3,"D",75):"RIGHT",
("C",0,3,"R",75):"LEFT",
("C",1,3,"D",75):"RIGHT",
("C",1,3,"R",75):"LEFT",
("C",2,3,"D",75):"RIGHT",
("C",2,3,"R",75):"LEFT",
("C",0,0,"D",100):"RIGHT",
("C",0,0,"R",100):"RIGHT",
("C",1,0,"D",100):"UP",
("C",1,0,"R",100):"UP",
("C",2,0,"D",100):"UP",
("C",2,0,"R",100):"UP",
("C",0,1,"D",100):"RIGHT",
("C",0,1,"R",100):"LEFT",
("C",1,1,"D",100):"RIGHT",
("C",1,1,"R",100):"UP",
("C",2,1,"D",100):"RIGHT",
("C",2,1,"R",100):"UP",
("C",0,2,"D",100):"RIGHT",
("C",0,2,"R",100):"LEFT",
("C",1,2,"D",100):"RIGHT",
("C",1,2,"R",100):"LEFT",
("C",2,2,"D",100):"RIGHT",
("C",2,2,"R",100):"LEFT",
("C",0,3,"D",100):"RIGHT",
("C",0,3,"R",100):"LEFT",
("C",1,3,"D",100):"RIGHT",
("C",1,3,"R",100):"LEFT",
("C",2,3,"D",100):"RIGHT",
("C",2,3,"R",100):"LEFT",
}

def simulate(start, policy, flag):
    cur = list(start) 

    while cur[4] > 0:
        curpolicy = policy[tuple(cur)]
        print(tuple(cur), curpolicy)

        if cur[3] == 'D':
            sim_random = rand.uniform(0,1)
            if sim_random <= 0.2:
                cur[3] = 'R'
        
        elif cur[3] == 'R':
            sim_random = rand.uniform(0,1)
            if sim_random <= 0.5:
                cur[3] = 'D'

                if cur[0] == 'C' or cur[0] == 'E':
                    cur[2] = 0
                    cur[4] = (cur[4] + 25 * (cur[4] != 100))
                    continue
        
        if cur[0] == 'W':
            if curpolicy == "RIGHT":
                cur[0] = 'C'

            elif curpolicy == "SHOOT":
                if cur[2] > 0:
                    cur[2] = cur[2] - 1

                    sim_random = rand.uniform(0,1)
                    if sim_random <= 0.25:
                        cur[4] = cur[4] - 25

        elif cur[0] == 'N':
            if curpolicy == "DOWN":
                sim_random = rand.uniform(0,1)
                if sim_random <= 0.85:
                    cur[0] = 'C'

                else:
                    cur[0] = 'E'

            elif curpolicy == "STAY":
                sim_random = rand.uniform(0,1)
                if sim_random <= 0.85:
                    cur[0] = 'N'

                else:
                    cur[0] = 'E'

            elif curpolicy == "CRAFT":
                if cur[1] > 0:
                    cur[1] = cur[1] - 1
                    sim_random = rand.uniform(0,1)
                    if sim_random <= 0.15:
                        cur[2] = 3

                    elif sim_random <= 0.5:
                        cur[2] = 3 - (not(cur[2]))

                    else:
                        cur[2] = cur[2] + (cur[2] !=3)

        elif cur[0] == 'E':
            if curpolicy == "LEFT" and flag != 1:
                cur[0] = 'C'

            elif curpolicy == "LEFT" and flag == 1:
                cur[0] = 'W'

            elif curpolicy == "SHOOT":
                if cur[2] > 0:
                    cur[2] = cur[2] - 1
                    sim_random = rand.uniform(0,1)
                    if sim_random <= 0.9:
                        cur[4] = cur[4] - 25

            elif curpolicy == "HIT":
                sim_random = rand.uniform(0,1)
                if sim_random <= 0.2:
                    cur[4] = cur[4] - 50

        elif cur[0] == 'S':
            if curpolicy == "UP":
                sim_random = rand.uniform(0,1)
                if sim_random <= 0.85:
                    cur[0] = 'C'

                else:
                    cur[0] = 'E'

            elif curpolicy == "STAY":
                sim_random = rand.uniform(0,1)
                if sim_random <= 0.85:
                    cur[0] = 'S'

                else:
                    cur[0] = 'E'

            elif curpolicy == "GATHER":
                    sim_random = rand.uniform(0,1)
                    if sim_random <= 0.75:
                        cur[1] = cur[1] + (cur[1] !=2)

        elif cur[0] == 'C':
            if curpolicy == "DOWN":
                sim_random = rand.uniform(0,1)
                if sim_random <= 0.85:
                    cur[0] = 'S'

                else:
                    cur[0] = 'E'

            elif curpolicy == "LEFT":
                sim_random = rand.uniform(0,1)
                if sim_random <= 0.85:
                    cur[0] = 'W'

                else:
                    cur[0] = 'E'

            elif curpolicy == "UP":
                sim_random = rand.uniform(0,1)
                if sim_random <= 0.85:
                    cur[0] = 'N'

                else:
                    cur[0] = 'E'

            elif curpolicy == "RIGHT":
                cur[0] = 'E'

            elif curpolicy == "STAY":
                sim_random = rand.uniform(0,1)
                if sim_random <= 0.85:
                    cur[0] = 'C'

                else:
                    cur[0] = 'E'

            elif curpolicy == "SHOOT":
                if cur[2] > 0:
                    cur[2] = cur[2] - 1
                    sim_random = rand.uniform(0,1)
                    if sim_random <= 0.5:
                        cur[4] = cur[4] - 25

            elif curpolicy == "HIT":
                sim_random = rand.uniform(0,1)
                if sim_random <= 0.1:
                    cur[4] = cur[4] - 50

print("First:")
simulate(["W",0,0,"D",100], policy, 0)
print("\nSecond:")
simulate(["C",2,0,"R",100], policy, 0)
print("\nThird:")
simulate(["E",0,1,"D",50], policy, 0)