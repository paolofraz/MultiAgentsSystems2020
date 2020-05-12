import numpy as np

class Agents():

	def __init__(self):
		self.count = 4
		self.t = 0


	''' Proposing the following rule-based system: Seeking agents allocate between eachother targets to pursue based 
	on distances to targets, and move towards them(because the agents are given the other agents' positions anyway). The hiders move away from the seekers in some 
	weighted manner.'''

	'''
	Ideas: 

		- keep a moving average of agent velocities/positions to check if we have hit a wall

		- compute hiders actions based on wanting to get out of the line of sight of agents who see them, 
		also try to avoid getting stuck in walls if agent is seen

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
			
			if team:
				#This should be the case where the agent is a hider...
				pass
			else:
				#...And this one a seeker
				pass
		action = {'action_movement': action_movement, 'action_pull': action_pull, 'action_glueall': action_glueall}
		return action

	def clear_memory(self):
		self.t = 0
