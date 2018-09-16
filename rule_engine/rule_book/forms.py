from django import forms
from .rule_creation import rule_provider

class rule_form(forms.Form):
    signal = forms.ChoiceField(choices=[item for item in rule_provider.retrieve()],
                            widget=forms.Select(attrs={
                                    'onchange':"getval()",
                                    'required' : 'true',
                                    'style' : 'align-content: center;margin-left:45%;border-radius:10px;height:30px;width:200px',
                            }))

    NewRule = forms.CharField(max_length=40, widget=forms.TextInput(attrs={
        'placeholder': 'Add new Rule', 'readonly': 'readonly',
        'style' : 'align-content: center;margin-left:45%;border-radius:10px;height:30px;width:200px',
    }))

    value_choices = (
        ("empty", "Select value type"),
        ("Integer", "Integer"),
        ("String", "String"),
        ("Datetime", "Datetime"),
    )
    value_type = forms.ChoiceField(choices=value_choices, widget=forms.Select(attrs={
        "required" : 'true', 'onchange' : "setting_dateTime()",'style' : 'align-content: center;margin-left:45%;border-radius:10px;height:30px;width:200px',
    }))
    
    value = forms.CharField(max_length=40, widget=forms.TextInput(attrs={
        'placeholder': 'Input signal value',
        "required" : 'true',
        'style' : 'align-content: center;margin-left:45%;border-radius:10px;height:30px;width:200px',
    }))


class display(forms.Form):
    regex_invalidated_data = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder' : "Regex invalidated data",
        'readonly': 'readonly',
        'style' : 'width: 100%',
        'rows' : '5',
    }))
    
    rule_invalidated_data = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder' : "Rule invalidated data",
        'readonly': 'readonly',
        'style' : 'width: 100%',
        'rows' : '5',
    }))

    accepted_data = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder' : "Accepted data",
        'readonly': 'readonly',
        'style' : 'width: 100%',
        'rows' : '5',
    }))