import sys
import re
import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import datetime
from xml.etree import ElementTree
from xml.dom import minidom

generated_on = str(datetime.datetime.now())

root = Element('ODM',
        {"xmlns":"http://www.cdisc.org/ns/odm/v1.3",
         "xmlns:def":"http://www.cdisc.org/ns/def/v2.1",
         "xmlns:xlink":"http://www.w3.org/1999/xlink",
         "xmlns:arm":"http://www.cdisc.org/ns/arm/v1.0",
         "FileOID":"www.cdisc.org/CDISC-Sample/ADaM/1/Define-XML_2.1.0",
         "ODMVersion":"1.3.2",
         "FileType":"Snapshot",
         "CreationDateTime":generated_on,
         "Originator":"CDISC Data Exchange Standards Team",
         "def:Context":"Submission",
         })
child = SubElement(root, 'Study', 
        {'OID':"STDY.www.cdisc.org/CDISC-Sample/ADaM",
            })
child2 = SubElement(child, 'GlobalVariables')

chid1 = SubElement(child2,'StudyName')
chid2 = SubElement(child2,'StudyDescription')
chid3 = SubElement(child2,'ProtocolName')
chid1.text='CDISC-Sample'
chid2.text='CDISC-Sample Data Definition'
chid3.text='CDISC-Sample'

child3 = SubElement(child, 'MetaDataVersion', 
         {'OID':"MDV.CDISC01.ADaMIG.1.1.ADaM.2.1",
          'Name':"Study CDISC-Sample, Data Definitions", 
          'Description':"Study CDISC-Sample, Data Definitions",
          'def:DefineVersion':"2.1.0",
          })

## generate the standard definition
body = SubElement(child3, 'def:Standards')
with open('standard.csv', 'rt') as f:
    reader1 = csv.reader(f )
    next(reader1)
    for row in reader1:
        OID, Name, Type, PublishingSet, Status, Version, CommentID, Comment = row 
        if re.search('[\w]', PublishingSet) and re.search('[\w]',Comment): 
            chld = SubElement(body, 'def:Standard', 
                {'OID': OID.strip(),
                 'Name':Name.strip(), 
                 'Type':Type.strip(),
                 'PublishingSet': PublishingSet.strip(), 
                 'Status':Status.strip(),
                 'Version':Version.strip(),
                 'def:CommentOID':'COM.'+CommentID.strip(),
                 })
        elif not re.search('[\w]', PublishingSet) and not re.search('[\w]',Comment): 
            chld = SubElement(body, 'def:Standard', 
                {'OID': OID.strip(),
                 'Name':Name.strip(), 
                 'Type':Type.strip(),
                 'Status':Status.strip(),
                 'Version':Version.strip(),
                 })
        elif not re.search('[\w]', PublishingSet) and re.search('[\w]',Comment): 
            chld = SubElement(body, 'def:Standard', 
                {'OID': OID.strip(),
                 'Name':Name.strip(), 
                 'Type':Type.strip(),
                 'Status':Status.strip(),
                 'Version':Version.strip(),
                 'def:CommentOID':'COM.'+CommentID.strip(),
                 })
        else:
            chld = SubElement(body, 'def:Standard', 
                {'OID': OID.strip(),
                 'Name':Name.strip(), 
                 'Type':Type.strip(),
                 'PublishingSet': PublishingSet.strip(), 
                 'Status':Status.strip(),
                 'Version':Version.strip(),
                 })

## generate the supplemental document section
body = SubElement(child3, 'def:SupplementalDoc')
chld = SubElement(body, 'def:DocumentRef', 
       {'leafID': 'LF.ADRG',
       })

## generate the ValueList definition section 
with open('defvar2.csv', 'rt') as f:
    reader2 = csv.reader(f)
    next(reader2)
    category = [ ] 
    for row in reader2: 
        Dataset, Variable, Paramcd, Mandatory, OrderNumber, Method, Document, PageRefs, Type, Typ, DataType, Length, DisplayFormat, SignificantDigits, Comment, Label, ValueList, Formatit, Origin, Orgdtl, Source = row
        if re.search('[\w]',Paramcd): 
            OID=Dataset.upper().strip()+'.'+Variable.upper().strip()
            if OID not in category: 
               category.append(OID)

for cat in category: 
    body = SubElement(child3, 'def:ValueListDef', 
          {'OID': 'VL.'+cat, 
           })
    with open('defvar2.csv', 'rt') as f:
        reader3 = csv.reader(f )
        next(reader3)
        for row in reader3:
            Dataset, Variable, Paramcd, Mandatory, OrderNumber, Method, Document, PageRefs, Type, Typ, DataType, Length, DisplayFormat, SignificantDigits, Comment, Label, ValueList, Formatit, Origin, Orgdtl, Source = row
            OID2=Dataset.upper().strip()+'.'+Variable.upper().strip()
            if OID2==cat and re.search('[\w]',Paramcd):
                if re.search('[\w]', Method): 
                    chld1 = SubElement(body, 'ItemRef', 
                            {'ItemOID': 'IT.'+Dataset.upper().strip()+'.'+Variable.upper().strip()+'.'+Paramcd.strip().upper(),
                             'Mandatory':Mandatory.strip(), 
                             'OrderNumber':OrderNumber.strip(),
                             'MethodOID':'MT.'+Dataset.upper().strip()+'.'+Variable.upper().strip()+'.'+Paramcd.strip().upper(), 
                             })
                else: 
                    chld1 = SubElement(body, 'ItemRef', 
                            {'ItemOID': 'IT.'+Dataset.upper().strip()+'.'+Variable.upper().strip()+'.'+Paramcd.strip().upper(),
                             'Mandatory':Mandatory.strip(), 
                             'OrderNumber':OrderNumber.strip(),
                             })
                chld2 = SubElement(chld1, 'def:WhereClauseRef',
                    {'WhereClauseOID':'WC.'+Dataset.upper().strip()+'.'+Variable.upper().strip()+'.'+Paramcd.strip().upper(),
                    }) 

## generate the WhereClause Definition Section 

with open('where_clause.csv', 'rt') as f:
    reader4 = csv.reader(f)
    next(reader4)
    category = [ ] 
    for row in reader4: 
        ID, Dataset, Variable, Comparator, CheckValue = row
        if ID not in category: 
            category.append(ID)

for cat in category: 
  body = SubElement(child3, 'def:WhereClauseDef', 
          {'OID': 'WC.'+cat, 
           })

  with open('where_clause.csv', 'rt') as f:
    reader5 = csv.reader(f)
    next(reader5)
    for row in reader5:
        ID, Dataset, Variable, Comparator, CheckValue = row
        if ID==cat:
            chld = SubElement(body, 'RangeCheck',
               {"Comparator": Comparator.strip(),
               "def:ItemOID": 'IT.'+Dataset.strip()+'.'+Variable.strip(), 
               })
            if not re.search(';',CheckValue):
                chld2=SubElement(chld,'CheckValue')
                chld2.text=CheckValue.strip()
            else:
                itms=CheckValue.split(";")
                for itm in itms:
                    chld2=SubElement(chld,'CheckValue')
                    chld2.text=itm.strip()

## generate the ItemGroupDef definition section

with open('defds.csv', 'rt') as f:
    reader6 = csv.reader(f )
    next(reader6)
    for row in reader6:
        Data, Repeating, IsReferenceData, Purpose, Standard, Structure, Label, Classit, SubClass, Comment, Doc1, Doc2, PageRef2, PageTyp2 = row
        body = SubElement(child3, 'ItemGroupDef', 
                {'OID': "IG."+ Data.upper().strip(),
                 'Name':Data.upper().strip(), 
                 'SASDatasetName':Data.upper().strip(),
                 'Repeating':Repeating.strip(),
                 'IsReferenceData':IsReferenceData.strip(),
                 'Purpose':Purpose.strip(),
                 'def:StandardOID':Standard.strip(),
                 'def:Structure':Structure.strip(),
                 'def:ArchiveLocationID':'LF.'+Data.upper().strip(),
                 'def:CommentOID':'COM.'+Data.upper().strip(),
                 })
        chld = SubElement(body, 'Description') 
        chld2 = SubElement(chld, 'TranslatedText',
                {'xml:lang':"en"
                    }) 
        chld2.text = Label.strip()
        with open('defvar.csv', 'rt') as g:
            reader7 = csv.reader(g)
            next(reader7)
            for row in reader7:
                Dataset, Variable, OrderNumber, Mandatory, KeySequence, Method, Typeit = row
                if Dataset.upper().strip()==Data.upper().strip() :
                    if re.search('[0-9]', KeySequence) and re.search('[\w]',Method): 
                        podc = SubElement(body, 'ItemRef',
                             {'ItemOID':'IT.'+ Dataset.upper().strip()+'.'+ Variable.upper().strip(),
                              'OrderNumber':OrderNumber.strip(),
                              'Mandatory':Mandatory.strip(),
                              'KeySequence':KeySequence.strip(),
                              'MethodOID':'MT.'+ Dataset.upper().strip()+'.'+Variable.upper().strip(),
                              })
                    elif not re.search('[0-9]', KeySequence) and not re.search('[\w]',Method): 
                        podc = SubElement(body, 'ItemRef',
                             {'ItemOID':'IT.'+ Dataset.upper().strip()+'.'+ Variable.upper().strip(),
                              'OrderNumber':OrderNumber.strip(),
                              'Mandatory':Mandatory.strip(),
                              })
                    elif not re.search('[0-9]', KeySequence) and re.search('[\w]',Method): 
                        podc = SubElement(body, 'ItemRef',
                             {'ItemOID':'IT.'+ Dataset.upper().strip()+'.'+ Variable.upper().strip(),
                              'OrderNumber':OrderNumber.strip(),
                              'Mandatory':Mandatory.strip(),
                              'MethodOID':'MT.'+ Dataset.upper().strip()+'.'+Variable.upper().strip(),
                              })
                    else: 
                        podc = SubElement(body, 'ItemRef',
                             {'ItemOID':'IT.'+ Dataset.upper().strip()+'.'+ Variable.upper().strip(),
                              'OrderNumber':OrderNumber.strip(),
                              'Mandatory':Mandatory.strip(),
                              'KeySequence':KeySequence.strip(),
                              })
        if not re.search('[\w]',SubClass):
            chld3 = SubElement(body,"def:Class",
                    {"Name":Classit.strip(),
                        })
        else:
            chld3 = SubElement(body,"def:Class",
                    {"Name":Classit.strip(),
                        })
            chld4 = SubElement(chld3,'def:SubClass', 
                    {"Name": SubClass
                        })
        chld5 = SubElement(body,"def:leaf",
                {'ID':'LF.'+Data.upper().strip(),
                 'xlink:href':Data.strip()+'.xpt', 
                    })
        chld6 = SubElement(chld5,"def:title")
        chld6.text = Data.strip()+'.xpt'

## generate the ItemDef definition section

with open('defvar2.csv', 'rt') as f:
    reader8 = csv.reader(f )
    next(reader8)
    for row in reader8:
        Dataset, Variable, Paramcd, Mandatory, Order, Method, Document, PageRefs, Type, Typ, DataType, Length, DisplayFormat, SignificantDigits, Comment, Label, ValueList, Formatit, Origin, Orgdtl, Source = row
        if re.search('[\w]',Paramcd):
            oid='IT.'+Dataset.upper().strip()+'.'+Variable.upper().strip()+'.'+Paramcd.upper().strip()
        else:
            oid='IT.'+Dataset.upper().strip()+'.'+Variable.upper().strip()

        if re.search('[\w]',Paramcd):
            com2='COM.'+Dataset.upper().strip()+'.'+Variable.upper().strip()+'.'+Paramcd.upper().strip()
        else:
            com2='COM.'+Dataset.upper().strip()+'.'+Variable.upper().strip()

        if re.search('[0-9]',Length):
            if re.search('[\w]',DisplayFormat) and re.search('[0-9]',SignificantDigits) and re.search('[\w]',Comment):
                body = SubElement(child3, 'ItemDef', 
                        {'OID': oid,
                         'Name':Variable.upper().strip(), 
                         'SASFieldName':Variable.upper().strip(),
                         'DataType':DataType.strip(),
                         'Length':Length.strip(),
                         'def:DisplayFormat':DisplayFormat.strip(),
                         'SignificantDigits':SignificantDigits.strip(),
                         'def:CommentOID':com2,
                          })
            elif re.search('[\w]',DisplayFormat) and re.search('[0-9]',SignificantDigits) and not re.search('[\w]',Comment):
                body = SubElement(child3, 'ItemDef', 
                        {'OID': oid,
                         'Name':Variable.upper().strip(), 
                         'SASFieldName':Variable.upper().strip(),
                         'DataType':DataType.strip(),
                         'Length':Length.strip(),
                         'def:DisplayFormat':DisplayFormat.strip(),
                         'SignificantDigits':SignificantDigits.strip(),
                          })
            elif re.search('[\w]',DisplayFormat) and not re.search('[0-9]',SignificantDigits) and re.search('[\w]',Comment):
                body = SubElement(child3, 'ItemDef', 
                        {'OID': oid,
                         'Name':Variable.upper().strip(), 
                         'SASFieldName':Variable.upper().strip(),
                         'DataType':DataType.strip(),
                         'Length':Length.strip(),
                         'def:DisplayFormat':DisplayFormat.strip(),
                         'def:CommentOID':com2,
                          })
            elif re.search('[\w]',DisplayFormat) and not re.search('[0-9]',SignificantDigits) and not re.search('[\w]',Comment):
                body = SubElement(child3, 'ItemDef', 
                        {'OID': oid,
                         'Name':Variable.upper().strip(), 
                         'SASFieldName':Variable.upper().strip(),
                         'DataType':DataType.strip(),
                         'Length':Length.strip(),
                         'def:DisplayFormat':DisplayFormat.strip(),
                          })
            elif not re.search('[\w]',DisplayFormat) and  re.search('[\w]',Comment):
                body = SubElement(child3, 'ItemDef', 
                        {'OID': oid,
                         'Name':Variable.upper().strip(), 
                         'SASFieldName':Variable.upper().strip(),
                         'DataType':DataType.strip(),
                         'Length':Length.strip(),
                         'def:CommentOID':com2,
                          })
            else:
                body = SubElement(child3, 'ItemDef', 
                        {'OID': oid,
                         'Name':Variable.upper().strip(), 
                         'SASFieldName':Variable.upper().strip(),
                         'DataType':DataType.strip(),
                         'Length':Length.strip(),
                          })
        else:
            body = SubElement(child3, 'ItemDef', 
                    {'OID': oid,
                    'Name':Variable.upper().strip(), 
                    'SASFieldName':Variable.upper().strip(),
                    'DataType':DataType.strip(),
                     })

        chld = SubElement(body, 'Description') 
        chld2 = SubElement(chld, 'TranslatedText',
                {'xml:lang':"en"
                    }) 
        chld2.text = Label.strip()

        if re.search('[\w]',ValueList):
            chld3=SubElement(body,'def:ValueListRef',
                    {'ValueListOID':'VL.'+Dataset.upper().strip()+'.'+Variable.upper().strip()
                        })
        if re.search('[\w]',Formatit):
            chld4=SubElement(body,'CodeListRef',
                    {'CodeListOID':'CL.'+Formatit.upper().strip()
                        })
        if re.search('[\w]',Origin):
            if Origin.strip() == 'Predecessor':
                chld5=SubElement(body,'def:Origin',
                        {'Type':Origin.strip()
                            })
                chld6 = SubElement(chld5,'Description')
                chld7 = SubElement(chld6,'TranslatedText',
                    {'xml:lang':"en"
                       }) 
                chld7.text = Orgdtl.strip()
            else:  
                chld5=SubElement(body,'def:Origin',
                        {'Type':Origin.strip(),
                         'Source':Source.strip(),
                            })

## generate the code list definition section

with open('code.csv', 'rt') as f:
    reader9 = csv.reader(f)
    next(reader9) 
    for row in reader9: 
        Frmt, Fmtname, Fmtnci, DataType, IsNonStandard, Standard = row
        if re.search('[\w]',IsNonStandard):
            body = SubElement(child3, 'CodeList', 
                {'OID': 'CL.'+Frmt.strip(),
                 'Name': Fmtname.strip(), 
                 'DataType': DataType.strip(), 
                 'def:IsNonStandard':IsNonStandard.strip(), 
                 })
            with open('codelist.csv', 'rt') as f:
                reader10 = csv.reader(f)
                next(reader10)
                for row in reader10: 
                    Fmt,  CodedValue, Valnci, Rank, OrderNumber, Decoded, Dictionary, Version, Href = row
                    if Fmt==Frmt:  
                        if re.search('[\w]',Dictionary):
                            chld = SubElement(body, 'ExternalCodeList',
                                {"Dictionary": Dictionary.strip(),
                                 "Version": Version.strip(), 
                                 "href":Href.strip(), 
                                 })
                        else:
                            if re.search('[\w]',Decoded) and re.search('[0-9]',Rank) and re.search('[0-9]',OrderNumber):
                                chld = SubElement(body, 'CodeListItem',
                                     {"CodedValue":CodedValue.strip(),
                                      "OrderNumber":OrderNumber.strip(), 
                                      "Rank":Rank.strip(), 
                                     })
                                chld2 = SubElement(chld, 'Decode')
                                chld3 = SubElement(chld2, 'TranslatedText')
                                chld3.text=Decoded.strip()
                            elif re.search('[\w]',Decoded) and re.search('[0-9]',Rank) and not re.search('[0-9]',OrderNumber):
                                chld = SubElement(body, 'CodeListItem',
                                     {"CodedValue":CodedValue.strip(),
                                      "Rank":Rank.strip(), 
                                     })
                                chld2 = SubElement(chld, 'Decode')
                                chld3 = SubElement(chld2, 'TranslatedText')
                                chld3.text=Decoded.strip()
                            elif re.search('[\w]',Decoded) and not re.search('[0-9]',Rank) and re.search('[0-9]',OrderNumber):
                                chld = SubElement(body, 'CodeListItem',
                                     {"CodedValue":CodedValue.strip(),
                                      "OrderNumber":OrderNumber.strip(), 
                                     })
                                chld2 = SubElement(chld, 'Decode')
                                chld3 = SubElement(chld2, 'TranslatedText')
                                chld3.text=Decoded.strip()
                            elif re.search('[\w]',Decoded) and not re.search('[0-9]',Rank) and not re.search('[0-9]',OrderNumber):
                                chld = SubElement(body, 'CodeListItem',
                                     {"CodedValue":CodedValue.strip(),
                                     })
                                chld2 = SubElement(chld, 'Decode')
                                chld3 = SubElement(chld2, 'TranslatedText')
                                chld3.text=Decoded.strip()
                            elif not re.search('[\w]',Decoded) and re.search('[0-9]',Rank) and re.search('[0-9]',OrderNumber):
                                chld = SubElement(body, 'EnumeratedItem',
                                     {"CodedValue":CodedValue.strip(),
                                      "OrderNumber":OrderNumber.strip(), 
                                      "Rank":Rank.strip(), 
                                     })
                            elif not re.search('[\w]',Decoded) and re.search('[0-9]',Rank) and not re.search('[0-9]',OrderNumber):
                                chld = SubElement(body, 'EnumeratedItem',
                                     {"CodedValue":CodedValue.strip(),
                                      "Rank":Rank.strip(), 
                                     })
                            elif not re.search('[\w]',Decoded) and not re.search('[0-9]',Rank) and re.search('[0-9]',OrderNumber):
                                chld = SubElement(body, 'EnumeratedItem',
                                     {"CodedValue":CodedValue.strip(),
                                      "OrderNumber":OrderNumber.strip(), 
                                     })
                            else:
                                chld = SubElement(body, 'EnumeratedItem',
                                     {"CodedValue":CodedValue.strip(),
                                     })
        if re.search('[\w]',Standard):
            body = SubElement(child3, 'CodeList', 
                {'OID': 'CL.'+Frmt.strip(),
                 'Name': Fmtname.strip(), 
                 'DataType': DataType.strip(), 
                 'def:StandardOID':Standard.strip(), 
                 })
            with open('codelist.csv', 'rt') as f:
                reader11 = csv.reader(f)
                next(reader11)
                for row in reader11: 
                    Fmt,  CodedValue, Valnci, Rank, OrderNumber, Decoded, Dictionary, Version, Href = row
                    if Fmt==Frmt:  
                        if re.search('[\w]',Dictionary):
                            chld = SubElement(body, 'ExternalCodeList',
                                {"Dictionary": Dictionary.strip(),
                                 "Version": Version.strip(), 
                                 "href":Href.strip(), 
                                 })
                        else:
                            if re.search('[\w]',Decoded) and re.search('[0-9]',Rank) and re.search('[0-9]',OrderNumber):
                                chld = SubElement(body, 'CodeListItem',
                                     {"CodedValue":CodedValue.strip(),
                                      "OrderNumber":OrderNumber.strip(), 
                                      "Rank":Rank.strip(), 
                                     })
                                chld2 = SubElement(chld, 'Decode')
                                chld3 = SubElement(chld2, 'TranslatedText')
                                chld3.text=Decoded.strip()

                                chld4=SubElement(body,'Alias', 
                                    {'Context':"nci:ExtCodeID", 
                                     'Name':Valnci.strip(),
                                    })
                            elif re.search('[\w]',Decoded) and re.search('[0-9]',Rank) and not re.search('[0-9]',OrderNumber):
                                chld = SubElement(body, 'CodeListItem',
                                     {"CodedValue":CodedValue.strip(),
                                      "Rank":Rank.strip(), 
                                     })
                                chld2 = SubElement(chld, 'Decode')
                                chld3 = SubElement(chld2, 'TranslatedText')
                                chld3.text=Decoded.strip()

                                chld4=SubElement(chld,'Alias', 
                                    {'Context':"nci:ExtCodeID", 
                                     'Name':Valnci.strip(),
                                    })
                            elif re.search('[\w]',Decoded) and not re.search('[0-9]',Rank) and re.search('[0-9]',OrderNumber):
                                chld = SubElement(body, 'CodeListItem',
                                     {"CodedValue":CodedValue.strip(),
                                      "OrderNumber":OrderNumber.strip(), 
                                     })
                                chld2 = SubElement(chld, 'Decode')
                                chld3 = SubElement(chld2, 'TranslatedText')
                                chld3.text=Decoded.strip()

                                chld4=SubElement(chld,'Alias', 
                                    {'Context':"nci:ExtCodeID", 
                                     'Name':Valnci.strip(),
                                    })
                            elif re.search('[\w]',Decoded) and not re.search('[0-9]',Rank) and not re.search('[0-9]',OrderNumber):
                                chld = SubElement(body, 'CodeListItem',
                                     {"CodedValue":CodedValue.strip(),
                                     })
                                chld2 = SubElement(chld, 'Decode')
                                chld3 = SubElement(chld2, 'TranslatedText')
                                chld3.text=Decoded.strip()

                                chld4=SubElement(chld,'Alias', 
                                    {'Context':"nci:ExtCodeID", 
                                     'Name':Valnci.strip(),
                                    })
                            elif not re.search('[\w]',Decoded) and re.search('[0-9]',Rank) and re.search('[0-9]',OrderNumber):
                                chld = SubElement(body, 'EnumeratedItem',
                                     {"CodedValue":CodedValue.strip(),
                                      "OrderNumber":OrderNumber.strip(), 
                                      "Rank":Rank.strip(), 
                                     })

                                chld4=SubElement(chld,'Alias', 
                                    {'Context':"nci:ExtCodeID", 
                                     'Name':Valnci.strip(),
                                    })
                            elif not re.search('[\w]',Decoded) and re.search('[0-9]',Rank) and not re.search('[0-9]',OrderNumber):
                                chld = SubElement(body, 'EnumeratedItem',
                                     {"CodedValue":CodedValue.strip(),
                                      "Rank":Rank.strip(), 
                                     })

                                chld4=SubElement(chld,'Alias', 
                                    {'Context':"nci:ExtCodeID", 
                                     'Name':Valnci.strip(),
                                    })
                            elif not re.search('[\w]',Decoded) and not re.search('[0-9]',Rank) and re.search('[0-9]',OrderNumber):
                                chld = SubElement(body, 'EnumeratedItem',
                                     {"CodedValue":CodedValue.strip(),
                                      "OrderNumber":OrderNumber.strip(), 
                                     })

                                chld4=SubElement(chld,'Alias', 
                                    {'Context':"nci:ExtCodeID", 
                                     'Name':Valnci.strip(),
                                    })
                            else:
                                chld = SubElement(body, 'EnumeratedItem',
                                     {"CodedValue":CodedValue.strip(),
                                     })
                                chld4=SubElement(chld,'Alias', 
                                    {'Context':"nci:ExtCodeID", 
                                     'Name':Valnci.strip(),
                                    })
            chld5=SubElement(body,'Alias', 
                    {'Context':"nci:ExtCodeID", 
                     'Name':Fmtnci.strip(),
                     })

## generate the methods definition section

with open('defvar.csv', 'rt') as g:
    reader12 = csv.reader(g)
    next(reader12)
    for row in reader12:
        Dataset, Variable, OrderNumber, Mandatory, KeySequence, Method, Typeit = row
        if re.search('[\w]',Method):
            podc = SubElement(child3, 'MethodDef',
                  {'OID':'MT.'+ Dataset.upper().strip()+'.'+ Variable.upper().strip(),
                   'Name':'MT.'+ Dataset.upper().strip()+'.'+ Variable.upper().strip(),
                   'Type':Typeit.strip(),
                   })
            chld3 = SubElement(podc,"Description")
            chld4 = SubElement(chld3,"TranslatedText")
            chld4.text = Method.strip() 

with open('defvar2.csv', 'rt') as f:
    reader13 = csv.reader(f)
    next(reader13)
    for row in reader13: 
        Dataset,Variable, Paramcd, Mandatory, OrderNumber, Method, Document, PageRefs, Type, Typ, DataType, Length, DisplayFormat, SignificantDigits, Comment, Label, ValueList, Formatit, Origin, Orgdtl, Source = row
        if re.search('[\w]',Paramcd) and re.search('[\w]',Method): 
            podc = SubElement(child3, 'MethodDef',
                  {'OID':'MT.'+ Dataset.upper().strip()+'.'+ Variable.upper().strip()+'.'+Paramcd.strip(),
                   'Name':'MT.'+ Dataset.upper().strip()+'.'+ Variable.upper().strip()+'.'+Paramcd.strip(),
                   'Type':Typ.strip(),
                   })
            chld3 = SubElement(podc,"Description")
            chld4 = SubElement(chld3,"TranslatedText")
            chld4.text = Method.strip() 
            if re.search('[\w]', Document): 
                chld5 = SubElement(podc,"def:DocumentRef", 
                        {'leafID':'LF.'+Document.strip()
                            })
                chld6 = SubElement(chld5,'def:PDFPageRef',
                        {'PageRefs':PageRefs,
                         'Type':Type, 
                         })

### generate the comments definition section

with open('defds.csv', 'rt') as f:
    reader14 = csv.reader(f )
    next(reader14)
    for row in reader14:
        Data, Repeating ,IsReferenceData,Purpose,Standard,Structure,Label ,Classit, SubClass, Comment ,Doc1,Doc2 ,PageRef2,PageTyp2 = row
        body = SubElement(child3, 'def:CommentDef', 
                {'OID': "COM."+ Data.upper().strip(),
                 })
        chld = SubElement(body, 'Description') 
        chld2 = SubElement(chld, 'TranslatedText',
                {'xml:lang':"en"
                    }) 
        chld2.text = Comment.strip()
        if re.search('[\w]',Doc1):
            chld3 = SubElement(body,'def:DocumentRef',
                {'leafID':'LF.'+Doc1.strip(),
                    })
        if re.search('[\w]',Doc2):
            chld4 = SubElement(body,'def:DocumentRef',
                {'leafID':'LF.'+Doc2.strip(),
                    })
            if re.search('[\w]',PageRef2):
                chld5 = SubElement(chld4,'def:PDFPageRef',
                    {'PageRefs': PageRef2.strip(), 
                     'Type': PageTyp2.strip(),
                     })

with open('defvar2.csv', 'rt') as f:
    reader15 = csv.reader(f )
    next(reader15)
    for row in reader15:
        Dataset,Variable, Paramcd, Mandatory, Order, Method, Document, PageRefs, Type, Typ, DataType, Length, DisplayFormat, SignificantDigits, Comment, Label, ValueList, Formatit, Origin, Orgdtl, Source = row
        if re.search('[\w]',Paramcd):
            oid='COM.'+Dataset.upper().strip()+'.'+Variable.upper().strip()+'.'+Paramcd.upper().strip()
        else:
            oid='COM.'+Dataset.upper().strip()+'.'+Variable.upper().strip()
        if re.search('[\w]',Comment):
            body = SubElement(child3, 'def:CommentDef', 
                    {'OID': oid,
                      })
            chld = SubElement(body, 'Description') 
            chld2 = SubElement(chld, 'TranslatedText',
                {'xml:lang':"en"
                }) 
            chld2.text = Comment.strip()

with open('standard.csv', 'rt') as f:
    reader16 = csv.reader(f )
    next(reader16)
    for row in reader16:
        OID,Name ,Type ,PublishingSet ,Status ,Version ,CommentID ,Comment = row 
        if re.search('[\w]',Comment):
            body = SubElement(child3, 'def:CommentDef', 
                   {'OID': 'COM.'+CommentID.strip(),
                   })
            chld = SubElement(body, 'Description') 
            chld2 = SubElement(chld, 'TranslatedText',
                    {'xml:lang':"en"
                    }) 
            chld2.text = Comment.strip()


with open('arm2.csv', 'rt') as g:
    reader17 = csv.reader(g)
    next(reader17)
    for row in reader17:
        Oid2, Id2, Parameter, AnalysisReason, AnalysisPurpose, AnalysisDescription, CommentID, Comment, Dataset, Variable,  Documentation,Document, PageRefs2, Type2, Title2, Context, Code, File = row
        if re.search('[\w]', CommentID): 
            body = SubElement(child3, 'def:CommentDef', 
                   {'OID': 'COM.'+CommentID.strip(),
                   })
            chld = SubElement(body, 'Description') 
            chld2 = SubElement(chld, 'TranslatedText',
                    {'xml:lang':"en"
                    }) 
            chld2.text = Comment.strip()

## generate the leafs definition section            

with open('leaf.csv', 'rt') as f:
    reader18 = csv.reader(f)
    next(reader18)
    for row in reader18: 
        ID, File, Name = row
        body = SubElement(child3, 'def:leaf', 
             {'ID': 'LF.'+ID.strip(),
              'xlink:href': File.strip(),
              })
        chld = SubElement(body, 'def:title')
        chld.text=Name.strip()

## generate the ARM section 

body = SubElement(child3, 'arm:AnalysisResultDisplays') 
with open('arm.csv', 'rt') as f:
    reader19 = csv.reader(f)
    next(reader19)
    for row in reader19:
        ID, Name, Description, Leaf, PageRefs, Typ, Title = row
        chld = SubElement(body, 'arm:ResultDisplay', 
                {'OID':'RD.'+ID.strip(),
                 'Name':Name.strip(), 
                 })
        chld1 = SubElement(chld, 'Description') 
        chld2 = SubElement(chld1, 'TranslatedText',
                {'xml:lang':"en", 
                }) 
        chld2.text = Description.strip()
        chld3 = SubElement(chld, 'def:DocumentRef',
                {'leafID':'LF.'+Leaf.strip(),
                }) 
        chld4 = SubElement(chld3, 'def:PDFPageRef',
                {'PageRefs':PageRefs.strip(), 
                 'Type':Typ.strip(),
                 'Title':Title.strip(),
                 }) 
        with open('arm2.csv', 'rt') as g:
            reader20 = csv.reader(g)
            next(reader20)
            for row in reader20:
                Oid2, Id2, Parameter, AnalysisReason, AnalysisPurpose, AnalysisDescription, CommentID, Comment, Dataset, Variable,  Documentation,Document, PageRefs2, Type2, Title2, Context, Code, File = row
                if Oid2.upper().strip()==ID.upper().strip() :
                    if re.search('[\w]', Parameter):  
                        podc = SubElement(chld, 'arm:AnalysisResult',
                                  {'OID':'AR.'+Id2.strip(),
                                   'ParameterOID':'IT.'+Dataset.strip()+'.'+Parameter.strip(),
                                   'AnalysisReason':AnalysisReason.strip(),
                                   'AnalysisPurpose':AnalysisPurpose.strip(),
                                   })
                    else: 
                        podc = SubElement(chld, 'arm:AnalysisResult',
                                  {'OID':'AR.'+Id2.strip(),
                                   'AnalysisReason':AnalysisReason.strip(),
                                   'AnalysisPurpose':AnalysisPurpose.strip()
                                   })
                    chld3 = SubElement(podc,"Description",
                            {"xml:lang":"en",
                            })
                    chld4 = SubElement(chld3,"TranslatedText")
                    chld4.text=AnalysisDescription.strip()
                    if not re.search('[\w]', CommentID): 
                        chld5 = SubElement(podc,"arm:AnalysisDatasets")
                    else:
                        chld5 = SubElement(podc,"arm:AnalysisDatasets", 
                                {'def:CommentOID':'COM.'+CommentID.strip()
                                    })
                    if not re.search(';', Dataset) and not re.search(';', Variable): 
                        chld6 = SubElement(chld5, "arm:AnalysisDataset", 
                                {'ItemGroupOID':'IG.'+Dataset.strip()
                                })

                        chld7 = SubElement(chld6,"def:WhereClauseRef", 
                                {'WhereClauseOID': 'WC.'+Id2.strip()+'.'+Dataset.strip(),
                                })
                        chld8 = SubElement(chld6,"arm:AnalysisVariable", 
                                {'ItemOID':'IT.'+Dataset.strip()+'.'+Variable.strip()
                                })


                    elif  not re.search(';', Dataset) and re.search(';', Variable):
                        it2ms=Variable.strip().split(';')
                        chld6 = SubElement(chld5, "arm:AnalysisDataset", 
                               {'ItemGroupOID':'IG.'+Dataset.strip()
                               })
                        chld7 = SubElement(chld6,"def:WhereClauseRef", 
                              {'WhereClauseOID': 'WC.'+Id2.strip()+'.'+Dataset.strip(),
                              })
                        for it2m in it2ms: 
                            chld8 = SubElement(chld6,"arm:AnalysisVariable", 
                                   {'ItemOID':'IT.'+it2m.strip()
                                   })
                    elif  re.search(';', Dataset) and re.search(';', Variable):
                        itms=Dataset.split(';')
                        it2ms=Variable.strip().split(';')
                        for itm in itms:
                            chld6 = SubElement(chld5, "arm:AnalysisDataset", 
                                   {'ItemGroupOID':'IG.'+itm.strip()
                                   })

                            chld7 = SubElement(chld6,"def:WhereClauseRef", 
                                  {'WhereClauseOID': 'WC.'+Id2.strip()+'.'+itm.strip(),
                                  })
                            for it2m in it2ms: 
                                if it2m[:len(itm)]==itm:
                                    chld8 = SubElement(chld6,"arm:AnalysisVariable", 
                                         {'ItemOID':'IT.'+it2m.strip()
                                         })
                    chld9 = SubElement(podc, 'arm:Documentation')
                    chld10 = SubElement(chld9,'Description')
                    chld11 = SubElement(chld10,'TranslatedText')
                    chld11.text=Documentation.strip()
                    chld12 = SubElement(chld9, 'def:DocumentRef', 
                            {'leafID':'LF.'+Document.strip(), 
                                })
                    chld13 = SubElement(chld12, 'def:PDFPageRef', 
                            {'PageRefs': PageRefs2.strip(), 
                             'Type': Type2.strip(), 
                             'Title': Title2.strip(), 
                             })
                    chld14 = SubElement(podc,'arm:ProgrammingCode', 
                            {'Context':Context.strip(),
                                })
                    if re.search('[\w]', Code): 
                        chld15 = SubElement(chld14, 'arm:Code')
                        chld15.text=Code.strip()
                    elif re.search('[\w]', File): 
                        chld15 = SubElement(chld14, 'def:DocumentRef', 
                                {'leafID': 'LF.'+File.strip()
                                    })

sys.stdout = open('define.xml','w')
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

print(prettify(root))
sys.stdout.close()
