from django.db import models


class ClientCountry(models.TextChoices):
    USA = 'USA', 'USA'
    AUSTRALIA = 'Australia', 'Australia'
    CANADA = 'Canada', 'Canada'
    UK = 'UK', 'UK'
    INDIA = 'India', 'India'


class ClientState(models.TextChoices):
    # USA States
    ALABAMA = 'Alabama', 'Alabama'
    ALASKA = 'Alaska', 'Alaska'
    ARIZONA = 'Arizona', 'Arizona'
    ARKANSAS = 'Arkansas', 'Arkansas'
    CALIFORNIA = 'California', 'California'
    COLORADO = 'Colorado', 'Colorado'
    CONNECTICUT = 'Connecticut', 'Connecticut'
    DELAWARE = 'Delaware', 'Delaware'
    FLORIDA = 'Florida', 'Florida'
    GEORGIA = 'Georgia', 'Georgia'
    HAWAII = 'Hawaii', 'Hawaii'
    IDAHO = 'Idaho', 'Idaho'
    ILLINOIS = 'Illinois', 'Illinois'
    INDIANA = 'Indiana', 'Indiana'
    IOWA = 'Iowa', 'Iowa'
    KANSAS = 'Kansas', 'Kansas'
    KENTUCKY = 'Kentucky', 'Kentucky'
    LOUISIANA = 'Louisiana', 'Louisiana'
    MAINE = 'Maine', 'Maine'
    MARYLAND = 'Maryland', 'Maryland'
    MASSACHUSETTS = 'Massachusetts', 'Massachusetts'
    MICHIGAN = 'Michigan', 'Michigan'
    MINNESOTA = 'Minnesota', 'Minnesota'
    MISSISSIPPI = 'Mississippi', 'Mississippi'
    MISSOURI = 'Missouri', 'Missouri'
    MONTANA = 'Montana', 'Montana'
    NEBRASKA = 'Nebraska', 'Nebraska'
    NEVADA = 'Nevada', 'Nevada'
    NEW_HAMPSHIRE = 'New Hampshire', 'New Hampshire'
    NEW_JERSEY = 'New Jersey', 'New Jersey'
    NEW_MEXICO = 'New Mexico', 'New Mexico'
    NEW_YORK = 'New York', 'New York'
    NORTH_CAROLINA = 'North Carolina', 'North Carolina'
    NORTH_DAKOTA = 'North Dakota', 'North Dakota'
    OHIO = 'Ohio', 'Ohio'
    OKLAHOMA = 'Oklahoma', 'Oklahoma'
    OREGON = 'Oregon', 'Oregon'
    PENNSYLVANIA = 'Pennsylvania', 'Pennsylvania'
    RHODE_ISLAND = 'Rhode Island', 'Rhode Island'
    SOUTH_CAROLINA = 'South Carolina', 'South Carolina'
    SOUTH_DAKOTA = 'South Dakota', 'South Dakota'
    TENNESSEE = 'Tennessee', 'Tennessee'
    TEXAS = 'Texas', 'Texas'
    UTAH = 'Utah', 'Utah'
    VERMONT = 'Vermont', 'Vermont'
    VIRGINIA = 'Virginia', 'Virginia'
    WASHINGTON = 'Washington', 'Washington'
    WEST_VIRGINIA = 'West Virginia', 'West Virginia'
    WISCONSIN = 'Wisconsin', 'Wisconsin'
    WYOMING = 'Wyoming', 'Wyoming'
    # Australia States and Territories
    AUSTRALIAN_CAPITAL_TERRITORY = 'Australian Capital Territory', 'Australian Capital Territory'
    NEW_SOUTH_WALES = 'New South Wales', 'New South Wales'
    NORTHERN_TERRITORY = 'Northern Territory', 'Northern Territory'
    QUEENSLAND = 'Queensland', 'Queensland'
    SOUTH_AUSTRALIA = 'South Australia', 'South Australia'
    TASMANIA = 'Tasmania', 'Tasmania'
    VICTORIA = 'Victoria', 'Victoria'
    WESTERN_AUSTRALIA = 'Western Australia', 'Western Australia'
    # UK States and Territories
    ENGLAND = 'England', 'England'
    SCOTLAND = 'Scotland', 'Scotland'
    WALES = 'Wales', 'Wales'
    NORTHERN_IRELAND = 'Northern Ireland', 'Northern Ireland'
    # Canada Provinces and Territories
    ALBERTA = 'Alberta', 'Alberta'
    BRITISH_COLUMBIA = 'British Columbia', 'British Columbia'
    MANITOBA = 'Manitoba', 'Manitoba'
    NEW_BRUNSWICK = 'New Brunswick', 'New Brunswick'
    NEWFOUNDLAND_AND_LABRADOR = 'Newfoundland and Labrador', 'Newfoundland and Labrador'
    NORTHWEST_TERRITORIES = 'Northwest Territories', 'Northwest Territories'
    NOVA_SCOTIA = 'Nova Scotia', 'Nova Scotia'
    NUNAVUT = 'Nunavut', 'Nunavut'
    ONTARIO = 'Ontario', 'Ontario'
    PRINCE_EDWARD_ISLAND = 'Prince Edward Island', 'Prince Edward Island'
    QUEBEC = 'Quebec', 'Quebec'
    SASKATCHEWAN = 'Saskatchewan', 'Saskatchewan'
    YUKON = 'Yukon', 'Yukon'
    # India States and Union Territories
    ANDHRA_PRADESH = 'Andhra Pradesh', 'Andhra Pradesh'
    ARUNACHAL_PRADESH = 'Arunachal Pradesh', 'Arunachal Pradesh'
    ASSAM = 'Assam', 'Assam'
    BIHAR = 'Bihar', 'Bihar'
    CHHATTISGARH = 'Chhattisgarh', 'Chhattisgarh'
    GOA = 'Goa', 'Goa'
    GUJARAT = 'Gujarat', 'Gujarat'
    HARYANA = 'Haryana', 'Haryana'
    HIMACHAL_PRADESH = 'Himachal Pradesh', 'Himachal Pradesh'
    JHARKHAND = 'Jharkhand', 'Jharkhand'
    KARNATAKA = 'Karnataka', 'Karnataka'
    KERALA = 'Kerala', 'Kerala'
    MADHYA_PRADESH = 'Madhya Pradesh', 'Madhya Pradesh'
    MAHARASHTRA = 'Maharashtra', 'Maharashtra'
    MANIPUR = 'Manipur', 'Manipur'
    MEGHALAYA = 'Meghalaya', 'Meghalaya'
    MIZORAM = 'Mizoram', 'Mizoram'
    NAGALAND = 'Nagaland', 'Nagaland'
    ODISHA = 'Odisha', 'Odisha'
    PUNJAB = 'Punjab', 'Punjab'
    RAJASTHAN = 'Rajasthan', 'Rajasthan'
    SIKKIM = 'Sikkim', 'Sikkim'
    TAMIL_NADU = 'Tamil Nadu', 'Tamil Nadu'
    TELANGANA = 'Telangana', 'Telangana'
    TRIPURA = 'Tripura', 'Tripura'
    UTTAR_PRADESH = 'Uttar Pradesh', 'Uttar Pradesh'
    UTTARAKHAND = 'Uttarakhand', 'Uttarakhand'
    WEST_BENGAL = 'West Bengal', 'West Bengal'
    ANDAMAN_AND_NICOBAR_ISLANDS = 'Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'
    CHANDIGARH = 'Chandigarh', 'Chandigarh'
    DADRA_NAGAR_HAVELI_DAMAN_DIU = 'Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'
    DELHI = 'Delhi', 'Delhi'
    JAMMU_AND_KASHMIR = 'Jammu and Kashmir', 'Jammu and Kashmir'
    LADAKH = 'Ladakh', 'Ladakh'
    LAKSHADWEEP = 'Lakshadweep', 'Lakshadweep'
    PUDUCHERRY = 'Puducherry', 'Puducherry'


class Client(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("pending", "Pending"),
        ("progress", "Progress"),
    )

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=50, choices=ClientCountry.choices, default=ClientCountry.INDIA)
    state = models.CharField(max_length=100, choices=ClientState.choices, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    projects_count = models.IntegerField(default=0)
    join_date = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "main_client"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
