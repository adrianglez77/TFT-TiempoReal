import pandas as pd
import requests
import xml.etree.ElementTree as ET
import csv
import time

for i in range (0, 400):
    t_end = time.time() + 60 * 1
    while time.time() < t_end:

        #DESCARGAR EL XML EN LOCAL

        url = 'http://www.mc30.es/images/xml/DatosTrafico.xml'
        headers = requests.utils.default_headers()
        headers.update(
            {
                'User-Agent': 'My User Agent 1.0',
            }
        )
        response = requests.get(url, headers=headers)
        open('/home/hduser/pruebas/DatosTrafico.xml', 'wb').write(response.content)

        #-------------------------------------------------------------------------------

        #PASARLO A CSV
        tree = ET.parse("/home/hduser/pruebas/DatosTrafico.xml")
        root = tree.getroot()

        # open a file for writing
        Resident_data = open("/home/hduser/pruebas/DatosTrafico"+str(i)+".csv", 'w')

        # create the csv writer object
        csvwriter = csv.writer(Resident_data)
        resident_head = []

        count = 0
        for member in root.findall('DatoGlobal'):
            DatoGlobal = []
            if count == 0:

                Nombre = member.find('Nombre').tag
                resident_head.append(Nombre)

                VALOR = member.find('VALOR').tag
                resident_head.append(VALOR)

                FECHA = member.find('FECHA').tag
                resident_head.append(FECHA)

                csvwriter.writerow(resident_head)
                count = count + 1

            Nombre = member.find('Nombre').text
            DatoGlobal.append(Nombre)

            VALOR = member.find('VALOR')
            if VALOR is not None:
                VALOR = VALOR.text
                DatoGlobal.append(VALOR)

            FECHA = member.find('FECHA')
            if FECHA is not None:
                FECHA = FECHA.text
            DatoGlobal.append(FECHA)

            csvwriter.writerow(DatoGlobal)

        Resident_data.close()

        #--------------------------------------------------------------------------

        #QUEDARNOS CON LAS FILAS QUE NOS INTERESAN

        df = pd.read_csv("/home/hduser/pruebas/DatosTrafico"+str(i)+".csv")

        data = df.drop(df[df.Nombre == "totalVehiculosTunel"].index)
        data = data.drop(df[df.Nombre == "velocidadMediaTunel"].index)
        data = data.drop(df[df.Nombre == "fechaActualizacionPMTunel"].index)
        data = data.drop(df[df.Nombre == "fechaActualizacionPMSuperficie"].index)
        data = data.drop(df[df.Nombre == "CortesImportantesWeb"].index)

        data.to_csv("/home/hduser/pruebas/DatosTrafico"+str(i)+".csv")
        print(data)

        #se muestra por que iteracion del LOOP va
        print("LOOP: ", (i))

        #espero 4 minuto para volver a empezar el while
        time.sleep(240) # Delay for 4 minute (60 seconds).

