from ompl import base as ob
from ompl import geometric as og
import matplotlib.pyplot as plt

from env import Env

step_size = 0.1  # Step size for the RRT* algorithm
goal_bias = 0.05  # Probability of selecting the goal state during sampling
rewire_factor = 1.0  # Factor for re-wiring the tree during the RRT* algorithm
solver_time_limit = 10.0  # Time limit for the solver in seconds

def main():
    # Create the environment
    env = Env()

    # Create the state space
    space = ob.RealVectorStateSpace(2)

    # Set the bounds of the state space
    bounds = ob.RealVectorBounds(2)
    bounds.setLow(0, env.x_range[0])
    bounds.setHigh(0, env.x_range[1])
    bounds.setLow(1, env.y_range[0])
    bounds.setHigh(1, env.y_range[1])
    space.setBounds(bounds)

    # Create a simple setup
    ss = og.SimpleSetup(space)

    # Set the state validity checker
    ss.setStateValidityChecker(ob.StateValidityCheckerFn(lambda state: not env.is_collision(state[0], state[1])))

    # Get the space information
    si = ss.getSpaceInformation()
    si.setStateValidityCheckingResolution(0.01)

    # Set the planner
    planner = og.RRTstar(si)
    planner.setRange(step_size)
    planner.setGoalBias(goal_bias)
    planner.setRewireFactor(rewire_factor)

    # space.setStateSamplerAllocator(
    #     ob.StateSamplerAllocator(lambda space: DMPGuidedSampler(space, si, y_reproduce))
    # )

    ss.setPlanner(planner)

    # Set the start and goal states
    start_state = ob.State(space)
    goal_state = ob.State(space)
    start_state[0], start_state[1] = 3, 3
    goal_state[0], goal_state[1] = 14, 9

    ss.setStartAndGoalStates(start_state, goal_state)

    # Solve the problem
    solved = ss.solve(solver_time_limit)


if __name__ == "__main__":
    main()