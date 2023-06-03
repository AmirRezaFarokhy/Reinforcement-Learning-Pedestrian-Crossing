import numpy as np 
import cv2
import time 

SIZE = 10
LINE_MAIN = 50 // 600
UPPER_LINE = 350 // 600
DOWNER_LINE = 350 // 600
START_POSITION_PLAYER = [[0, 0], [LINE_MAIN, LINE_MAIN]]
TARGET_POSITION = [[0, 6], [0, 6]]

class CreateGameWalkingStreet:

	def __init__(self):
		self.colors = {'background':(0, 0, 0), 
					'player':(0, 0, 0), 
					'corner':(255, 255, 255),
					'endgame':(255, 0, 0),
					'text':(0, 0, 153)}

		self.world_size = (10, 10, 3)
		img = self.ImportantParametr(START_POSITION_PLAYER, TARGET_POSITION)


	def ImportantParametr(self, position_player, target_position):
		img = cv2.imread('pedestrian.png')
		img = cv2.resize(img, (SIZE, SIZE))

		cv2.rectangle(img,
					(position_player[0]), 
					(position_player[1]), 
					self.colors['player'], -1)

		cv2.rectangle(img, 
					(target_position[0]),
					(target_position[1]),
					self.colors['endgame'], -1)

		lines_lst = [[(1, 0), (1, 5)], [(8, 0), (8, 5)], 
					[(1, 8), (1, 10)], [(8, 8), (8, 10)],
					[(1, 8), (8, 8)], [(1, 5), (8, 5)],
					[(6, 5), (6, 8)], [(4, 5), (4, 8)],
					[(2, 5), (2, 8)], [(8, 5), (8, 8)]]

		for line in lines_lst:
			cv2.line(img, line[0], line[1], self.colors['corner'])
		
		return img, position_player


	def ConditionRight(self, position):
		if 8>=position[0][1]>=5 and position[1][0]!=10:
			return True
		else:
			return False

	def ConditionLeft(self, position):
		if position[0][0]<=0:
			return False
		elif position[0][0]==9:
			return False 
		else:
			return True

	def ConditionUp(self, position):
		if position[0][1]<=0:
			return False
		elif 8>=position[0][1]>=5 and position[0][0]>=1 and position[1][0]!=9:
			return False
		else:
			return True

	def ConditionDown(self, position):
		if position[1][1]>=9:
			return False
		elif 8>=position[0][1]>=5 and position[0][0]>=1 and position[1][0]!=9:
			return False
		else:
			return True

	def DangerousPlace(self, position):
		if 8>=position[0][0]>=2 and 4>=position[0][1]>=0:
			return False 
		else:
			return True

	def Actions(self, k, position):
		move_player = 1
		if k==0: # Right
			position[0][0] += move_player
			position[1][0] += move_player
			return position, 'Right'
		
		elif k==1: # Left
			position[0][0] -= move_player
			position[1][0] -= move_player
			return position, 'Left'

		elif k==2: # Up
			position[0][1] -= move_player
			position[1][1] -= move_player
			return position, 'Up'

		elif k==3: # Down
			position[0][1] += move_player
			position[1][1] += move_player
			return position, 'Down'





	# def ConditionRight(self, position):
	#     if 400>=position[0][1]>=350 and 450>=position[1][1]>=400 and position[1][0]!=800:
	#         return True
	#     else:
	#         return False

	# def ConditionLeft(self, position):
	#     if position[0][0]<=0:
	#         return False 
	#     else:
	#         return True

	# def ConditionUp(self, position):
	#     if position[0][0]>=50:
	#         return False 
	#     elif position[0][1]==0:
	#         return False
	#     else:
	#         return True

	# def ConditionDown(self, position):
	#     if position[1][0]>=100:
	#         return False
	#     elif position[1][1]==600:
	#         return False
	#     else:
	#         return True


#     def PlayGame(self):
#         run = True
#         move_player = 50
#         prev_button_direction = 1
#         position_player = [[0, 0], [50, 50]]
#         button_direction = 1
#         while run:
#             img = self.ImportantParametr(position_player)
#             cv2.imshow('a', img)
#             cv2.waitKey(1)
#             t_end = time.time() + 0.2
#             k = -1
#             while time.time()<t_end:
#                 if k==-1:
#                     k = cv2.waitKey(125)
#                 else:
#                     continue

			# if k==self.actions['Rigth'] and self.ConditionRight(position_player):
			#     position_player[0][0] += move_player
			#     position_player[1][0] += move_player
			
			# elif k==self.actions['Left'] and self.ConditionLeft(position_player):
			#     position_player[0][0] -= move_player
			#     position_player[1][0] -= move_player

			# elif k==self.actions['Up'] and self.ConditionUp(position_player):
			#     position_player[0][1] -= move_player
			#     position_player[1][1] -= move_player

			# elif k==self.actions["Down"] and self.ConditionDown(position_player):
			#     position_player[0][1] += move_player
			#     position_player[1][1] += move_player

			# elif k==self.actions['break']:
			#     run = False

#             print(position_player)


# game = CreateGameWalkingStreet()
# game.PlayGame()
# cv2.destroyAllWindows()


