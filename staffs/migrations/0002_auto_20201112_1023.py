# Generated by Django 3.1 on 2020-11-12 02:23
import csv
from django.db import migrations, models
from datetime import datetime
# Start migration
def add_landgate_staffs(apps, schema_editor):
	try:
		StaffType = apps.get_model("staffs", "StaffType")
		with open("assets/staff_data/staff_types.csv", 'r') as f:
			reader = csv.reader(f); header = next(reader)
			for row in reader:
				staff_type = StaffType.objects.create(staff_type = row[0], thermal_coefficient = row[1])

		
		Staff = apps.get_model("staffs", "Staff")
		with open("assets/staff_data/staffs.csv", 'r') as f:
			reader = csv.reader(f); header = next(reader)
			for row in reader:
				#print(row)
				calibration_date  = datetime.strptime(row[5], "%d/%m/%Y")
				staff_type = StaffType.objects.get(staff_type= row[1])
				staff = Staff.objects.create(
										user_id = 1,
										#authority_id = 2,
										staff_number = row[0], 
										staff_type = staff_type,
										staff_length = row[2],
										standard_temperature = row[3],
										correction_factor = row[4],
										calibration_date = calibration_date)
		
		DigiLevel = apps.get_model("staffs", "DigitalLevel")
		with open("assets/staff_data/digital_levels.csv", 'r') as f:
			reader = csv.reader(f); header = next(reader)
			for row in reader:
				digilevel = DigiLevel.objects.create(
													user_id = 1,
													#authority_id = 2,
													level_number = row[0], 
													level_make = row[1],
													level_model = row[2])

	except:
		pass



def reverse_func(apps, schema_editor):
	try:
		StaffType = apps.get_model("staffs", "StaffType")
		StaffType.objects.all().delete()

		Staff = apps.get_model("staffs", "Staff")
		Staff.objects.all().delete()

		DigiLevel = apps.get_model("staffs", "DigitalLevel")
		DigiLevel.objects.all().delete()
	except:
		pass


class Migration(migrations.Migration):

    dependencies = [
        ('staffs', '0001_initial'),
    ]

    operations = [
        	migrations.RunPython(add_landgate_staffs, reverse_func),
    ]
