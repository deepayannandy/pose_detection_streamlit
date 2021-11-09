import base64
from fpdf import FPDF
import datetime
import pytz
tz_In = pytz.timezone('Asia/Kolkata')
x = datetime.datetime.now(tz_In)


print(x.strftime("%I:%M %d/%m/%y"))


def get_report(company_name,caddress,doc_add,doct_con,Pname,sp,sex,age,pcontact,bpart,report_data,img):
    x = datetime.datetime.now(tz_In)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(0, 10, company_name,border=True,align='C',ln=True)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 10, caddress, border=True, align='C',ln=True)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, doc_add, border=True, align='C',ln=True)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 10, doct_con, border=True, align='C', ln=True)
    pdf.set_font('Arial',size=10)
    pdf.cell(0, 10, "Date: "+x.strftime("%I:%M %d/%m/%y"),align='L',ln=True)
    pdf.set_font('Arial', size=12)
    pdf.cell(0, 10, "Patient Name: " + Pname, align='L',ln=True)
    pdf.cell(0, 10, "Sex: " + sex, align='L',ln=True)
    pdf.cell(0, 10, "Patient Age: " +str(age)+" Years", align='L', ln=True)
    pdf.cell(0, 10, "Contact: " + pcontact,ln=True, align='L')
    pdf.set_font('Arial', 'U', size=16)
    pdf.cell(0, 10, "Report Image:", ln=True, align='L')
    pdf.image(img,w=180,h=105)
    pdf.set_font('Arial', size=12)
    pdf.cell(0, 10, " ", ln=True, align='L')
    pdf.set_font('Arial','U', size=16)
    pdf.cell(0, 10, "Body Part: " + bpart+" ("+sp+")",border=True, ln=True, align='L')
    j=0
    for i in report_data:
        pdf.set_font('Arial','B',size=14)
        if j==2:
            pdf.set_text_color(30,220,30)
        pdf.cell(0, 10, i, ln=True, align='L',border=True)
        j+=1
    b64 = base64.b64encode(pdf.output(dest="S").encode("latin-1"))  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{"Report"}.pdf">Download file</a>'