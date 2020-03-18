from environment import *
import time


class MyAgent(BlocksWorldAgent):

    _plan = []

    def __init__(self, name: str, desired_state: BlocksWorld):
        super(MyAgent, self).__init__(name=name)

        self.desired_state = desired_state

    def response(self, perception: BlocksWorldPerception) -> BlocksWorldAction:
        # TODO: revise beliefs; if necessary, make a plan; return an action.
        # raise NotImplementedError("not implemented yet; todo by student")

        number_of_stacks = len(self.desired_state.get_stacks())
        completed_stacks = 0
        for desired_stack in self.desired_state.get_stacks():
            for stack in perception.visible_stacks:
                if desired_stack == stack:
                    completed_stacks += 1
        if completed_stacks == number_of_stacks:
            return AgentCompleted()

        if len(self.plan()) > 0:
            current_action = self.plan().pop()
            if current_action.get_type() == "stack":
                for stack in perception.visible_stacks:
                    if current_action.get_second_arg() == stack.get_top_block():
                        return current_action
                self.plan().append(current_action)
                return NoAction()
            elif current_action.get_type() == "pickup":
                for stack in perception.visible_stacks:
                    if current_action.get_argument() == stack.get_top_block():
                        return current_action
                self.plan().append(current_action)
                return NoAction()
            elif current_action.get_type() == "lock":
                # for stack in perception.visible_stacks:
                #     if current_action.get_argument() == stack.get_top_block():
                #         for visible_stack in perception.visible_stacks:
                #             if current_action.get_argument() in visible_stack.get_blocks():
                #
                #                 if visible_stack.get_below(current_action.get_argument())
                #         return current_action
                return NoAction()
            return current_action

        for stack in perception.visible_stacks: # if bottom bloc is on the table block it
            if stack.is_single_block():
                if self.desired_state.get_stack(stack.get_top_block()).get_bottom_block() == stack.get_top_block():
                    if not stack.is_locked(stack.get_top_block()):
                        return Lock(stack.get_top_block())

        for stack in perception.visible_stacks:
            if not stack.is_locked(stack.get_top_block()):
                stack_to_compare = self.desired_state.get_stack(stack.get_top_block())
                if stack.get_below(stack.get_top_block()) is None: #is on the table
                    if stack.get_top_block() == stack_to_compare.get_bottom_block():
                        return Lock(stack.get_top_block())
                    else: #block is on the table but is not a bottom block
                        block_to_stack = stack_to_compare.get_below(stack.get_top_block())
                        for stack1 in perception.visible_stacks:
                            if stack1.get_top_block() == block_to_stack and stack1.is_locked(block_to_stack):
                                self.plan().append(Lock(stack.get_top_block()))
                                self.plan().append(Stack(stack.get_top_block(), block_to_stack))
                                return PickUp(stack.get_top_block())

                elif stack.is_locked(stack.get_below(stack.get_top_block())):
                    try:
                        if stack_to_compare.is_on(stack.get_top_block(), stack.get_below(stack.get_top_block())):
                            return Lock(stack.get_top_block())
                        self.plan().append(PutDown(stack.get_top_block()))
                        return Unstack(stack.get_top_block(), stack.get_below(stack.get_top_block()))
                    except:
                        self.plan().append(PutDown(stack.get_top_block()))
                        return Unstack(stack.get_top_block(), stack.get_below(stack.get_top_block()))
                else:
                    self.plan().append(PutDown(stack.get_top_block()))
                    return Unstack(stack.get_top_block(), stack.get_below(stack.get_top_block()))

        return NoAction()

    def revise_beliefs(self, perceived_world_state: BlocksWorld):
        # TODO: check if what the agent knows corresponds to what the agent sees
        #raise NotImplementedError("not implemented yet; todo by student")
        pass


    def plan(self) -> List[BlocksWorldAction]:
        # TODO: return a new plan, as a sequence of `BlocksWorldAction' instances, based on the agent's knowledge.

        return self._plan


    def status_string(self):
        # TODO: return information about the agent's current state and current plan.
        return str(self) + " : PLAN MISSING"



class Tester(object):
    STEP_DELAY = 0.5
    TEST_SUITE = "tests/0e-large/"

    EXT = ".txt"
    SI  = "si"
    SF  = "sf"

    DYNAMICITY = .5

    AGENT_NAME = "*A"

    def __init__(self):
        self._environment = None
        self._agents = []

        self._initialize_environment(Tester.TEST_SUITE)
        self._initialize_agents(Tester.TEST_SUITE)



    def _initialize_environment(self, test_suite: str) -> None:
        filename = test_suite + Tester.SI + Tester.EXT

        with open(filename) as input_stream:
            self._environment = DynamicEnvironment(BlocksWorld(input_stream=input_stream))


    def _initialize_agents(self, test_suite: str) -> None:
        filename = test_suite + Tester.SF + Tester.EXT

        agent_states = {}

        with open(filename) as input_stream:
            desires = BlocksWorld(input_stream=input_stream)
            agent = MyAgent(Tester.AGENT_NAME, desires)

            agent_states[agent] = desires
            self._agents.append(agent)

            self._environment.add_agent(agent, desires, None)

            print("Agent %s desires:" % str(agent))
            print(str(desires))


    def make_steps(self):
        print("\n\n================================================= INITIAL STATE:")
        print(str(self._environment))
        print("\n\n=================================================")

        completed = False
        nr_steps = 0

        while not completed:
            completed = self._environment.step()

            time.sleep(Tester.STEP_DELAY)
            print(str(self._environment))

            for ag in self._agents:
                print(ag.status_string())

            nr_steps += 1

            print("\n\n================================================= STEP %i completed." % nr_steps)

        print("\n\n================================================= ALL STEPS COMPLETED")





if __name__ == "__main__":
    tester = Tester()
    tester.make_steps()
