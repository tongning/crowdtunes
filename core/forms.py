from django import forms
scoreChoices = (0,1,2,3,4,5)
class scoreForm(forms.Form):
    preferred_drink = forms.ChoiceField(choices=scoreChoices,
                                        widget=forms.RadioSelect())
