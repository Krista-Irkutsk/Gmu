#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Выгрузка на сайт ГМУ форм 0503721
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
ORG_NAME_INN_Dict={
'МБДОУ "Детский сад № 29"':'3819009393',
'МБУ "Спортивный центр"':'3819009805',
'МБОУ "СОШ № 12"':'3819009121',
'МБУДО "ДЮСШ №1"':'3819009770',
'МБУ ДО "Детская художественная школа"':'3819008689',
'МБУДО "СЮН"':'3819009516',
'МБДОУ "Детский сад № 6"':'3819009040',
'МБДОУ "Детский сад № 32"':'3819009280',
'МБДОУ "Детский сад № 2"':'3851007707',
'МБДОУ "Детский сад № 17"':'3819009241',
'МБОУ "Гимназия № 1"':'3819009080',
'МБОУ "Лицей №1"':'3819005381',
'МБДОУ "Д/С № 37"':'3819009403',
'МБОУ "Средняя общеобразовательная школа № 2"':'3819009428',
'МБКДУ "Дворец культуры" ':'3819003472',
'МБОУ СОШ № 3':'3819009643',
'МБУК "ДК Мир"':'3819012484',
'МБОУ "СОШ № 6"':'3819009227',
'МБОУ "ООШ № 8 имени  А.А. Разгуляева"':'3819009185',
'МБУДО "ДДТ"':'3819009330',
'МБДОУ "Детский сад № 3"':'3819009202',
'МБДОУ "Детский сад № 18"':'3819009266',
'МБДОУ "Детский сад № 44"':'3819009354',
'МБУК "УГ ЦБС"':'3819012491',
'МБДОУ "Детский сад № 35"':'3819009315',
'МБОУ "СОШ № 17" ':'3819009153',
'МБДОУ "Детский сад № 8"':'3819014788',
'МБОУ "СОШ № 15"':'3819009629',
'МБДОУ "Детский сад № 5"':'3819009234',
'МБДОУ "Детский сад № 25"':'3819009555',
'МБДОУ "Детский сад № 1"':'3819009604',
'МБДОУ "Детский сад № 7"':'3819009259',
'МБДОУ "ДС № 40"':'3819009450',
'МБОУ "СОШ № 10"':'3819009308',
'МБДОУ "ДС № 34"':'3851007457',
'МБДОУ "ДС № 42"':'3819009273',
'МБДОУ "Д/с № 26"':'3819009322',
'МБОУ "СОШ № 13"':'3819009298',
'МБДОУ "Детский сад №33"':'3819009523',
'МБДОУ "Детский сад № 10"':'3819005744',
'МБУК "Усольский историко-краеведческий музей"':'3819012501',
'МБУ "СК "Химик"':'3819000337',
'МБДОУ "Детский сад № 21"':'3819020799',
'МБДОУ "Детский сад № 31"':'3819009562',
'МБДОУ "Детский сад № 38"':'3819009474',
'МБУ ДО "ДМШ"':'3819008671',
'МБОУ "СОШ № 5"':'3819005470',
'МБОУ "Гимназия № 9"':'3819009139',
'МБДОУ "Детский сад № 22"':'3819009107',
'МБОУ "СОШ № 16"':'3819005790',
'МБДОУ "Детский сад № 43"':'3819009210',
'МБДОУ "Детский сад № 39"':'3819009467',
'МБДОУ "детский сад № 28"':'3851025463'
}
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

def delapostrof(string):
    string=string.replace(" ","")
    string=string.replace('"', "") 
    return string
	
	
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


def getRazedlreferenceFromFile(xml_str):
  pathtofile='C:\\gmu\\'
  with open (pathtofile+'reference.xml', 'r') as f:
    reference_xml = f.read()
    str=xml_str.decode()
    str=str.replace('<reference/>', reference_xml)
    xml_str=str.encode()
    return xml_str
  
def getRazedl(start, name):
  result=doc.createElement(name)
  i = start
  lineCode=''
  ex = 0
  while True:
   if ex == 1: break
   if (name == 'financialAssets' and lineCode == '560'): ex = 1
   if str(worksheet.cell(i, 0).value)[:8] == 'Директор' : break
   strName=worksheet.cell(i, 0).value
   if strName == '     ':
    i += 1 
    continue
   reg = re.compile('[^a-zA-Z0-9А-Яа-я ]')
   strName=reg.sub('', strName)
   strName=strName.replace ("из них:"," ")
   strName=strName.replace ("из них"," ")
   strName=strName.replace ("в том числе:"," ")
   strName=strName.replace ("     "," ")
   strName=strName.replace ("    "," ")
   strName=strName.replace ("   "," ")
   lineCode=worksheet.cell(i, 12).value
   print(lineCode)
   if lineCode == '' or lineCode == 'Код строки' or lineCode == '2': 
    i += 1 
    continue
   if (name == 'income' and int(lineCode) > 110): break
   if (name == 'expense' and int(lineCode) > 302): break
   if (name == 'nonFinancialAssets' and int(lineCode) > 390): break
   if (name == 'financialAssets' and int(lineCode) > 560): break
   j = i
   if (name=='income' and int(lineCode)<=110)or(name=='expense' and int(lineCode)>110 and int(lineCode)<=302)or(name=='nonFinancialAssets' and int(lineCode)>302 and int(lineCode)<=390)or(name=='financialAssets' and int(lineCode)>390 and int(lineCode)<=560):
    reportItem=doc.createElement('reportItem')
    reportItem.appendChild(AddKinder('manually', 'false'))
    reportItem.appendChild(AddKinder('name', strName))
    if int(lineCode)< 100:
      reportItem.appendChild(AddKinder('lineCode', '0'+ str(int(lineCode))))
    else:
      reportItem.appendChild(AddKinder('lineCode', str(int(lineCode))))
    analyticCode = str(ParseFloat(worksheet.cell(i, 13).value))
    if len(analyticCode) == 3:
        if analyticCode[-1] == 'Х':
            print(analyticCode+'  ' + 'ggggggg')
            analyticCode = analyticCode[:2] + '0'
            reportItem.appendChild(AddKinder('analyticCode', analyticCode))
        else:
            reportItem.appendChild(AddKinder('analyticCode', analyticCode))
    reportItem.appendChild(AddKinder('targetFunds',
        ParseFloat(worksheet.cell(i, 18).value)))   
    reportItem.appendChild(AddKinder('stateTaskFunds',
        ParseFloat(worksheet.cell(i, 20).value)))      
    reportItem.appendChild(AddKinder('revenueFunds',
        ParseFloat(worksheet.cell(i, 24).value)))
    if (str(ParseFloat(worksheet.cell(i, 30).value)) != '0.00'):
        reportItem.appendChild(AddKinder('total',
            ParseFloat(worksheet.cell(i, 30).value)))
    j = i + 1
    lineCode_1=worksheet.cell(j, 12).value
    if lineCode_1 == '' or lineCode_1 == 'Код строки' or lineCode_1 == '2':
        print('aaaaaaaaaaa')
        if worksheet.cell(j, 0).value !='     в том числе:':
            result.appendChild(reportItem)
            i += 1 
            continue
        elif worksheet.cell(j+1, 12).value == lineCode and worksheet.cell(j+1, 0).value == '     ':
            result.appendChild(reportItem)
            i += 1 
            continue
        else:
            j+=1
            lineCode_1=worksheet.cell(j, 12).value
        print(lineCode_1)
    while str(int(lineCode_1))[-1] != '0' or lineCode_1 == lineCode:
        strName=worksheet.cell(j, 0).value
        if strName == '     ':
            j += 1 
            continue
        reg = re.compile('[^a-zA-Z0-9А-Яа-я ]')  
        strName=reg.sub('', strName)
        strName=strName.replace ("из них:"," ")
        strName=strName.replace ("из них"," ")
        strName=strName.replace ("в том числе:"," ")
        strName=strName.replace ("в том числе"," ")
        strName=strName.replace ("     "," ")
        strName=strName.replace ("    "," ")
        strName=strName.replace ("   "," ")  
        reportSubItem=doc.createElement('reportSubItem')
        reportSubItem.appendChild(AddKinder('manually', 'false'))
        reportSubItem.appendChild(AddKinder('name', strName))
        if int(lineCode_1)< 100:
          reportSubItem.appendChild(AddKinder('lineCode', '0'+ str(int(lineCode_1))))
        else:
          reportSubItem.appendChild(AddKinder('lineCode', str(int(lineCode_1))))
        analyticCode = str(ParseFloat(worksheet.cell(j, 13).value))
        if len(analyticCode) == 3:
            if analyticCode[-1] == 'Х':
                print(analyticCode + 'fffffffffff')
                analyticCode = analyticCode[:2] + '0'
                reportSubItem.appendChild(AddKinder('analyticCode', analyticCode))
            else:
                reportSubItem.appendChild(AddKinder('analyticCode', analyticCode))
        reportSubItem.appendChild(AddKinder('targetFunds',
            ParseFloat(worksheet.cell(j, 18).value)))   
        reportSubItem.appendChild(AddKinder('stateTaskFunds',
            ParseFloat(worksheet.cell(j, 20).value)))      
        reportSubItem.appendChild(AddKinder('revenueFunds',
            ParseFloat(worksheet.cell(j, 24).value)))
        if (str(ParseFloat(worksheet.cell(j, 30).value)) != '0.00'):
            reportSubItem.appendChild(AddKinder('total',
                ParseFloat(worksheet.cell(j, 30).value)))
        reportItem.appendChild(reportSubItem)
        j += 1
        lineCode_1=worksheet.cell(j, 12).value
        while lineCode_1 == '' or lineCode_1 == 'Код строки' or lineCode_1 == '2':
            print(worksheet.cell(j, 12).value)
            if worksheet.cell(j-1, 12).value == worksheet.cell(j+1, 12).value and worksheet.cell(j+1, 0).value == '':
                j+=2
            else:
                j+=1
            lineCode_1=worksheet.cell(j, 12).value
    result.appendChild(reportItem)
    if i == 1000: break
   
   if i < j:
      i = j
   else:
       i += 1
    
  return result
	
# Открываем рабочий файл
print (sys.argv[0])
pathtofile = os.path.dirname(sys.argv[0])
if pathtofile!='' : pathtofile=pathtofile+'\\'
#print (pathtofile)
# Пауза
#os.system('pause')

workbook = xlrd.open_workbook(sys.argv[1])
worksheet = workbook.sheet_by_index(0)

# Создаём коренной элемент
doc = minidom.Document()
root = doc.createElement('ns2:annualBalanceF0503721_2015')
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
#inn=(str(worksheet.cell(4, 6).value))
#inn=(str(worksheet.cell(4, 6).value))
oktmostr=str(int(worksheet.cell(5, 30).value))

# kpp=str(worksheet.cell(20, 64).value)
kpp=''
fullNameOrg=str(worksheet.cell(4, 6).value)
inn=ORG_NAME_INN_Dict[fullNameOrg]
oktmostr=regNum_Dict[inn]
fullNameOrg=fullNameOrg.replace ("\"","'")  
glavaCode=str(worksheet.cell(8, 30).value)
general_date=str(worksheet.cell(3, 30).value)
general_date='2021-01-01'



glava_regnum=''
glava_inn=''
glava_kpp=''
founderAuthorityOkpo=''
separateStructuralUnitOkpo=''

if glavaCode[:17]=='отдел образования' :
   glava_regnum='25304951'
   glava_inn='3819005092'
   glava_kpp='385145003'
   general_date='2010-11-30+03:00'
   founderAuthorityOkpo='68596576'
   founderNamefullName='ОТДЕЛ ОБРАЗОВАНИЯ УПРАВЛЕНИЯ ПО СОЦИАЛЬНО-КУЛЬТУРНЫМ ВОПРОСАМ АДМИНИСТРАЦИИ ГОРОДА УСОЛЬЕ-СИБИРСКОЕ'

if glavaCode[:17]!='отдел образования' :
   glava_regnum='253D0130'
   glava_inn='3819005092'
   glava_kpp='385145002'
   general_date='2010-11-30+03:00'
   founderAuthorityOkpo='04027906'
   founderNamefullName='ОТДЕЛ КУЛЬТУРЫ УПРАВЛЕНИЯ ПО СОЦИАЛЬНО-КУЛЬТУРНЫМ ВОПРОСАМ АДМИНИСТРАЦИИ ГОРОДА УСОЛЬЕ-СИБИРСКОЕ'


   
#regNum=regNum_Dict[inn]
#print (regNum)

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

# Доходы
income = getRazedl(19, 'income')
# Финансовые активы  
expense = getRazedl(19, 'expense')
# Обязательства, Пассив
nonFinancialAssets = getRazedl(19, 'nonFinancialAssets')
# Финансовые результат
financialAssets = getRazedl(19, 'financialAssets')
# 

ns2_position.appendChild(income)
ns2_position.appendChild(expense)
ns2_position.appendChild(nonFinancialAssets)
ns2_position.appendChild(financialAssets)

xml_str = doc.toprettyxml(encoding="utf-8")
# xml_str=getRazedlreferenceFromFile(xml_str)
filenameoutput='annualAccountancy_all_'+inn+'_721'+'.xml'

with open(pathtofile+filenameoutput, "wb") as f:
    f.write(xml_str)
	
"""
with open ('test.txt', 'r') as f:
  old_data = f.read()

new_data = old_data.replace('что_меняем', 'на_что_меняем')

with open ('test.txt', 'w') as f:
  f.write(new_data)

"""