import numpy as np

class Agents():

	def __init__(self):
		self.count = 4
		self.n_hiders = 2
		self.n_seekers = self.count - self.n_hiders
		
		self.t = 0


	''' Proposing the following rule-based system: Seeking agents allocate between eachother targets to pursue based 
	on distances to targets, and move towards them(because the agents are given the other agents' positions anyway). The hiders move away from the seekers in some 
	weighted manner.'''

	'''
	Ideas: 

		- keep a moving average of agent velocities/positions to check if we have hit a wall

		- compute hiders actions based on wanting to get out of the line of sight of agents who see them, 
		also try to avoid getting stuck in walls if agent is seen

		- team co-operation: teammates sharing information

		- try to detect doors based on lidar input: A door would be implied by having a spot with a longer lidar distance between two spots with a shorter distance

	'''

	
	def act(self, ob):
		action_movement = np.random.randint(0, 10, (self.count, 3))
		action_pull = np.random.randint(0, 1, 4)
		action_glueall = np.random.randint(0, 1, 4)
		for i in range(self.count):
			ob_self = ob['observation_self'][i, :]

			x = ob_self[0]
			y = ob_self[1]
			
			#This one contains mask bits to cover hidden agents from eachother, so True should imply that agent i sees agent j
			aa_mask = ob['mask_aa_obs'][i, :]

			#This one contains all the information about other agents, but it's masked if the agents are hidden
			agent_qpos_qvel = ob['agent_qpos_qvel'][i, :, :]

			
			#check the team of the agent
			team = ob_self[8]

			idx = np.where(aa_mask)[0]

			for i_ in idx:
				#Iterate over agents that agent can see and do something with that information
				agent_info = agent_qpos_qvel[i_, :]
				x_ = agent_info[0]
				y_ = agent_info[1]

				#These might be the velocity parameters, let's see...
				v_x = agent_info[2]
				v_y = agent_info[3]

				team_ = agent_info[8]

				if team:
					#This should be the case where the agent is a hider...
					if not team_:
						action_movement[i, :] = np.array([min(10, max(int(x-v_x*2), 0)), min(10, max(int(y-v_y*2), 0)), 0])
				else:
					#...And this one a seeker
					if team_:
						action_movement[i, :] = np.array([int(x_), int(y_), 0])

			
			
		action = {'action_movement': action_movement, 'action_pull': action_pull, 'action_glueall': action_glueall}
		return action

	def clear_memory(self):
		self.t = 0
