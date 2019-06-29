import sys, random

print("Fase1")
print("https://github.com/poseidon9/Taller-Videojuegos")

score = 0

while(1):
	print("1:Jugar\n2:Salir")
	opc = raw_input()

	if opc == "1":
		throw = random.randint(1,6)
		print("Adivina el dado 1-6\n")
		guess = int(raw_input())
		if throw == guess:
			score += 1
			print("ACERTASTE!, punctuacion actual: "+str(score))
		print("el dado tirado fue: "+str(throw))
	elif opc == "2":
		print("Se acabo, Su punctuacion Final fue: "+str(score))
		break
	else:
		print("No existe Dicha Opcion")


