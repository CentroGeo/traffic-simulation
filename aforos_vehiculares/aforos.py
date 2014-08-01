# -*- coding: utf-8 -*-
import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
import xlrd

workbook = xlrd.open_workbook('data/Aforo_Eje 10_Lado-Burger_King_Dir-Pte.xls')
worksheet = workbook.sheet_by_name('Hoja1')
num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row = -1
dates = [datetime.date(2010,i,9) for i in range(5,13)]
print dates
delta_t = datetime.timedelta(hours=1)
dias = []
cuenta_coches = 0


for start_date in dates:
    intervalos = []
    if start_date == datetime.date(2010,5,9):
        #el primer dia empieza a las 9 de la mañana
        start_time = datetime.time(9,0,0)
    else:
        start_time = datetime.time(0,0,0)

    for i in xrange(12,num_rows):
        curr_date = xlrd.xldate_as_tuple(worksheet.cell_value(i, 0), 0)
        curr_date = datetime.date(*curr_date[:3])
        if curr_date == start_date:
            curr_time = xlrd.xldate_as_tuple(worksheet.cell_value(i, 1), 0)
            curr_time = datetime.time(*curr_time[3:])
            end_time = datetime.datetime.combine(datetime.date.today(),start_time)  + delta_t
            if start_time < datetime.time(23,0,0): #para que al agregar el delta nos se pase de las 00:00
                if curr_time >= (datetime.datetime.combine(datetime.date.today(),start_time)  + delta_t).time():
                    start_time = xlrd.xldate_as_tuple(worksheet.cell_value(i, 1), 0)
                    start_time = datetime.time(*start_time[3:])
                    intervalos.append(cuenta_coches)
                    cuenta_coches = 0

                if curr_time < (datetime.datetime.combine(start_date,start_time)  + delta_t).time():
                    cuenta_coches += worksheet.cell_value(i, 2)
            else:
                #completamos la última hora
                cuenta_coches += worksheet.cell_value(i, 2)

    #le ponemos el último intervalo
    intervalos.append(cuenta_coches)
    #completamos las listas para el primero y el último dia, así todas son de la misma longitud
    if start_date == datetime.date(2010,5,9):
        for i in range(0,9):
            intervalos.insert(i, 0.0)

    if start_date == datetime.date(2010,12,9):
        for i in range(0,16):
            intervalos.append(0.0)


    dias.append(intervalos)

#mezcalmos los dos domingos en uno solo y lo cambiamos por los dos de la lista
primer_dom = dias[0]
primer_dom = primer_dom[8:]
ult_dom = dias[7]
ult_dom = ult_dom[:8]
domingo = primer_dom + ult_dom
del dias[0]
del dias[6]
dias.insert(0, domingo)
#promedio para dia laboral
suma = [a+b+c+d+e for a,b,c,d,e in zip(dias[1], dias[2], dias[3],
        dias[3], dias[5])]
suma = np.asarray(suma)
promedio_laboral = suma*(1/5.0)
#promedio_laboral = np.transpose(promedio_laboral)

#lo escribimos a un archivo
with open('output/promedio_laboral.csv', 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    rows=[]
    for p in promedio_laboral:
      row=[]
      row.append(p)
      rows.append(row)
      row=[]

    a.writerows(rows)

#suma= dias[1]
print 'promedio_laboral:'
print suma
print 'lunes:'
print dias[1]
#sacamos los totales por dia
totales_diarios = [sum(l) for l in dias]
#print totales_diarios

#construimos la gráfica para los aforos por hora
x = range(24)
labels = [u'Domingo',u'Lunes',u'Martes',u'Miércoles',u'Jueves',u'Viernes',u'Sábado']
colormap = plt.cm.gist_ncar
plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, 8)])
fig_1=plt.figure(1)
fig_1.suptitle('Aforos por hora (Eje 10 del lado de Burger King)')
for y,label in zip(dias,labels):
    plt.plot(x,y,label=label,linewidth=2.0)

plt.xlabel('Hora')
plt.ylabel('Aforo')
#plt.title("Aforos por hora (Eje 10 del lado de Burger King)")
plt.legend()

# la gráfica de barras para los totales por dia
ind = np.arange(len(totales_diarios))
fig_2=plt.figure(2)
fig_2.suptitle('Totales diarios (Eje 10 del lado de Burger King)')
ax = plt.subplot(111)
#ax.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, 7)])
ax.bar(ind, totales_diarios,color=['b','r','g','c','m','y','k'])
ax.set_ylabel('Total')
ax.set_xticks(ind+0.4)
ax.set_xticklabels( (u'Domingo',u'Lunes',u'Martes',u'Miércoles',u'Jueves',u'Viernes',u'Sábado') )

#fig_2.set_xticklabels( (u'Domingo',u'Lunes',u'Martes',u'Miércoles',u'Jueves',u'Viernes',u'Sábado') )
plt.show()
