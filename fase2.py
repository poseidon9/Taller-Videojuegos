import sys, random

def checkIfOver(gato, turn):
	if checkRow(gato[0], turn) or checkRow(gato[1], turn) or checkRow(gato[2], turn)\
	or checkColumn(getColumn(gato, 0), turn) or checkColumn(getColumn(gato, 1), turn) or checkColumn(getColumn(gato, 2), turn)\
	or checkDiagonalL(gato, turn) or checkDiagonalR(gato, turn):
		print "Gano el jugador " + str(turn)
		return True
	else:
		return False


def checkRow(row, turn):
	if(row[0] == turn and row[1] == turn and row[2] == turn):
		return True

def getColumn(gato, column_index):
	return [gato[0][column_index], gato[1][column_index], gato[2][column_index]]

def checkColumn(column, turn):
	if column[0] == turn and column[1] == turn and column[2] == turn:
		return True

def checkDiagonalL(gato, turn):
	if(gato[0][0] == turn and gato[1][1] == turn and gato[2][2] == turn):
		return True

def checkDiagonalR(gato, turn):
	if(gato[2][0] == turn and gato[1][1] == turn and gato[0][2] == turn):
		return True

def playTurn(gato, turn):
	print("Turno del Jugador: " + str(turn))
	while(True):
		x = int(raw_input("X: "))
		y = int(raw_input("Y: "))

		if(gato[x][y] != 0):
			print("Ese espacio esta ocupado, elija otro")
		else:
			gato[x][y] = turn
			break

def changeTurn(turn):
	if turn == 1:
		return 2
	else:
		return 1

def printGato(gato):
	print(str(gato[0][0]) + "|" + str(gato[0][1]) + "|" + str(gato[0][2]))
	print("_|_|_")
	print(str(gato[1][0]) + "|" + str(gato[1][1]) + "|" + str(gato[1][2]))
	print("_|_|_")
	print(str(gato[2][0]) + "|" + str(gato[2][1]) + "|" + str(gato[2][2]))


def main():
	print("Fase2")
	print("https://github.com/poseidon9/Taller-Videojuegos")

	gato = [[0,0,0],[0,0,0],[0,0,0]]

	while(1):
		print("1:Jugar\n2:Salir")
		opc = raw_input()
		end = False
		turn = 1

		gato = [[0,0,0],[0,0,0],[0,0,0]]
		if opc == "1":
			while(not end):
				printGato(gato)
				playTurn(gato, turn)
				if(checkIfOver(gato, turn)):
					break
				turn = changeTurn(turn)
		elif opc == "2":
			break
		else:
			print("No existe Dicha Opcion")

main()
