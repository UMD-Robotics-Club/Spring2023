class Motor:
    pwm_pin
    last_time
    velocity
    acceleration
    dt = (cur_time - last_time)

    def __init__(self, pwm_pin):
        self.pwm_pin = pwm_pin
        
        return

    def set_acceleration(acceleration)
        self.acceleration = acceleration
        return

    def get_acceleration()
        return (cur_vel - last_vel) / dt

    def set_velocity(targ_velocity)
        while self.velocity != targ_velocity:
            self.velocity + 1
        return

    def get_velocity()
        return self.acceleration * dt

    def update()
        return
