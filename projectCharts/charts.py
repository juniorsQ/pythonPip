import matplotlib.pyplot as plt


def generateBarChart(name,labels, values):
  name=name+'_pieChart'
  fig, ax = plt.subplots()
  ax.bar(labels, values)
  plt.xticks(rotation=40)
  plt.savefig(f'./img/{name}.png')
  plt.close()


def generatePieChart(name,labels, values):
  name=name+'_pieChart'
  fig, ax = plt.subplots()
  ax.pie(values, labels=labels)
  ax.axis('equal')
  plt.savefig(f'./img/{name}.png')
  plt.close()


if __name__ == '__main__':

  # labels = ['a', 'b', 'c']
  # values = [100, 400, 200]
  # #generateBarChart(labels, values)
  # generatePieChart(labels, values)
    generateBarChart(name,labels, values)
    generatePieChart(marca,labels, values)