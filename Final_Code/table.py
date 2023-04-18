import numpy as np
import matplotlib.pyplot as plt

title_text = 'Fluid Volume Data'
footer_text = str(day) + "_" + str(time) + "_data"
fig_background_color = 'black'
fig_border = 'white'

reagent1 = 'cc1'
reagent2 = 'cc2'
reagent3 = 'cc3'
reagent4 = 'cc4'

bottle1 = 123
bottle2 = 234
bottle3 = 345
bottle4 = 456

toFill1 = 4800 - int(bottle1)
toFill2 = 2400 - int(bottle2)
toFill3 = 2400 - int(bottle3)
toFill4 = 4800 - int(bottle4)


data = [[reagent1, reagent2, reagent3, reagent4],
        ['Measured', bottle1, bottle2, bottle3, bottle4],
        ['To be filled', toFill1, toFill2, toFill3, toFill4]]

column_headers = data.pop(0)
row_headers = [x.pop(0) for x in data]

cell_text = []
for row in data:
    cell_text.append([f'{x/1000:1.1f}' for x in row])

# Create the figure. Setting a small pad on tight_layout
# seems to better regulate white space. Sometimes experimenting
# with an explicit figsize here can produce better outcome.
plt.figure(linewidth=2,
           edgecolor=fig_border,
           facecolor=fig_background_color,
           tight_layout={'pad':1},
           #figsize=(5,3)
          )

# Get some lists of color specs for row and column headers
rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))

# Add a table at the bottom of the axes
the_table = plt.table(cellText=cell_text,
                      rowLabels=row_headers,
                      rowColours=rcolors,
                      rowLoc='right',
                      colColours=ccolors,
                      colLabels=column_headers,
                      loc='center')


# Scaling is the only influence we have over top and bottom cell padding.
# Make the rows taller (i.e., make cell y scale larger).
the_table.scale(1, 1.5)
# Hide axes
ax = plt.gca()
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
# Hide axes border
plt.box(on=None)
# Add title
plt.suptitle(title_text)
# Add footer
plt.figtext(0.95, 0.05, footer_text, horizontalalignment='right', size=6, weight='light')
# Force the figure to update, so backends center objects correctly within the figure.
# Without plt.draw() here, the title will center on the axes and not the figure.
plt.draw()
# Create image. plt.savefig ignores figure edge and face colors, so map them.
fig = plt.gcf()
plt.savefig("data",
            #bbox='tight',
            edgecolor=fig.get_edgecolor(),
            facecolor=fig.get_facecolor(),
            dpi=150
            )
plt.savefig(str(day) + "_" + str(time) + "_data",
            #bbox='tight',
            edgecolor=fig.get_edgecolor(),
            facecolor=fig.get_facecolor(),
            dpi=150
            )

plt.show()