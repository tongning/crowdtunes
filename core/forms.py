from django import forms
scoreChoices = ((0,'0'),
                (1, '1'),
                (2, '2'),
                (3, '3'),
                (4, '4'),
                (5, '5'),)
class ScoreForm(forms.Form):
    chosenScore = forms.ChoiceField(choices=scoreChoices,
                                        widget=forms.RadioSelect())
