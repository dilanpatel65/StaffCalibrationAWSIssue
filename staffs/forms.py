from django import forms
# from django.views import generic
from .models import (
    Staff,
    StaffType,
    DigitalLevel,
    #Surveyors
    )
from datetime import date

class StaffTypeForm(forms.ModelForm):
    class Meta:
        model = StaffType
        fields = ['staff_type', 'thermal_coefficient']
        widgets = {
            'staff_type' : forms.TextInput(attrs={'placeholder':'e.g., Fibreglass, Steel'}),
            'thermal_coefficient' : forms.TextInput(attrs={'placeholder':'Enter value in ppm'})
        }

    def clean_staff_type(self):
        return self.cleaned_data['staff_type'].strip()

class StaffForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        user = kwargs.pop('user', None)
        super(StaffForm, self).__init__(*args, **kwargs)   
        self.base_fields['staff_owner'].initial = user.authority
        if not user.is_staff:
            self.fields['staff_owner'].disabled = True

    class Meta:
        model = Staff
        fields = ['staff_number','staff_type', 'staff_length', 'staff_owner', 'correction_factor','calibration_date']
        readonly = ['correction_factor','calibration_date']
        widgets = {
            'staff_number' : forms.TextInput(attrs={'placeholder':'Enter you staff serial number'}),
            'staff_length' : forms.TextInput(attrs={'placeholder':'Enter length in meters. E.g., 4'}),
            'correction_factor' : forms.TextInput(attrs={'placeholder':'Enter value, if available'}),
            'calibration_date': forms.DateInput(format=('%d-%m-%Y'), attrs={'placeholder':'Select a date', 'type':'date'}),
            }

        error_messages = {
            'staff_number': {
                'unique': 'Choose a different staff number, e.g., LG02365'
            },
            'staff_length': {
                'invalid': 'Please enter a valid staff number'
            },
            'correction_factor': {
                'invalid': 'Please enter a scale factor, if known'
            },
        }

    def clean_staff_number(self):
        return self.cleaned_data['staff_number'].strip()

    def clean_correction_factor(self):
        correction_factor = self.cleaned_data['correction_factor']
        if correction_factor: 
            if correction_factor >= 0.99 or correction_factor <= 1.01:
                return correction_factor
            else:  
                raise forms.ValidationError('The scale factor you have entered is not valid')     

    def clean_calibration_date(self):
        correction_factor = self.cleaned_data['correction_factor']
        calibration_date = self.cleaned_data['calibration_date']

        if calibration_date and not correction_factor:
            raise forms.ValidationError('You have a calibration date but did not provide a corrector factor. If you have a calibration record, provide the details.')
        elif correction_factor and not calibration_date:
            raise forms.ValidationError('You have given a scale factor but no calibration date. If you have a calibration record, provide the details.')
        elif correction_factor and calibration_date:
            if correction_factor < 0.99 or correction_factor > 1.01:
                raise forms.ValidationError('The scale factor you have entered is not valid')   
            elif calibration_date and calibration_date > date.today():
                raise forms.ValidationError('Please provide a valid date of your staff calibration')
            else:
                return calibration_date
        
            

class DigitalLevelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        user = kwargs.pop('user', None)
        super(DigitalLevelForm, self).__init__(*args, **kwargs)   
        self.base_fields['level_owner'].initial = user.authority
        if not user.is_staff:
            self.fields['level_owner'].disabled = True
        #self.fields['staff_type'].queryset = StaffType.objects.all()

    class Meta:
        model = DigitalLevel
        fields = ['level_number','level_make', 'level_model', 'level_owner']
        
        widgets = {
            'level_number' : forms.TextInput(attrs={'placeholder':'Enter you level serial number'}),
            'level_make' : forms.TextInput(attrs={'placeholder':'E.g., Leica, Trimble'}),
            'level_model' : forms.TextInput(attrs={'placeholder':'E.g., DNA03, LS15'}),
            }
        error_messages = {
            'level_number': {
                'unique': 'Choose a different level number, e.g., LG02365'
            },
        }

    def clean_level_number(self):
        return self.cleaned_data['level_number'].strip()

class StaffUpdateForm(forms.ModelForm):

    class Meta:
        model = Staff
        fields = ['user', 'staff_number','staff_type', 'staff_length', 'staff_owner']
        readonly = ['correction_factor','calibration_date']
        widgets = {
            'staff_number' : forms.TextInput(attrs={'placeholder':'Enter you staff serial number'}),
            'staff_length' : forms.TextInput(attrs={'placeholder':'Enter length in meters. E.g., 4'}),
            }

        error_messages = {
            'staff_number': {
                'unique': 'Choose a different staff number, e.g., LG02365'
            },
            'staff_length': {
                'invalid': 'Please enter a valid staff number'
            },
            'correction_factor': {
                'invalid': 'Please enter a correction factor, if known'
            },
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(StaffUpdateForm, self).__init__(*args, **kwargs)
        self.fields['staff_type'].queryset = StaffType.objects.all()
        if not user.is_staff:
            del self.fields['user']
    
    def clean_staff_number(self):
        return self.cleaned_data['staff_number'].strip()

    def clean_staff_length(self):
        staff_length = self.cleaned_data['staff_length']
        if staff_length < 3 and staff_length > 7:
            raise forms.ValidationError('Your staff may be too short or too long') 
        else:
            return staff_length # return self.cleaned_data['staff_length'].strip()

    def clean_correction_factor(self):
        correction_factor = self.cleaned_data['correction_factor']
        if correction_factor: 
            if correction_factor >= 0.99 or correction_factor <= 1.01:
                return correction_factor
            else:  
                raise forms.ValidationError('The scale factor you have entered is not valid')     

    def clean_calibration_date(self):
        correction_factor = self.cleaned_data['correction_factor']
        calibration_date = self.cleaned_data['calibration_date']

        if calibration_date and not correction_factor:
            raise forms.ValidationError('You have a calibration date but did not provide a corrector factor. If you have a calibration record, provide the details.')
        elif correction_factor and not calibration_date:
            raise forms.ValidationError('You have given a scale factor but no calibration date. If you have a calibration record, provide the details.')
        elif correction_factor and calibration_date:
            if correction_factor < 0.99 or correction_factor > 1.01:
                raise forms.ValidationError('The scale factor you have entered is not valid')   
            elif calibration_date and calibration_date > date.today():
                raise forms.ValidationError('Please provide a valid date of your staff calibration')
            else:
                return calibration_date

class DigitalLevelUpdateForm(forms.ModelForm):
    class Meta:
        model = DigitalLevel
        fields = ['user', 'level_number','level_make', 'level_model', 'level_owner']
        
        widgets = {
            'level_number' : forms.TextInput(attrs={'placeholder':'Enter you level serial number'}),
            'level_make' : forms.TextInput(attrs={'placeholder':'E.g., Leica, Trimble'}),
            'level_model' : forms.TextInput(attrs={'placeholder':'E.g., DNA03, LS15'}),
            }
        error_messages = {
            'level_number': {
                'unique': 'Choose a different level number, e.g., LG02365'
            },
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(DigitalLevelUpdateForm, self).__init__(*args, **kwargs)
        if not user.is_staff:
            del self.fields['user']
            
    def clean_level_number(self):
        return self.cleaned_data['level_number'].strip()
