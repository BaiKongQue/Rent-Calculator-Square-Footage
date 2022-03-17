class RentCalculator:
    """
    API to interact and calculate how much each person pays what for rent
    based on the square footage of the rooms.
    """
    def __init__(self):
        self._data = {}
        return
    
# PRIVATE #
    def _clear(self):
        """
        Reset and clear the current data being held for the apartment
        and set a general structure for the data
        """
        self._data = {
            "num_rooms": None,
            "num_people": None,
            "apt_cost": None,
            "rooms": {},
            "rooms_shared": {}
        }

    def _get_input(self, S, T = str, C = lambda i: i.strip() == "", Err = "Error input not valid"):
        """
        Get User input and turn it into dtype T, loop while C is true
        
        @param S string: string to display for input
        @param T dtype: input data type
        @param C lambda: loops while C is true
        @return T: valid user input
        """
        while True:                         # loop until return result
            try:
                user_input = T(input(S))    # Get user input
            except ValueError:              # if input is not int
                print(Err)                  # print err
            else:                           # else input is valid int
                if C(user_input):           # if C is true
                    print(Err)              # print err and continue loop
                else:
                    return user_input       # return result

    def _sum(self, location, F):
        """
        Iterate over _data.rooms array and sum up the specified key

        @param key string: name of the key to get a summation on
        @return float: sum of _data.rooms[key]
        """
        sum = 0
        for v in location:          # loop _data.rooms
            sum += F(location[v])   # sum up _data.rooms[key]
        return sum                  # return sum
    
    def _calculate(self):
        """
        Calculate and set totals for all rooms.
        """
        sqr_ft_sum = self._sum(self._data['rooms'], lambda v: v["size"])            # get the sum of all the square footage of each room
        
        for room in self._data['rooms']:                                            # loop each room
            percent = (self._data['rooms'][room]['size'] / sqr_ft_sum)              # calculate percentage of each room
            self._data['rooms'][room]['total'] = self._data['apt_cost'] * percent   # set how much room cost based on percentage

# PUBLIC #
    def new_apartment(self):
        """
        User Interface for creating apartment data with user input
        """
        self._clear()                                                                                           # clear _data
        self._data['num_rooms'] = self._get_input("Number of rooms: ", int, lambda i: i <= 0)                   # store the number of rooms
        self._data['num_people'] = self._get_input("Number of people: ", int, lambda i: i <= 0)                 # store the number of people
        self._data['apt_cost'] = self._get_input("Cost of the Apartment: ", int, lambda i: i <= 0)              # store the cost of the apartment
        
        for i in range(0, self._data['num_rooms']):                                                             # loop to get each room information
            print("-" * 10 + " Room", i + 1 , "-" * 10)
            room = self._get_input("Name of Room %s: " % (i + 1), str).lower().strip()                          # get name of room
            
            room_size = self._get_input(                                                                        # get size of room
                "%s Square Footage: " % (room),
                float,
                lambda i: i <= 0,                                                                               # continue loop if i <= 0
                "Room size must be > 0"
            )

            room_shared = self._get_input(                                                                      # get user input if room being shared between everyone
                "Eveyone shares this room: ",
                str,
                lambda i: i.lower() not in ['yes', 'no', 'true', 'false', 'y', 'n', 't', 'f', '1', '0'],        # continue loop if not one of these key boolean words
                "Input must be: yes, no, true, false, y, n, t, f, 1, or 0"
            ).lower().strip()
            room_shared = True if room_shared in ['yes', 'true', 'y', 't', '1'] else False                      # set True if one of the true key words else False

            self._data["rooms"][room] ={"size": room_size, "sharing": room_shared, "num_share": 0, "total": 0}  # add and set all obtained room data into _data['rooms'][room]

        print("-" * 10 + " Rooms People Pay for ", "-" * 10)
        print("List the rooms each person will pay for separated by a \", \".")
        for i in range(0, self._data['num_people']):                                                            # loop the number of people there are
            rooms_shared_list = self._get_input(                                                                # get a list of what rooms this person is sharing
                "Person " + str(i+1) + ": ",
                str,
                lambda i: not(set(i.split(", ")).issubset(self._data['rooms']) or i in self._data['rooms']),    # continue loop if room does not exist or invalid
                "One or more of the rooms are invalid!"
            )
            rooms_shared_list = rooms_shared_list.split(", ")                                                   # get list from string
            for room in rooms_shared_list:                                                                      # loop each room in list
                if self._data['rooms'][room]['sharing']:                                                        # if room is shared between everyone
                    rooms_shared_list.remove(room)                                                              # take off this list
                else:                                                                                           # else
                    self._data['rooms'][room]['num_share'] += 1                                                 # increment how many people share this room
            self._data['rooms_shared']['person ' + str(i+1)] = rooms_shared_list                                # add person and the rooms they share too _data['rooms_shared']['person #']

        self._calculate()                                                                                       # calculate each room's amount

    def get_room_pay(self):
        """
        Get how much each room owes

        @return dict: key is the name of the room and value is
        amount
        """
        room_pay = {}
        for room in self._data['rooms']:        # loop rooms
            room_pay[room.name] = room.total    # store room.name: room.total
        return room_pay                         # return dict of room_pay

    def get_person_pay(self):
        """
        Get how much each person owes. this function calculates
        the amount of the rooms everyone is sharing then
        calculates each person's amount of the rooms they are
        sharing individually and adding the shared amount.

        @return dict: key is person #, and value is the amount
        they owe
        """
        per_pay = {}                                                                    # hold the result
        everyone_sharing_pay = 0                                                        # amount everyone will share
        
        for room in self._data['rooms']:                                                # loop rooms
            if self._data['rooms'][room]['sharing']:                                    # if room is shared by everyone
                everyone_sharing_pay += self._data['rooms'][room]['total']              # add toom total to everyone_sharing_pay

        if everyone_sharing_pay != 0: everyone_sharing_pay /= self._data['num_people']  # if everyone_sharing_pay is not 0 then divide it by number of people

        for person, rooms in self._data['rooms_shared'].items():                        # loop all the rooms a person shares
            if len(rooms) > 0:                                                          # if rooms is not empty
                per_pay[person] = (self._sum({room: self._data['rooms'][room] for room in rooms}, lambda v: v['total'] / v['num_share'])) + everyone_sharing_pay # calculate how much each person owes
            else:                                                                       # else
                per_pay[person] = everyone_sharing_pay                                  # their pay is just what everyone shares

        return per_pay                                                                  # return each persons pay in dict