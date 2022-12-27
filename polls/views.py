from django.shortcuts import render

from django.http import HttpResponse

def index(request):
	return HttpResponse("Bonjour! Ici l'index des sondages.")

def detail(request, question_id):
	return HttpResponse(f"Vous regardez la question n°{question_id}")

def results(request, question_id):
	return HttpResponse(f"Vous regardez les résultats de la question n°{question_id}")

def vote(request, question_id):
	return HttpResponse(f"Vous votez pour la question n°{question_id}")