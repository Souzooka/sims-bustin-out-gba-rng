from enum import Flag, IntEnum

# Some funky constants
class Input(Flag, IntEnum):
    A = 1
    B = 2
    Select = 4
    Start = 8
    Right = 16
    Left = 32
    Up = 64
    Down = 128
    RShoulder = 256
    LShoulder = 516

# Used for initializing rand, can be w/e
frames_since_boot = 0xA04
input_bitset = Input.A

class SimsMtRand():
    UPPER_MASK = 0x80000000
    LOWER_MASK = 0x7FFFFFFF
    TEMPERING_MASK_B = 0x9D2C5680
    TEMPERING_MASK_C = 0xEFC60000
    STATE_VECTOR_LENGTH = 624
    STATE_VECTOR_M = 397
    mag = [0x0, 0x9908B0DF]

    def __init__(self, frames, input):
        self.stateVector = [0] * self.STATE_VECTOR_LENGTH
        self.index1 = 0
        self.index2 = 0
        self.timesSeeded = 0
        self.seed = 0
        self.seedRand(frames, input)

    def seedRand(self, frames, input):
        self.index1 = -1
        self.index2 = -1
        
        self.seed = (frames * 16) + (input * 4)

        if self.seed == 0:
            # theoretically should never happen
            self.seed = (self.rand() % 0xFFF1F) + 1

        self.timesSeeded += 1
        self.seed = ((self.seed << 8) + (frames << 6) + (self.timesSeeded << 4)) | input
        self.m_seedRand(self.seed)

    def m_seedRand(self, seed):
        self.index1 = 0
        self.stateVector[0] = seed | 1
        for i in range(1, self.STATE_VECTOR_LENGTH):
            self.stateVector[i] = (self.stateVector[i-1] * 69069) & 0xFFFFFFFF

    # Not sure when/if the game calls this
    def setRandSeed(seed):
        self.seed = seed
        self.m_seedRand(seed)
        self.index1 = self.STATE_VECTOR_LENGTH - 1

    def rand(self):
        return self.rand1()

    def rand1(self):
        self.index1 -= 1
        if self.index1 < 0:
            self.m_seedRand(self.seed)

            for i in range(0, self.STATE_VECTOR_LENGTH - self.STATE_VECTOR_M):
                y = (self.stateVector[i] & self.UPPER_MASK) | (self.stateVector[i+1] & self.LOWER_MASK)
                self.stateVector[i] = self.stateVector[i+self.STATE_VECTOR_M] ^ (y >> 1) ^ self.mag[y & 0x1]
            
            for i in range(self.STATE_VECTOR_LENGTH - self.STATE_VECTOR_M, self.STATE_VECTOR_LENGTH - 1):
                y = (self.stateVector[i] & self.UPPER_MASK) | (self.stateVector[i+1] & self.LOWER_MASK)
                self.stateVector[i] = self.stateVector[i+(self.STATE_VECTOR_M-self.STATE_VECTOR_LENGTH)] ^ (y >> 1) ^ self.mag[y & 0x1]
            
            y = (self.stateVector[-1] & self.UPPER_MASK) | (self.stateVector[0] & self.LOWER_MASK)
            self.stateVector[-1] = self.stateVector[self.STATE_VECTOR_M-1] ^ (y >> 1) ^ self.mag[y & 0x1]

            self.index1 = self.STATE_VECTOR_LENGTH - 2
        
        y = self.stateVector[-(self.index1 + 1)]
        y ^= (y >> 11)
        y ^= (y << 7) & self.TEMPERING_MASK_B
        y ^= (y << 15) & self.TEMPERING_MASK_C
        y ^= (y >> 18)
        return y & 0xFFFFFFFF

    def rand2(self):
        self.index2 -= 1
        if self.index2 < 0:
            self.index2 = self.STATE_VECTOR_LENGTH - 2
        
        y = self.stateVector[-(self.index2 + 1)]
        y ^= (y >> 11)
        y ^= (y << 7) & self.TEMPERING_MASK_B
        y ^= (y << 15) & self.TEMPERING_MASK_C
        y ^= (y >> 18)
        return y & 0xFFFFFFFF

    def percentage1(self, percentage):
        return self.percentage(percentage, 0)
    def percentage2(self, percentage):
        return self.percentage(percentage, 1)

    def percentage(self, percentage, genIndex=0):
        gen = [self.rand1, self.rand2][genIndex]
        y = gen() & 0x7FFF
        y = (y * 101) >> 15
        return y < percentage

    def randmax(self, max):
        return self.randrange(max, 0)
    def randmax(self, max):
        return self.randrange(max, 1)

    def randmax(self, max, genIndex=0):
        gen = [self.rand1, self.rand2][genIndex]
        y = gen() & 0x7FFF
        max += 1
        y *= max
        return (y << 1) >> 16

    def randincrange1(self, min, max):
        return self.randincrange(min, max, 0)
    def randincrange2(self, min, max):
        return self.randincrange(min, max, 1)

    def randincrange(self, min, max, genIndex=0):
        gen = [self.rand1, self.rand2][genIndex]
        y = gen() & 0x7FFF
        max = max - min + 1
        y *= max
        y >>= 15
        return y + min


rng = SimsMtRand(frames_since_boot, input_bitset)
for i in range(20):
    print(rng.percentage1(40))