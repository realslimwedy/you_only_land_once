import time

# KEYBOARD RC ##########################################################################################################

def keyboard_rc(drone, rc_values, pygame_instance, speed):
    py_g = pygame_instance
    lr, fb, ud, yv = rc_values
    speed = speed

    # Takeoff and land
    if py_g.get_key('e') and not drone.me.is_flying:
        drone.flight_phase = "Take-off"
        drone.me.takeoff()
        return 0, 0, 0, 0
    elif py_g.get_key('q') and drone.me.is_flying:
        drone.flight_phase = "Touch-down"
        drone.me.land()
        time.sleep(2)
        return 0, 0, 0, 0

    # Movement
    if py_g.get_key('RIGHT'):
        lr = speed
    elif py_g.get_key('LEFT'):
        lr = -speed
    if py_g.get_key('UP'):
        fb = speed
    elif py_g.get_key('DOWN'):
        fb = -speed
    if py_g.get_key('w'):
        ud = speed
    elif py_g.get_key('s'):
        ud = -speed
    if py_g.get_key('d'):
        yv = speed
    elif py_g.get_key('a'):
        yv = -speed

    # Flips
    if py_g.get_key('0'):
        drone.me.flip_forward()

    return lr, fb, ud, yv

# IMAGE CAPTURE #######################################################################################################

def taking_pictures_key_pressed(pygame_instance):
    py_g = pygame_instance
    if py_g.get_key('SPACE'):
        print('SPACE pressed - Image saving...')
        return True
    return False


def recording_video_key_pressed(pygame_instance):
    py_g = pygame_instance
    if py_g.get_key('v'):
        print('v pressed: Video capture...')
        return True
    return False

# EXIT #################################################################################################################

def exit_app_key_pressed(pygame_instance):
    py_g = pygame_instance
    if py_g.get_key('ESCAPE'):
        return True
    return False

# AUTO-PILOT ##########################################################################################################

def auto_pilot_key_pressed(pygame_instance):
    py_g = pygame_instance
    if py_g.get_key('p'):
        print("p pressed: AUTO-PILOT...")
        return True
    return False

# FLIGHT PHASES ######################################################################################################

def takeoff_phase_key_pressed(pygame_instance):
    py_g = pygame_instance
    if py_g.get_key('1'):
        return True
    return False


def hover_phase_key_pressed(pygame_instance):
    py_g = pygame_instance
    if py_g.get_key('2'):
        return True
    return False


def obj_det_phase_key_pressed(pygame_instance):
    py_g = pygame_instance
    if py_g.get_key('3'):
        return True
    return False


def seg_phase_key_pressed(pygame_instance):
    py_g = pygame_instance
    if py_g.get_key('4'):
        return True
    return False


def risk_map_key_pressed(pygame_instance):
    py_g = pygame_instance
    if py_g.get_key('5'):
        return True
    return False


def approach_phase_key_pressed(pygame_instance):
    py_g = pygame_instance
    if py_g.get_key('6'):
        return True
    return False


def landing_phase_key_pressed(pygame_instance):
    py_g = pygame_instance
    if py_g.get_key('7'):
        return True
    return False

# SPEED ###############################################################################################################

def switch_speed_key_pressed(pygame_instance):
    py_g = pygame_instance
    if py_g.get_key('o'):
        return True
    return False
