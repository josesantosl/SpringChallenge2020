from math import sqrt
from random import choice
#Ho scelto cambiare la strutura lineale per OOP nel mio codice per avere un ordiner migliore tra le variabili e la redondanza

reserva=[]#Questo serve per evitare i blochi per non avere indirizzi
counters=[]
registers=[]
ids=[]

class Pac:
    def __init__(self,x,y,pac_id,type_id,speed_turns_left,cooldown):#constructor
        self.x=x
        self.y=y
        self.pac_id=str(pac_id)
        self.turns=(1 if speed_turns_left>=0 else 0)
        self.type_id=type_id
        self.cooldown=cooldown

    def dist(self,obj):#Calcola la distanza tra il pallet e il Pacman
       return sqrt(pow(self.x-obj.x,2)+pow(self.y-obj.y,2))

    def mangiavile(self,obj):
       return (self.type_id=='ROCK'and obj.type_id=='SCISSORS')or(self.type_id=='SCISSORS'and obj.type_id=='PAPER') or(self.type_id=='PAPER'and obj.type_id=='ROCK')

    def mov(self,lista,nem):#cerca la miglior scelta
        output=''
        while self.turns>0:
            self.turns-=1#per ridure la capacita' dei turni
            if self.cooldown == 0:#usare abilità ogni volta che sia possibile 
                self.cooldown=10#per evitare un'altra attivazzione 
                if len(nem)>0:
                    distanza=self.dist(nem[0])
                    vicino=nem[0]
                    for i in nem:
                        if self.dist(i)<distanza:
                            distanza=self.dist(i)
                            vicino=i
                    if distanza<7 and not self.mangiavile(vicino):#se questo è vero vuol dire che c'e un nemico vicino che puo amazarlo
                        if vicino.type_id=='PAPER':
                            self.type_id='SCISSORS'
                        elif vicino.type_id=='SCISSORS':
                            self.type_id='ROCK'
                        else:
                            self.type_id='PAPER'
                            output+="SWITCH "+self.pac_id+" "+self.type_id+"|"
                    else:
                        output+="SPEED "+self.pac_id+"|"
                else:#ma se non ho nessun nemico attivo la funzione speed
                    output+="SPEED "+self.pac_id+"|"
            else:#SECCION DEL COMANDO MOVE
                distanza=99999
                if len(lista)>0:
                    vicino=lista[0]
                    for i in lista:
                        if self.dist(i)<distanza and not(vicino.value==10 and (self.x==vicino.x or self.y==vicino.y)):
                            distanza=self.dist(i)
                            vicino=i
                    if vicino.value<10 and len(nem)>0:
                        for i in nem:
                            if self.mangiavile(i) and self.dist(i)<5:
                                vicino=i
                    if 'Pallet' in str(type(vicino)):
                        lista.remove(vicino)
                        for i in reserva:
                            if i.x==vicino.x and i.y==vicino.y:
                                reserva.remove(i)                        
                    else:
                        nem.remove(vicino)

                    if registers[ids.index(self.pac_id)].x == vicino.x and registers[ids.index(self.pac_id)].y == vicino.y :
                        if counters[ids.index(self.pac_id)]>=2:
                            if len(lista)>1: vicino=choice(lista)
                            else:vicino=choice(reserva)
                        else:
                            counters[ids.index(self.pac_id)]+=1
                    else:
                        counters[ids.index(self.pac_id)]=0
                        registers[ids.index(self.pac_id)]=vicino
                            
                    output+="MOVE "+self.pac_id+" "+str(vicino.x)+" "+str(vicino.y)+"|"

                elif len(nem)>0:
                    vicino=nem[0]
                    for i in nem:
                        if self.mangiavile(i) and self.dist(i)<5:
                            vicino=i
                    nem.remove(vicino)
                    output+="MOVE "+self.pac_id+" "+str(vicino.x)+" "+str(vicino.y)+"|"
        if output=='':
            aleatorio=choice(reserva)
            reserva.remove(aleatorio)
            output+="MOVE "+self.pac_id+" "+str(aleatorio.x)+" "+str(aleatorio.y)
                        
        return output
                
class Pallet:
    def __init__(self,x,y,value):
        self.x=x
        self.y=y
        self.value=value

#=======INIZIO DEL CODICE PIANO =========
width, height = [int(i) for i in input().split()]
mapa=[]
for i in range(height):
    mapa.append(input())  # one line of tphe grid: space " " is floor, pound "#" is wall


while True:
    my_score, opponent_score = [int(i) for i in input().split()]
    visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
    mios=[]
    tuyos=[]
    for i in range(visible_pac_count):
        pac_id, mine, x, y, type_id, speed_turns_left, ability_cooldown = input().split()
        pac_id = int(pac_id)
        mine = mine != "0"
        x = int(x)
        y = int(y)
        speed_turns_left = int(speed_turns_left)
        ability_cooldown = int(ability_cooldown)
        if mine:
            mios.append(Pac(x,y,pac_id,type_id,speed_turns_left,ability_cooldown))
        else:
            tuyos.append(Pac(x,y,pac_id,type_id,speed_turns_left,ability_cooldown))

    for  i in range(len(mios)):
        registers.append(Pallet(0,0,0))
        counters.append(0)
        ids.append(mios[i].pac_id)
    visible_pellet_count = int(input())  # all pellets in sight
    pallets=[]
    if visible_pellet_count==0:
        for i in range(len(mios)*2):
            pallets.append(choice(reserva))
            
                                    
    for i in range(visible_pellet_count):
        x,y,value = [int(j) for j in input().split()]
        pallets.append(Pallet(x,y,value))
        reserva.append(Pallet(x,y,value))
            
    output=''#ultima palabra e unico print
    for i in mios:
        output+=i.mov(pallets,tuyos)
    print(output)#gran final.
