#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Выгрузка на сайт ГМУ форм 0503730
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
  if str=='-' or str=='X':
   str='0.00'
  return str

def getRazedlreference():
  result=doc.createElement('reference')
  """"  
  reportItem=doc.createElement("<reportItem> <name>Имущество, полученное в пользование</name> <lineCode>010</lineCode> <targetFundsStartYear>0.00</targetFundsStartYear> <targetFundsEndYear>0.00</targetFundsEndYear> <stateTaskFundsStartYear>0.00</stateTaskFundsStartYear> <stateTaskFundsEndYear>0.00</stateTaskFundsEndYear><revenueFundsStartYear>0.00</revenueFundsStartYear><revenueFundsEndYear>0.00</revenueFundsEndYear><totalStartYear>0.00</totalStartYear><totalEndYear>0.00</totalEndYear></reportItem>")
  result.appendChild(reportItem)
"""      
  return result  

def getRazedlreferenceFromFile(xml_str):
  pathtofile='C:\\gmu\\'
  with open (pathtofile+'reference.xml', 'r') as f:
    reference_xml = f.read()
    str=xml_str.decode()
    str=str.replace('<reference/>', reference_xml)
    xml_str=str.encode()
    return xml_str
  
def getRazedl(start, end, name):
  result=doc.createElement(name)
  i = start
  while i < end:
   strName=worksheet.cell(i, 0).value
   reg = re.compile('[^a-zA-Z0-9А-Яа-я ]')  
   strName=reg.sub('', strName)
   strName=strName.replace ("     "," ")
   strName=strName.replace ("    "," ")
   strName=strName.replace ("   "," ")  
   lineCode=worksheet.cell(i, 12).value
# Целевые   
   targetFundsStartYear=ParseFloat(worksheet.cell(i, 16).value)
   targetFundsEndYear=ParseFloat(worksheet.cell(i, 34).value)
#  Государственное задание
   stateTaskFundsStartYear=ParseFloat(worksheet.cell(i, 19).value)
   stateTaskFundsEndYear=ParseFloat(worksheet.cell(i, 37).value)
#  Приносящая доход
   revenueFundsStartYear=ParseFloat(worksheet.cell(i, 25).value)
   revenueFundsEndYear=ParseFloat(worksheet.cell(i, 43).value)
#  Итого   
   totalStartYear=ParseFloat(worksheet.cell(i, 29).value)
   totalEndYear=ParseFloat(worksheet.cell(i, 46).value)
   if (lineCode=='010'):
    strName='Основные средства (балансовая стоимость, 010100000)*'
   if (lineCode=='190') :
    strName='Итого по разделу I (стр.030 + стр.060 + стр.070 + стр.080 + стр.100 + стр.120 + стр.130 + стр.150 + стр.160)'	
   if (lineCode=='200'):
    strName='Денежные средства учреждения (020100000), всего'
   if (lineCode=='340') :
    strName='Итого по разделу II (стр.200 + стр.240 + стр.250 + стр.260 + стр.270 + стр.280 + стр.290)'	
   if (lineCode=='400') :
    strName='Расчеты с кредиторами по долговым обязательствам (030100000), всего'	
   if (lineCode=='550') :
    strName='Итого по разделу III (стр.400 + стр.410 + стр.420 + стр.430 + стр.470 + стр.480 + стр.510 + стр.520)'	
   if (lineCode=='570') :
    strName='Финансовый результат экономического субъекта'	
   if (strName!='') and (lineCode!='') and (lineCode!='х') and (len (lineCode)==3)	:
    reportItem=doc.createElement('reportItem')
    reportItem.appendChild(AddKinder('name',strName))
    reportItem.appendChild(AddKinder('lineCode',lineCode))
    reportItem.appendChild(AddKinder('targetFundsStartYear',targetFundsStartYear))
    reportItem.appendChild(AddKinder('targetFundsEndYear',targetFundsEndYear))   
    reportItem.appendChild(AddKinder('stateTaskFundsStartYear',stateTaskFundsStartYear))      
    reportItem.appendChild(AddKinder('stateTaskFundsEndYear',stateTaskFundsEndYear))      
    reportItem.appendChild(AddKinder('revenueFundsStartYear',revenueFundsStartYear))      
    reportItem.appendChild(AddKinder('revenueFundsEndYear',revenueFundsEndYear))      
    reportItem.appendChild(AddKinder('totalStartYear',totalStartYear))
    reportItem.appendChild(AddKinder('totalEndYear',totalEndYear))
    result.appendChild(reportItem)
   i = i + 1  
  return result
	
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
root = doc.createElement('ns2:annualBalanceF0503730_2015')
root.setAttributeNS("xmlns", "xmlns", "http://bus.gov.ru/types/1" )
root.setAttributeNS("xmlns", "xmlns:ns2", 'http://bus.gov.ru/external/1')
root.setAttributeNS("xmlns", "xmlns:ns3", 'http://bus.gov.ru/fk/1')
root.setAttributeNS("xmlns", "xmlns:ns4", 'http://bus.gov.ru/nsi/1')
root.setAttributeNS("xmlns", "xmlns:xs", 'http://www.w3.org/2001/XMLSchema')
root.setAttributeNS("xmlns", "xmlns:xsi", 'http://www.w3.org/2001/XMLSchema-instance')


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
ns2_body = doc.createElement('ns2:body')
root.appendChild(ns2_body)

# ns2:position
ns2_position = doc.createElement('ns2:position')
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
#placer = doc.createElement('placer')
#ns2_position.appendChild(placer)

# Нужно отнимать 1 от колонки и от строки в реальности от Экселя
inn=str(worksheet.cell(7, 44).value)
oktmostr=str(worksheet.cell(8, 44).value)

# kpp=str(worksheet.cell(20, 64).value)
kpp=''
fullNameOrg=str(worksheet.cell(5, 6).value)
fullNameOrg=fullNameOrg.replace ("\"","'")  
glavaCode=str(worksheet.cell(10, 44).value)
general_date=str(worksheet.cell(4, 44).value)
general_date='2021-01-01'

glava_regnum=''
glava_inn=''
glava_kpp=''
founderAuthorityOkpo=''
separateStructuralUnitOkpo=''

if glavaCode=='905' :
   glava_regnum='25304951'
   glava_inn='3819005092'
   glava_kpp='385145003'
   general_date='2010-11-30+03:00'
   founderAuthorityOkpo='68596576'
   founderNamefullName='ОТДЕЛ ОБРАЗОВАНИЯ УПРАВЛЕНИЯ ПО СОЦИАЛЬНО-КУЛЬТУРНЫМ ВОПРОСАМ АДМИНИСТРАЦИИ ГОРОДА УСОЛЬЕ-СИБИРСКОЕ'

if glavaCode=='906' :
   glava_regnum='253D0130'
   glava_inn='3819005092'
   glava_kpp='385145002'
   general_date='2010-11-30+03:00'
   founderAuthorityOkpo='04027906'
   founderNamefullName='ОТДЕЛ КУЛЬТУРЫ УПРАВЛЕНИЯ ПО СОЦИАЛЬНО-КУЛЬТУРНЫМ ВОПРОСАМ АДМИНИСТРАЦИИ ГОРОДА УСОЛЬЕ-СИБИРСКОЕ'


   
regNum=regNum_Dict[inn]
print (regNum)

# placer, initiator  убрал в 2021 году
#placer.appendChild(AddKinder('regNum',regNum))
#placer.appendChild(AddKinder('fullName',fullNameOrg))
#placer.appendChild(AddKinder('inn',inn))
#placer.appendChild(AddKinder('kpp',kpp))

# initiator
#initiator = doc.createElement('initiator')
#ns2_position.appendChild(initiator)

# regNum
#initiator_regNum = doc.createElement('regNum')
#initiator_regNum.appendChild(doc.createTextNode(regNum))
#initiator.appendChild(initiator_regNum)

# fullName
#initiator_fullName = doc.createElement('fullName')
#initiator_fullName.appendChild(doc.createTextNode(fullNameOrg))
#initiator.appendChild(initiator_fullName)

# initiator inn
#initiator.appendChild(AddKinder('inn',inn))
# initiator kpp
#initiator.appendChild(AddKinder('kpp',kpp))
# versionNumber
ns2_position.appendChild(AddKinder('formationPeriod', '2020'))


# now
now = datetime.now()

#generalData
generalData=doc.createElement('generalData')
ns2_position.appendChild(generalData)

generalData.appendChild(AddKinder('date', general_date))
generalData.appendChild(AddKinder('periodicity', 'annual'))
#  okei
okei = doc.createElement('okei')
okei.appendChild(AddKinder('code','383'))
okei.appendChild(AddKinder('symbol','руб'))
generalData.appendChild(okei)
generalData.appendChild(AddKinder('okpo', '51517756'))
generalData.appendChild(AddKinder('inn', inn))
generalData.appendChild(AddKinder('section', '864'))
# oktmo
oktmo = doc.createElement('oktmo')
oktmo.appendChild(AddKinder('code',oktmostr))
oktmo.appendChild(AddKinder('name','г.Усолье-Сибирское'))
generalData.appendChild(oktmo)
generalData.appendChild(AddKinder('founderName', founderNamefullName))


founderAuthority = doc.createElement('founderAuthority')
founderAuthority.appendChild(AddKinder('regNum', glava_regnum))
founderAuthority.appendChild(AddKinder('fullName', founderNamefullName))
generalData.appendChild(founderAuthority)

generalData.appendChild(AddKinder('founderAuthorityOkpo', founderAuthorityOkpo))
generalData.appendChild(AddKinder('separateStructuralUnitOkpo', founderAuthorityOkpo))
ns2_position.appendChild(generalData)

# Нефинансовые активы
nonFinancialAssets=getRazedl(21,45,'nonFinancialAssets')
# Финансовые активы  
financialAssets=getRazedl(46,72,'financialAssets')
# Обязательства, Пассив
commitments=getRazedl(76,93,'commitments')
# Финансовые результат
financialResult=getRazedl(94,97,'financialResult')
# 
reference=getRazedlreference()

ns2_position.appendChild(nonFinancialAssets)
ns2_position.appendChild(financialAssets)
ns2_position.appendChild(commitments)
ns2_position.appendChild(financialResult)
ns2_position.appendChild(reference)

xml_str = doc.toprettyxml(encoding="utf-8")
xml_str=getRazedlreferenceFromFile(xml_str)
filenameoutput='annualAccountancy_all_'+inn+'.xml'

with open(pathtofile+filenameoutput, "wb") as f:
    f.write(xml_str)
	
"""
with open ('test.txt', 'r') as f:
  old_data = f.read()

new_data = old_data.replace('что_меняем', 'на_что_меняем')

with open ('test.txt', 'w') as f:
  f.write(new_data)

"""