import random
import math

import game
from agents import Agent


# Example agent, behaves randomly.
# ONLY StudentAgent and his descendants have a 0 id. ONLY one agent of this type must be present in a game.
# Agents from bots.py have successive ids in a range from 1 to number_of_bots.


class StudentAgent(Agent):
    def __init__(self, position, file_name):
        super().__init__(position, file_name)
        self.id = 0

    @staticmethod
    def kind():
        return '0'

    # Student shall override this method in derived classes.
    # This method should return one of the legal actions (from the Actions class) for the current state.
    # state - represents a state object.
    # max_levels - maximum depth in a tree search. If max_levels eq -1 than the tree search depth is unlimited.
    def get_next_action(self, state, max_levels):
        actions = self.get_legal_actions(state)  # equivalent of state.get_legal_actions(self.id)
        chosen_action = actions[random.randint(0, len(actions) - 1)]
        # Example of a new_state creation (for a chosen_action of a self.id agent):
        # new_state = state.apply_action(self.id, chosen_action)
        return chosen_action


class MinimaxAgent(StudentAgent):

    def minimax(self, state, max_levels, player, previous_action):

        id_leg = self.id
        if self.id != 0:
            id_leg = 1
        playerMax = id_leg
        playerMin = 1 - id_leg


        my_actions = self.get_legal_actions(state)
        opponents_actions = self.get_legal_actions_opponent(state, 1-id_leg)

        if player == playerMax:
            if len(my_actions) == 0 or (max_levels == 0 and len(my_actions) <= len(opponents_actions)):
                return -(len(opponents_actions) - len(my_actions)), previous_action
            elif max_levels == 0 and len(my_actions) >= len(opponents_actions):
                return (len(my_actions) - len(opponents_actions)), previous_action
        if player == playerMin:
            if len(opponents_actions) == 0 or (max_levels == 0 and len(my_actions) >= len(opponents_actions)):
                return (len(my_actions) - len(opponents_actions)), previous_action
            elif max_levels == 0 and len(my_actions) <= len(opponents_actions):  #
                return -(len(opponents_actions) - len(my_actions)), previous_action

        if player == playerMax:
            actions = my_actions
        elif player == playerMin:
            actions = opponents_actions

        if player == playerMax:
            score = -math.inf
            best_action = None
            for action in actions:
                new_state = state.apply_action(player, action)
                new_score, _ = self.minimax(new_state, max_levels - 1, playerMin,
                                            action)
                if new_score > score or best_action is None:
                    best_action = action
                    score = new_score

            return score, best_action

        if player == playerMin:
            score = +math.inf
            best_action = None
            for action in actions:
                new_state = state.apply_action(player, action)

                new_score, _ = self.minimax(new_state, max_levels - 1, playerMax,
                                            action)
                if new_score < score or best_action is None:
                    best_action = action
                    score = new_score

            return score, best_action

    def get_next_action(self, state, max_levels):
        id_leg = self.id
        if self.id != 0:
            id_leg = 1
        actions = state.get_legal_actions(id_leg)
        isAll = True
        maxScore = None
        maxAction = None

        for action in actions:
            new_state = state.apply_action(id_leg, action)
            score, _ = self.minimax(new_state, max_levels, 1 - id_leg, None)
            if maxScore is None or score > maxScore:
                maxScore = score
                maxAction = action
            if score != -1:
                isAll = False

        if not isAll:
            return maxAction
        else:
            if "NORTH" in actions:
                return "NORTH"
            elif "NE" in actions:
                return "NE"
            elif "EAST" in actions:
                return "EAST"
            elif "SE" in actions:
                return "SE"
            elif "SOUTH" in actions:
                return "SOUTH"
            elif "SW" in actions:
                return "SW"
            elif "WEST" in actions:
                return "WEST"
            elif "NW " in actions:
                return "NW "


class MinimaxABAgent(StudentAgent):

    def minimax_alpha_beta(self, state, max_levels, player, previous_action, alpha, beta):

        id_leg = self.id
        if self.id != 0:
            id_leg = 1
        playerMax= id_leg
        playerMin= 1-id_leg

        my_actions = self.get_legal_actions(state)
        opponents_actions = self.get_legal_actions_opponent(state, 1-id_leg)


        if player == playerMax:
            if len(my_actions) == 0 or (max_levels == 0 and len(my_actions) <= len(opponents_actions)):
                return -(len(opponents_actions) - len(my_actions)), previous_action
            elif max_levels == 0 and len(my_actions) >= len(opponents_actions):
                return (len(my_actions) - len(opponents_actions)), previous_action
        if player == playerMin:
            if len(opponents_actions) == 0 or (max_levels == 0 and len(my_actions) >= len(opponents_actions)):
                return (len(my_actions) - len(opponents_actions)), previous_action
            elif max_levels == 0 and len(my_actions) <= len(opponents_actions):
                return -(len(opponents_actions) - len(my_actions)), previous_action


        if player == playerMax:
            actions = my_actions
        elif player == playerMin:
            actions = opponents_actions

        if player == playerMax:
            score = -math.inf
            best_action = None
            for action in actions:
                new_state = state.apply_action(player, action)
                new_score, _ = self.minimax_alpha_beta(new_state, max_levels - 1, playerMin,
                                                       action, alpha, beta)
                if new_score > score or best_action is None:
                    best_action = action
                    score = new_score

                alpha = max(alpha, score)
                if alpha >= beta:
                    break

            return score, best_action

        if player == playerMin:
            score = +math.inf
            best_action = None

            for action in actions:

                new_state = state.apply_action(player, action)
                new_score, _ = self.minimax_alpha_beta(new_state, max_levels - 1, playerMax,
                                                       action, alpha, beta)
                if new_score < score or best_action is None:
                    best_action = action
                    score = new_score

                beta = min(beta, score)
                if alpha >= beta:
                    break

            return score, best_action

    def get_next_action(self, state, max_levels):
        id_leg = self.id
        if self.id != 0:
            id_leg = 1
        actions = state.get_legal_actions(id_leg)
        isAll = True
        maxScore = None
        maxAction = None

        for action in actions:
            new_state = state.apply_action(id_leg, action)
            score, _ = self.minimax_alpha_beta(new_state, max_levels-1, 1-id_leg, None, -math.inf, math.inf)
            if maxScore is None or score > maxScore:
                maxScore = score
                maxAction = action
            if score != -1:
                isAll = False

        if not isAll:
            return maxAction
        else:
            if "NORTH" in actions:
                return "NORTH"
            elif "NE" in actions:
                return "NE"
            elif "EAST" in actions:
                return "EAST"
            elif "SE" in actions:
                return "SE"
            elif "SOUTH" in actions:
                return "SOUTH"
            elif "SW" in actions:
                return "SW"
            elif "WEST" in actions:
                return "WEST"
            elif "NW " in actions:
                return "NW "

    # return action


class ExpectAgent(StudentAgent):
    playerMax = 0
    chance = 1

    def expectimax(self, state, max_levels, player, previous_action):

        my_actions = self.get_legal_actions(state)
        opponents_actions = self.get_legal_actions_opponent(state)

        if player == self.playerMax:
            if len(my_actions) == 0:
                return -1, None

        if player == self.chance:
            if len(opponents_actions) == 0:
                return 1, None

        if max_levels == 0:
            # ret_score = math.inf if player == self.playerMin else -math.inf
            ret_score = -math.inf
            return ret_score, previous_action

        if player == self.playerMax:
            actions = my_actions

        elif player == self.chance:
            actions = opponents_actions

        if player == self.playerMax:
            score = -math.inf
            best_action = None
            for action in actions:
                new_state = state.apply_action(self.id, action)
                new_score, _ = self.expectimax(new_state, max_levels - 1, self.chance,
                                               action)
                if new_score > score or best_action is None:
                    best_action = action
                    score = new_score

            return score, best_action

        if player == self.chance:
            score = 0
            prob = 1 / len(actions)
            for action in actions:
                new_state = state.apply_action(self.chance, action)
                new_score, _ = self.expectimax(new_state, max_levels - 1, self.playerMax,
                                               action)
                score += new_score * prob

            return score, None

    def get_next_action(self, state, max_levels):
        move, action = self.expectimax(state, max_levels, self.playerMax, None)
        return action


class MaxNAgent(StudentAgent):

    def maxNAgent(self, state, max_levels, player, previous_action):

        actions = state.get_legal_actions(player)

        if len(actions) == 0:
            state.agents[player].active = False
        else:
            only_me_active = True
            for i in range(0, len(state.agents)):
                if i == player:
                    continue
                if state.agents[i].active:
                    only_me_active = False
                    break
            if only_me_active:
                return 1, previous_action

        if max_levels == 0:
            ret_score = -math.inf
            return ret_score, previous_action

        score = -math.inf
        best_action = None

        for action in actions:
            new_state = state.apply_action(player, action)
            for i in range((player + 1) % len(state.agents), len(state.agents)):
                if state.agents[i].active:
                    next_player = i
                    break
                if i == len(state.agents) - 1:
                    for i in range(0, player):
                        if state.agents[i].active:
                            next_player = i
                            break

            new_score, _ = self.maxNAgent(new_state, max_levels - 1, next_player, action)
            if new_score > score or best_action is None:
                best_action = action
                score = new_score

        return score, best_action

    def get_next_action(self, state, max_levels):
        # agent_index = state.agents.index(self)

        agent_index = 0

        for i in range(0, len(state.agents)):
            if state.agents[i].id == self.id:
                agent_index = i
                break

        move, action = self.maxNAgent(state, max_levels, agent_index, None)
        return action
