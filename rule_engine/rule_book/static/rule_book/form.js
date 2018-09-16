function getval()
{
    document.getElementById("id_NewRule").value = "";
    document.getElementById("id_NewRule").readOnly = false;
    document.getElementById("id_sig_name").innerHTML = "";
    document.getElementById("id_success").innerHTML = "";
    if(document.getElementById("id_signal").value == "Input Signal Name")
    {
        document.getElementById("id_sig_name").innerHTML = "    Enter Signal name";
    }
    else
    {
        document.getElementById("id_NewRule").readOnly = true;
        document.getElementById("id_NewRule").value= document.getElementById("id_signal").value ;

    }
}

function validate()
{
    var new_rule = document.getElementById("id_NewRule").value;
    var result = new_rule.match(/^ATL[0-9]+$/);
    document.getElementById("id_error").value = "";
    if(!result)
    {
        document.getElementById("id_error").innerHTML = "Signal name must be of form [ATL followed by digits from 0-9]\n";
        return false;
    }

    var val = document.getElementById("id_value").value;
    var val_type = document.getElementById("id_value_type").value;
    switch(val_type)
    {
        case "Integer":
            result = val.match(/^[0-9]+[-][0-9]+$/);
            if(!result)
            {
                document.getElementById("id_error").innerHTML = "Range value must be integer type [int-int]\n";
                return false;
            }
            break;
        case "String":
            result = val.match(/^[a-zA-Z]+$/);
            if(!result)
            {
                document.getElementById("id_error").innerHTML = "Value must be of String type [[A-Za-z]]\n";
                return false;
            }
        }
        

}

function padding_date_str(arg)
{
    return ('0' + arg).slice(-2)
}
function setting_dateTime()
{
    document.getElementById("id_format").innerHTML = "";
    document.getElementById("id_success").innerHTML = "";
    document.getElementById("id_value").value= "";
    document.getElementById("id_value").readOnly = false;
    if(document.getElementById("id_value_type").value == "Datetime")
    {
        var today = new Date();
        var date_string = today.getFullYear()+"-"+padding_date_str(today.getMonth())+"-"+
                padding_date_str(today.getDate())+" "+padding_date_str(today.getHours())+
                    ":"+padding_date_str(today.getMinutes())+":"+padding_date_str(today.getSeconds());
        document.getElementById("id_value").value = date_string;
        document.getElementById("id_value").readOnly = true;
    }
    else if(document.getElementById("id_value_type").value == "Integer")
    {
        document.getElementById("id_format").innerHTML = "    Format [int-int Ex : 0-240 inclusive of boundary value]";
    }
}