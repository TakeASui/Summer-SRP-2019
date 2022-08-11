from gym.envs.registration import register

register(
    id='nim-v0',
    entry_point='gym_foo.envs:NimEnv',
)
register(
    id='nimWCash-v0',
    entry_point='gym_foo.envs:NimWCashEnv',
)
