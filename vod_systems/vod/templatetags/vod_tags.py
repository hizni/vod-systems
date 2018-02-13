from django import template
from datetime import timedelta, datetime

register = template.Library()


def days_between(d1, d2):
    return abs((d2 - d1).days)

@register.simple_tag
def bilirubin_rating(data):

    test_value = data.data_value

    if test_value < 34:
        return_value = 0
    elif test_value >= 34 and test_value < 51:
        return_value = 1
    elif test_value >= 51 and test_value < 85:
        return_value = 2
    elif test_value >= 85 and test_value < 136:
        return_value = 3
    elif test_value >= 136:
        return_value = 4
    else:
        return_value = 99

    return str(return_value) + " ( +" + str(days_between(data.fk_transplant_day_zero, data.data_date)) + " d )"

@register.simple_tag
def renal_function_grade(data, transplant_start_renal_fn):

    test_value = data.data_value
    calculated_val = test_value/ transplant_start_renal_fn
    if calculated_val < 1.2:
        return_value = 1
    elif calculated_val >= 1.2 and calculated_val < 1.5:
        return_value = 2
    elif calculated_val >= 1.5 and calculated_val < 2:
        return_value = 3
    elif calculated_val >= 2:
        return_value = 4
    else:
        return_value = 99

    return str(return_value) + " ( +" + str(days_between(data.fk_transplant_day_zero, data.data_date)) + " d )"

@register.simple_tag
def weight_grade(data, transplant_start_weight):

    data_value = data.data_value
    calculated_value = ((data_value - transplant_start_weight) / data_value) * 100
    if calculated_value < 5:
        return_value = 1
    elif calculated_value >= 5 and calculated_value < 10:
        return_value = 2.5
    elif calculated_value >= 10:
        return_value = 4
    else:
        return_value = 99

    return str(return_value) + " ( +" + str(days_between(data.fk_transplant_day_zero, data.data_date)) + " d )"

@register.simple_tag
def classical_vod(transplant_date, start_weight, bilirubin_data, weight_data):

    # intialise trigger boolean variables
    bilirubin_trigger = False
    weight_trigger = False
    hepatomegaly_trigger = False
    ascites_trigger = False

    # iterate through bilirubin results within +21 days from transplant
    # and check if bilirubin >= 2 mg/dl (or >= 34 umol/L)
    for i in bilirubin_data:
        if i.data_date < (transplant_date + timedelta(days=21)):
            if i.fk_data_type == 'serum-total-bilirubin-micromol-litre':
                if i.data_value >= 34:
                    bilirubin_trigger = True

            # include following stanza if bilirubin results may be measured using miligram per litre
            # if i.fk_data_type == 'serum-total-bilirubin-milligram-litre':
            #     if i.data_value >= 2:
            #         bilirubin_trigger = True

    # if bilirubin trigger was true, check other results for triggering criteria
    if bilirubin_trigger:
        # weight data test
        min_weight_gain = start_weight * 1.05
        for i in weight_data:
            if i.data_date < (transplant_date + timedelta(days=21)):
                if i.fk_data_type == 'weight-kilos':
                    if i.data_value >= min_weight_gain:
                        weight_trigger = True

        #TODO - add painful hepatomegaly observed

        #TODO - add ascites observed

    if bilirubin_trigger:
        if (weight_trigger and hepatomegaly_trigger) \
                or (weight_trigger and ascites_trigger) \
                or (hepatomegaly_trigger and ascites_trigger):
            return True

    return False


@register.simple_tag
def new_vod_severity(transplant_date, start_weight, bilirubin_data, weight_data, renal_fn_data):
    #TODO - add logic to implement new VOD severity grading
    return True
