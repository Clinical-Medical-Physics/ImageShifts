--this file will find all patients treated on the machine for a given date range
--python code that calls this file should replace the following items
-- strtdate
-- enddate
-- activityName
-- machineId

select distinct  Patient.PatientId,Patient.LastName,Patient.FirstName,ScheduledActivity.ScheduledStartTime,ScheduledActivity.ActualStartDate,
ScheduledActivity.ScheduledActivityCode,Hospital.HospitalName,Department.DepartmentName,Activity.ActivityCode,Activity.ObjectStatus,
Patient.PatientSer,Machine.MachineId,vv_ActivityLng.Expression1
from Activity, vv_ActivityLng,Department,Hospital,Patient,ScheduledActivity,Machine,ResourceActivity,ActivityInstance
where (Patient.PatientSer=ScheduledActivity.PatientSer) and
(ActivityInstance.DepartmentSer=Department.DepartmentSer) and
(ScheduledActivity.ActivityInstanceSer=ActivityInstance.ActivityInstanceSer) and
(Department.HospitalSer=Hospital.HospitalSer) and
(ActivityInstance.ActivitySer=Activity.ActivitySer) and
(Activity.ActivityCode=vv_ActivityLng.LookupValue) and
(Machine.ResourceSer=ResourceActivity.ResourceSer) and
(ScheduledActivity.ScheduledActivitySer=ResourceActivity.ScheduledActivitySer) and
((ScheduledActivity.ObjectStatus='Active') and (ScheduledActivity.ScheduledStartTime between '{strtdate}' and '{enddate}')) 
--only look for completed appointments
and (ScheduledActivity.ScheduledActivityCode like '%Complete%')
--look for this activity name 
and (vv_ActivityLng.Expression1 like '{activityName}')
and Machine.MachineId='{machineId}'
--these are needed to remove phantom patients
--could be done on the python side as well 
and (Patient.PatientId not like 'ZZZZ%')
and (Patient.PatientId not like '9999%')