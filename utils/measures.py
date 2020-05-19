import numpy as np


class Measure():

	def __init__(self):
		self.objects_moved = 0
		self.object_positions = None

		self.hiders_movement = 0.0
		self.seekers_movement = 0.0

		self.hiders_positions = None
		self.seekers_positions = None


	def check_objects(self, ob):
			
			box_positions = ob['box_obs'][0, :, 0:2]
			ramp_positions = ob['ramp_obs'][0, :, 0:2]
	
			curr_pos = np.concatenate((box_positions, ramp_positions), axis=0)

			if self.object_positions is None:
				self.object_positions = curr_pos
			else:
				diff = self.object_positions - curr_pos
				self.objects_moved += np.sum((np.sum(diff, axis=1) != 0))
				self.object_positions = curr_pos

	def check_agents(self, ob):
		
		agent_pos = ob['observation_self'][:, 0:2]
		agent_teams = ob['observation_self'][:, 8].reshape((agent_pos.shape[0], 1))

		curr_hiders = agent_pos[np.concatenate((agent_teams > 0, agent_teams > 0), axis=1)].reshape((np.sum(agent_teams > 0), agent_pos.shape[1]))
		curr_seekers = agent_pos[np.concatenate((agent_teams == 0, agent_teams == 0), axis=1)].reshape((np.sum(agent_teams == 0), agent_pos.shape[1]))

		if self.hiders_positions is None or self.seekers_positions is None:
			self.hiders_positions = curr_hiders
			self.seekers_positions = curr_seekers
		else:
			self.hiders_movement += np.linalg.norm(curr_hiders - self.hiders_positions, axis = 1).sum()
			self.seekers_movement += np.linalg.norm(curr_seekers - self.seekers_positions, axis = 1).sum()

			self.hiders_positions = curr_hiders
			self.seekers_positions = curr_seekers
