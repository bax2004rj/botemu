import pygame  # To identify event types
import controllerHandler

# Custom event names
terminate = "terminate"

mouse_wheel = "mouse_wheel"
mouse_motion = "mouse_motion"

mouse_button_down = "mouse_button_down"
mouse_button_up = "mouse_button_up"

left_mouse_button_down = "left_mouse_button_down"
left_mouse_button_up = "left_mouse_button_up"

scroll_mouse_button_down = "scroll_mouse_button_down"
scroll_mouse_button_up = "scroll_mouse_button_up"

right_mouse_button_down = "right_mouse_button_down"
right_mouse_button_up = "right_mouse_button_up"

user_event_1 = "user_event_1"
user_event_2 = "user_event_2"

space_down = "space_down"
space_up = "space_up"

key_down = "key_down"
enter_key_down = "enter_key_down"
up_down = "up_key_down"
right_down = "right_key_down"
left_down = "left_key_down"
down_down = "down_key_down"
esc_down = "esc_key_down"
right_side_up_down = "right_side_up_down"
right_side_down_down = "right_side_down_down"
run_intake = "run_intake"

key_up = "key_up"
enter_key_up = "enter_key_up"
up_up = "up_key_up"
right_up = "right_key_up"
left_up = "left_key_up"
down_up = "down_key_up"
esc_up = "esc_key_up"
right_side_up_up = "right_side_up_up"
right_side_down_up = "right_side_down_up"
stop_intake = "stop_intake"

fieldUp_down = "fieldUp_down"
fieldUp_up = "fieldUp_up"
fieldDown_down = "fieldDown_down"
fieldDown_up = "fieldDown_up"
fieldLeft_down = "fieldLeft_down"
fieldLeft_up = "fieldLeft_up"
fieldRight_down = "fieldRight_down"
fieldRight_up = "fieldRight_up"
fieldZoomIn_down = "fieldZoomIn_down"
fieldZoomIn_up = "fieldZoomIn_up"
fieldZoomOut_down = "fieldZoomOut_down"
fieldZoomOut_up = "fieldZoomOut_up"
power_up = "powerUp"
power_down = "powerDown"
fire = "fire"

control = controllerHandler.controller()

eventButton = [False,False,False]
eventPos = [0,0]
scrollAmount = 0

# Function to return a list of all events in a frame
# Loops through pygame events, appends them to a list if they are needed, returns list
def get_events():
    global eventButton
    global eventPos
    global scrollAmount
    global control
    events = []
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            events.append(terminate)
        
        if event.type == pygame.MOUSEWHEEL:
            events.append(mouse_wheel)
            scrollAmount= event.y


        if event.type == pygame.MOUSEMOTION:
            events.append(mouse_motion)
            eventButton = event.buttons
            eventPos = event.pos

        if event.type == pygame.MOUSEBUTTONDOWN:
            events.append(mouse_button_down)
            eventButton = event.button
            eventPos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            events.append(mouse_button_up)
            eventPos = event.pos

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            events.append(left_mouse_button_down)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            events.append(left_mouse_button_up)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            events.append(scroll_mouse_button_down)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 2:
            events.append(scroll_mouse_button_up)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            events.append(right_mouse_button_down)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            events.append(right_mouse_button_up)
        if event.type == pygame.KEYDOWN:
            events.append(key_down)
            if event.key == pygame.K_SPACE:
                events.append(space_down)
            if event.key == pygame.K_w:
                events.append(up_down)
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                events.append(right_down)
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                events.append(left_down)
            if event.key == pygame.K_s:
                events.append(down_down)
            if event.key == pygame.K_UP:
                events.append(right_side_up_down)
            if event.key == pygame.K_DOWN:
                events.append(right_side_down_down)
            if event.key == pygame.K_i:
                events.append(fieldUp_down)
            if event.key == pygame.K_l:
                events.append(fieldRight_down)
            if event.key == pygame.K_j:
                events.append(fieldLeft_down)
            if event.key == pygame.K_k:
                events.append(fieldDown_down)
            if event.key == pygame.K_u:
                events.append(fieldZoomIn_down)
            if event.key == pygame.K_o:
                events.append(fieldZoomOut_down)
            if event.key == pygame.K_q:
                events.append(run_intake)
            if event.key == pygame.K_e:
                events.append(power_up)

            if event.key == pygame.K_ESCAPE:
                events.append(esc_down)
            if event.key == pygame.K_RETURN:
                events.append(enter_key_down)

        if event.type == pygame.KEYUP:
            events.append(key_up)
            if event.key == pygame.K_SPACE:
                events.append(space_up)
            if event.key == pygame.K_w:
                events.append(up_up)
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                events.append(right_up)
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                events.append(left_up)
            if event.key == pygame.K_s:
                events.append(down_up)
            if event.key == pygame.K_UP:
                events.append(right_side_up_up)
            if event.key == pygame.K_DOWN:
                events.append(right_side_down_up)
            if event.key == pygame.K_i:
                events.append(fieldUp_up)
            if event.key == pygame.K_l:
                events.append(fieldRight_up)
            if event.key == pygame.K_j:
                events.append(fieldLeft_up)
            if event.key == pygame.K_k:
                events.append(fieldDown_up)
            if event.key == pygame.K_u:
                events.append(fieldZoomIn_up)
            if event.key == pygame.K_o:
                events.append(fieldZoomOut_up)
            if event.key == pygame.K_q:
                events.append(stop_intake)
            if event.key == pygame.K_e:
                events.append(power_down)
            if event.key == pygame.K_TAB:
                events.append(fire)
            

            if event.key == pygame.K_ESCAPE:
                events.append(esc_up)
            if event.key == pygame.K_RETURN:
                events.append(enter_key_up)

        if event.type == pygame.USEREVENT + 1:
            events.append(user_event_1)

        if event.type == pygame.USEREVENT + 2:
            events.append(user_event_2)
        
        if event.type == pygame.JOYBUTTONDOWN:
            if control.get_button(5):
                events.append(run_intake)

    try:   
        controllerHandler.controller.get_axisVal(control)
    except AttributeError:
        pass


    return events
