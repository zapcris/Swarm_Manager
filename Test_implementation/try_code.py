import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

m = pd.DataFrame({'newvalue': np.random.randint(10, 20, 4), 'name': [*'ABDE']})
j = pd.DataFrame({'newvalue': np.random.randint(10, 20, 4), 'name': [*'ACEF']})
h = pd.DataFrame({'newvalue': np.random.randint(10, 20, 4), 'name': [*'BDEG']})
x = pd.DataFrame({'newvalue': np.random.randint(10, 20, 4), 'name': [*'ABCE']})

# let colors be a list of unique colors, at least one for each name
colors = plt.get_cmap('tab10').colors
# make a set of all the names
all_names = {*m.name, *j.name, *h.name, *x.name}
# map each of the unique names to a color
name_to_color = {name: color for name, color in zip(all_names, colors)}

fig, axs = plt.subplots(2, 2, figsize=(9, 12), dpi=100, facecolor='w', edgecolor='k')
axs[0, 0].pie(m.newvalue, labels=m.name, labeldistance=None, colors=m.name.map(name_to_color))
axs[0, 0].set_title('Axis [0, 0]')
axs[0, 1].pie(j.newvalue, labels=j.name, labeldistance=None, colors=j.name.map(name_to_color))
axs[0, 1].set_title('Axis [0, 1]')
axs[1, 0].pie(h.newvalue, labels=h.name, labeldistance=None, colors=h.name.map(name_to_color))
axs[1, 0].set_title('Axis [1, 0]')
axs[1, 1].pie(x.newvalue, labels=x.name, labeldistance=None, colors=x.name.map(name_to_color))
axs[1, 1].set_title('Axis [1, 1]')

handles = [plt.Rectangle((0, 0), 0, 0, color=name_to_color[name], label=name) for name in name_to_color]
axs[0, 0].legend(handles=handles, bbox_to_anchor=(0.2, 1.1), loc='lower left')

plt.tight_layout()
plt.show()