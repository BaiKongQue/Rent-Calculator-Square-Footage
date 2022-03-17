from RentCalculator import RentCalculator

if __name__ == "__main__":
    RC = RentCalculator()
    RC.new_apartment()
    print(RC.get_person_pay())