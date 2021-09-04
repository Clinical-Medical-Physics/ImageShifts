--this file will return parts of the patient plan that was delivered during a date range
--python code that calls this file should replace the following items
-- strtdate
-- enddate
-- patientId
--Notes on returned values
-- [index] Label
-- 8 Iso X
-- 9 iso Y
-- 10 Iso Z
select distinct RadiationHstry.TreatmentStartTime,CONVERT(VARCHAR(20), RadiationHstry.TreatmentStartTime, 100)as v11TreatmentDateTime,
Course.CourseId,PlanSetup.PlanSetupId,RTPlan.RTPlanId as FractionationId,
RadiationHstry.FractionNumber,RadiationHstry.RadiationId as FieldId,
RadiationHstry.TreatmentDeliveryType,
ExternalFieldCommon.IsoCenterPositionX,ExternalFieldCommon.IsoCenterPositionY,ExternalFieldCommon.IsoCenterPositionZ
from Patient,Course,PlanSetup,Radiation,RadiationHstry,ExternalFieldCommonHstry,RTPlan,Session,ExternalFieldCommon
where (Patient.PatientId='{patientId}')
and (Course.PatientSer=Patient.PatientSer)
and (Course.CourseSer=PlanSetup.CourseSer)
and (PlanSetup.PlanSetupSer=Radiation.PlanSetupSer)
and (Radiation.RadiationSer=RadiationHstry.RadiationSer)
and (RadiationHstry.RadiationHstrySer=ExternalFieldCommonHstry.RadiationHstrySer)
and (Radiation.RadiationSer = ExternalFieldCommon.RadiationSer)
and (RTPlan.PlanSetupSer=PlanSetup.PlanSetupSer)
--and (RadiationHstry.TreatmentDeliveryType like 'TREATMENT')
and (upper(Course.CourseId) not like '%QA%')
and (RadiationHstry.TreatmentStartTime between '{strtdate}' and '{enddate}')
order by RadiationHstry.TreatmentStartTime,v11TreatmentDateTime,RadiationHstry.FractionNumber