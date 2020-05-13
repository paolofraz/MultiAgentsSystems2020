import numpy as np

class Agents():

	def __init__(self):
		self.count = 4
		self.n_hiders = 2
		self.n_seekers = self.count - self.n_hiders
		self.t = 0
		self.alpha = 2
		self.objects_moved = 0
		self.object_positions = None


	''' Proposing the following rule-based system: Seeking agents allocate between eachother targets to pursue based 
	on distances to targets, and move towards them(because the agents are given the other agents' positions anyway). The hiders move away from the seekers in some 
	weighted manner.'''

	''' in actions, 5 means no motion, 0 is backwards and 10 is forward ''' 

	'''
	Ideas: 

		- keep a moving average of agent velocities/positions to check if we have hit a wall

		- compute hiders actions based on wanting to get out of the line of sight of agents who see them, 
		also try to avoid getting stuck in walls if agent is seen

		- team co-operation: teammates sharing information

		- try to detect doors based on lidar input: A door would be implied by having a spot with a longer lidar distance between two spots with a shorter distance

		- find  a point that's far away from seekers and go there

	'''

	def check_objects(self, ob):
		
		box_positions = ob['box_obs'][0, :, 0:2]
		ramp_positions = ob['ramp_obs'][0, :, 0:2]

		if self.object_positions is None:
			self.object_positions = np.concatenate((box_positions, ramp_positions), axis=0)
		else:
			diff = self.object_positions - np.concatenate((box_positions, ramp_positions), axis=0)
			self.objects_moved += np.sum((np.sum(diff, axis=1) != 0))
			self.object_positions = np.concatenate((box_positions, ramp_positions), axis=0)

	
	def act(self, ob): 
		action_movement = np.random.randint(0, 11, (self.count, 3))
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
						action_movement[i, :] = np.array([5 - int(v_x), 5 - int(v_y), 5])
						if np.all(action_movement[i, :] == 5):
							action_movement[i, :] = np.random.randint(0, 11, 3)
						
				else:
					#...And this one a seeker
					if team_:
						action_movement[i, :] = np.array([5 - int(x - x_), 5 - int(y - y_), 5])

			
			
		action = {'action_movement': action_movement, 'action_pull': action_pull, 'action_glueall': action_glueall}
		return action

	def clear_memory(self):
		self.t = 0
