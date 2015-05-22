import bfs
import game
import sys

level = ''
fil = open(sys.argv[1],'r')
for l in fil:
    level+=l
fil.close()
level = level[:-1]
game.setLevel(level)
bfs.start(game,40)

#2
level = """                                 
                                 
                                 
   wwwwwwwwwwwww                 
   wwwwwwwwwwwww  e              
   wwwwwwwwwwwww                 
   wwwwwwwwww fw                 
   wwwwwwwwww     Gggf           
   wwwwwwwwww  wwwww             
   wwwwwwwwwwwwwwwww             
   wwwwwwwwwwwwwwwww             
   wwwwwwwwwwwwwwwww             
   wwwwwwwwwwwwwwwww             """
#3
level = """                                 
                                 
                                 
        e                        
    gG                           
    gf    f                      
      s                          
      swwwwwwwwww                
    wwwwwwwwwwwww                
    wwwwwwwwwwwww                
    wwwwwwwwwwwww                
    wwwwwwwwwwwww                
                                 """
#4
level = """                                 
                                 
                                 
                                 
           ggG e                 
           gw                    
                                 
         ws   sw                 
          s                      
          ssws                   
            f                    
              w                  
             ww                  
             ww                  
                                 """
#5
level = """                                 
                                 
                                 
                                 
               e                 
             w                   
            f  fw                
                                 
            sw  w                
             gGss                
             gws                 
                                 
                                 
                                 
                                 """
