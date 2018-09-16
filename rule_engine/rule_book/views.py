from django.shortcuts import render, redirect
from .forms import rule_form, display
from.rule_creation import rule_provider, display_content
from .models import Mymodel

# Create your views here.

def rule(request, id = ""):
    if request.method == 'POST':
        rule = rule_form(request.POST)
        if rule.is_valid():
            if rule.cleaned_data['value_type'] == "String":
                rule.cleaned_data['value'] = rule.cleaned_data['value'].upper()
            r = rule_provider()
            r.add(rule.cleaned_data['NewRule'], rule.cleaned_data['value'], rule.cleaned_data['value_type'])
            
            return redirect('rule', "2")

    else:
        rule = rule_form()
        d = display_content()
        last_five = Mymodel.objects.all().order_by('-id')[:5]
        last_five_in_ascending_order = reversed(last_five)

        accepted_data = []
        for item in last_five_in_ascending_order:
            accepted_data.append(item.timestamp+" ====> "+item.data)

        regex_invalidated = d.read_regex_invalidated_file()
        rule_invalidated = d.read_rule_invalidated_file()

        if id == "2":
            success = "New Rules successfully added"
        else:
            success = "false"
        dis = display(initial={'regex_invalidated_data': "\n".join(regex_invalidated), 'rule_invalidated_data' : "\n".join(rule_invalidated),'accepted_data' : "\n".join(accepted_data)})
        context = {'rule': rule, 'dis':dis, 'success' : success }

        return render(request, 'rule_book/rule_book.html', context)
