import cv2
import numpy as np
import imutils
import time
import pickle
from Envirenment import CreateGameWalkingStreet

SIZE = 10
HM_EPISODES = 6000
MOVE_PENALTY = 1
start_q_table = None #'qtable 1685833442.0569775.pickle' 
FOOD_REWARD = 25
CORNER_PENALTY = 100
DANGEROUS_PENALTY = 300
epsilon = 0.9
EPS_DECAY = 0.9998
SHOW_EVERY = 200
LEARNING_RATE = 0.1
DISCOUNT = 0.95
TARGET_POSITION = [[1, 6], [1, 6]]
LINE_MAIN = 50 // 600

colors = {'background':(0, 0, 0), 
		'player':(0, 0, 0), 
		'corner':(255, 255, 255),
		'endgame':(255, 0, 0),
		'text':(0, 0, 153)}


if start_q_table is None:
	q_table = {}
	for x1 in range(-SIZE+1, SIZE):
		for y1 in range(-SIZE+1, SIZE):
			for x2 in range(-SIZE+1, SIZE):
				for y2 in range(-SIZE+1, SIZE):
					q_table[((x1, y1),(x2, y2))] = [np.random.uniform(-5, 0) for i in range(4)]


else:
	with open(start_q_table, "rb") as f:
		q_table = pickle.load(f)


ep_rewards = []
start_position_player = [[0, 0], [LINE_MAIN, LINE_MAIN]]
for episode in range(HM_EPISODES):
	player = CreateGameWalkingStreet()
	if episode%SHOW_EVERY==0:
		show = True
	else:
		show = False
	ep_reward = 0
	for i in range(250):
		obs = [list(np.array(start_position_player)[0] - np.array(TARGET_POSITION)[0]), 
			   list(np.array(start_position_player)[1] - np.array(TARGET_POSITION)[1])]

		if np.random.random()>epsilon:
			action = np.argmax(q_table[tuple(obs[0]), tuple(obs[1])])
		else:
			action = np.random.randint(0, 4)

		start_position_player, val = player.Actions(action, start_position_player)

		if not player.ConditionRight(start_position_player) and val=='Right':
			start_position_player = [[0, 4], [LINE_MAIN, LINE_MAIN+4]]
		
		elif not player.ConditionLeft(start_position_player) and val=='Left':
			start_position_player = [[0, 4], [LINE_MAIN, LINE_MAIN+4]]

		elif not player.DangerousPlace(start_position_player) and val=='Right':
			start_position_player = [[0, 4], [LINE_MAIN, LINE_MAIN+4]]
		
		elif not player.ConditionDown(start_position_player) and val=='Down': 
			start_position_player = [[0, 4], [LINE_MAIN, LINE_MAIN+4]]

		elif not player.ConditionUp(start_position_player) and val=='Up':
			start_position_player = [[0, 4], [LINE_MAIN, LINE_MAIN+4]]



		if start_position_player[0]==TARGET_POSITION[0] and start_position_player[1]==TARGET_POSITION[1]:
			reward = FOOD_REWARD

		elif not player.ConditionRight(start_position_player) and val=='Right':
			reward = -CORNER_PENALTY

		elif not player.DangerousPlace(start_position_player) and val=='Right':
			reward = -DANGEROUS_PENALTY

		elif not player.ConditionLeft(start_position_player) and val=='Left':
			reward = -CORNER_PENALTY
		
		elif not player.ConditionDown(start_position_player) and val=='Down': 
			reward = -CORNER_PENALTY

		elif not player.ConditionUp(start_position_player) and val=='Up':
			reward = -CORNER_PENALTY

		else:
			reward = -MOVE_PENALTY

		new_obs = [list(np.array(start_position_player)[0] - np.array(TARGET_POSITION)[0]), 
			  	   list(np.array(start_position_player)[1] - np.array(TARGET_POSITION)[1])]

		max_future_q = np.max(q_table[tuple(new_obs[0]), tuple(new_obs[1])])

		current_q = q_table[tuple(obs[0]), tuple(obs[1])][action]

		if reward==FOOD_REWARD:
			new_q = FOOD_REWARD
		else:
			new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

		q_table[tuple(obs[0]), tuple(obs[1])][action] = new_q


		if show:
			env, start_position_player = player.ImportantParametr(start_position_player, TARGET_POSITION)
			img = imutils.resize(env, width=600, height=600)						
			if reward==FOOD_REWARD:
				if TARGET_POSITION[0][0]!=9:
					TARGET_POSITION[0][0] += 2
					TARGET_POSITION[1][0] += 2 
					print(TARGET_POSITION)

				cv2.putText(img=img, 
							text='AI Recieved!!!', 
							org=(200, 200), 
							fontFace=cv2.FONT_HERSHEY_TRIPLEX, 
							fontScale=1, 
							color=colors['text'], 
							thickness=1)

				cv2.imshow("RainForcement Learning", np.array(img))
				print("AI Recieved!!!")
				print(f"future q {max_future_q}")
				print(f'current q {current_q}')
				if cv2.waitKey(500) & 0xFF==ord("q"):
					break
			else:
				cv2.imshow("RainForcement Learning", np.array(img))
				if cv2.waitKey(1) & 0xFF==ord("q"):
					break


		ep_reward += reward
		if reward==FOOD_REWARD:
			break 

	ep_rewards.append(ep_reward)
	epsilon *= EPS_DECAY


with open(f"qtable {time.time()}.pickle", 'wb') as f:
	pickle.dump(q_table, f)


