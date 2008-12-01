from django.http import *
from django.db import models
import datetime
from tracker.models import Slip, TimeSlice
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required()
def todays_week(request, user_id):
    if int(request.user.id) != int(user_id):
        return HttpResponseForbidden('Access denied')
    else:
        week = datetime.datetime.now().isocalendar()[1]
        year = datetime.datetime.now().isocalendar()[0]
        return render_to_response('statistics/week.html', {'week' : week, 'year': year, 'user_id': user_id},
                                      context_instance=RequestContext(request))


@login_required()
def week(request, user_id, year, week):
    if int(request.user.id) != int(user_id):
        return HttpResponseForbidden('Access denied')


    return render_to_response('statistics/week.html', {'week': week, 'year': year, 'user_id': user_id},
                                      context_instance=RequestContext(request))


@login_required()
def todays_month(request, user_id):
    if int(request.user.id) != int(user_id):
        return HttpResponseForbidden('Access denied')

    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    return render_to_response('statistics/month.html', {'month' : month, 'year': year, 'user_id': user_id},
                                      context_instance=RequestContext(request))


@login_required()
def month(request, user_id, year, month):
    if int(request.user.id) != int(user_id):
        return HttpResponseForbidden('Access denied')

    return render_to_response('statistics/month.html', {'month' : month, 'year': year, 'user_id': user_id},
                                      context_instance=RequestContext(request))

@login_required()
def date(request, user_id):
    if int(request.user.id) != int(user_id):
        return HttpResponseForbidden('Access denied')

    return render_to_response('statistics/date.html', {'user_id': user_id},
                                      context_instance=RequestContext(request))


def get_data(request, action, data, year, user_id):
    if request.method != 'GET':
         return HttpResponseNotAllowed('GET')

    if action == 'week':
        week = data
        slice_set = TimeSlice.objects.filter(week_number=week, year = year, user = user_id)
        monday = []
        tuesday = []
        wednesday = []
        thursday = []
        friday = []
        saturday = []
        sunday =  []
        names = []
        times = []
        monday_date = tuesday_date = wednesday_date = thursday_date = friday_date = saturday_date = sunday_date = ''

        for slice in slice_set:
            if slice.begin.weekday() == 0:
                if slice.slip not in monday:
                    monday.append(slice.slip)
                    monday_date = slice.create_date
            elif slice.begin.weekday() == 1:
                if slice.slip not in tuesday:
                    tuesday.append(slice.slip)
                    tuesday_date = slice.create_date
            elif slice.begin.weekday() == 2:
                if slice.slip not in wednesday:
                    wednesday.append(slice.slip)
                    wednesday_date = slice.create_date
            elif slice.begin.weekday() == 3:
                if slice.slip not in thursday:
                    thursday.append(slice.slip)
                    thursday_date = slice.create_date
            elif slice.begin.weekday() == 4:
                if slice.slip not in friday:
                    friday.append(slice.slip)
                    friday_date = slice.create_date
            elif slice.begin.weekday() == 5:
                if slice.slip not in saturday:
                    saturday.append(slice.slip)
                    saturday_date = slice.create_date
            else:
                if slice.slip not in sunday:
                    sunday.append(slice.slip)
                    sunday_date = slice.create_date


        week_days = [ monday, tuesday, wednesday, thursday, friday, saturday, sunday]
        j = 0
        date = monday_date
        for day in week_days:
            i=0
            temp = ''
            temp_max = 0.0
            while i < len(day):
                if not temp:
                    temp += '['
                temp += '{ "val" :' + day[i].display_days_time(date) + ', "tip": "' + day[i].name + '<br>day: #x_label#<br>time: #val# total: #total#"}'
                temp_max += float(day[i].display_days_time(date))
                if i != len(day)-1:
                    temp += ','
                if i == len(day)-1:
                    temp += ']'
                i += 1
            if not temp:
                temp = '[0]'
            if j == 0:
                monday_val = temp
                mon_max = temp_max
                date = tuesday_date
            elif j == 1:
                tuesday_val = temp
                tue_max = temp_max
                date = wednesday_date
            elif j == 2:
                date = thursday_date
                wednesday_val = temp
                wed_max = temp_max
            elif j == 3:
                date = friday_date
                thursday_val = temp
                thur_max = temp_max
            elif j == 4:
                date = saturday_date
                friday_val = temp
                fri_max = temp_max
            elif j == 5:
                date = sunday_date
                saturday_val = temp
                sat_max = temp_max
            else:
                sunday_val = temp
                sun_max = temp_max
            j +=1




        max_val = max(mon_max, tue_max, wed_max, thur_max, fri_max, sat_max, sun_max)
        step = max_val/10


        return HttpResponse('{ "elements": [ { "type": "bar_stack",'
                            '"colours": [ "#F00000", "#FFFF00", "#300030", "#000000", "#D54C78", "#D54C78" ],'
                            '"values": ['+ monday_val + ',' + tuesday_val + ',' + wednesday_val + ',' + thursday_val + ',' + friday_val + ',' + saturday_val + ',' + sunday_val +']} ],'
                            '"title": { "text": "Year '+str(year)+' Week ' + str(week) + '" , "style": "{font-size: 20px; color: #F24062; text-align: center;}" },'
                            '"bg_colour": "#FEFEFE",'
                            '"x_axis": { "labels": { "labels": [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" ] } },'
                            '"y_axis": {    "min": 0, "max": '+str(max_val)+', "steps": '+str(step)+' }, "tooltip": { "mouse": 2 } }')

    if action == 'month':
        month = int(data)
        year = int(year)
        slice_set = TimeSlice.objects.filter(user=1, month_number = month, year = year)
        var_1 = []
        var_2 = []
        var_3 = []
        var_4 = []
        var_5 = []
        var_6 = []
        var_7 = []
        var_8 = []
        var_9 = []
        var_10 = []
        var_11 = []
        var_12 = []
        var_13 = []
        var_14 = []
        var_15 = []
        var_16 = []
        var_17 = []
        var_18 = []
        var_19 = []
        var_20 = []
        var_21 = []
        var_22 = []
        var_23 = []
        var_24 = []
        var_25 = []
        var_26 = []
        var_27 = []
        var_28 = []
        var_29 = []
        var_30 = []
        var_31 = []
        # this for loop, will go through a month's timeslices and put the slip of the timeslice
        # into a var, depending on which day the timeslice was created.
        # var_1 will hold all slips that have active timeslices on day 1 ect.
        var_1_date = var_2_date = var_3_date = var_4_date = var_5_date = var_6_date = var_7_date = var_8_date = var_9_date = var_10_date = var_11_date = var_12_date = var_13_date = var_14_date = var_15_date = var_16_date = var_17_date = var_18_date = var_19_date = var_20_date = var_21_date = var_22_date = var_23_date = var_24_date = var_25_date = var_26_date = var_27_date = var_28_date = var_29_date = var_30_date = var_31_date = 0
        for slice in slice_set:
            if slice.day_number <= 16:
                if slice.day_number <= 8:
                    if slice.day_number <=4:
                        if slice.day_number <=2:
                            if slice.day_number == 1:
                                if slice.slip not in var_1:
                                    var_1.append(slice.slip)
                                    var_1_date = slice.create_date

                            else:
                                if slice.slip not in var_2:
                                    var_2.append(slice.slip)
                                    var_2_date = slice.create_date

                        else:
                            if slice.day_number == 3:
                                if slice.slip not in var_3:
                                    var_3.append(slice.slip)
                                    var_3_date = slice.create_date

                            else:
                                if slice.slip not in var_4:
                                    var_4.append(slice.slip)
                                    var_4_date = slice.create_date
                    else:
                        if slice.day_number <=6:
                            if slice.day_number == 5:
                                if slice.slip not in var_5:
                                    var_5.append(slice.slip)
                                    var_5_date = slice.create_date

                            else:
                                if slice.slip not in var_6:
                                    var_6.append(slice.slip)
                                    var_6_date = slice.create_date

                        else:
                            if slice.day_number == 7:
                                if slice.slip not in var_7:
                                    var_7.append(slice.slip)
                                    var_7_date = slice.create_date

                            else:
                                if slice.slip not in var_8:
                                    var_8.append(slice.slip)
                                    var_8_date = slice.create_date
                else:
                    if slice.day_number <=12:
                        if slice.day_number <=10:
                            if slice.day_number == 9:
                                if slice.slip not in var_9:
                                    var_9.append(slice.slip)
                                    var_9_date = slice.create_date

                            else:
                                if slice.slip not in var_10:
                                    var_10.append(slice.slip)
                                    var_10_date = slice.create_date

                        else:
                            if slice.day_number == 11:
                                if slice.slip not in var_11:
                                    var_11.append(slice.slip)
                                    var_11_date = slice.create_date

                            else:
                                if slice.slip not in var_12:
                                    var_12.append(slice.slip)
                                    var_12_date = slice.create_date
                    else:
                        if slice.day_number <=14:
                            if slice.day_number == 13:
                                if slice.slip not in var_13:
                                    var_13.append(slice.slip)
                                    var_13_date = slice.create_date

                            else:
                                if slice.slip not in var_14:
                                    var_14.append(slice.slip)
                                    var_14_date = slice.create_date

                        else:
                            if slice.day_number == 15:
                                if slice.slip not in var_15:
                                    var_15.append(slice.slip)
                                    var_15_date = slice.create_date

                            else:
                                if slice.slip not in var_16:
                                    var_16.append(slice.slip)
                                    var_16_date = slice.create_date
            else:
                if slice.day_number <= 24:
                    if slice.day_number <=20:
                        if slice.day_number <=18:
                            if slice.day_number == 17:
                                if slice.slip not in var_17:
                                    var_17.append(slice.slip)
                                    var_17_date = slice.create_date

                            else:
                                if slice.slip not in var_18:
                                    var_18.append(slice.slip)
                                    var_18_date = slice.create_date

                        else:
                            if slice.day_number == 19:
                                if slice.slip not in var_19:
                                    var_19.append(slice.slip)
                                    var_19_date = slice.create_date

                            else:
                                if slice.slip not in var_20:
                                    var_20.append(slice.slip)
                                    var_20_date = slice.create_date
                    else:
                        if slice.day_number <=22:
                            if slice.day_number == 21:
                                if slice.slip not in var_21:
                                    var_21.append(slice.slip)
                                    var_21_date = slice.create_date

                            else:
                                if slice.slip not in var_22:
                                    var_22.append(slice.slip)
                                    var_22_date = slice.create_date

                        else:
                            if slice.day_number == 23:
                                if slice.slip not in var_23:
                                    var_23.append(slice.slip)
                                    var_23_date = slice.create_date

                            else:
                                if slice.slip not in var_24:
                                    var_24.append(slice.slip)
                                    var_24_date = slice.create_date
                else:
                    if slice.day_number <=28:
                        if slice.day_number <=26:
                            if slice.day_number == 25:
                                if slice.slip not in var_25:
                                    var_25.append(slice.slip)
                                    var_25_date = slice.create_date

                            else:
                                if slice.slip not in var_26:
                                    var_26.append(slice.slip)
                                    var_26_date = slice.create_date

                        else:
                            if slice.day_number == 27:
                                if slice.slip not in var_27:
                                    var_27.append(slice.slip)
                                    var_27_date = slice.create_date

                            else:
                                if slice.slip not in var_28:
                                    var_28.append(slice.slip)
                                    var_28_date = slice.create_date
                    else:
                        if slice.day_number <=30:
                            if slice.day_number == 29:
                                if slice.slip not in var_29:
                                    var_29.append(slice.slip)
                                    var_29_date = slice.create_date

                            else:
                                if slice.slip not in var_30:
                                    var_30.append(slice.slip)
                                    var_30_date = slice.create_date

                        else:
                            if slice.slip not in var_31:
                                var_31.append(slice.slip)
                                var_31_date = slice.create_date



        if month in [1, 3, 5, 7, 8, 10, 12]:
            indicate = 4
        elif month in [4, 6, 9, 11]:
            indicate = 3
        else:
            if year % 4 == 0:
                indicate = 2
            else:
                indicate = 1


        if indicate == 1:
            month_total = [ var_1, var_2, var_3, var_4, var_5, var_6, var_7, var_8, var_9, var_10, var_11, var_12, var_13, var_14, var_15, var_16, var_17, var_18, var_19, var_20, var_21, var_22, var_23, var_24, var_25, var_26, var_27, var_28]
        if indicate == 2:
            month_total = [ var_1, var_2, var_3, var_4, var_5, var_6, var_7, var_8, var_9, var_10, var_11, var_12, var_13, var_14, var_15, var_16, var_17, var_18, var_19, var_20, var_21, var_22, var_23, var_24, var_25, var_26, var_27, var_28, var_29]
        if indicate == 3:
            month_total = [ var_1, var_2, var_3, var_4, var_5, var_6, var_7, var_8, var_9, var_10, var_11, var_12, var_13, var_14, var_15, var_16, var_17, var_18, var_19, var_20, var_21, var_22, var_23, var_24, var_25, var_26, var_27, var_28, var_29, var_30]
        if indicate == 4:
            month_total = [ var_1, var_2, var_3, var_4, var_5, var_6, var_7, var_8, var_9, var_10, var_11, var_12, var_13, var_14, var_15, var_16, var_17, var_18, var_19, var_20, var_21, var_22, var_23, var_24, var_25, var_26, var_27, var_28, var_29, var_30, var_31]


        j = 0
        max_list = [0.01]
        date = var_1_date
        for day in month_total:
            j += 1
            i=0
            temp = ''
            temp_max = 0.0
            while i < len(day):
                if not temp:
                    temp += '['
                temp += '{ "val" :' + day[i].display_days_time(date) + ', "tip": "' + day[i].name + '<br> time: #val# total: #total#"}'
                temp_max += float(day[i].display_days_time(date))
                if i != len(day)-1:
                    temp += ','
                if i == len(day)-1:
                    temp += ']'
                i += 1
            if not temp:
                temp = '[0]'
            if j <= 16:
                if j <= 8:
                    if j <=4:
                        if j <=2:
                            if j == 1:
                                val_1 = temp + ','
                                max_list.append(temp_max)
                                date = var_2_date
                            else:
                                val_2 = temp + ','
                                max_list.append(temp_max)
                                date = var_3_date
                        else:
                            if j == 3:
                                val_3 = temp + ','
                                max_list.append(temp_max)
                                date = var_4_date
                            else:
                                val_4 = temp + ','
                                max_list.append(temp_max)
                                date = var_5_date
                    else:
                        if j <=6:
                            if j == 5:
                                val_5 = temp + ','
                                max_list.append(temp_max)
                                date = var_6_date
                            else:
                                val_6 = temp + ','
                                max_list.append(temp_max)
                                date = var_7_date
                        else:
                            if j == 7:
                                val_7 = temp + ','
                                max_list.append(temp_max)
                                date = var_8_date
                            else:
                                val_8 = temp + ','
                                max_list.append(temp_max)
                                date = var_9_date
                else:
                    if j <=12:
                        if j <=10:
                            if j == 9:
                                val_9 = temp + ','
                                max_list.append(temp_max)
                                date = var_10_date
                            else:
                                val_10 = temp + ','
                                max_list.append(temp_max)
                                date = var_11_date
                        else:
                            if j == 11:
                                val_11 = temp + ','
                                max_list.append(temp_max)
                                date = var_12_date
                            else:
                                val_12 = temp + ','
                                max_list.append(temp_max)
                                date = var_13_date
                    else:
                        if j <=14:
                            if j == 13:
                                val_13 = temp + ','
                                max_list.append(temp_max)
                                date = var_14_date
                            else:
                                val_14 = temp + ','
                                max_list.append(temp_max)
                                date = var_15_date
                        else:
                            if j == 15:
                                val_15 = temp + ','
                                max_list.append(temp_max)
                                date = var_16_date
                            else:
                                val_16 = temp + ','
                                max_list.append(temp_max)
                                date = var_17_date
            else:
                if j <= 24:
                    if j <=20:
                        if j <=18:
                            if j == 17:
                                val_17 = temp + ','
                                max_list.append(temp_max)
                                date = var_18_date
                            else:
                                val_18 = temp + ','
                                max_list.append(temp_max)
                                date = var_19_date
                        else:
                            if j == 19:
                                val_19 = temp + ','
                                max_list.append(temp_max)
                                date = var_20_date
                            else:
                                val_20 = temp + ','
                                max_list.append(temp_max)
                                date = var_21_date
                    else:
                        if j <=22:
                            if j == 21:
                                val_21 = temp + ','
                                max_list.append(temp_max)
                                date = var_22_date

                            else:
                                val_22 = temp + ','
                                max_list.append(temp_max)
                                date = var_23_date

                        else:
                            if j == 23:
                                val_23 = temp + ','
                                max_list.append(temp_max)
                                date = var_24_date

                            else:
                                val_24 = temp + ','
                                max_list.append(temp_max)
                                date = var_25_date
                else:
                    if j <=28:
                        if j <=26:
                            if j == 25:
                                val_25 = temp + ','
                                max_list.append(temp_max)
                                date = var_26_date
                            else:
                                val_26 = temp + ','
                                max_list.append(temp_max)
                                date = var_27_date
                        else:
                            if j == 27:
                                val_27 = temp + ','
                                max_list.append(temp_max)
                                date = var_28_date
                            else:
                                val_28 = temp
                                max_list.append(temp_max)
                                date = var_29_date
                    else:
                        if j <=30:
                            if j == 29:
                                val_29 = temp
                                max_list.append(temp_max)
                                date = var_30_date
                            else:
                                val_30 = temp
                                max_list.append(temp_max)
                                date = var_31_date
                        else:
                            val_31 = temp
                            max_list.append(temp_max)



        if month <= 6:
            if month <=3:
                if month == 1:
                    month_text = 'January'
                elif month == 2:
                    month_text = 'Febuary'
                else:
                    month_text = 'March'
            else:
                if month == 4:
                    month_text = 'April'
                elif month == 5:
                    month_text = 'May'
                else:
                    month_text = 'June'
        else:
            if month <=9:
                if month == 7:
                    month_text = 'July'
                elif month == 8:
                    month_text = 'August'
                else:
                    month_text = 'September'
            else:
                if month == 10:
                    month_text = 'October'
                elif month == 11:
                    month_text = 'November'
                else:
                    month_text = 'December'

        if indicate == 1:
            label = '"1", "2", "3", "4", "5", "6", "7", "8",  "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28"'
        if indicate == 2:
            label = '"1", "2", "3", "4", "5", "6", "7", "8",  "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29"'
        if indicate == 3:
            label = '"1", "2", "3", "4", "5", "6", "7", "8",  "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"'
        if indicate == 4:
            label = '"1", "2", "3", "4", "5", "6", "7", "8",  "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"'


        max_val = max(max_list)
        step = max_val*0.1

        if indicate == 1:
            val_all = val_1 + val_2 + val_3 + val_4 + val_5 + val_6 + val_7 + val_8 + val_9 + val_10 + val_11 + val_12 + val_13 + val_14 + val_15 + val_16 + val_17 + val_18 + val_19 + val_20 + val_21 + val_22 + val_23 + val_24 + val_25 + val_26 + val_27 + val_28
        if indicate == 2:
            val_all = val_1 + val_2 + val_3 + val_4 + val_5 + val_6 + val_7 + val_8 + val_9 + val_10 + val_11 + val_12 + val_13 + val_14 + val_15 + val_16 + val_17 + val_18 + val_19 + val_20 + val_21 + val_22 + val_23 + val_24 + val_25 + val_26 + val_27 + val_28 + ',' + val_29
        if indicate == 3:
            val_all = val_1 + val_2 + val_3 + val_4 + val_5 + val_6 + val_7 + val_8 + val_9 + val_10 + val_11 + val_12 + val_13 + val_14 + val_15 + val_16 + val_17 + val_18 + val_19 + val_20 + val_21 + val_22 + val_23 + val_24 + val_25 + val_26 + val_27 + val_28 + ',' + val_29 + ',' + val_30
        if indicate == 4:
            val_all = val_1 + val_2 + val_3 + val_4 + val_5 + val_6 + val_7 + val_8 + val_9 + val_10 + val_11 + val_12 + val_13 + val_14 + val_15 + val_16 + val_17 + val_18 + val_19 + val_20 + val_21 + val_22 + val_23 + val_24 + val_25 + val_26 + val_27 + val_28 + ',' + val_29 + ',' + val_30 + ',' + val_31

        return HttpResponse('{ "elements": [ { "type": "bar_stack",'
                            '"colours": [ "#F00000", "#FF0000", "#FFF000", "#FFFF00", "#FFFFF0", "#FFFFFF" ],'
                            '"values": ['+ val_all +'],'
                            '"tip": "#y_label# X label [#x_label#], Value [#val#] Total [#total#]" } ],'
                            '"title": { "text": "' + str(year)+ ' ' + month_text + '" , "style": "{font-size: 20px; color: #F24062; text-align: center;}" },'
                            '"x_axis": { "labels": { "labels": [ ' + label + '] } },'
                            '"y_axis": {  "min": 0, "max": '+str(max_val)+', "steps": '+str(step)+' }, "tooltip": { "mouse": 2 } }')


def get_date_data(request, user_id, start_date, end_date):
    # we want start and end date to be lists: [yyyy, mm, dd]:

    s_date = datetime.date(start_date[0], start_date[1], start_date[2])
    e_date = datetime.date(end_date[0], end_date[1], end_date[2])
    w_date = s_date
    dates = {}
    while w_date != e_date:
        dates[w_date]=[]
        w_date += datetime.timedelta(days=1)
    dates[e_date] = []

    slice_set = TimeSlice.objects.filter(user = user_id, create_date__gte=s_date, create_date__lte=e_date)
    for slice in slice_set:
        if slice.slip not in dates[slice.create_date]:
            dates[slice.create_date].append(slice.slip)

    max_list = [0.01]
    for date in dates.keys():
        i=0
        temp = ''
        temp_max = 0.0
        while i < len(dates[date]):
            if not temp:
                temp += '['
            temp += '{ "val" :' + dates[date][i].display_days_time(date) + ', "tip": "' + dates[date][i].name + '<br> time: #val# total: #total#"}'
            temp_max += float(dates[date][i].display_days_time(date))
            if i != len(dates[date])-1:
                temp += ','
            if i == len(dates[date])-1:
                temp += ']'
            i += 1
        if not temp:
            temp = '[0]'
        dates[date] = temp
        max_list.append(temp_max)

    max_val = max(max_list)
    step = max_val*0.1

    label_list = []

    for key in dates.keys():
        label_list.append(key)

    label_list.sort()

    val_all = ''
    for sorted_date in label_list:
        val_all += dates[sorted_date] + ','

    label = ''
    for labl in label_list:
        label += '"' + str(labl.day) +'",'

    return HttpResponse('{ "elements": [ { "type": "bar_stack",'
                            '"colours": [ "#F00000", "#FF0000", "#FFF000", "#FFFF00", "#FFFFF0", "#FFFFFF" ],'
                            '"values": ['+ val_all[:-1] +'],'
                            '"tip": "#y_label# X label [#x_label#], Value [#val#] Total [#total#]" } ],'
                            '"title": { "text": "From ' + str(start_date)+ ' to ' + str(end_date) + '" , "style": "{font-size: 20px; color: #F24062; text-align: center;}" },'
                            '"x_axis": { "labels": { "labels": [ ' + label[:-1] + '] } },'
                            '"y_axis": {  "min": 0, "max": '+str(max_val)+', "steps": '+str(step)+' }, "tooltip": { "mouse": 2 } }')
