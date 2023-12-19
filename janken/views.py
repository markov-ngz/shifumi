from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
import random
# Create your views here.


def game_choice(request):
    return render(request,"janken/game_choice.html")

class Play(View) :
    def get(self, request):
        resultat = "start"
        return render(request,"janken/play.html",{"resultat":resultat})

    def post(self, request) :
        nombre_coups_possibles = 3
        coup_pc = random.randint(1,nombre_coups_possibles)
        coup_user = int(request.POST["pierre"])

        print(coup_user)
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
        
        return render(request,"janken/play.html",{"resultat":resultat, "id":id})