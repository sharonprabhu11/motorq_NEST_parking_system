from collections import deque
import time
from enum import Enum
from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Tuple, Any


class ParkingSpaceType(Enum):
    REGULAR = "regular"
    ELECTRIC = "electric"
    HANDICAPPED = "handicapped"


class ParkingSpace:
    
    def __init__(self, space_id: int, space_type: ParkingSpaceType):
        self.space_id = space_id
        self.space_type = space_type
        self.is_occupied = False
        self.is_reserved = False
        self.car = None
        self.entry_time = None
        self.reservation_info = None
    
    def occupy(self, car, entry_time: float) -> None:
        if self.is_occupied or self.is_reserved:
            raise ValueError("Parking space is already occupied or reserved")
        
        self.is_occupied = True
        self.car = car
        self.entry_time = entry_time
    
    def vacate(self) -> Tuple[Any, float]:
        if not self.is_occupied:
            raise ValueError("Parking space is not occupied")
        
        car = self.car
        entry_time = self.entry_time
        
        self.is_occupied = False
        self.car = None
        self.entry_time = None
        
        return car, entry_time
    
    def reserve(self, reservation_info: Dict) -> None:
        if self.is_occupied or self.is_reserved:
            raise ValueError("Parking space is already occupied or reserved")
        
        self.is_reserved = True
        self.reservation_info = reservation_info
    
    def cancel_reservation(self) -> Dict:
        if not self.is_reserved:
            raise ValueError("Parking space is not reserved")
        
        info = self.reservation_info
        self.is_reserved = False
        self.reservation_info = None
        
        return info


class Car:
    """Class representing a car"""
    
    def __init__(self, license_plate: str, space_type: ParkingSpaceType):
        self.license_plate = license_plate
        self.space_type = space_type


class ParkingLot:
    """Class managing the entire parking lot"""

    MAX_SLOTS = {
        ParkingSpaceType.REGULAR: 30,
        ParkingSpaceType.ELECTRIC: 20,
        ParkingSpaceType.HANDICAPPED: 10
    }
    
    BASE_HOURLY_RATE = 40  # $40 per hour
    OVERTIME_HOURLY_RATE = 10  # Additional $10 per hour after MAX_PARKING_TIME
    MAX_PARKING_TIME = 5  # Hours
    
    def __init__(self):
        self.spaces: Dict[ParkingSpaceType, List[ParkingSpace]] = {
            space_type: [] for space_type in ParkingSpaceType
        }
        
        for space_type in ParkingSpaceType:
            for i in range(1, self.MAX_SLOTS[space_type] + 1):
                self.spaces[space_type].append(ParkingSpace(i, space_type))
        
    
        self.waitlist: Dict[ParkingSpaceType, deque] = {
            space_type: deque() for space_type in ParkingSpaceType
        }
    
        self.tickets = {}
        self.ticket_counter = 1
    
    def _find_available_space(self, space_type: ParkingSpaceType) -> Optional[ParkingSpace]:
        for space in self.spaces[space_type]:
            if not space.is_occupied and not space.is_reserved:
                return space
        return None
    
    def park_car(self, license_plate: str, space_type_str: str) -> Dict:
        try:
            space_type = ParkingSpaceType(space_type_str)
        except ValueError:
            raise ValueError(f"Invalid parking space type: {space_type_str}")

        space = self._find_available_space(space_type)
        
        if not space:
            car = Car(license_plate, space_type)
            self.waitlist[space_type].append(car)
            return {"status": "waitlisted", "message": "No available spaces. Added to waitlist."}
        
        car = Car(license_plate, space_type)
        entry_time = time.time()
        space.occupy(car, entry_time)
        
        ticket_id = self.ticket_counter
        self.ticket_counter += 1
        
        ticket = {
            "ticket_id": ticket_id,
            "space_type": space_type.value,
            "space_id": space.space_id,
            "license_plate": license_plate,
            "entry_time": entry_time
        }
        
        self.tickets[ticket_id] = (space_type, space.space_id)
        
        return ticket
    
    def exit_car(self, ticket_id: int) -> Dict:
        if ticket_id not in self.tickets:
            raise ValueError(f"Invalid ticket ID: {ticket_id}")
        
        space_type, space_id = self.tickets[ticket_id]
        
        space = next(s for s in self.spaces[space_type] if s.space_id == space_id)
     
        car, entry_time = space.vacate()
        
        exit_time = time.time()
        duration_hours = (exit_time - entry_time) / 3600
        
        fee = self.BASE_HOURLY_RATE * duration_hours
        
        if duration_hours > self.MAX_PARKING_TIME:
            overtime_hours = duration_hours - self.MAX_PARKING_TIME
            fee += self.OVERTIME_HOURLY_RATE * overtime_hours
        
        if self.waitlist[space_type]:
            waiting_car = self.waitlist[space_type].popleft()
            space.occupy(waiting_car, time.time())
        
        del self.tickets[ticket_id]
        
        return {
            "status": "success",
            "license_plate": car.license_plate,
            "duration_hours": duration_hours,
            "fee": round(fee, 2)
        }
    
    def make_reservation(self, name: str, space_type_str: str, phone_number: str) -> Dict:
        try:
            space_type = ParkingSpaceType(space_type_str)
        except ValueError:
            raise ValueError(f"Invalid parking space type: {space_type_str}")
        
        # Find an available space
        space = self._find_available_space(space_type)
        
        if not space:
            return {"status": "failed", "message": "No available spaces for reservation."}
        
        # Create reservation info
        reservation_id = self.ticket_counter
        self.ticket_counter += 1
        
        reservation_info = {
            "reservation_id": reservation_id,
            "name": name,
            "phone_number": phone_number,
            "space_type": space_type.value,
            "space_id": space.space_id
        }
        
        # Reserve the space
        space.reserve(reservation_info)
        
        return {
            "status": "success",
            "reservation_id": reservation_id,
            "space_type": space_type.value,
            "space_id": space.space_id
        }
    
    def cancel_reservation(self, reservation_id: int) -> Dict:
        """Cancel a reservation"""
        # Find the space with this reservation
        for space_type in ParkingSpaceType:
            for space in self.spaces[space_type]:
                if (space.is_reserved and 
                    space.reservation_info and 
                    space.reservation_info.get("reservation_id") == reservation_id):
                    
                    info = space.cancel_reservation()
                    
                    return {
                        "status": "success",
                        "message": f"Reservation {reservation_id} cancelled successfully."
                    }
        
        return {"status": "failed", "message": f"Reservation {reservation_id} not found."}
    
    def get_availability(self) -> Dict:
        """Get availability information for all parking space types"""
        availability = {}
        
        for space_type in ParkingSpaceType:
            available = sum(1 for space in self.spaces[space_type] 
                          if not space.is_occupied and not space.is_reserved)
            total = len(self.spaces[space_type])
            waitlist_count = len(self.waitlist[space_type])
            
            availability[space_type.value] = {
                "available": available,
                "total": total,
                "occupied": total - available,
                "waitlist": waitlist_count
            }
        
        return availability



if __name__ == "__main__":
    parking_lot = ParkingLot()
    
    # Park some cars
    print("Parking a regular car:")
    ticket = parking_lot.park_car("TN046756", "regular")
    print(ticket)
    
    # Check availability
    print("\nCurrent availability:")
    availability = parking_lot.get_availability()
    print(availability)
    
    # Make a reservation
    print("\nMaking a reservation:")
    reservation = parking_lot.make_reservation("John Doe", "electric", "1234567890")
    print(reservation)
    
    # Let car exit
    print("\nCar exiting:")
    time.sleep(2)  # Wait a bit to simulate time passing
    exit_info = parking_lot.exit_car(ticket["ticket_id"])
    print(exit_info)
    
    print("\nUpdated availability:")
    availability = parking_lot.get_availability()
    print(availability)