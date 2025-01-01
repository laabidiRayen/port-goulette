from models.parking import Parking

# Get all parking spaces
def get_all_parking_spaces():
    return Parking.query.all()

# Get a specific parking space by ID
def get_parking_by_id(id):
    return Parking.query.get(id)

# Book a parking space
def book_parking_space(parking_id, user_id):
    # Assuming ParkingSpace has a status field indicating if it is booked or not
    parking_space = Parking.query.get(parking_id)
    
    if not parking_space:
        return None  # Parking space not found
    
    if parking_space.status == 'booked':
        return None  # Parking space already booked
    
    # Assuming the ParkingSpace model has a booking system
    parking_space.status = 'booked'
    parking_space.user_id = user_id  # Assuming parking space has a `user_id` field
    parking_space.save()  # Save the booking status to the database
    
    return True

# Update a parking space (e.g., mark as occupied or free)
def update_parking_space(id, status):
    parking_space = Parking.query.get(id)
    
    if not parking_space:
        return None  # Parking space not found
    
    parking_space.status = status
    parking_space.save()  # Save the updated status to the database
    
    return parking_space

# Delete a parking space
def delete_parking_space(id):
    parking_space = Parking.query.get(id)
    
    if not parking_space:
        return None  # Parking space not found
    
    parking_space.delete()  # Delete the parking space from the database
    return True
