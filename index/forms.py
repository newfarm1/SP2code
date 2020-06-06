from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

class DateImput(forms.DateInput):
    """Class to make date input a HTML5 date picker

    Arguments:
        forms {Django form} -- Django validation and HTML form handling.
    """
    input_type = 'date'

class Add_item(forms.Form):
    """Form for adding new items on only EAN number, storage and experdate

    Arguments:
        forms {Django form} -- Django validation and HTML form handling.
    """
    EAN = forms.IntegerField(help_text = "The barcode of your item/ingredient", required = True)
    expiredate = forms.DateField(widget=DateImput, required = True)
    storage = forms.ChoiceField(choices=[('dry', 'Dry storage'), ('freezer', 'Freezer storage'), ('fridge', 'Fridge storage')],
                                        widget=forms.RadioSelect, initial = 'dry')

     # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('EAN', css_class='input-xlarge'),
        'expiredate',
        'storage',
        FormActions(
            Submit('Submit', 'Submit', css_class="btn-primary"),
        )
    )

class Full_item(forms.Form):
    """Form for adding new items with name, EAN, expiredate, storage and default amount

    Arguments:
        forms {Django form} -- Django validation and HTML form handling.
    """
    name = forms.CharField(help_text = "Name of ingredient/item")
    amount = forms.IntegerField(help_text = "Default amount of the item")
    EAN = forms.IntegerField(help_text = "The barcode of your item/ingredient")
    expiredate = forms.DateField(widget=DateImput)
    storage = forms.ChoiceField(choices=[('dry', 'Dry storage'), ('freezer', 'Freezer storage'), ('fridge', 'Fridge storage')],
                                        widget=forms.RadioSelect, initial = 'dry')

     # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('name', css_class='input-xlarge'),
        'amount',
        'EAN',
        'expiredate',
        'storage',
        FormActions(
            Submit('Submit', 'Submit', css_class="btn-primary")
        )
    )

class Use_item(forms.Form):
    """Form for using an item baced on amount, EAN and storage

    Arguments:
        forms {Django form} -- Django validation and HTML form handling.
    """
    EAN = forms.IntegerField(help_text = "The barcode of your item/ingredient")
    amount = forms.IntegerField(help_text = "The amount you are useing")
    storage = forms.ChoiceField(choices=[('dry', 'Dry storage'), ('freezer', 'Freezer storage'), ('fridge', 'Fridge storage')],
                                        widget=forms.RadioSelect, initial = 'dry')
   

     # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('EAN', css_class='input-xlarge'),
        'amount',
        'storage',
        FormActions(
            Submit('Submit', 'Submit', css_class="btn-primary"),
        )
    )

class Search_item(forms.Form):
    """Form for item/ingredient search by name

    Arguments:
        forms {[type]} -- [description]
    """
    name = forms.CharField(help_text = "Name of ingredient/item")

     # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('name', css_class='input-xlarge'),
        FormActions(
            Submit('Submit', 'Submit', css_class="btn-primary")
        )
    )