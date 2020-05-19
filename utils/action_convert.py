
def action_to_1d(action):
	return 121*action[0] + 11*action[1] + action[2]

def one_d_to_action(action):
	return action // 121, (action % 121)//11, action % 11
