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
    def removeItem(self, item, desc):
    # remove the item and desc from the appropriate lists
        self._items.remove(item)
        self._itemDescriptions.remove(desc)
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
    r5 = Room("Room 5")
    r6 = Room("the secret room")
    # add exits to room 1
    r1.addExit("east", r2) # -> to the east of room 1 is room 2
    r1.addExit("south", r3)
    # add grabbables to room 1
    
    # add items to room 1
    r1.addItem("canvas", "A blank canvas. If I had a paint brush I bet I could make a masterpiece.")
    r1.addItem("mirror", "You look in the mirror. You're frowning :(")
    r1.addItem("drawer_container", "You look at the drawer container and see three seperate drawers.")
    # add grabbables to room 1
    r1.addGrabbable("crystal")
    # add exits to room 2
    r2.addExit("west", r1)
    r2.addExit("south", r4)
    # add items to room 2
    r2.addItem("unlit_torch", "the torch on the wall is not lit.")
    r2.addItem("fireplace", "The fire is warm and makes you feel good.")
    r2.addItem("sword", "The sword is lodged in a stone.")
    # add grabbables to room 2
    r2.addGrabbable("sword")
    r2.addGrabbable("unlit_torch")
    # add exits to room 3
    r3.addExit("north", r1)
    r3.addExit("south", r5)
    r3.addExit("", r6)

    # add items to room 3
    r3.addItem("bookshelves", "They're filled up with books, except one spot that looks like a book could fit.")
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
    # add grabbables to room 3
    r3.addGrabbable("book")
    # add exits to room 4
    r4.addExit("north", r2)
    r4.addExit("south", None) # DEATH!
    
    # add items to room 4
    r4.addItem("alchemy_station", "It's an alchemy station for brewing potions. There's instruction sitting by it.")
    r4.addItem("instructions", "INGREDIENTS: stardust, crystal, elixer \n\nSTEP 1: place crystal in tube 3. \nSTEP 2: place stardust in tube 1. \nSTEP 3: place elixer in tube 2. \nSTEP 4: mix ingredients for 2 minutes.")

    # add exit to secret room
    r6.addExit("east", r3)

    # add items to secret room
    r6.addItem("chest", "You open the chest. Theres an elixer inside")
    # add grabbable items
    r6.addGrabbable("elixer")
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
door_lock2 = True

# item variables to ensure they do not respawn
key_check = False
key_flag = False
drawer_check = False
paintbrush_flag = False
paintbrush_check = False


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
    response = "I don't understand. Try verb noun. Valid verbs are go, look, take, and use"
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
                if currentRoom.name == "Room 1" and noun == "east" and door_lock == True:
                    response = "The door seems to be locked."
                    break
                if currentRoom.name == "Room 2" and noun == "south" and door_lock2 == True:
                    response = "The door is covered in spiderwebs and you can't open it."
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
                if (currentRoom.name) == "Room 1" and smile and noun == "mirror" and key_check == False:
                    response = currentRoom.itemDescriptions[i] = "You look at the mirror and see your beautiful smile. The mirror then shatters revealing a secret compartment. You see a key inside."
                    if key_check == False and key_flag == False:
                        currentRoom.addGrabbable("key")
                        # this flag ensures the key is only appended once
                        key_flag = True        
                # changes the description for the mirror after you took the key
                elif (currentRoom.name) == "Room 1" and key_check and noun == "mirror":
                    response = currentRoom.itemDescriptions[i] = "The mirror is now shattered."
                # changes the description for the blank canvas after you painted on it
                if (currentRoom.name) == "Room 1" and smile and noun == "canvas":
                    response = currentRoom.itemDescriptions[i] = "The canvas now has the beautiful painting of the Mona Lisa on it. It makes you smile. :)"
                if (currentRoom.name) == "Room 1" and noun == "drawer_container" and drawer_check == False:
                    currentRoom.addItem("drawer_1", "You open drawer_1. There's a crystal inside.")
                    currentRoom.addItem("drawer_2", "You open drawer_2. It's empty.")
                    currentRoom.addItem("drawer_3", "You open drawer_3. There's a paintbrush inside.")
                    drawer_check = True
                if (currentRoom.name) == "Room 1" and noun == "drawer_3" and drawer_check == True and paintbrush_flag == False:
                    currentRoom.addGrabbable("paintbrush")
                    paintbrush_flag = True

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
            # for the key in room 1.
            for grabbable in currentRoom.grabbables:
                if (currentRoom.name == "Room 1" and grabbable == "key"):
                    key_check = True
                    inventory.append(grabbable)
                    currentRoom.delGrabbable(grabbable)
                    response = "Item grabbed."
                    break
                elif (currentRoom.name == "Room 1" and grabbable == "paintbrush" and "crystal" in inventory or currentRoom.name == "Room 1" and grabbable == "crystal" and "paintbrush" in inventory):
                    inventory.append(grabbable)
                    currentRoom.delGrabbable(grabbable)
                    response = "Item grabbed"
                    currentRoom.removeItem("drawer_1", "You open drawer_1. There's a crystal inside.")
                    currentRoom.removeItem("drawer_2", "You open drawer_2. It's empty.")
                    currentRoom.removeItem("drawer_3", "You open drawer_3. There's a paintbrush inside.")
                    paintbrush_check = True
                    break
                if (currentRoom.name == "Room 2" and noun == "sword" and grabbable == "sword"):
                    response = "You try as hard as you can to pull the sword from the stone but it won't budge. You are just not strong enough."
                    break
                elif (currentRoom.name == "Room 2" and noun == "unlit_torch" and grabbable == "unlit_torch"):
                    inventory.append(grabbable)
                    currentRoom.delGrabbable(grabbable)
                    response = "Item grabbed"
                    break
    # a valid grabbable item is found
                elif (noun == grabbable):
    # add the grabbable item to the player's inventory
                    inventory.append(grabbable)
    # remove the grabbable item from the room
                    currentRoom.delGrabbable(grabbable)
    # set the response (success)
                    response = "Item grabbed."
    # no need to check any more grabbable items
                    break
    # the verb is: use
        elif (verb == "use"):
    # set a default response
            response = "can not use this here."
    # check for valid usable items
            for item in inventory:
                if (noun == item):
                    if (currentRoom.name) == "Room 1" and noun == "paintbrush" and "paintbrush" in inventory:
                        response = "You took out your paintbrush and painted the Mona Lisa on the blank canvas. It's beautiful. It makes you smile. :)"
                        inventory.remove("paintbrush")
                        smile = True
                    if (currentRoom.name == "Room 1" and noun == "key" and "key" in inventory):
                        response = "You used the key to unlock the east door!"
                        inventory.remove("key")
                        door_lock = False
                    if (currentRoom.name == "Room 3" and noun == "book" and "book" in inventory):
                        response = "You put the book in the the missing spot on the bookshelf. The book shelf slides to the right revealing a secret door. (You can now go west.)"
                        inventory.remove("book")
                        currentRoom.exits[2] = "west"
                    if (currentRoom.name == "Room 2" and noun == "unlit_torch" and "unlit_torch" in inventory):
                        response = "You stick the unlit torch into the fireplace. You now have a lit torch!"
                        inventory.remove("unlit_torch")
                        inventory.append("lit_torch")
                    if (currentRoom.name == "Room 2" and noun == "lit_torch" and "lit_torch" in inventory):
                        response = "You use the torch to burn all the spiderwebs blocking the sothern door. You can now go south."
                        inventory.remove("lit_torch")
                        door_lock2 = False
                        
                        
                        
                    
    # clear screen so the response appears to update.
    os.system('cls' if os.name == 'nt' else 'clear')