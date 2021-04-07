import numpy as np

def calc_burning_height(start_height, start_velocity, landing_velocity, landing_height, boost, g_fall):

    h_s = (start_velocity ** 2 - landing_velocity ** 2 + 2 * (g_fall * start_height + boost * landing_height))/(2 * (g_fall + boost))
   
    return h_s

def free_fall_est(start_height, start_velocity, g_fall, burning_height):

    t_fall = (start_velocity + np.sqrt(start_velocity ** 2 + 2 * g_fall * (start_height - burning_height))) / g_fall

    v_end = start_velocity - g_fall * t_fall
    
    return t_fall, v_end

def parameters_change(start_velocity, height_landing, rocket_m, boost, g_fall, u_gas, d_t, landing_t):

    fuel_burst = rocket_m * (boost + g_fall) / u_gas
    start_velocity += boost * d_t
    height_landing += start_velocity * d_t
    rocket_m -= fuel_burst * d_t
    landing_t += d_t
    
    return start_velocity, height_landing, rocket_m, fuel_burst, landing_t

def main():

    dt = 1e-4 #smaller dt means higher accuracy
    acceleration_time = 0
    rocket_mass_0 = 2350
    rocket_mass = rocket_mass_0
    g = 1.62
    h_0 = 1068
    height = h_0
    fuel_0 = 200
    fps = 0
    v_0 = 56
    v_land = -1
    velocity = v_0
    v_gas = 3660
    acceleration = 20
    free_fps_min = 0
    free_fps_max = 0

    print('{:^10}|{:^10}|{:^10}|{:^14}|{:^15}'
    .format('Velocity', 'Height', 'Fuel per second min', 'Fuel per second max', 'Maneuver time'))

    h_s = calc_burning_height(height, v_0, v_land, 0, acceleration, g)

    maneuver_t, velocity = free_fall_est(height, v_0, g, h_s)

    print('{:^10}|{:^10}|{:^19}|{:^19}|{:^15.3}'
    .format(v_0, h_0, free_fps_min, free_fps_max, maneuver_t))

    height = calc_burning_height(h_0, v_0, v_land, 0, acceleration, g)
    acceleration_velocity = velocity
    acceleration_height = height

    _, _, _, fps_max, _ = parameters_change(acceleration_velocity, acceleration_height, rocket_mass, acceleration, g, v_gas, dt, 0)

    while acceleration_height > 0:
        acceleration_velocity, acceleration_height, rocket_mass, fps, acceleration_time = parameters_change(acceleration_velocity, acceleration_height, rocket_mass, acceleration, g, v_gas, dt, acceleration_time)
        #print('{:^10.3f}|{:^10.3f}|{:^19.3f}|{:^15.2f}'                                #if you want to see current state of vessel during maneuver, uncomment these two lines and comment last print line
        #.format(acceleration_velocity, acceleration_height, fps, acceleration_time))
    
    _, _, _, fps_min, _ = acceleration_velocity, acceleration_height, rocket_mass, fps, acceleration_time = parameters_change(acceleration_velocity, acceleration_height, rocket_mass, acceleration, g, v_gas, dt, acceleration_time)
    
    print('{:^10.3f}|{:^10.3f}|{:^19.3f}|{:^19.3f}|{:^15.2f}'
    .format(velocity, height, fps_min, fps_max, acceleration_time))
    
    return


if __name__ == '__main__':
    main()