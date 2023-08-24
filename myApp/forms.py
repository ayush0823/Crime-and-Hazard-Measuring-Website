from datetime import datetime


class LoginForm():
    def __init__(self, data):
        self.UserName = data['UserName']
        self.Password = data['Password']
    def is_valid(self):
        if (self.UserName == '' or self.Password == ''): 
            return False
        return True

class RegisterationForm():
    def __init__(self, data):
        self.UserName = data['UserName']
        self.FirstName = data['FirstName']
        self.LastName = data['LastName']
        self.Email = data['Email']
        self.Password = data['Password']
        self.ConfirmPassword = data['ConfirmPassword']
        self.DOB = data['DOB']
        self.UpVoted = {'hello': True, 'world': True}
        self.DownVoted = {'hello': True, 'world': True}
    def is_valid(self):
        if (self.Email.find('@') == -1 or self.Email.find('.') == -1):
            return False
        if (self.UserName == '' or self.FirstName == '' or self.LastName == '' or self.Email == '' or self.Password == '' or self.ConfirmPassword == '' or self.DOB == ''):
            return False
        if (self.Password != self.ConfirmPassword):
            return False
        return True
    def to_dict(self):
        return {
            'UserName': self.UserName,
            'FirstName': self.FirstName,
            'LastName': self.LastName,
            'Email': self.Email,
            'Password': self.Password,
            'DOB': self.DOB,
            'upvoted': self.UpVoted,
            'downvoted': self.DownVoted
        }
    
class EditDetailsForm():
    def __init__(self, data):
        self.FirstName = data['FirstName']
        self.LastName = data['LastName']
        self.Email = data['Email']
        self.DOB = data['DOB']
        self.AddressLine1 = data['AddressLine1']
        self.AddressLine2 = data['AddressLine2']
        self.Locality = data['Locality']
        self.Pincode = data['Pincode']
        self.City = data['City']
        self.State = data['State']
        self.Country = data['Country']
        self.Latitude = data['Latitude']
        self.Longitude = data['Longitude']
        self.Mobile = data['Mobile']
        self.Instagram = data['Instagram']
        self.Twitter = data['Twitter']
    def is_valid(self):
        return True
    def to_dict(self):
        return {
            'FirstName': self.FirstName,
            'LastName': self.LastName,
            'Email': self.Email,
            'DOB': self.DOB,
            'AddressLine1': self.AddressLine1,
            'AddressLine2': self.AddressLine2,
            'Locality': self.Locality,
            'Pincode': self.Pincode,
            'City': self.City,
            'State': self.State,
            'Country': self.Country,
            'Latitude': self.Latitude,
            'Longitude': self.Longitude,
            'Mobile': self.Mobile,
            'Instagram': self.Instagram,
            'Twitter': self.Twitter
        }

class PostIncidentForm():
    def __init__(self, data, username):
        self.title = data['Title']
        self.description = data['Description']
        self.longitude = float(data['Longitude'])
        self.latitude = float(data['Latitude'])
        self.author = username

        incident_type_mapping = {
            'Fire': 1,
            'Flood': 2,
            'Earthquake': 3,
            'Landslide': 4,
            'Tsunami': 5,
            'Virus and Bacteria': 6,
            'Cyclone': 7,
            'Drought': 8,
            'Forest Fire': 9,
            'Industrial Accident': 10,
            'Tax Fraud': 11,
            'Money Laundering': 12,
            'Theft': 13,
            'Smuggling': 14,
            'CyberCrime': 15,
            'Bribe': 16,
            'Hit and Run': 17,
            'Kidnap': 18,
            'Rape': 19
        }

        self.incident_type = incident_type_mapping.get(data['IncidentType'], 20)
        self.time = data['Time']
        self.is_authentic = False
        self.upvotes = 0
        self.downvotes = 0
        self.post_ID = username + datetime.now().strftime("%m%d%Y%H%M%S")
    def is_valid(self):
        if (self.title == '' or self.description == '' or self.longitude == '' or self.latitude == '' or self.author == '' or self.incident_type == '' or self.time == ''):
            return False
        return True
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'author': self.author,
            'incident_type': self.incident_type,
            'time': self.time,
            'is_authentic': self.is_authentic,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'post_ID': self.post_ID
        }
    
class PostPropertyForm():
    def __init__(self, data, username):
        self.title = data['Title']
        self.description = data['Description']
        self.longitude = float(data['Longitude'])
        self.latitude = float(data['Latitude'])
        self.author = username
        self.score = 0
        self.pincode = int(data['Pincode'])
        self.city = data['City']
        self.state = data['State']
        self.country = data['Country']
        self.address_line1 = data['AddressLine1']
        self.address_line2 = data['AddressLine2']
        self.post_ID = username + datetime.now().strftime("%m%d%Y%H%M%S")
    def is_valid(self):
        if (self.title == '' or self.description == '' or self.longitude == '' or self.latitude == '' or self.author == '' or self.pincode == '' or self.city == '' or self.state == '' or self.country == '' or self.address_line1 == '' or self.address_line2 == ''):
            return False
        return True
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'author': self.author,
            'score': self.score,
            'pincode': self.pincode,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'post_ID': self.post_ID
        }
    
class ChangePasswordForm():
    def __init__(self, data):
        self.UserName = data['UserName']
        self.DOB = data['DOB']
        self.new_password = data['newPassword']
        self.confirm_password = data['confirmNewPassword']
    def is_valid(self):
        if (self.UserName == '' or self.DOB == '' or self.new_password == '' or self.confirm_password == ''): 
            return False
        if (self.new_password != self.confirm_password):
            return False
        return True
    
class ForgotPasswordForm():
    def __init__(self, data):
        self.UserName = data['UserName']
        self.DOB = data['DOB']
    def is_valid(self):
        if (self.UserName == '' or self.DOB == ''):
            return False
        return True