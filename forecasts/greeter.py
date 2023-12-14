from datetime import datetime
from types import NoneType
from django.contrib import messages
from django.utils.html import format_html
import os
from django.conf import settings
import numpy as np
import pandas as pd
from confirm_invoice.models import ConfirmInvoiceDetail, ConfirmInvoiceHeader
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, Paragraph, Table, Frame
from reportlab.lib import colors
from books.models import Book, ReviseBook
from products.models import Product, ProductGroup

from upload_forecast.models import ForecastErrorLogs, OnMonthList, OnYearList
from users.models import PlanningForecast, Section, Supplier

styles = getSampleStyleSheet()
styleN = styles['Normal']
style = getSampleStyleSheet()
styleH = styles['Heading1']


import nanoid
import requests

from forecasts.models import Forecast, ForecastDetail
from open_pds.models import PDSDetail, PDSHeader
from formula_vcst.models import BOOK, COOR, CORP, DEPT, EMPLOYEE, PROD, SECT, UM, NoteCut, OrderH, OrderI

def create_purchase_order(request, id, prefixRef="PR", bookGroup="0002"):
    dte = datetime.now()
    ordH = None
    # return print(request.POST.get("pds_delivery_date"))
    try:
        ## Line Notification
        token = os.environ.get("LINE_TOKEN")
        if type(request.user.line_notification_id) != type(None):
            token = request.user.line_notification_id.token
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {token}'
        }
        
        ### Get Formula Master Data
        formulaUser = "TEST"
        if type(request.user.formula_user_id) != type(None):
            formulaUser = request.user.formula_user_id.code
            
        formulaDepartment = "-"
        if type(request.user.department_id)!= type(None):
            formulaDepartment = request.user.department_id.code
            
        formulaSect = "-"
        if type(request.user.section_id)!= type(None):
            formulaSect = request.user.section_id.code
        
        emp = EMPLOYEE.objects.filter(FCCODE=formulaUser).values()
        dept = DEPT.objects.filter(FCCODE=formulaDepartment).values()
        sect = SECT.objects.filter(FCCODE=formulaSect).values()
        corp = CORP.objects.filter(FCCODE="2023 (2566)").values()
        ordBook = BOOK.objects.filter(FCREFTYPE=prefixRef, FCCODE=bookGroup).values()
        
        fcStep = "1"
        if prefixRef == "PO":
            # fcStep = "P"
            obj = PDSHeader.objects.get(id=id)
            ### Get Supplier Information
            supplier = COOR.objects.filter(FCCODE=obj.forecast_id.supplier_id.code).values()
            ordH = None
            if obj.ref_formula_id is None:
                lastNum = OrderH.objects.filter(FDDATE__lte=obj.pds_date).order_by('-FCCODE').first()
                if lastNum is None:
                    lastNum = "0"
                fccodeNo = f"{int(str(lastNum)) + 1:07d}"
                prNo = f"{str(ordBook[0]['FCPREFIX']).strip()}{fccodeNo}"### PR TEST REFNO
                msg = f"message=เรียนแผนก PU\nขณะนี้ทางแผนก Planning ได้ทำการเปิดเอกสาร{str(ordBook[0]['FCNAME']).strip()} เลขที่ {prNo} เรียบร้อยแล้วคะ"
                
                ordH = OrderH()
                ordH.FCSKID=nanoid.generate(size=8)
                ordH.FDDUEDATE=request.POST.get("pds_delivery_date")
                ordH.FCCODE=fccodeNo
                ordH.FCREFNO=prNo
                obj.ref_formula_id = ordH.FCSKID
                
            else:
                ordH = OrderH.objects.get(FCSKID=obj.ref_formula_id)
                pass
            
            ordH.FCREFTYPE=prefixRef
            ordH.FCDEPT=dept[0]['FCSKID']
            ordH.FCSECT=sect[0]['FCSKID']
            ordH.FCBOOK=ordBook[0]['FCSKID']
            ordH.FCCREATEBY=emp[0]['FCSKID']
            ordH.FCAPPROVEB=""
            ordH.FCCOOR=supplier[0]['FCSKID']
            ordH.FCCORP=corp[0]['FCSKID']
            ordH.FDDATE=obj.pds_date
            ordH.FNAMT=obj.qty
            ordH.FCSTEP=fcStep
            ordH.save()
            
            ### Create Confirm Invoice
            confirmInv = ConfirmInvoiceHeader()
            confirmInv.approve_by_id = request.user
            confirmInv.pds_id = obj
            confirmInv.supplier_id = obj.supplier_id
            confirmInv.part_model_id = obj.part_model_id
            confirmInv.purchase_no = ordH.FCREFNO
            confirmInv.inv_date = datetime.now()
            confirmInv.item = 0
            confirmInv.qty = 0
            confirmInv.is_active = True
            confirmInv.save()
            
            ordDetail = PDSDetail.objects.filter(pds_header_id=obj, qty__gt=0).all()
            seq = 1
            qty = 0
            summary_price = 0
            summary_balance = 0
            for i in ordDetail:
                #### Sum Balance
                summary_balance += i.balance_qty
                
                if i.is_select is True and i.qty > 0:
                    ordI = None
                    ordProd = PROD.objects.filter(FCCODE=i.forecast_detail_id.product_id.code,FCTYPE=i.forecast_detail_id.product_id.prod_type_id.code).values()
                    unitObj = UM.objects.filter(FCCODE=i.forecast_detail_id.product_id.unit_id.code).values()
                    summary_price += int(ordProd[0]['FNSTDCOST']) * i.qty
                    currentPrice = int(ordProd[0]['FNSTDCOST']) * i.qty
                    try:
                        # ordI = OrderI.objects.get(FCSKID=i.ref_formula_id)
                        ordI = OrderI.objects.get(FCORDERH=ordH.FCSKID,FCPROD=ordProd[0]["FCSKID"])
                        ordI.FCCOOR=supplier[0]['FCSKID']
                        ordI.FCCORP=corp[0]['FCSKID']
                        ordI.FCDEPT=dept[0]['FCSKID']
                        ordI.FCORDERH=ordH.FCSKID
                        ordI.FCPROD=ordProd[0]["FCSKID"]
                        ordI.FCPRODTYPE=ordProd[0]["FCTYPE"]
                        ordI.FCREFTYPE=prefixRef
                        ordI.FCSECT=sect[0]['FCSKID']
                        ordI.FCSEQ=f"{seq:03d}"
                        ordI.FCSTUM=unitObj[0]["FCSKID"]
                        ordI.FCUM=unitObj[0]["FCSKID"]
                        ordI.FCUMSTD=unitObj[0]["FCSKID"]
                        ordI.FDDATE=obj.pds_date
                        ordI.FNQTY=i.qty
                        ordI.FMREMARK=i.remark
                        #### Update Nagative to Positive
                        olderQty = int(ordI.FNBACKQTY)
                        ordI.FNBACKQTY=abs(int(i.qty)-olderQty)
                        ######
                        ordI.FNPRICE=currentPrice
                        ordI.FNPRICEKE=currentPrice
                        ordI.FCSHOWCOMP=""
                        ordI.FCSTEP=fcStep
                            
                    except OrderI.DoesNotExist as e:
                        ordI = OrderI(
                            FCSKID=nanoid.generate(size=8),
                            FCCOOR=supplier[0]['FCSKID'],
                            FCCORP=corp[0]['FCSKID'],
                            FCDEPT=dept[0]['FCSKID'],
                            FCORDERH=ordH.FCSKID,
                            FCPROD=ordProd[0]["FCSKID"],
                            FCPRODTYPE=ordProd[0]["FCTYPE"],
                            FCREFTYPE=prefixRef,
                            FCSECT=sect[0]['FCSKID'],
                            FCSEQ=f"{seq:03d}",
                            FCSTUM=unitObj[0]["FCSKID"],
                            FCUM=unitObj[0]["FCSKID"],
                            FCUMSTD=unitObj[0]["FCSKID"],
                            FDDATE=obj.pds_date,
                            FNQTY=i.qty,
                            FMREMARK=i.remark,
                            FNBACKQTY=i.balance_qty,
                            FNPRICE=currentPrice,
                            FNPRICEKE=currentPrice,
                            FCSHOWCOMP="",
                            FCSTEP=fcStep,
                        )
                        pass
                    
                    ordI.save()
                    
                    ### Create Notecut
                    orderPRID = obj.forecast_id.ref_formula_id
                    orderPRDetailID = i.forecast_detail_id.ref_formula_id
                    
                    ### Update PR to FCSTEP='P'
                    prHeader = OrderH.objects.get(FCSKID=orderPRID)
                    prHeader.FCSTEP = fcStep
                    prHeader.save()
                    
                    prDetail = OrderI.objects.get(FCSKID=orderPRDetailID)
                    prDetail.FCSTEP = fcStep
                    prDetail.save()
                    #### End Update FCSTEP
                    
                    ### Create Invoice Details
                    invDetail = ConfirmInvoiceDetail()
                    invDetail.invoice_header_id = confirmInv
                    invDetail.pds_detail_id = i
                    invDetail.seq = seq
                    invDetail.qty = i.qty
                    invDetail.confirm_qty = i.qty
                    invDetail.total_qty = i.qty
                    invDetail.price = int(ordProd[0]['FNSTDCOST'])
                    invDetail.remark = ""
                    invDetail.ref_formula_id = ordI.FCSKID
                    invDetail.save()
                    
                    ### Save Invoice Detail
                    orderPOID = ordH.FCSKID
                    orderPODetailID = ordI.FCSKID
                    
                    ### Create Notecut
                    noteCut = NoteCut(
                            FCAPPNAME="",
                            FCSKID=nanoid.generate(size=8),
                            FCCHILDH=orderPRID,
                            FCCHILDI=orderPRDetailID,
                            FCMASTERH=orderPOID,
                            FCMASTERI=orderPODetailID,
                            FNQTY=i.qty,
                            FNUMQTY=i.qty,
                            FCCORRECTB=emp[0]["FCSKID"],
                            FCCREATEBY=emp[0]["FCSKID"],
                            FCCREATETY="",
                            FCCUACC="",
                            FCDATAIMP="",
                            FCORGCODE="",
                            FCSELTAG="",
                            FCSRCUPD="",
                            FCU1ACC="",
                            FCUDATE="",
                            FCUTIME="",
                            FCCORP=corp[0]['FCSKID']
                        )
                    noteCut.save()
                    # Update Status Order Details
                    i.ref_formula_id = ordI.FCSKID
                    i.request_status = "1"
                    i.qty = i.balance_qty
                    i.is_select = i.balance_qty > 0
                    i.save()
                    
                    # Summary Seq/Qty
                    seq += 1
                    qty += i.qty
            
            ordH.FNAMT=summary_price
            ordH.save()
            # print(f"{ordH.FCREFNO}: {len(ordH.FCREFNO)}")
            # ordDetail = PDSDetail.objects.filter(pds_header_id=obj, qty__gt=0).all()
            # seq = 1
            # qty = 0
            # summary_price = 0
            # summary_balance = 0
            ordDetail = PDSDetail.objects.filter(pds_header_id=obj, qty__gt=0).all()
            seq = 0
            qty = 0
            summary_price = 0
            for i in ordDetail:
                seq += 1
                qty += i.qty
                summary_price += int(i.price) * i.qty
                i.seq = seq
                i.is_select = True
                i.save()
                
            obj.approve_by_id = request.user
            obj.item = seq
            obj.qty = qty
            obj.balance_qty = qty
            obj.summary_price = summary_price
            
            if summary_balance == 0:
                obj.pds_status = "2"
                obj.pds_no = ordH.FCREFNO
                obj.ref_formula_id = ordH.FCSKID
                
            else:
                obj.pds_status = "1"
                obj.pds_delivery_date = None
            obj.save()
            
            
            # confirmInv.inv_delivery_date
            # confirmInv.inv_no
            conInvDetail = ConfirmInvoiceDetail.objects.filter(invoice_header_id=confirmInv)
            seq = 0
            qty = 0
            summary_price = 0
            for i in conInvDetail:
                seq += 1
                qty += i.qty
                summary_price += int(i.price) * i.qty
            
            confirmInv.item = seq
            confirmInv.qty = qty
            confirmInv.confirm_qty = qty
            confirmInv.summary_price = summary_price
            confirmInv.inv_status = "0"
            confirmInv.ref_formula_id = ordH.FCSKID
            confirmInv.save()
            
            ### Message Notification
            msg = f"message=เรียนแผนก PU \nขณะนี้ทางแผนก Planning ได้ทำการอนุมัติเอกสาร {ordH.FCREFNO} เรียบร้อยแล้วคะ"
            requests.request("POST", "https://notify-api.line.me/api/notify", headers=headers, data=msg.encode("utf-8"))
        else:
            ### Create PR
            obj = Forecast.objects.get(id=id)
            ### Create PDSHeader
            pdsHead = None
            pdsCount = PDSHeader.objects.filter(pds_date=dte).count() + 1
            pds_no = f"PDS{str(dte.strftime('%Y%m'))[3:]}{pdsCount:04d}"
            try:
                pdsHead = PDSHeader.objects.get(forecast_id=obj)
            except PDSHeader.DoesNotExist:
                pdsHead = PDSHeader()
                pass
            
            pdsHead.forecast_id = obj
            pdsHead.supplier_id = obj.supplier_id
            pdsHead.part_model_id = obj.part_model_id
            pdsHead.forecast_plan_id = obj.forecast_plan_id
            pdsHead.pds_date = datetime.now()
            pdsHead.pds_revise_id = obj.forecast_revise_id
            pdsHead.pds_on_month_id = obj.forecast_on_month_id
            pdsHead.pds_on_year_id = obj.forecast_on_year_id
            pdsHead.pds_no = pds_no
            pdsHead.item = 0
            pdsHead.qty = 0
            pdsHead.balance_qty = 0
            pdsHead.summary_price = 0
            pdsHead.is_active = True
            pdsHead.save()
            ### End PDSHeader
            
            supplier = COOR.objects.filter(FCCODE=obj.supplier_id.code).values()
            ordH = None
            if obj.ref_formula_id is None:
                ### Create PR to Formula
                # #### Create Formula OrderH
                lastNum = OrderH.objects.filter(FDDATE__lte=obj.forecast_date).order_by('-FCCODE').first()
                if lastNum is None:
                    lastNum = "0"
                    
                fccodeNo = f"{int(str(lastNum)) + 1:07d}"
                prNo = f"{str(ordBook[0]['FCPREFIX']).strip()}{fccodeNo}"### PR TEST REFNO
                msg = f"message=เรียนแผนก Planning\nขณะนี้ทางแผนก PU ได้ทำการอนุมัติเอกสาร {prNo} เรียบร้อยแล้วคะ"
                ordH = OrderH()
                ordH.FCCODE = fccodeNo
                ordH.FCREFNO = prNo
                ordH.FCSKID=nanoid.generate(size=8)
                obj.ref_formula_id = ordH.FCSKID
                
            else:
                ordH = OrderH.objects.get(FCSKID=obj.ref_formula_id)
                msg = f"message=เรียนแผนก Planning\nขณะนี้ทางแผนก PU ได้ทำการอนุมัติเอกสาร {ordH.FCREFNO} เรียบร้อยแล้วคะ"
                pass
            
            ordH.FCREFTYPE=prefixRef
            ordH.FCDEPT=dept[0]['FCSKID']
            ordH.FCSECT=sect[0]['FCSKID']
            ordH.FCBOOK=ordBook[0]['FCSKID']
            ordH.FCCREATEBY=emp[0]['FCSKID']
            ordH.FCAPPROVEB=""
            ordH.FCCOOR=supplier[0]['FCSKID']
            ordH.FCCORP=corp[0]['FCSKID']
            ordH.FDDATE=obj.forecast_date
            ordH.FDDUEDATE=obj.forecast_date
            ordH.FNAMT=0
            ordH.FCSTEP=fcStep
            ordH.save()
            # ### OrderI
            # # Get Order Details
            ordDetail = ForecastDetail.objects.filter(forecast_id=obj, request_qty__gt=0).all()
            seq = 1
            qty = 0
            summary_price = 0
            for i in ordDetail:
                ### Create OrderI Formula
                try:
                    ordProd = PROD.objects.filter(FCCODE=i.product_id.code,FCTYPE=i.product_id.prod_type_id.code).values()
                    unitObj = UM.objects.filter(FCCODE=i.product_id.unit_id.code).values()
                    summary_price += int(ordProd[0]['FNSTDCOST']) * int(i.request_qty)
                    currentPrice = int(ordProd[0]['FNSTDCOST']) * int(i.request_qty)
                    ### Create PDS Detail
                    pdsDetail = None
                    try:
                        pdsDetail = PDSDetail.objects.get(pds_header_id=pdsHead,forecast_detail_id=i)
                    except PDSDetail.DoesNotExist:
                        pdsDetail = PDSDetail()
                        pdsDetail.pds_header_id = pdsHead
                        pdsDetail.forecast_detail_id = i
                        pass
                    
                    pdsDetail.seq = seq
                    pdsDetail.qty = i.request_qty
                    pdsDetail.balance_qty = i.request_qty
                    pdsDetail.price = currentPrice
                    # pdsDetail.total_seq = seq
                    # pdsDetail.total_qty = i.request_qty
                    # pdsDetail.total_balance_qty = i.request_qty
                    # pdsDetail.total_price = currentPrice 
                    pdsDetail.remark = i.remark
                    pdsDetail.is_active = True
                    pdsDetail.save()
                    print(f"Save PDS Detail: {pdsDetail}")
                    ### End PDS Detail
                
                    ordI = None
                    try:
                        ordI = OrderI.objects.get(FCSKID=i.ref_formula_id)
                        ordI.FCCOOR=supplier[0]['FCSKID']
                        ordI.FCCORP=corp[0]['FCSKID']
                        ordI.FCDEPT=dept[0]['FCSKID']
                        ordI.FCORDERH=ordH.FCSKID
                        ordI.FCPROD=ordProd[0]["FCSKID"]
                        ordI.FCPRODTYPE=ordProd[0]["FCTYPE"]
                        ordI.FCREFTYPE=prefixRef
                        ordI.FCSECT=sect[0]['FCSKID']
                        ordI.FCSEQ=f"{seq:03d}"
                        ordI.FCSTUM=unitObj[0]["FCSKID"]
                        ordI.FCUM=unitObj[0]["FCSKID"]
                        ordI.FCUMSTD=unitObj[0]["FCSKID"]
                        ordI.FDDATE=obj.forecast_date
                        ordI.FNQTY=i.request_qty
                        ordI.FMREMARK=i.remark
                        #### Update Nagative to Positive
                        olderQty = int(ordI.FNBACKQTY)
                        ordI.FNBACKQTY=abs(int(i.request_qty)-olderQty)
                        ordI.FCSTEP = fcStep
                        ######
                        ordI.FNPRICE=currentPrice
                        ordI.FNPRICEKE=currentPrice
                        ordI.FCSHOWCOMP=""
                            
                    except OrderI.DoesNotExist as e:
                        ordI = OrderI(
                            FCSKID=nanoid.generate(size=8),
                            FCCOOR=supplier[0]['FCSKID'],
                            FCCORP=corp[0]['FCSKID'],
                            FCDEPT=dept[0]['FCSKID'],
                            FCORDERH=ordH.FCSKID,
                            FCPROD=ordProd[0]["FCSKID"],
                            FCPRODTYPE=ordProd[0]["FCTYPE"],
                            FCREFTYPE=prefixRef,
                            FCSECT=sect[0]['FCSKID'],
                            FCSEQ=f"{seq:03d}",
                            FCSTUM=unitObj[0]["FCSKID"],
                            FCUM=unitObj[0]["FCSKID"],
                            FCUMSTD=unitObj[0]["FCSKID"],
                            FDDATE=obj.forecast_date,
                            FNQTY=i.request_qty,
                            FMREMARK=i.remark,
                            FNBACKQTY=i.request_qty,
                            FNPRICE=currentPrice,
                            FNPRICEKE=currentPrice,
                            FCSHOWCOMP="",
                            FCSTEP = fcStep,
                        )
                        pass
                    
                    ordI.save()
                    # Update Status Order Details
                    i.ref_formula_id = ordI.FCSKID
                    i.request_status = "1"
                    
                except Exception as e:
                    messages.error(request, str(e))
                    ordH.delete()
                    return
                # Summary Seq/Qty
                seq += 1
                qty += i.request_qty
                i.save()
                
            ordH.FNAMT = summary_price
            ordH.save()
                
            pdsHead.item = (seq - 1)
            pdsHead.qty = qty
            pdsHead.balance_qty = qty
            pdsHead.summary_price = summary_price
            # ### Original
            # pdsHead.total_item = (seq - 1)
            # pdsHead.total_qty = qty
            # pdsHead.total_balance_qty = qty
            # pdsHead.total_summary_price = summary_price
            pdsHead.save()
                
            obj.forecast_no = ordH.FCREFNO
            obj.forecast_status = "1"
            obj.forecast_qty = qty
            obj.forecast_item = (seq - 1)
            obj.save()
            
            ### Message Notification
            msg = f"message=เรียนแผนก Planning\nขณะนี้ทางแผนก PU ได้ทำการอนุมัติเอกสาร {obj.forecast_no} เรียบร้อยแล้วคะ"
            requests.request("POST", "https://notify-api.line.me/api/notify", headers=headers, data=msg.encode("utf-8"))
            # messages.success(request, f"บันทึกข้อมูลเรียบร้อยแล้ว")
        
    except Exception as ex:
        messages.error(request, str(ex))
        return False
        # pass
    
    return True

def upload_file_forecast(request, obj, form, change):
    try:
        isAllErrors = 0
        ### Read Excel data
        data = pd.read_excel(request.FILES['file_forecast'], sheet_name=0)
        ### - To Nan
        data.replace('-', np.nan, inplace=True)
        
        ### VCST To Nan
        data.replace('VCST', np.nan, inplace=True)
        
        ### Nan to 0
        data.fillna(0, inplace=True)
        df = data.to_records()
        docs = []
        i = 0
        for r in df:
            if i > 0:
                rows = int(r[0]) + 2
                partNo = str(r[2]).strip()
                partCode = str(r[3]).strip()
                partDescription = str(r[4]).strip()
                supName = str(r[5]).strip()
                partModel = str(r[6]).strip()
                rev0 = int(r[7])
                rev1 = int(r[8])
                rev2 = int(r[9])
                rev3 = int(r[10])
                month0 = 0
                month1 = int(r[11])
                month2 = int(r[12])
                month3 = int(r[13])
                
                isError = False
                msgProduct = ""
                msgSup = ""
                msgPartModel = ""
                description  = ""
                part = None
                if partCode == "0":
                    isError = True
                    msgProduct = f"ไม่ระบุ Part Code"
                    
                else:
                    part = Product.objects.filter(code=str(partCode).strip()).count()
                    if part == 0:
                        msgProduct = f"ไม่พบข้อมูล Part:{partNo}"
                        isError = True
                
                supFilter = None
                if supName == "0":
                    isError = True
                    msgSup = f"ไม่ระบุ Sup."
                    
                else:                   
                    supFilter = Supplier.objects.filter(code=str(supName).strip()).count()
                    if supFilter == 0:
                        isError = True
                        msgSup = f"ไม่พบข้อมูล Sup:{supName}"
                        
                # partModelFilter = None
                # if partModel == "0":
                #     isError = True
                #     msgPartModel = f"ไม่ระบุ Model."
                    
                # else:                   
                #     partModelFilter = ProductGroup.objects.filter(code=str(partModel).strip()).count()
                #     if partModelFilter == 0:
                #         isError = True
                #         msgPartModel = f"ไม่พบข้อมูล Model:{partModel}"
                        
                
                # try:
                #     partFormula = PROD.objects.get(FCCODE=str(partCode).strip())
                #     # print(partFormula)
                # except PROD.DoesNotExist:
                #     print(f"Not Found: {partCode}")
                # print(partModel)
                # print(f"====")
                ### Check revise type
                qty = rev0
                if obj.forecast_revise_id.code == 1:
                    qty = rev1
                    
                elif obj.forecast_revise_id.code == 2:
                    qty = rev2
                    
                elif obj.forecast_revise_id.code == 3:
                    qty = rev3
                
                docs.append({
                    "rows": rows,
                    "partNo": partNo,
                    "partCode": partCode,
                    "partDescription": partDescription,
                    "supName": supName,
                    "partModel": partModel,
                    "rev0": rev0,
                    "rev1": rev1,
                    "rev2": rev2,
                    "rev3": rev3,
                    "qty": qty,
                    "month0": qty,
                    "month1": month1,
                    "month2": month2,
                    "month3": month3,
                })
                if isError:
                    # description = str(f"{msgSup} {msgProduct} {msgPartModel} บรรทัดที่ {rows}").lstrip()
                    description = str(f"{msgSup} {msgProduct} บรรทัดที่ {rows}").lstrip()
                    
                    logError = ForecastErrorLogs()
                    logError.file_name = str(obj.id)
                    logError.row_num=rows
                    logError.item=i
                    logError.part_code=partCode
                    logError.part_no=partNo
                    logError.part_name=partDescription
                    logError.supplier=supName
                    logError.model=partModel
                    logError.rev_0=rev0
                    logError.rev_1=rev1
                    logError.rev_2=rev2
                    logError.rev_3=rev3
                    logError.remark=description
                    logError.is_error=isError
                    logError.is_success=False
                    logError.save()
                    isAllErrors += 1
                
            i += 1
        
        if isAllErrors > 0:
            messages.warning(request, format_html("{} <a class='text-primary' href='/forecast/logging/{}'>{}</a>", f"เกิดข้อผิดพลาดไม่สามารถอัพโหลดข้อมูลได้", str(obj.id), "รบกวนกดที่ลิงค์นี้เพื่อตรวจข้อผิดพลาดดังกล่าว"))
            obj.delete()
            return
            
        else:
            ### Create File Forecast Upload
            mydate = datetime.now()
            onMonth = int(mydate.month)
            onYear = int(mydate.year)
            
            if obj.forecast_month is None:
                onMonthList = OnMonthList.objects.get(value=str(onMonth))
                obj.forecast_month = onMonthList
                
            else:
                if obj.forecast_month.value != onMonth:
                    messages.warning(request, "กรุณาเลือกเดือน Forecast ให้ถูกต้องด้วย")
                    return
                    

            if obj.forecast_year is None:
                onYearList = OnYearList.objects.get(value=str(onYear))
                obj.forecast_year = onYearList
                
            else:
                if obj.forecast_year.value != onYear:
                    messages.warning(request, "กรุณาเลือกปี Forecast ให้ถูกต้องด้วย")
                    return
            
            if obj.forecast_book_id is None:
                bookData = Book.objects.get(id=request.POST.get('forecast_book_id'))
                if len(request.POST.get('forecast_book_id')) == 0: 
                    reviseData = ReviseBook.objects.get(name='Upload EDI') 
                    bookData = Book.objects.get(id=reviseData.book_id)
                    obj.forecast_book_id = bookData
            ### Save Data
            obj.save()
            
            planForecast = PlanningForecast.objects.get(plan_month=str(obj.forecast_month.value), plan_year=obj.forecast_year.value)
            sectionData = request.user.section_id
            if request.user.section_id is None:
                sectionData = Section.objects.get(code="-")
                
            for r in docs:
                part = Product.objects.get(code=str(r['partCode']).strip())
                supFilter = Supplier.objects.get(code=str(r['supName']).strip())
                # partModel = ProductGroup.objects.get(code=str(r['partModel']).strip())
                pdsHeader = None
                try:
                    pdsHeader = Forecast.objects.get(file_forecast_id=obj,supplier_id=supFilter,forecast_plan_id=planForecast,forecast_revise_id=obj.forecast_revise_id, part_model_id=part.prod_group_id)
                    
                except Forecast.DoesNotExist as ex:
                    rndNo = f"FC{str(obj.forecast_date.strftime('%Y%m'))[3:]}"
                    rnd = f"{rndNo}{(Forecast.objects.filter(forecast_no__gte=rndNo).count() + 1):05d}"
                    pdsHeader = Forecast()
                    pdsHeader.forecast_plan_id=planForecast
                    pdsHeader.file_forecast_id=obj
                    pdsHeader.supplier_id=supFilter
                    pdsHeader.part_model_id=part.prod_group_id
                    pass
                
                pdsHeader.section_id=sectionData
                pdsHeader.book_id=obj.forecast_book_id
                pdsHeader.forecast_no=rnd
                pdsHeader.forecast_date=obj.forecast_date
                pdsHeader.forecast_revise_id=obj.forecast_revise_id
                pdsHeader.forecast_on_month_id=obj.forecast_month
                pdsHeader.forecast_on_year_id=obj.forecast_year
                pdsHeader.forecast_by_id=request.user
                pdsHeader.forecast_status="0"
                pdsHeader.save()
                ### Create PDS Detail
                pdsDetail = None
                try:
                    pdsDetail = ForecastDetail.objects.get(forecast_id=pdsHeader,product_id=part)
                    
                except ForecastDetail.DoesNotExist as ex:
                    pdsDetail = ForecastDetail()
                    pdsDetail.forecast_id=pdsHeader
                    pdsDetail.product_id=part
                    pass
                
                pdsDetail.request_qty=r["qty"]
                pdsDetail.balance_qty=r["qty"]
                pdsDetail.month_0 = str(r['month0'])
                pdsDetail.month_1 = str(r['month1'])
                pdsDetail.month_2 = str(r['month2'])
                pdsDetail.month_3 = str(r['month3'])
                pdsDetail.price=part.price
                pdsDetail.request_by_id=request.user
                pdsDetail.request_status="0"
                pdsDetail.import_model_by_user=r['partModel']
                pdsDetail.save()
                
            #####
            forecastData = Forecast.objects.filter(file_forecast_id=obj.id)
            for pHeader in forecastData:
                items = ForecastDetail.objects.filter(forecast_id=pHeader)
                rNum = 0
                rQty = 0
                rPrice = 0
                rMonth0 = 0
                rMonth1 = 0
                rMonth2 = 0
                rMonth3 = 0
                for r in items:
                    rQty += r.request_qty
                    rPrice += float(r.product_id.price)
                    rMonth0 += r.month_0
                    rMonth1 += r.month_1
                    rMonth2 += r.month_2
                    rMonth3 += r.month_3
                    rNum += 1
                    r.seq = rNum
                    r.save()
                    
                pHeader.forecast_item = rNum
                pHeader.forecast_qty = rQty
                pHeader.forecast_total_qty = rQty
                pHeader.forecast_price = rPrice
                pdsHeader.forecast_m0 = rMonth0
                pdsHeader.forecast_m1 = rMonth1
                pdsHeader.forecast_m2 = rMonth2
                pdsHeader.forecast_m3 = rMonth3                
                pHeader.save()
                
            messages.success(request, f"Upload {str(obj.id)} Successfully")
            #### Send notification
            token = os.environ.get("LINE_TOKEN")
            if type(request.user.line_notification_id) != type(None):
                token = request.user.line_notification_id.token
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {token}'
            }
            
            msg = f"message=เรียนแผนก PU\nขณะนี้ทางแผนก Planning\nทำการอัพโหลด Forecast({pHeader.forecast_plan_id}) {pHeader.forecast_revise_id.name}\nกรุณาทำการยืนยันให้ด้วยคะ"
            requests.request("POST", "https://notify-api.line.me/api/notify", headers=headers, data=msg.encode("utf-8"))
        
    except Exception as ex:
        messages.error(request, f"รูปแบบเอกสารที่ใช้อัพโหลดข้อมูลไม่ถูกต้อง {str(ex)}")
        obj.delete()
        return
    
    return obj
    
class fcMaker(object):
    """"""
    def __init__(self, response):
        self.PAGE_SIZE = (8.27*inch, 11.69*inch)
        self.c = canvas.Canvas(response, pagesize=self.PAGE_SIZE)
        self.styles = style
        self.width, self.height = self.PAGE_SIZE

    def createDocument(self):
        """"""
        # Title Page
        title = """Title goes here"""
        p = Paragraph(title, styleH)

        logo = Image(os.path.join(settings.STATIC_ROOT,"img/honeybadger.jpg"))
        logo.drawHeight = 99
        logo.drawWidth = 99

        data = [[logo], [p]]
        table = Table(data, colWidths=2.25*inch)
        table.setStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("TOPPADDING", (0, 0), (-1, -1), 20)])
        table.wrapOn(self.c, self.width, self.height)
        table.drawOn(self.c, *self.coord(.25, 2.75, inch))

        self.c.showPage()

        #Page Two
        side1_text = """Text goes here"""
        p = Paragraph(side1_text, styleH)

        side1_image = Image(os.path.join(settings.STATIC_ROOT,"img/honeybadger.jpg"))
        side1_image.drawHeight = 99
        side1_image.drawWidth = 99

        data = [[side1_image], [p]]
        table = Table(data, colWidths=2.25*inch)
        table.setStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("TOPPADDING", (0, 0), (-1, -1), 3)])
        table.wrapOn(self.c, self.width, self.height)
        table.drawOn(self.c, *self.coord(.25, 2.75, inch))

        self.c.showPage()

        #Page Three
        side2_text = """<font size = '14'>This is where and how the main text will appear on the rear of this card.
        </font>"""
        p_side2 = Paragraph(side2_text, styleH)
        data = [[p_side2]]
        table_side2 = Table(data, colWidths=2.25*inch, rowHeights=2.55*inch)
        table_side2.setStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("TOPPADDING", (0, 0), (-1, -1), 3),
                        ("BOX", (0, 0), (-1,-1), 0.25, colors.red)])
        front_page = []
        front_page.append(table_side2)

        f = Frame(inch*.25, inch*.5, self.width-.5*inch, self.height-1*inch, showBoundary=1)
        f.addFromList(front_page, self.c)

    def coord(self, x, y, unit=1):
        """
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, self.height -  y * unit
        return x, y

    def savePDF(self):
        """"""
        self.c.save()