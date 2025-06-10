from collections import defaultdict
from collections import deque
import time

MAX_SLOTS_REGULAR = 30
MAX_SLOTS_ELECTRIC = 20
MAX_SLOTS_HANDICAPPED = 10
MAX_SLOTS = MAX_SLOTS_REGULAR + MAX_SLOTS_ELECTRIC + MAX_SLOTS_HANDICAPPED
MAX_PARKING_TIME = 5
WAITLIST = deque()

class ParkingSystem:
    
    def __init__(self):
        self.regular = {}
        self.electric = {}
        self.handicapped = {}
       
        self.regular_next_key = 1
        self.electric_next_key = 1
        self.handicapped_next_key = 1

    def add_cars(self, car_type: str, license_plate: str) -> dict:
        entry_time = time.time()  
        
        if car_type == "regular":
            if len(self.regular) < MAX_SLOTS_REGULAR:
                key = self.regular_next_key
                self.regular[key] = [car_type, license_plate, entry_time]
                self.regular_next_key += 1
                parking_ticket = {"car_type": car_type, "slot": key, "license_plate": license_plate, "entry_time": entry_time}
            else:
                WAITLIST.append([car_type, license_plate])
                return "Slots full!"
                
        elif car_type == "electric":  
            if len(self.electric) < MAX_SLOTS_ELECTRIC:
                key = self.electric_next_key
                self.electric[key] = [car_type, license_plate, entry_time]
                self.electric_next_key += 1
                parking_ticket = {"car_type": car_type, "slot": key, "license_plate": license_plate, "entry_time": entry_time}
            else:
                WAITLIST.append([car_type, license_plate])
                return "Slots full!"
                
        elif car_type == "handicapped":
            if len(self.handicapped) < MAX_SLOTS_HANDICAPPED:
                key = self.handicapped_next_key
                self.handicapped[key] = [car_type, license_plate, entry_time]
                self.handicapped_next_key += 1
                parking_ticket = {"car_type": car_type, "slot": key, "license_plate": license_plate, "entry_time": entry_time}
            else:
                WAITLIST.append([car_type, license_plate])
                return "Slots full!"
        else:
            return "Invalid car type!"
             
        return parking_ticket  
                
    def calculate_duration_fee(self, parking_ticket: dict) -> int:
        entry_time = parking_ticket["entry_time"]
        exit_time = time.time()
        
        
        duration_seconds = exit_time - entry_time
        duration_hours = duration_seconds / 3600  
        fee = 40 * duration_hours
        
        if duration_hours > MAX_PARKING_TIME:
            fee += 10 * (duration_hours - MAX_PARKING_TIME)
        
        key = parking_ticket["slot"]
        car_type = parking_ticket["car_type"]
        
        
        if car_type == "regular":
            if key in self.regular:
                del self.regular[key]
        elif car_type == "electric":
            if key in self.electric:
                del self.electric[key]
        elif car_type == "handicapped":
            if key in self.handicapped:
                del self.handicapped[key]
        
       
        if WAITLIST:
            wait_car = WAITLIST.popleft()
            self.add_cars(wait_car[0], wait_car[1])
        
        return fee
    
    def reservation(self, name: str, car_type: str, ph_no: int):
        if car_type == "regular":
            if len(self.regular) < MAX_SLOTS_REGULAR:
                key = self.regular_next_key
                self.regular[key] = [name, car_type, ph_no]
                self.regular_next_key += 1
                return {"reservation_id": key, "car_type": car_type, "name": name}
            else:
                return "Slots full!"
                
        elif car_type == "electric":
            if len(self.electric) < MAX_SLOTS_ELECTRIC:
                key = self.electric_next_key
                self.electric[key] = [name, car_type, ph_no]
                self.electric_next_key += 1
                return {"reservation_id": key, "car_type": car_type, "name": name}
            else:
                return "Slots full!"
                
        elif car_type == "handicapped":
            if len(self.handicapped) < MAX_SLOTS_HANDICAPPED:
                key = self.handicapped_next_key
                self.handicapped[key] = [name, car_type, ph_no]
                self.handicapped_next_key += 1
                return {"reservation_id": key, "car_type": car_type, "name": name}
            else:
                return "Slots full!"
        else:
            return "Invalid car type!"


if __name__ == "__main__":
    instance = ParkingSystem()
    check_1 = instance.add_cars("regular", "TN046756")
    print(check_1)
   
    if isinstance(check_1, dict):  
        fee = instance.calculate_duration_fee(check_1)
        print(f"Parking fee: {fee}")
    
    
    reservation = instance.reservation("John Doe", "electric", 1234567890)
    print(reservation)