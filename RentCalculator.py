"""
@author     Lee Perkins
@email      2lperkins@gmail.com
@version    1.0
@since      2019-03-03

Copyright (c) 2019 MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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
        while True:
            try:                            # Get user input
                user_input = T(input(S))
            except ValueError:              # if input is not int
                print(Err)
                continue
            else:                           # else input is valid int
                if C(user_input):
                    print(Err)
                else:
                    return user_input       # return result

    def _sum(self, location, F):
        """
        Iterate over _data.rooms array and sum up the specified key

        @param key string: name of the key to get a summation on
        @return float: sum of _data.rooms[key]
        """
        sum = 0
        for v in location:   # loop _data.rooms
            sum += F(location[v]) # sum up _data.rooms[key]
        return sum           # return sum
    
    def _calculate(self):
        sqr_ft_sum = self._sum(self._data['rooms'], lambda v: v["size"])                          # get the sum of all the square footage of each room
        
        for room in self._data['rooms']:                        # loop each room
            percent = (self._data['rooms'][room]['size'] / sqr_ft_sum)               # calculate percentage of each room
            self._data['rooms'][room]['total'] = self._data['apt_cost'] * percent    # set how much room cost based on percentage

# PUBLIC #
    def new_apartment(self):
        """
        User Interface for creating apartment data with user input
        """
        self._clear()                                                                                 # clear _data
        self._data['num_rooms'] = self._get_input("Number of rooms: ", int, lambda i: i <= 0)         # store the number of rooms
        self._data['num_people'] = self._get_input("Number of people: ", int, lambda i: i <= 0)       # store the number of people
        self._data['apt_cost'] = self._get_input("Cost of the Apartment: ", int, lambda i: i <= 0)    # store the cost of the apartment
        
        for i in range(0, self._data['num_rooms']):                                                                         # loop to get each room information
            print("-" * 10 + " Room", i + 1 , "-" * 10)
            room = self._get_input("Name of Room %s: " % (i + 1), str).lower().strip()                                      # get name of room
            
            room_size = self._get_input("%s Square Footage: " % (room), float, lambda i: i <= 0, "Room size must be > 0")          # get size of room

            room_shared = self._get_input("Eveyone shares this room: ", str, lambda i: i not in ['yes', 'no', 'true', 'false', 'y', 'n', 't', 'f', '1', '0'], "Input must be: yes, no, true, false, y, n, t, f, 1, or 0").lower().strip()
            room_shared = True if room_shared in ['yes', 'true', 'y', 't', '1'] else False


            self._data["rooms"][room] ={"size": room_size, "sharing": room_shared, "num_share": 0, "total": 0}

        print("-" * 10 + " Rooms People Pay for ", "-" * 10)
        print("List the rooms each person will pay for separated by a \", \".")
        for i in range(0, self._data['num_people']):
            rooms_shared_list = self._get_input("Person " + str(i+1) + ": ", str, lambda i: not(set(i.split(", ")).issubset(self._data['rooms']) or i in self._data['rooms']), "One or more of the rooms are invalid!")
            rooms_shared_list = rooms_shared_list.split(", ")
            for room in rooms_shared_list:
                if self._data['rooms'][room]['sharing']:
                    rooms_shared_list.remove(room)
                else:
                    self._data['rooms'][room]['num_share'] += 1
            self._data['rooms_shared']['person ' + str(i+1)] = rooms_shared_list

        self._calculate()                                                           # calculate each room's amount

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
        Get how much each person owes

        @return dict: key is person #, and value is the amount
        they owe
        """
        per_pay = {}                                                                                    # hold the result
        everyone_sharing_pay = 0                                                                        # amount everyone will share
        
        for room in self._data['rooms']:                                                  # loop rooms
            if self._data['rooms'][room]['sharing']:
                everyone_sharing_pay += self._data['rooms'][room]['total']

        if everyone_sharing_pay != 0: everyone_sharing_pay /= self._data['num_people']

        for person, rooms in self._data['rooms_shared'].items():
            if len(rooms) > 0:
                per_pay[person] = (self._sum({room: self._data['rooms'][room] for room in rooms}, lambda v: v['total'] / v['num_share'])) + everyone_sharing_pay
            else:
                per_pay[person] = everyone_sharing_pay

        return per_pay