from collections import namedtuple, deque
import random, torch, numpy as np

from .parameters import device

Experience = namedtuple("Experience", ("state", "action", "reward", "next_state", "done"))


class ReplayMemory:
    def __init__(self, capacity, batch_size):
        self.states = deque([], maxlen=capacity)
        self.actions = deque([], maxlen=capacity)
        self.rewards = deque([], maxlen=capacity)
        self.next_states = deque([], maxlen=capacity)
        self.dones = deque([], maxlen=capacity)
        self.size = 0
        self.capacity = capacity
        self.batch_size = batch_size

    def push(self, state, action, reward, next_state, done):
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)
        self.next_states.append(next_state)
        self.dones.append(done)
        self.size = min(self.size + 1, self.capacity)

    def sample(self):
        indices = random.sample(range(self.size), k=self.batch_size)
        exps = (self.states, self.actions, self.rewards, self.next_states)
        extract = lambda list_: [list_[i] for i in indices]
        states, actions, rewards, next_states = map(torch.cat, map(extract, exps))
        dones = torch.from_numpy(np.vstack(extract(self.dones)).astype(np.uint8))
        tofloat = lambda x: x.float().to(device)
        tolong = lambda x: x.long().to(device)
        return (
            tofloat(states),
            tolong(actions),
            tofloat(rewards),
            tofloat(next_states),
            tofloat(dones),
        )

    def __len__(self):
        return self.size