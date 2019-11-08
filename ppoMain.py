import gym
import matplotlib.pyplot as plt
from PPO import PPO
import numpy as np
import tensorflow as tf

tf.reset_default_graph()
env = gym.make('Pendulum-v0')
obs_space = env.observation_space.shape[0]
action_space = env.action_space.shape[0]

print("Observation Space: {}".format(obs_space))

def trainingLoop(model, episodes = 1000):
    
    done = False
    reward_history = []
    global_t = 0
    for i in range(episodes):
        epsReward = 0
        state_trajectory = []
        reward_trajectory = []
        obs = env.reset()
        obs = np.expand_dims(obs, axis = 0)
        t = 0
        
        while not done and t < 200:
            action = model.predictPolicy(obs)
            new_obs, reward, done, _ = env.step(action)
            new_obs = np.reshape(new_obs, (-1, obs_space))
            state_trajectory.append(obs)
            reward_trajectory.append(reward)
            obs = new_obs
            epsReward += reward
            t += 1
            global_t += 1
            #sample = model.return_sample(obs)  
            #print(sample)
        if done:
            reward_trajectory.append(100)
        policyParam = model.getParam()
        model.trainingStep(reward_trajectory, state_trajectory)
        reward_history.append(epsReward)
        done = False
    
        if i > 0:
            model.updateOldPolicy(policyParam) 
        if (i+1) % 50 == 0:
            print("Last Action: {}".format(action))
            print("Average of last 50 episodes: {}".format(np.mean(np.array(reward_history[-50:]))))
            print("Episode Reward on Episode {}: {}".format(i, epsReward))
            print("Global Time Step: {}".format(global_t)) 
    plt.plot(reward_history)
    
if __name__ == '__main__':
    
    if len(np.array(obs_space).shape) != 0:
        state_space = (None, *obs_space)
    else:
        state_space = (None, obs_space)

    model = PPO(state_space, action_space)
    
    trainingLoop(model)
