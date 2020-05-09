import threading
import ftplib
from getSNMP import consultaSNMP
from fpdf import FPDF
import getpass
import sys
import telnetlib
from creaPDF import create_pdf
import os
import sh
import subprocess


def main():
    print("Menu principal")
    print("1. Generar la configuracion")
    print("2. Extraer el archivo de configuración")
    print("3. Mandar archivo de configuración")
    print("4. Reporte")
    x = input("Opción: ")

    if x == '1':
        genera()
    if x == '2':
        extrae()
    if x == '3':
        manda()
    if x == '4':
        creaPDF()


def genera():
    print("\n")
    host = input("Ingresa la direccion del host: ")
    user = input("Ingresa el usuario: ")
    password = getpass.getpass(prompt='Password: ', stream=None)

    tn = telnetlib.Telnet(host)

    tn.read_until(b"User: ")
    tn.write(user.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

    tn.write(b"enable\n")
    tn.write(b"copy running-config startup-config\n")
    tn.write(b"exit\n")

    print(tn.read_all().decode('ascii'))
    print("Hecho. Se ha generado la configuración.")
    print("\n")
    main()


def extrae():
    print("\n")
    host = input("Ingresa la direccion del host: ")
    user = input("Ingresa el usuario: ")
    password = getpass.getpass(prompt='Password: ', stream=None)
    ftp = ftplib.FTP(host)
    ftp.login(user, password)
    ftp.retrlines('LIST')
    ftp.retrbinary('RETR startup-config', open('startup-config', 'wb').write)
    ftp.quit()
    print("Hecho. El archivo se encuentra en el mismo directorio de este proyecto.\n")
    print("\n")
    main()


def manda():
    print("\n")
    host = input("Ingresa la direccion del host: ")
    user = input("Ingresa el usuario: ")
    password = getpass.getpass(prompt='Password: ', stream=None)
    ftp = ftplib.FTP(host)
    ftp.login(user, password)
    ftp.retrlines('LIST')
    archivo = open('startup-config', 'rb')
    ftp.storbinary('STOR startup-config', archivo)
    ftp.quit()
    print("Hecho. El archivo se colocó en el router.\n")
    main()


def creaPDF():
    comu = input("Ingresa el nomnre de la comunidad: ")
    ip = input("Ingresa la direccion IP: ")
    logo = "rcp-logo.png"
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=7)
    pdf.image(logo, 10, 8, 33)
    pdf.set_font('Arial', 'B', 15)

    # Add an address
    #1.3.6.1.2.1.2.2.1.2. para nombres de interfaces
    #1.3.6.1.2.1.2.2.1.8. para estados de interfaces
    pdf.cell(100)
    infoagente = str(consultaSNMP(comu, ip, '1.3.6.1.2.1.1.1.0'))
    pdf.cell(0, 5, "Reporte Agente RCP: " + infoagente, ln=1)
    pdf.cell(100)
    infoagente2 = str(consultaSNMP(comu, ip, '1.3.6.1.2.1.1.3.0'))
    infoagente3 = str(consultaSNMP(comu, ip, '1.3.6.1.2.1.2.1.0'))
    pdf.cell(0, 5, txt="Uptime: "+ infoagente2 + "", ln=1)
    pdf.cell(200, 45, "Nombre de comunidad SNMP: " + comu, ln=1, align="C")
    pdf.cell(200, 47, "Dirección: " + ip, ln=1, align="C")
    pdf.cell(200, 49, "Interfaces: " + infoagente3, ln=1, align="C")
    a = []
    b = []
    for k in range(int(infoagente3)):
        a.append(str(consultaSNMP(comu, ip, '1.3.6.1.2.1.2.2.1.2.'+str(k+1))))
        c = str(consultaSNMP(comu, ip, '1.3.6.1.2.1.2.2.1.8.'+str(k+1)))
        if c == "1":
            c = "up"
        else:
            c = "down"
        b.append(c)
    pdf.cell(200, 50, "Nombres: " + str(a).strip('[]'), ln=1)
    pdf.cell(200, 52, "Estados: " + str(b).strip('[]'), ln=1)
    pdf.output("%s.pdf" % comu)
    print("PDF creado correctamente. \n")
    main()


main()