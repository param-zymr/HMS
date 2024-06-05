"""Appointment scheduling core logic"""
from datetime import datetime, date, timedelta
from src.app.database.patient_queries.appointments import patient_appointments_query
from src.app.database.doctor_queries.schedule import doctor_schedule_query
from src.app.database.doctor_queries.appointments import doctor_appointment_query
from src.main import app_settings

def check_availibility(data, apnt_id=None):
    if not doctor_schedule_query.check_shift_availibility(data):
        return False
    if apnt_id:
        all_appointments = patient_appointments_query.appointments_list_by_id(data, apnt_id)
    else:
        all_appointments = patient_appointments_query.appointments_list(data)
    availibility = True
    doctor_appointments = []
    apnt_start_temp = datetime.strptime(data["APNT_START_TIME"], "%H:%M") \
        - timedelta(minutes=app_settings.APPOINTMENT_OFFSET)
    apnt_end_temp = datetime.strptime(data["APNT_END_TIME"], "%H:%M") \
        + timedelta(minutes=app_settings.APPOINTMENT_OFFSET)
    if apnt_end_temp - apnt_start_temp < timedelta(minutes=app_settings.APPOINTMENT_MIN_TIME):
        return False
    apnt_start = apnt_start_temp.time()
    apnt_end = apnt_end_temp.time()
    if all_appointments:
        for appointment in all_appointments:
            appointment_timings = (appointment.APNT_START_TIME, appointment.APNT_END_TIME)
            doctor_appointments.append(appointment_timings)
        list_size = len(doctor_appointments)
        if apnt_start < doctor_appointments[list_size-1][1] and \
            apnt_end > doctor_appointments[0][0]:
            availibility = False
            if list_size > 1:
                for i in range(list_size-1):
                    if apnt_start > doctor_appointments[i][1] and \
                        apnt_end < doctor_appointments[i+1][0]:
                        availibility = True
                        break
    return availibility


def availibility_list(doc_id, apnt_date):
    doctor_shift_temp = doctor_schedule_query.get_doctor_shift(doc_id, apnt_date)
    all_appointments = doctor_appointment_query.appointments_list(doc_id, apnt_date)
    doctor_appointments = []
    availibility_list = []
    apnt_offset = app_settings.APPOINTMENT_OFFSET
    apnt_min_time = app_settings.APPOINTMENT_MIN_TIME
    temp_date = date.today()
    if doctor_shift_temp:
        doctor_shift = doctor_shift_temp.__dict__
        shift_start = datetime.combine(temp_date, doctor_shift["SHIFT_START_TIME"]) \
            + timedelta(minutes=apnt_offset)
        shift_end = datetime.combine(temp_date, doctor_shift["SHIFT_END_TIME"]) \
            - timedelta(minutes=apnt_offset)
        if all_appointments:
            for appointment in all_appointments:
                datetime.combine(temp_date, appointment.APNT_END_TIME)
                appointment_timings = (datetime.combine\
                    (temp_date, appointment.APNT_START_TIME)-timedelta(minutes=apnt_offset), \
                    datetime.combine(temp_date, appointment.APNT_END_TIME)\
                    +timedelta(minutes=apnt_offset))
                doctor_appointments.append(appointment_timings)
            list_size = len(doctor_appointments)
            apnt_start_time = shift_start
            apnt_end_time = shift_end
            for i in range(list_size+1):
                if i == list_size:
                    apnt_end_time = shift_end
                else:
                    apnt_end_time = doctor_appointments[i][0]
                if apnt_end_time - apnt_start_time >= timedelta(minutes=apnt_min_time):
                    availibility_list.append((apnt_start_time.time(), apnt_end_time.time()))
                if i < list_size:
                    apnt_start_time = doctor_appointments[i][1]
        else:
            if shift_end - shift_start >= timedelta(minutes=apnt_min_time):
                availibility_list.append((shift_start.time(), shift_end.time()))
    return availibility_list
