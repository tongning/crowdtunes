from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML
from crispy_forms.bootstrap import StrictButton, InlineRadios, Field, FieldWithButtons

scoreChoices = ((0,'0'),
                (1, '1'),
                (2, '2'),
                (3, '3'),
                (4, '4'),
                (5, '5'),)
class ScoreForm(forms.Form):
    chosenScore = forms.ChoiceField(label='How would you rate this?',
                                    choices=scoreChoices)

    def __init__(self, *args, **kwargs):
        super(ScoreForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(


            InlineRadios('chosenScore'),

            StrictButton('Vote', css_class='btn-success', type='submit')

        )


