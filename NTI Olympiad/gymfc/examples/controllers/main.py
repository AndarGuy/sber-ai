import argparse
import os

import gym


def main(env_id, seed):
    env = gym.make(env_id)
    title = "PID Step Response in Environment {}".format(env_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Evaluate a PID controller")
    parser.add_argument('--env-id', help="The Gym environement ID", type=str,
                        default="AttFC_GyroErr-MotorVel_M4_Ep-v0")
    parser.add_argument('--seed', help='RNG seed', type=int, default=17)

    args = parser.parse_args()
    current_dir = os.path.dirname(__file__)
    config_path = os.path.join(current_dir,
                               "../configs/iris.config")
    print("Loading config from ", config_path)
    os.environ["GYMFC_CONFIG"] = config_path

    main(args.env_id, args.seed)
