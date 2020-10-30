
'''
    A class for a simple Sonic agent that runs to right and jumps every now and then.
'''
class runRightJumpSometimesAgent:
    def __init__(self, jumpInterval=500, airTime=20):
        self.iteration = 0
        self.jump = False
        self.airTime = airTime
        self.jumpInterval = jumpInterval
    
    '''
        Returns an array of bits - Each bit represents a button on the Genesis controller
        A 1 indicates the button being pressed.
    '''
    def getAction(self):
        if self.jump:
            action = [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
        else:
            action = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        self._iterate()
        return action
    
    def _iterate(self):
        self.iteration += 1
        self.jump = True if self.iteration % self.jumpInterval < self.airTime else False