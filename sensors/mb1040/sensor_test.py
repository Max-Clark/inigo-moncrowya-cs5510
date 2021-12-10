import pigpio
import time

class PwmMeasure:
    def __init__(self, pi, gpio, weighting=0.0):
        self.pi = pi
        self.gpio = gpio
        
        if not (weighting >= 0.0 and weighting <= 1.0):
            weighting = 0.0
        
        self._new = 1.0-weighting
        self._old = weighting
        
        self._high_tick = None
        self._period = None
        self._high = None
        
        pi.set_mode(gpio, pigpio.INPUT)
        
        self._cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cbf)
    
    def _cbf(self, gpio, level, tick):
        if level == 1:
            if not self._high_tick is None:
                t = pigpio.tickDiff(self._high_tick, tick)
                
                if self._period is None:
                    self._period = t
                else:
                    self._period = (self._old * self._period) + (self._new * t)
            
            self._high_tick = tick
        else:
            if not self._high_tick is None:
                t = pigpio.tickDiff(self._high_tick, tick)
                
                if self._high is None:
                    self._high = t
                else:
                    self._high = (self._old * self._high) + (self._new * t)
    
    def frequency(self):
        if self._high is None:
            return 0.0
            
        return 1000000.0 / self._period
            
    def pulse_width(self):
        if self._high is None:
            return 0.0
            
        return self._high
        
    def duty_cycle(self):
        if self._high is None:
            return 0.0
            
        return 100.0 * self._high / self._period
        
    def cancel(self):
        self._cb.cancel()
        
if __name__ == "__main__":
    IN_GPIO = 4 # Named 18 by RPi
    RUN_TIME = 60.0
    SAMPLE_TIME = 0.5

    pi = pigpio.pi()
    p = PwmMeasure(pi, IN_GPIO)
    start = time.time()
    
    while(True):
        time.sleep(SAMPLE_TIME)
        
        f = p.frequency()
        pw = p.pulse_width()
        dc = p.duty_cycle()
        
        #print(f'f={f}, pw={pw}, dc={dc}')
        print(f'inches={pw / 147}, cm={(pw / 147)*2.54}, m={((pw / 147)*2.54)/100}')

    

