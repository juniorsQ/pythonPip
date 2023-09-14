import utils
import read_csv as csv
import charts


def run():
  data = csv.read_csv('data.csv')
  #print(data)
  #ver gráfica rating mode de telefono por marca
  marca = input(
      'Ingrese Marca de Smartphone para graficar el rendimiento Modelo: ')

  data = list(filter(lambda item: item['brand_name'] == marca, data))
  if len(data) > 0:
    model = list(map(lambda x: x['model'], data))
    rating = list(
        map(lambda x: int(float(x['rating'])) if x['rating'] else 0, data))
    charts.generateBarChart(marca,model, rating)
    charts.generatePieChart(marca,model, rating)
  else:
    print('Marca de Smartphone no encontrada')


#entry print esto hace que se pueda llamar desde otro modulo y a su vez del mismo modulo
if __name__ == '__main__':
  run()
