from RADeath import death
import os


######################################################################
# the blueprint for a room
class Room:
# the constructor
    def __init__(self, name):
        # rooms have a name, exits (e.g., south), exit locations
        # (e.g., to the south is room n), items (e.g., table), item
        # descriptions (for each item), and grabbables (things that
        # can be taken into inventory)
        self.name = name
        self.exits = []
        self.exitLocations = []
        self.items = []
        self.itemDescriptions = []
        self.grabbables = []
    
    # getters and setters for the instance variables
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
    @property
    def exits(self):
        return self._exits
    @exits.setter
    def exits(self, value):
        self._exits = value
    @property
    def exitLocations(self):
        return self._exitLocations
    @exitLocations.setter
    def exitLocations(self, value):
        self._exitLocations = value
    @property
    def items(self):
        return self._items
    @items.setter
    def items(self, value):
        self._items = value
    @property
    def itemDescriptions(self):
        return self._itemDescriptions
    @itemDescriptions.setter
    def itemDescriptions(self, value):
        self._itemDescriptions = value
    @property
    def grabbables(self):
        return self._grabbables
    @grabbables.setter
    def grabbables(self, value):
        self._grabbables = value
    
    # adds an exit to the room
    # the exit is a string (e.g., north)
    # the room is an instance of a room
    def addExit(self, exit, room):
    # append the exit and room to the appropriate lists
        self._exits.append(exit)
        self._exitLocations.append(room)
    # adds an item to the room
    # the item is a string (e.g., table)
    # the desc is a string that describes the item (e.g., it is made
    # of wood)
    def addItem(self, item, desc):
    # append the item and exit to the appropriate lists
        self._items.append(item)
        self._itemDescriptions.append(desc)
    # adds a grabbable item to the room
    # the item is a string (e.g., key)
    def addGrabbable(self, item):
    # append the item to the list
        self._grabbables.append(item)
    # removes a grabbable item from the room
    # the item is a string (e.g., key)
    def delGrabbable(self, item):
    # remove the item from the list
        self._grabbables.remove(item)
    # returns a string description of the room
    def __str__(self):
    # first, the room name
        s = "You are in {}.\n".format(self.name)
    # next, the items in the room
        s += "You see: "
        for item in self.items:
            s += item + " "
            s += "\n"
    # next, the exits from the room
        s += "Exits: "
        for exit in self.exits:
            s += exit + " "
        return s


######################################################################
# creates the rooms
def createRooms():
    # r1 through r4 are the four rooms in the mansion
    # currentRoom is the room the player is currently in (which can
    # be one of r1 through r4)
    # since it needs to be changed in the main part of the program,
    # it must be global
    global currentRoom
    # create the rooms and give them meaningful names
    r1 = Room("Room 1")
    r2 = Room("Room 2")
    r3 = Room("Room 3")
    r4 = Room("Room 4")
    # add exits to room 1
    r1.addExit("east", r2) # -> to the east of room 1 is room 2
    r1.addExit("south", r3)
    # add grabbables to room 1
    #r1.addGrabbable("key")
    r1.addGrabbable("paintbrush")
    # add items to room 1
    r1.addItem("canvas", "A blank canvas. If I had a paint brush I bet I could make a masterpiece.")
    r1.addItem("mirror", "You look in the mirror. You're frowning :(")
    # add exits to room 2
    r2.addExit("west", r1)
    r2.addExit("south", r4)
    # add items to room 2
    r2.addItem("unlit_torch", "the torch on the wall is not lit")
    r2.addItem("fireplace", "The fire is warm and makes you feel good.")
    r2.addItem("sword", "The sword is lodged in a stone")
    # add exits to room 3
    r3.addExit("north", r1)
    r3.addExit("east", r4)
    # add grabbables to room 3
    r3.addGrabbable("book")
    # add items to room 3
    r3.addItem("bookshelves", "They are empty. Go figure.")
    r3.addItem("statue", "There is nothing special about it.")
    r3.addItem("desk", "The statue is resting on it. So is a book.")
    r3.addItem("skeleton", """
A spooky skeleton is guarding the door. 
If only you had a weapon.
      .-.
     (o.o)
      |=|
     __|__
   //.=|=.\\\\
  // .=|=. \\\\
  \\\\ .=|=. //
   \\\\(_=_)//
    (:| |:)
     || ||
     () ()
     || ||
     || ||
    ==' '==""")
    # add exits to room 4
    r4.addExit("north", r2)
    r4.addExit("west", r3)
    r4.addExit("south", None) # DEATH!
    # add grabbables to room 4
    r4.addGrabbable("6-pack")
    # add items to room 4
    r4.addItem("brew_rig", "Gourd is brewing some sort of oatmeal stout on the brew rig. A 6-pack is resting beside it.")
    # set room 1 as the current room at the beginning of the game
    currentRoom = r1

    
######################################################################
# START THE GAME!!!
inventory = [] # nothing in inventory...yet
response = ""
createRooms() # add the rooms to the game
# play forever (well, at least until the player dies or asks to quit)

# game variables
smile = False
door_lock = True

# item variables to ensure they do not respawn
key_check = False


while (True):
# set the status so the player has situational awareness
# the status has room and inventory information
    status = "{}\nYou are carrying: {}\n".format(currentRoom,inventory)
# if the current room is None, then the player is dead
# this only happens if the player goes south when in room 4
    if (currentRoom == None):
        status = "You are dead."
    # display the status
    print(f"""========================================================\n
{status}\n
{response}

""")

    # if the current room is None (and the player is dead), exit the
    # game
    if (currentRoom == None):
        death()
        break
    # prompt for player input
    # the game supports a simple language of <verb> <noun>
    # valid verbs are go, look, and take
    # valid nouns depend on the verb
    # set the user's input to lowercase to make it easier to compare
    # the verb and noun to known values
    action = input("What to do? ")
    action = action.lower()
    # exit the game if the player wants to leave (supports quit,
    # exit, and bye)
    if (action == "quit" or action == "exit" or action == "bye"):
        break
    if (action == "die"):
        death()
    # set a default response
    response = "I don't understand. Try verb noun. Valid verbs are go, look, and take"
    # split the user input into words (words are separated by spaces)
    words = action.split()
    # the game only understands two word inputs
    if (len(words) == 2):
    # isolate the verb and noun
        verb = words[0]
        noun = words[1]
    # the verb is: go
        if (verb == "go"):
    # set a default response
            response = "Invalid exit."
    # check for valid exits in the current room
            for i in range(len(currentRoom.exits)):
    # a valid exit is found
                if currentRoom.name == "Room 1":
                    if "key" not in inventory and noun == "east" and door_lock == True:
                        response = "The door seems to be locked."
                        break
                    elif "key" in inventory and noun == "east" and door_lock == True:
                        response = "you unlocked the door. (go east again to go through door)"
                        door_lock = False
                        inventory.remove("key")
                        break
                    else:
                        currentRoom = currentRoom.exitLocations[i]
                        response = "Room changed."
                        break
                elif (noun == currentRoom.exits[i]):
    # change the current room to the one that is
    # associated with the specified exit
                    currentRoom = currentRoom.exitLocations[i]              
    # set the response (success)
                    response = "Room changed."
    # no need to check any more exits
                    break
    # the verb is: look
        elif (verb == "look"):
# set a default response
            response = "I don't see that item."
# check for valid items in the current room
            for i in range(len(currentRoom.items)):
                if (currentRoom.name) == "Room 1" and "paintbrush" in inventory and noun == "canvas":
                    response = currentRoom.itemDescriptions[i] = "You took out your paintbrush and painted the Mona Lisa. It's beautiful. It makes you smile."
                    inventory.remove("paintbrush")
                    smile = True
                if (currentRoom.name) == "Room 1" and smile and noun == "mirror":
                    response = currentRoom.itemDescriptions[i] = "You look at the mirror and see your beautiful smile. The mirror then shatters revealing a secret compartment. You see a key inside."
                    if key_check == False:
                        currentRoom.addGrabbable("key")
                        key_check = True

# a valid item is found
                if (noun == currentRoom.items[i]):
# set the response to the item's description
                    response = currentRoom.itemDescriptions[i]
# no need to check any more items
                    break
    # the verb is: take
        elif (verb == "take"):
    # set a default response
            response = "I don't see that item."
    # check for valid grabbable items in the current room
            for grabbable in currentRoom.grabbables:
    # a valid grabbable item is found
                if (noun == grabbable):
    # add the grabbable item to the player's
    # inventory
                    inventory.append(grabbable)
    # remove the grabbable item from the room
                    currentRoom.delGrabbable(grabbable)
    # set the response (success)
                    response = "Item grabbed."
    # no need to check any more grabbable items
                    break
    # display the response
    

    os.system('cls' if os.name == 'nt' else 'clear')