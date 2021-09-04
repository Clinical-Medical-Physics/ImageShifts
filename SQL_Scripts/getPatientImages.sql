--this file will find patient images for given date range
--python code that calls this file should replace the following items
-- strtdate
-- enddate
-- patientId

-- Notes on returned table
-- index Label
-- 0 PatientId
-- 5 SpatialRegistration Transformation Matrix as hex string will need to be converted
-- 9 Image Transformation Matrix
-- 10 Image VolumeTransformation Matrix
-- 11 Image UserOrigin only X,Y,Z here
-- 12 Image DisplayTransformation Matrix
-- 17 Slice Transformation Matrix
-- 18 Slice Couch Lat
-- 19 Slice Couch lng
-- 20 Slice Couch Vrt
-- 21 Slice Couch Rot
-- 22 Slice Couch Pitch
-- 23 Slice Couch Roll
select Patient.PatientId,Patient.LastName,Patient.FirstName,
SpatialRegistration.RegTypeCodeMeaning,SpatialRegistration.RegSubType,SpatialRegistration.Transformation,SpatialRegistration.StatusDate,
Image.CreationDate,Image.StatusDate,Image.Status,
Image.Transformation,Image.VolumeTransformation,Image.UserOrigin,Image.DisplayTransformation,
Image.PatientOrientation,
Slice.CreationDate,Slice.AcquisitionDateTime,Slice.SliceNumber,
Slice.Transformation,
Slice.CouchLat,Slice.CouchLng,Slice.CouchVrt,
Slice.PatientSupportAngle,Slice.PatSupportPitchAngle,Slice.PatSupportRollAngle 
from SpatialRegistrationImage,SpatialRegistration,Image,Patient,Slice,ImageSlice
where Slice.AcquisitionDateTime between '{strtdate}' and '{enddate}'
and SpatialRegistration.SpatialRegistrationSer = SpatialRegistrationImage.SpatialRegistrationSer
and ((SpatialRegistration.RegSubType like 'Online3D%'))--(SpatialRegistration.RegSubType like 'Offline%') or 
and Image.ImageSer = SpatialRegistrationImage.ImageSer
and Image.PatientSer = Patient.PatientSer
and Image.ImageSer = ImageSlice.ImageSer
and ImageSlice.SliceSer = Slice.SliceSer
and Patient.PatientId like '{patientId}'
order by Patient.PatientId,SpatialRegistration.StatusDate,Slice.SliceNumber