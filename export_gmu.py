#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import uuid
import pytz
import xlrd
from xml.dom import minidom
from datetime import datetime
from importlib import reload

# Словарь регистрационных номеров учреждений, связано с тем что Смета не заполняет Рег номер.
regNum_Dict={
'3819009241':'25301853',
'3819020799':'25301856',
'3819005744':'25301852',
'3819009266':'25301854',
'3819009555':'25301858',
'3819019200':'253Г8833',
'3819009080':'25301832',
'3851009415':'253D0188',
'3819000337':'25302220',
'3819009315':'25301960',
'3819009516':'25301836',
'3819009770':'25301838',
'3819009330':'25301834',
'3819009040':'25301846',
'3819009805':'25302139',
'3819009234':'25301844',
'3819014788':'25301850',
'3819009227':'25302313',
'3819009604':'25301840',
'3819009523':'25301956',
'3819009629':'25302417',
'3819009280':'25301955',
'3819009562':'25301952',
'3819012491':'25302049',
'3819009273':'25302112',
'3819009467':'25302045',
'3819009107':'25302047',
'3819009403':'25301987',
'3819005381':'25302005',
'3819009474':'25302040',
'3819008689':'25302204',
'3819009354':'25302131',
'3819008671':'25302206',
'3819009210':'25302119',
'3819011949':'253Г8006',
'3819005790':'25302435',
'3819016344':'253Ц5329',
'3819012484':'25302217',
'3819014682':'253Ц5304',
'3819009643':'25302306',
'3819009153':'25302455',
'3851007707':'25325036',
'3819009139':'25302326',
'3819009308':'25302359',
'3819009428':'25302456',
'3819005470':'25302307',
'3819009185':'25302314',
'3819003472':'25302218',
'3819009298':'25302385',
'3819012501':'25302219',
'3819009393':'25301861',
'3819021785':'253J4929',
'3819005127':'253J4931',
'3819021168':'253Е8490',
'3819009202':'25301842',
'3819009259':'25301848',
'3819009450':'25302048',
'3851007457':'25305276',
'3851025463':'253Ж3920',
'3819009322':'25301859',
'3819009121':'25302360'
}

# Устанавливаем стандартную кодировку
reload(sys)
# Питон 3 уже УТФ-8
#sys.setdefaultencoding('utf8')

# Полезные переменные
local_tz = pytz.timezone('Europe/Moscow')

# Полезные функции
def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

def insert_str(string, str_to_insert, index):
    return string[:index] + str_to_insert + string[index:]
# Добавить ребенка в XML
def AddKinder(name, value):
	Temp = doc.createElement(name)
	Temp.appendChild(doc.createTextNode(value)) 
	return Temp

def ParseFloat(str):
  str=str.replace(" ","")
  str=str.replace(",",".")  
  return str

	
# Открываем рабочий файл
print (sys.argv[1])
pathtofile = os.path.dirname(sys.argv[1])
if pathtofile!='' : pathtofile=pathtofile+'\\'
#print (pathtofile)
# Пауза
#os.system('pause')

workbook = xlrd.open_workbook(sys.argv[1])
worksheet = workbook.sheet_by_index(0)

# Создаём коренной элемент
doc = minidom.Document()
root = doc.createElement('ns3:financialActivityPlan2020')
root.setAttributeNS("xmls", "xsi:schemaLocation", 'http://bus.gov.ru/External/1 http://bus.gov.ru/public/schema/TFF-1.7.8.19/External.xsd')
root.setAttributeNS("xmls", "xmlns", 'http://bus.gov.ru/types/1')
root.setAttributeNS("xmls", "xmlns:ns2", 'http://bus.gov.ru/types/3')
root.setAttributeNS("xmls", "xmlns:ns4", 'http://bus.gov.ru/types/2')
root.setAttributeNS("xmls", "xmlns:ns3", 'http://bus.gov.ru/external/1')
root.setAttributeNS("xmls", "xmlns:xsi", 'http://www.w3.org/2001/XMLSchema-instance')
doc.appendChild(root)

# Header
header = doc.createElement('header')
root.appendChild(header)

# ID
id = doc.createElement('id')
id.appendChild(doc.createTextNode(str(uuid.uuid4())))
header.appendChild(id)

# createDateTime
createDateTime = doc.createElement('createDateTime')
createDateTime.appendChild(doc.createTextNode(str(utc_to_local(datetime.utcnow()).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "+03:00")))
header.appendChild(createDateTime)

# ns2:body
ns2_body = doc.createElement('ns3:body')
root.appendChild(ns2_body)

# ns2:position
ns2_position = doc.createElement('ns3:position')
ns2_body.appendChild(ns2_position)

# positionId
positionId = doc.createElement('positionId')
positionId.appendChild(doc.createTextNode(str(uuid.uuid4())))
ns2_position.appendChild(positionId)

# changeDate
changeDate = doc.createElement('changeDate')
changeDate.appendChild(doc.createTextNode(str(utc_to_local(datetime.utcnow()).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "+03:00")))
ns2_position.appendChild(changeDate)

# placer
placer = doc.createElement('placer')
ns2_position.appendChild(placer)

# Нужно отнимать 1 от колонки и от строки в реальности от Экселя
inn=str(worksheet.cell(19, 64).value)
kpp=str(worksheet.cell(20, 64).value)
fullNameOrg=str(worksheet.cell(20, 3).value)
fullNameOrg=fullNameOrg.replace ("\"","'")  
glavaCode=str(worksheet.cell(17, 64).value)
glava_regnum=''
glava_inn=''
glava_kpp=''

if glavaCode=='905' :
   glava_regnum='25304951'
   glava_inn='3819005092'
   glava_kpp='385145003'
   general_date='2010-11-30+03:00'

if glavaCode=='906' :
   glava_regnum='253D0130'
   glava_inn='3819005092'
   glava_kpp='385145002'
   general_date='2010-11-30+03:00'

   
regNum=regNum_Dict[inn]
print (regNum)

placer.appendChild(AddKinder('regNum',regNum))
placer.appendChild(AddKinder('fullName',fullNameOrg))
placer.appendChild(AddKinder('inn',inn))
placer.appendChild(AddKinder('kpp',kpp))

# initiator
initiator = doc.createElement('initiator')
ns2_position.appendChild(initiator)

# regNum
initiator_regNum = doc.createElement('regNum')
initiator_regNum.appendChild(doc.createTextNode(regNum))
initiator.appendChild(initiator_regNum)

# fullName
initiator_fullName = doc.createElement('fullName')
initiator_fullName.appendChild(doc.createTextNode(fullNameOrg))
initiator.appendChild(initiator_fullName)

# initiator inn
initiator.appendChild(AddKinder('inn',inn))
# initiator kpp
initiator.appendChild(AddKinder('kpp',kpp))
# versionNumber
ns2_position.appendChild(AddKinder('versionNumber', '0'))


# now
now = datetime.now()

# financialYear, planFirstYear, planLastYear
Year= int(worksheet.cell(11, 31).value)
ns2_position.appendChild(AddKinder('ns2:financialYear',str(Year)))
ns2_position.appendChild(AddKinder('ns2:planFirstYear',str(Year+1)))
ns2_position.appendChild(AddKinder('ns2:planLastYear',str(Year+2)))

#generalData
generalData=doc.createElement('ns2:generalData')
ns2_position.appendChild(generalData)

generalData.appendChild(AddKinder('ns2:date', general_date))
generalData.appendChild(AddKinder('ns2:dateApprovel', general_date))

founderAuthority = doc.createElement('ns2:founderAuthority')
founderAuthority.appendChild(AddKinder('regNum', glava_regnum))
founderAuthority.appendChild(AddKinder('inn', glava_inn))
founderAuthority.appendChild(AddKinder('kpp', glava_kpp))
founderAuthority.appendChild(AddKinder('ns2:glavaCode', glavaCode))
generalData.appendChild(founderAuthority)

okei = doc.createElement('ns2:okei')
okei.appendChild(AddKinder('code','383'))
okei.appendChild(AddKinder('symbol','руб'))
generalData.appendChild(okei)
ns2_position.appendChild(generalData)


# Хороший цикл по разделу № 1, Стартуем с 28 строки
i = 28
while i < worksheet.nrows:
  strName=worksheet.cell(i, 0).value
  reg = re.compile('[^a-zA-Z0-9А-Яа-я ]')  
  strName=reg.sub('', strName)
  strName=strName.replace ("     "," ")
  strName=strName.replace ("    "," ")
  strName=strName.replace ("   "," ")  
  lineCode=worksheet.cell(i, 18).value
  kbk=worksheet.cell(i, 22).value  
  analyticCode=worksheet.cell(i, 29).value    
  financialYearSum=str(worksheet.cell(i, 36).value)    
  if financialYearSum=='' : financialYearSum='0'
  
  planFirstYearSum=str(worksheet.cell(i, 48).value)    
  if planFirstYearSum=='' : planFirstYearSum='0'  
  
  planLastYearSum=str(worksheet.cell(i, 56).value)     
  if planLastYearSum=='' : planLastYearSum='0'  
  
  autPlanYearSum=str(worksheet.cell(i, 63).value)      
  if autPlanYearSum=='' : autPlanYearSum='0'  
  
  razdel2=strName.find ('Раздел 2')
  # print(razdel2)
  i = i + 1  
  if razdel2>=0:    break
  if (strName!=''):
    planPaymentIndex=doc.createElement('ns2:planPaymentIndex')
    planPaymentIndex.appendChild(AddKinder('ns2:name',strName))
    planPaymentIndex.appendChild(AddKinder('ns2:lineCode',lineCode))
    planPaymentIndex.appendChild(AddKinder('ns2:manually','false'))
#    if kbk!='х': planPaymentIndex.appendChild(AddKinder('ns2:kbk',kbk))
    if analyticCode!='' and analyticCode!='х' : planPaymentIndex.appendChild(AddKinder('ns2:analyticCode',analyticCode))	
    sum = doc.createElement('ns2:sum')
    sum.appendChild(AddKinder('ns2:financialYearSum',(financialYearSum)))
    sum.appendChild(AddKinder('ns2:planFirstYearSum',(planFirstYearSum)))
    sum.appendChild(AddKinder('ns2:planLastYearSum',(planLastYearSum)))
    if autPlanYearSum!='х' : sum.appendChild(AddKinder('ns2:autPlanYearSum',(autPlanYearSum)))
    planPaymentIndex.appendChild(sum)
    ns2_position.appendChild(planPaymentIndex)
  
# Хороший цикл по разделу № 2, Стартуем с начала раздела 2 --------------------------------
# i = razdel2
i=i+4 # Отступ 4 строки
print  (i)
while i < worksheet.nrows:
  lineNum=worksheet.cell(i, 0).value
  strName=worksheet.cell(i, 1).value
  reg = re.compile('[^a-zA-Z0-9А-Яа-я ]')  
  strName=reg.sub('', strName)
  strName=strName.replace ("     "," ")
  strName=strName.replace ("    "," ")
  strName=strName.replace ("   "," ")  
  lineCode=worksheet.cell(i, 21).value
  kbk=worksheet.cell(i, 22).value  
  analyticCode=worksheet.cell(i, 29).value    
  financialYearSum=str(worksheet.cell(i, 28).value)    
  if financialYearSum=='' : financialYearSum='0'
  financialYearSum=financialYearSum.replace(" ","")
  financialYearSum=financialYearSum.replace(",",".")  
  
  planFirstYearSum=str(worksheet.cell(i, 43).value)    
  if planFirstYearSum=='' : planFirstYearSum='0'  
  planFirstYearSum=ParseFloat(planFirstYearSum)
  
  planLastYearSum=str(worksheet.cell(i, 51).value) 
  if planLastYearSum=='' : planLastYearSum='0'
  planLastYearSum=ParseFloat(planLastYearSum)
  
  autPlanYearSum=str(worksheet.cell(i, 62).value)      
  if autPlanYearSum=='' : autPlanYearSum='0'
  autPlanYearSum=ParseFloat(autPlanYearSum)

  
  if strName.find ('Руководитель учреждения')>=0:    break
  
  
  i = i + 1  
  if (strName!='') and (lineCode!=''):
    planPaymentIndex=doc.createElement('ns2:planPaymentTRU')
    planPaymentIndex.appendChild(AddKinder('ns2:name',strName))
    planPaymentIndex.appendChild(AddKinder('ns2:lineCode',lineCode))
    planPaymentIndex.appendChild(AddKinder('ns2:manually','false'))    
    if analyticCode!='' and analyticCode!='х' : planPaymentIndex.appendChild(AddKinder('analyticCode',analyticCode))	
    sum = doc.createElement('ns2:sum')
    sum.appendChild(AddKinder('ns2:financialYearSum',(financialYearSum)))
    sum.appendChild(AddKinder('ns2:planFirstYearSum',(planFirstYearSum)))
    sum.appendChild(AddKinder('ns2:planLastYearSum',(planLastYearSum)))
    if autPlanYearSum!='х' : sum.appendChild(AddKinder('ns2:autPlanYearSum',(autPlanYearSum)))
    planPaymentIndex.appendChild(sum)
    ns2_position.appendChild(planPaymentIndex)
  

  
#xml_str = doc.toprettyxml(indent="    ")
xml_str = doc.toprettyxml(encoding="utf-8")

#with open(sys.argv[2], "w") as f:
filenameoutput='financialActivityPlan_all_'+inn+'.xml'
#with open(sys.argv[2], "wb") as f:
with open(pathtofile+filenameoutput, "wb") as f:
    f.write(xml_str)
