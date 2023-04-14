from ursina import *
import random
from  AutomaticSimulation import *
import sys
from ursina import text

app = Ursina()
vehicles = []

trafficSystem = AutomaticSimulation()

# Create a camera with a bird's eye view
camera.orthographic = True
camera.position = (35, 25, -35)
camera.rotation = (25, -45, 45)
camera.fov = 100

# create base
box = Entity(model='quad', scale=180, color=rgb(51,165,50))

# create roads
roads_name = []
for i in range(len(trafficSystem.intersection_list)):
    for j in range(len(trafficSystem.intersection_list[i])):
        # Create a TextEntity with the desired string
        road_name = trafficSystem.intersection_list[i][j]["road"]

        check_duplicate = False
        for k in range(len(roads_name)):
             if(roads_name[k] == road_name):
                 check_duplicate = True

        
        if(check_duplicate == False):

            roads_name.append(road_name)
            road_position = trafficSystem.intersection_list[i][j]["position"]
            
            print(road_name)
            print(road_position)

            if (road_name[0] == "N" or road_name[0] == "S") and road_name[1] == " ":  # Verticle Roads
                # Create the object_rec Entity and pass text_entity as a child
                road_model = Entity(model='cube', scale=(4, 100, 0.1), color=color.gray)
                road_model.y = road_position/2   
                road_model.x = road_position*5
                roadText= Text(text=road_name, scale=(15,1))
                roadText.parent = road_model
                roadText.z = -.5
                roadText.y = -.5
                road_model.name = road_name
                
                
            elif (road_name[0] == "E" or road_name[0] == "W") and road_name[1] == " ": # Horizontal Roads
                # Create the object_rec Entity and pass text_entity as a child
                road_model = Entity(model='cube', scale=(100, 4, 0.1), color=color.gray)
                road_model.y = road_position/2
                roadText= Text(text=road_name, scale=(1,15))
                roadText.parent = road_model
                roadText.z = -2
                roadText.y = -.5

            else:
                print("Please Declair N|S|E|W in the", trafficSystem.file_name, "input file")
                # Terminate the program without specifying an exit code
                sys.exit()

stopSign1 = Entity(model='sphere', scale=1, color=color.red)
stopSign1.x = 3
stopSign1.y = -3

busStop1 = Entity(model='cube', scale=1, color=color.blue)
busStop1.x = -25
busStop1.y = 23

traffic_light1 = Entity(model='cube', scale=(1, 3, 1), color=color.green)
traffic_light1.x = 0
traffic_light1.y = 25

#Loop through vehicle list to spawn cars and set attributes 
for i in range(len(trafficSystem.vehicle_list)):
    # Get the vehicle properties from the list
    vehicle_props = trafficSystem.vehicle_list[i]

    # Create a new car entity with the properties
    car = Entity(model='cube', scale=(2, 1, 1), color=color.red)
    
    car.speed = vehicle_props["speed"] / 100
    #car.acceleration = vehicle_props["acceleration"] / 100
    car.type = vehicle_props["type"]
    car.road = vehicle_props["road"]
    if (car.road[0] == "N" or car.road[0] == "S") and car.road[1] == " ":
        car.is_on_y_axis = True
    else:
        car.is_on_y_axis = False
    
    #need to fix car position relative to road
    car.position = (0,25)
    
    # Add the car to the list of vehicles
    vehicles.append(car)


# Define a function to move the cars
def update():
    traffic_light_time = time.time() % 16 # repeat cycle every 16 seconds
    
   #  trafficSystem.update()

    if traffic_light_time < 7:
        traffic_light1.color = color.green
    elif traffic_light_time < 9:
        traffic_light1.color = color.yellow
    else:
        traffic_light1.color = color.red
    
    for vehicle in vehicles:
        if vehicle.is_on_y_axis:
            vehicle.y += vehicle.speed
            if vehicle.y > 49:
                vehicle.y = -49
        else:
            vehicle.x += vehicle.speed
            if vehicle.x > 49:
                vehicle.x = -49

# Create the button
def add_vehicle():
    # Define code to add a vehicle here
    pass

def on_button_click():
    # Choose a random car position
    
    car_position = random.choice(car_positions)

    # Create a new vehicle entity
    available_colors = [color.red, color.green, color.blue, color.yellow, color.orange, color.cyan] # list of available colors
    vehicle = Entity(model='cube', scale=(2, 1, 1), color=random.choice(available_colors)) # choose a random color from the list
    
    
    if car_position == car_positions[2]:
        vehicle.rotation = (0, 0, 90)
        vehicle.is_on_y_axis = True
    else:
        vehicle.is_on_y_axis = False
        
    # Set the position of the new vehicle to the chosen car position
    vehicle.position = car_position
    
    vehicle.speed = random.uniform(0.05, 0.2) # set a random speed between 0.05 and 0.2
    
    vehicles.append(vehicle)
    # Make the new vehicle visible
    vehicle.visible = True
    
def reset_program():
    # Reset the initial state of the program
    global vehicles
    for vehicle in vehicles:
        destroy(vehicle)
    vehicles = [] 
    
button = Button(text='Add\nVehicle', color=color.azure, highlight_color=color.cyan, position=(0.65, 0.45), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=on_button_click)
startButton = Button(text='Restart\nSimulation', color=rgb(128, 128, 0), highlight_color=color.cyan, position=(0.40, 0.45), scale=(0.1, 0.1), model='circle', text_scale=0.3, on_click=on_button_click)

app.run()