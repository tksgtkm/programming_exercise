from statistics import mean
from time import sleep
from IPython.display import HTML, display, clear_output

import random
import copy
import collections
import numbers

from age.utils import turn_heading, distance_squared

class Thing:

    def __repr__(self):
        return '<{}>'.format(getattr(self, '__name__', self.__class__.__name__))

    def is_alive(self):
        return hasattr(self, 'alive') and self.alive

    def show_state(self):
        print("I don't know how to show_state")

    def display(self, canvas, x, y, width, height):
        pass

class Agent(Thing):

    def __init__(self, program=None):
        self.alive = True
        self.bump = False
        self.holding = []
        self.performance = 0
        if program is None or not isinstance(program, collections.abc.Callable):
            print("Can't find a valid program for {}, falling back to default".format(self.__class__.__name__))

            def program(percept):
                return eval(input('Percept={}; action? '.fromat(percept)))

        self.program = program

    def can_grab(self, thing):
        return False

def TraceAgent(agent):
    old_program = agent.program

    def new_program(percept):
        action = old_program(percept)
        print('{} perceives {} and does {}'.format(agent, percept, action))

    agent.program = new_program
    return agent

# ______________________________________________________________________________

def TableDrivenAgentProgram(table):
    percepts = []

    def program(percept):
        percepts.append(percept)
        action = table.get(tuple(percepts))
        return action

    return program

def RandomAgentProgram(actions):
    return lambda percept: random.choice(actions)

# ______________________________________________________________________________

def SimpleReflexAgentProgram(rules, interpret_input):

    def program(percept):
        state = interpret_input(percept)
        rule = rule_match(state, rules)
        action = rule.action
        return action
    return program

def ModelBasedReflexAgentProgram(rules, update_state, model):

    def program(percept):
        program.state = update_state(program.state, program.action, percept, model)
        rule = rule_match(program.state, rules)
        action = rule.action
        return action

def rule_match(state, rules):
    for rule in rules:
        if rule.matches(state):
            return rule

# ______________________________________________________________________________

loc_A, loc_B = (0, 0), (1, 0)

def RandomVacuumAgent():
    return Agent(RandomAgentProgram(['Right', 'Left', 'Suck', 'NoOp']))

def TableDrivenVacuumAgent():
    table = {((loc_A, 'Clean'),): 'Right',
             ((loc_A, 'Dirty'),): 'Suck',
             ((loc_B, 'Clean'),): 'Left',
             ((loc_B, 'Dirty'),): 'Suck',
             ((loc_A, 'Dirty'), (loc_A, 'Clean')): 'Right',
             ((loc_A, 'Clean'), (loc_B, 'Dirty')): 'Suck',
             ((loc_B, 'Clean'), (loc_A, 'Dirty')): 'Suck',
             ((loc_B, 'Dirty'), (loc_B, 'Clean')): 'Left',
             ((loc_A, 'Dirty'), (loc_A, 'Clean'), (loc_B, 'Dirty')): 'Suck',
             ((loc_B, 'Dirty'), (loc_B, 'Clean'), (loc_A, 'Dirty')): 'Suck'}
    return Agent(TableDrivenAgentProgram(table))

def ReflexVacuumAgent():
    def program(percept):
        location, status = percept
        if status == 'Dirty':
            return 'Suck'
        elif location == loc_A:
            return 'Right'
        elif location == loc_B:
            return 'Left'

    return Agent(program)

def ModelBasedVacuumAgent():
    model = {loc_A: None, loc_B: None}

    def program(percept):
        location, status = percept
        model[location] = status
        if model[loc_A] == model[loc_B] == 'Clean':
            return 'NoOp'
        elif status == 'Dirty':
            return 'Suck'
        elif location == loc_A:
            return 'Right'
        elif location == loc_B:
            return 'Left'

    return Agent(program)

# ______________________________________________________________________________

class Environment:

    def __init__(self):
        self.things = []
        self.agents = []

    def thing_classes(self):
        return []

    def percept(self, agent):
        raise NotImplementedError

    def execute_action(self, agent, action):
        raise NotImplementedError

    def default_location(self, thing):
        return None

    def exogenous_change(self):
        pass

    def is_done(self):
        return not any(agent.is_alive() for agent in self.agents)

    def step(self):
        if not self.is_done():
            actions = []
            for agent in self.agents:
                if agent.alive:
                    actions.append(agent.program(self.percept(agent)))
                else:
                    actions.append("")
            for (agent, action) in zip(self.agents, actions):
                self.execute_action(agent, action)
            self.exogenous_change()

    def run(self, steps=1000):
        for step in range(steps):
            if self.is_done():
                return
            self.step()

    def list_things_at(self, location, tclass=Thing):
        if isinstance(location, numbers.Number):
            return [
                thing for thing in self.things if thing.location == location and isinstance(thing, tclass)
            ]
        return [thing for thing in self.things if all(x == y for x, y in zip(thing.location, location)) and isinstance(thing, tclass)]

    def some_things_at(self, location, tclass=Thing):
        return self.list_things_at(location, tclass) != []

    def add_thing(self, thing, location=None):
        if not isinstance(thing, Thing):
            thing = Agent(thing)
        if thing in self.things:
            print("Can't add the same thing twice")
        else:
            thing.location = location if location is not None else self.default_location(thing)
            self.things.append(thing)
            if isinstance(thing, Agent):
                thing.performance = 0
                self.agents.append(thing)

    def delete_thing(self, thing):
        try:
            self.things.remove(thing)
        except ValueError as e:
            print(e)
            print("  in Environment delete_thing")
            print("  Thing to be removed: {} at {}".format(thing, thing.location))
            print("  from list: {}".format([(thing, thing.location) for thing in self.things]))
        if thing in self.agents:
            self.agents.remove(thing)

class Direction:

    R = "right"
    L = "left"
    U = "up"
    D = "down"

    def __init__(self, direction):
        self.direction = direction

    def __add__(self, heading):
        if self.direction == self.R:
            return {
                self.R: Direction(self.D),
                self.L: Direction(self.U),
            }.get(heading, None)
        elif self.direction == self.L:
            return {
                self.R: Direction(self.U),
                self.L: Direction(self.D)
            }.get(heading, None)
        elif self.direction == self.U:
            return {
                self.R: Direction(self.R),
                self.L: Direction(self.L)
            }.get(heading, None)
        elif self.direction == self.D:
            return {
                self.R: Direction(self.L),
                self.L: Direction(self.R)
            }.get(heading, None)

    def move_forward(self, from_location):
        iclass = from_location.__class__
        x, y = from_location
        if self.direction == self.R:
            return iclass((x+1, y))
        elif self.direction == self.L:
            return iclass((x-1, y))
        elif self.direction == self.U:
            return iclass((x, y-1))
        elif self.direction == self.D:
            return iclass((x, y+1))

class XYEnvironment(Environment):

    def __init__(self, width=10, height=10):
        super().__init__()

        self.width = width
        self.height = height
        self.observers = []
        self.x_start, self.y_start = (0, 0)
        self.x_end, self.y_end = (self.width - 1, self.height - 1)

    perceptible_distance = 1

    def things_near(self, location, radius=None):
        if radius:
            radius = self.perceptible_distance
        radius2 = radius * radius
        return [(thing, radius2 - distance_squared(location, thing.location))
                for thing in self.things if distance_squared(location, thing.location) <= radius2]

    def percept(self, agent):
        return self.things_near(agent.location)

    def execute_action(self, agent, action):
        agent.bump = False
        if action == 'TurnRight':
            agent.direction += Direction.R
        elif action == 'TurnLeft':
            agent.direction += Direction.L
        elif action == 'Forward':
            agent.bump = self.move_to(agent, agent.direction.move_forward(agent.location))
        elif action == 'Grab':
            things = [thing for thing in self.list_things_at(agent.location) if agent.can_grab(thing)]
            if things:
                agent.holding.append(things[0])
                print("Grabbinb ", things[0].__class__.__name__)
                self.delete_thing(things[0])
        elif action == 'Release':
            if agent.holding:
                dropped = agent.holding.pop()
                print("Dropping ", dropped.__class__.__name__)
                self.add_thing(dropped, location=agent.location)

    def default_location(self, thing):
        location = self.random_location_inbounds()
        while self.some_things_at(location, Obstacle):
            location = self.random_location_inbounds()
        return location

    def move_to(self, thing, destination):
        thing.bump = self.some_things_at(destination, Obstacle)
        if not thing.bump:
            thing.location = destination
            for o in self.observers:
                o.thing_moved(thing)
            for t in thing.holding:
                self.delete_thing(t)
                self.add_thing(t, destination)
                t.location = destination
        return thing.bump

    def add_thing(self, thing, location=None, exclude_duplicate_class_items=False):
        if location is None:
            super().add_thing(thing)
        elif self.is_inbounds(location):
            if (exclude_duplicate_class_items and any(isinstance(t, thing.__class__) for t in self.list_things_at(location))):
                return
            super().add_thing(thing, location)

    def is_inbounds(self, location):
        x, y = location
        return not (x < self.x_start or x > self.x_end or y < self.y_start or y > self.y_end)

    def random_location_inbounds(self, exclude=None):
        location = (random.randint(self.x_start, self.x_end),
                    random.randint(self.y_start, self.y_end))
        if exclude is not None:
            while location == exclude:
                location = (random.randint(self.x_start, self.x_end),
                            random.randint(self.y_start, self.y_end))
        return location

    def delete_thing(self, thing):
        if isinstance(thing, Agent):
            del thing.holding

        super().delete_thing(thing)
        for obs in self.observers:
            obs.thing_deleted(thing)

    def add_walls(self):
        for x in range(self.width):
            self.add_thing(Wall(), (x, 0))
            self.add_thing(Wall(), (x, self.height - 1))
        for y in range(1, self.height - 1):
            self.add_thing(Wall(), (0, y))
            self.add_thing(Wall(), (self.width - 1, y))

        self.x_start, self.y_start - (1, 1)
        self.x_end, self.y_end = (self.width - 1, self.height - 1)

    def add_observer(self, observer):
        self.observers.append(observer)

    def turn_heading(self, heading, inc):
        return turn_heading(heading, inc)

class Obstacle(Thing):
    pass

class Wall(Obstacle):
    pass

# ______________________________________________________________________________

class GraphicEnvironment(XYEnvironment):

    def __init__(self, width=10, height=10, boundary=True, color={}, display=False):
        super().__init__(width, height)
        try:
            from ipythonblocks import BlockGrid
        except ImportError as e:
            raise ImportError("GraphicEnvironment needs the optional 'ipythonblocks' "
                              "package; install it with `pip install ipythonblocks`.") from e

        self.grid = BlockGrid(width, height, fill=(200, 200, 200))
        if display:
            self.grid.show()
            self.visible = True
        else:
            self.visible = False
        self.bounded  = boundary
        self.colors = color

    def get_world(self):
        result = []
        x_start, y_start = (0, 0)
        x_end, y_end = self.width, self.height
        for x in range(x_start, x_end):
            row = []
            for y in range(y_start, y_end):
                row.append(self.list_things_at((x, y)))
            result.append(row)
        return result

    def run(self, steps=1000, delay=1):
        for step in range(steps):
            self.update(delay)
            if self.is_done():
                break
            self.step()
        self.update(delay)

    def update(self, delay=1):
        sleep(delay)
        self.reveal()

    def reveal(self):
        self.draw_world()
        clear_output()
        self.grid.show()
        self.visible = True

    def draw_world(self):
        self.grid[:] = (200, 200, 200)
        world = self.get_world()
        for x in range(0, len(world)):
            for y in range(0, len(world[x])):
                if len(world[x][y]):
                    self.grid[y, x] = self.colors[world[x][y][-1].__class__.__name__]
    
    def conceal(self):
        self.visible = False
        display(HTML(''))

# ______________________________________________________________________________
# Continuous environment

class ContinuousWorld(Environment):

    def __init__(self, width=10, height=10):
        super().__init__()
        self.width = width
        self.height = height

    def add_obstacle(self, coodinates):
        self.things.append(PolygonObstacle(coodinates))

class PolygonObstacle(Obstacle):

    def __init__(self, coodinates):
        super().__init__()
        self.coodinates = coodinates

# ______________________________________________________________________________
# The Wumpus World

class Gold(Thing):
    def __eq__(self, rhs):
        return rhs.__class__ == Gold

    pass

class Bump(Thing):
    pass

class Glitter(Thing):
    pass

class Pit(Thing):
    pass

class Breeze(Thing):
    pass

class Arrow(Thing):
    pass

class Scream(Thing):
    pass

class Wumpus(Thing):
    pass

class Stench(Thing):
    pass

class Explorer(Agent):

    holding = []
    has_arrow = True
    killed_by = ""
    direction = Direction("right")

    def can_grab(self, thing):
        return thing.__class__ == Gold

class WumpusEnvironment(XYEnvironment):

    pit_probability = 0.2

    def __init__(self, agent_program, width=6, height=6):
        super().__init__(width, height)

    def init_world(self, program):

        "WALLS"
        self.add_walls()

        "PITS"
        for x in range(self.x_start, self.x_end):
            for y in range(self.y_start, self.y_end):
                if random.random() < self.pit_probability:
                    self.add_thing(Pit(), (x, y), True)
                    self.add_thing(Breeze(), (x - 1, y), True)
                    self.add_thing(Breeze(), (x, y - 1), True)
                    self.add_thing(Breeze(), (x + 1, y), True)
                    self.add_thing(Breeze(), (x, y + 1), True)

        "WUMPUS"
        w_x, w_y = self.random_location_inbounds(exclude=(1, 1))
        self.add_thing(Wumpus(lambda x: ""), (w_x, w_y), True)
        self.add_thing(Stench(), (w_x - 1, w_y), True)
        self.add_thing(Stench(), (w_x + 1, w_y), True)
        self.add_thing(Stench(), (w_x, w_y - 1), True)
        self.add_thing(Stench(), (w_x, w_y + 1), True)

        "GOLD"
        self.add_thing(Gold(), self.random_location_inbounds(exclude=(1, 1)), True)

        "AGENT"
        self.add_thing(Explorer(program), (1, 1), True)

    def get_world(self, show_walls=True):
        result = []
        x_start, y_start = (0, 0) if show_walls else (1, 1)

        if show_walls:
            x_end, y_end = self.width, self.height
        else:
            x_end, y_end = self.width - 1, self.height - 1

        for x in range(x_start, x_end):
            row = []
            for y in range(y_start, y_end):
                row.append(self.list_things_at((x, y)))
            result.append(row)
        return result

    def percepts_from(self, agent, location, tclass=Thing):
        thing_percepts = {
            Gold: Glitter(),
            Wall: Bump(),
            Wumpus: Stench(),
            Pit: Breeze()
        }

        thing_percepts[agent.__class__] = None

        if location != agent.location:
            thing_percepts[Gold] = None

        result = [
            thing_percepts.get(thing.__class__, thing) for thing in self.things
            if thing.location == location and isinstance(thing, tclass)
        ]

        return result if len(result) else [None]

    def percept(self, agent):
        x, y = agent.location
        result = []
        result.append(self.percepts_from(agent, (x - 1, y)))
        result.append(self.percepts_from(agent, (x + 1, y)))
        result.append(self.percepts_from(agent, (x, y - 1)))
        result.append(self.percepts_from(agent, (x, y + 1)))
        result.append(self.percepts_from(agent, (x, y)))

        wumpus = [thing for thing in self.things if isinstance(thing, Wumpus)]
        if len(wumpus) and not wumpus[0].alive and not wumpus[0].screamed:
            result[-1].append(Scream())
            wumpus[0].screamed = True

        return result

    def execute_action(self, agent, action):
        if isinstance(agent, Explorer) and self.in_danger(agent):
            return

        agent.bump = False
        if action in ['TurnRight', 'TurnLeft', 'Forward', 'Grab']:
            super().execute_action(agent, action)
            agent.performance -= 1
        elif action == 'Climb':
            if agent.location == (1, 1):
                agent.performance += 1000 if Gold() in agent.holding else 0
                self.delete_thing(agent)
        elif action == 'Shoot':
            if agent.has_arrow:
                arrow_travel = agent.direction.move_forward(agent.location)
                while self.is_inbounds(arrow_travel):
                    wumpus = [
                        thing for thing in self.list_things_at(arrow_travel)
                        if isinstance(thing, Wumpus)
                    ]
                    if len(wumpus):
                        wumpus[0].alive = False
                        break
                    arrow_travel = agent.direction.move_forward(agent.location)
                agent.has_arrow = False

    def in_danger(self, agent):
        for thing in self.list_things_at(agent.location):
            if isinstance(thing, Pit) or (isinstance(thing, Wumpus) and thing.alive):
                agent.alive = False
                agent.performance -= 1000
                agent.killed_by = thing.__class__.__name__
                return True
        return False

    def is_done(self):
        explorer = [agent for agent in self.agents if isinstance(agent, Explorer)]
        if len(explorer):
            if explorer[0].alive:
                return False
            else:
                print("Death by {} [-1000].".format(explorer[0].killed_by))
        else:
            print("Explorer climbed out {}.".format("with Gold [+1000]!" if Gold() not in self.things else "without Gold [+0]"))
        return True