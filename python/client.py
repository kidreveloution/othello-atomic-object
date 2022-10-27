#!/usr/bin/python

import math
import sys
import json
import socket
from random import choice
import pandas as pd

def secureCorners(possibleMoves): #Given all the possible Moves, if one of the 4 corners in the list, secure that corner First
  corners = [[0,0],[7,7],[0,7],[7,0]] 
  if corners[0] in possibleMoves: 
    returnedAns = "[0,0]"
    return returnedAns
  if corners[1] in [possibleMoves]:
    returnedAns = "[7,7]"
    return returnedAns
  if corners[2] in possibleMoves:
    returnedAns = "[7,0]"
    return returnedAns
  if corners[3] in [possibleMoves]:
    returnedAns = "[0,7]"
    return returnedAns
  
def gravitateAwayFromCenter(possibleMoves): #This function finds which 'possibleMove' is farthest away from the center and returns it
  center = [0,0]
  returnedAns = possibleMoves[0]
  tempDist = math.dist(possibleMoves[0],center)
  for x in range(len(possibleMoves)):
    if math.dist(possibleMoves[x],center)>tempDist: # Here, we avoid the center as much as possible
      tempDist = math.dist(possibleMoves[0],center)
      returnedAns = possibleMoves[x]
  returnedAns = "["+str(returnedAns[1])+","+str(returnedAns[0])+"]" #Formatting the answer
  return returnedAns

def gravitateToCenter(possibleMoves): #This function finds which 'possibleMove' is closest to the center, and returns it
  center = [0,0]
  returnedAns = possibleMoves[0]
  tempDist = math.dist(possibleMoves[0],center)
  for x in range(len(possibleMoves)):
    if math.dist(possibleMoves[x],center)<tempDist: # Here, we avoid the center as much as possible
      tempDist = math.dist(possibleMoves[0],center)
      returnedAns = possibleMoves[x]
  returnedAns = "["+str(returnedAns[1])+","+str(returnedAns[0])+"]" #Formatting the answer
  return returnedAns

def bestMove(player,possibleMoves): #Given the player, and all the 'possibleMoves' find the 'best' move to make
  
  returnedAns = secureCorners(possibleMoves) #We should ALWAYS aim to secure any of the 4 corners when we can
  if returnedAns != None:
    return returnedAns

  if player == 1: 
    returnedAns = gravitateToCenter(possibleMoves)
    return returnedAns

  if player == 2:
    returnedAns = gravitateToCenter(possibleMoves)
    return returnedAns
    
def findLeadingPiece(player,posName,ans,df): #After finding all the places where there are empty spaces, we now must find acceptable moves given we MUST flank every pieace

  #The way this works is, given the player(what pieaces we should be looking for)
  #Then given the posName (know the direction which we go opposite of to look for a pieace)
  #We then iterate opposite of the starting point (ans)
  #We need the dataframe to iterate through it. Dataframe == Board
  if posName == 'topLeft':
    try:
      while (True):
        if (df[ans[0]+1][ans[1]+1] == player):
          return True
        if (df[ans[0]+1][ans[1]+1] == 0):
          return False
        ans = ans[0]+1,ans[1]+1
    except:
      return False
  if posName == 'centerTop':
    try:
      while (True):
        if (df[ans[0]+1][ans[1]] == player):
          return True
        if (df[ans[0]+1][ans[1]] == 0):
          return False
        ans = ans[0]+1,ans[1]
    except:
      return False
  if posName == 'topRight':
    try:
      while (True):
        if (df[ans[0]+1][ans[1]-1] == player):
          return True
        if (df[ans[0]+1][ans[1]-1] == 0):
          return False
        ans = ans[0]+1,ans[1]-1

    except:
      return(False)
  if posName == 'left':
    try:
      while (True):
        if (df[ans[0]][ans[1]+1] == player):
          return True
        if (df[ans[0]][ans[1]+1]  == 0):
          return False
        ans = ans[0],ans[1]+1
    except:
      return False
  if posName == 'right':
    try:
      while (True):
        if (df[ans[0]][ans[1]-1]  == player):
          return True
        if (df[ans[0]][ans[1]-1] == 0):
          return False
        ans = ans[0],ans[1]-1
    except:
      return False
  if posName == 'bottomLeft':
    try:
      while (True):
        if (df[ans[0]-1][ans[1]+1] == player):
          return True
        if (df[ans[0]-1][ans[1]+1] == 0):
          return False
        ans = ans[0]-1,ans[1]+1
    except:
      return False
  if posName == 'centerBottom':
    try:
      while (True):
        if (df[ans[0]-1][ans[1]] == player):
          return True
        if (df[ans[0]-1][ans[1]] == 0):
          return False
        ans = ans[0]-1,ans[1]
    except:
      return False
  if posName == 'bottomRight':
    try:
      while (True):
        if (df[ans[0]-1][ans[1]-1] == player):
          return True
        if (df[ans[0]-1][ans[1]-1] == 0):
          return False
        ans = ans[0]-1,ans[1]-1
    except:
      return False

def findNearby0(player,df,pieaces): #Given the enemy pieaces, we find all zeros next to it
  counter = 1 #This is an edge case counter. If we find a enemy piece, surronded entirely by our pieaces, we then iterate this counter to look 2 pieaces away from the enemy pieace for empty slots
  possiblePlacements = [] #Initiate possible placements
  while True:
    for x in range(len(pieaces)):
      x_cord = pieaces[x][1]
      y_cord = pieaces[x][0]
      try:
        topLeft = df[x_cord-counter][y_cord-counter]
        if topLeft == 0 and findLeadingPiece(player,'topLeft',(x_cord-counter,y_cord-counter),df): #As long as the piece we are looking at is Empty (==0) AND has a leading Piece.....
          possiblePlacements.append([x_cord-counter,y_cord-counter]) #It becomes an acceptable answer
      except:
        pass
      try:
        centerTop = df[x_cord-counter][y_cord]
        if centerTop == 0 and findLeadingPiece(player,'centerTop',(x_cord-counter,y_cord),df): #Same goes for the rest
          possiblePlacements.append([x_cord-counter,y_cord])
      except:
        pass
      try:
        topRight = df[x_cord-counter][y_cord+counter]
        if topRight == 0 and findLeadingPiece(player,'topRight',(x_cord-counter,y_cord+counter),df):
          possiblePlacements.append([x_cord-counter,y_cord+counter])
      except:
        pass
      try:
        left = df[x_cord][y_cord-counter] 
        if left == 0 and findLeadingPiece(player,"left",([x_cord,y_cord-counter]),df):
          possiblePlacements.append([x_cord,y_cord-counter])
      except:
        pass
      try:
        right = df[x_cord][y_cord+counter]
        if right == 0 and findLeadingPiece(player,"right",([x_cord,y_cord+counter]),df):
          possiblePlacements.append([x_cord,y_cord+counter]) 
      except:
        pass
      try:
        bottomLeft = df[x_cord+counter][y_cord-counter]
        if bottomLeft == 0 and findLeadingPiece(player,"bottomLeft",([x_cord+counter,y_cord-counter]),df):
          possiblePlacements.append([x_cord+counter,y_cord-counter])
      except:
        pass
      try:
        centerBottom = df[x_cord+counter][y_cord]
        if centerBottom == 0 and findLeadingPiece(player,"centerBottom",([x_cord+counter,y_cord]),df):
          possiblePlacements.append([x_cord+counter,y_cord])
      except:
        pass
      try:
        bottomRight = df[x_cord+counter][y_cord+counter]
        if bottomRight == 0 and findLeadingPiece(player,"bottomRight",([x_cord+counter,y_cord+counter]),df):
          possiblePlacements.append([x_cord+counter,y_cord+counter])
      except:
        pass

    if possiblePlacements == None:
      counter += 1
      print(counter, possiblePlacements)
    else:
      return(possiblePlacements)

def findEnemyPiece(df,player): #Here, we find ALL pieaces that our enemy has on the board
  pieaces = []
  for x in range(len(df)):
    for y in range(len(df)):
      if player == 1:
        if df.iloc[x][y]==2:
          pieaces.append([x,y])
      if player ==2:
        if df.iloc[x][y]==1:
          pieaces.append([x,y])
  return(findNearby0(player,df,pieaces))

def get_move(player, board):
  df = pd.DataFrame(board)
  #print(df) <---Uncomment this to view the board in python Terminal
  if player ==1:
    move = findEnemyPiece(df,1) #Find all possible moves, starting at the enemy piece
    return bestMove(player,move) # find the BEST move given the pieces
  else: 
    move = findEnemyPiece(df,2)
    return bestMove(player,move)

def prepare_response(move):
  response = '{}\n'.format(move).encode()
  print('sending {!r}'.format(response))
  return response

if __name__ == "__main__":
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.connect((host, port))
    while True:
      data = sock.recv(1024)
      if not data:
        print('connection to server closed')
        break
      json_data = json.loads(str(data.decode('UTF-8')))
      board = json_data['board']
      maxTurnTime = json_data['maxTurnTime']
      player = json_data['player']
      #print(player, maxTurnTime, board)

      move = get_move(player, board)
      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close()
