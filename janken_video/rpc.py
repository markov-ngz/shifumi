import random


def jouer(coup:int)->dict:
        
        nombre_coups_possibles = 3
        coup_pc = random.randint(1,nombre_coups_possibles)
        coup_user = coup

        coup_user_modulo = coup_user % nombre_coups_possibles
        coup_pc_modulo = coup_pc % nombre_coups_possibles

        if coup_pc == coup_user :
            resultat = "Egalité ! Rompez "
            id = 0 
        elif coup_user_modulo == coup_pc_modulo + 1: 
            resultat = " Défaite implacable !"
            id = -1
        else :
            resultat = " Victoire Ecrasante ! "
            id = 1 

        return {"resultat":resultat, "id":id}