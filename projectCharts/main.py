import charts
import read_csv as csv
from predict import calculate_rating_trend


def _normalize_brand(value: str) -> str:
  return value.strip().lower()


def run() -> None:
  data = csv.read_csv('data.csv')
  marca_input = input('Ingrese Marca de Smartphone para analizar el rendimiento: ').strip()

  if not marca_input:
    print('Debe ingresar una marca de smartphone.')
    return

  brand_key = _normalize_brand(marca_input)
  brand_data = [
      item for item in data if _normalize_brand(item.get('brand_name', '')) == brand_key
  ]

  if not brand_data:
    print('Marca de Smartphone no encontrada.')
    return

  models = []
  ratings = []

  for item in brand_data:
    model_name = item.get('model', 'Modelo desconocido')
    rating_str = (item.get('rating') or '').strip()
    if not rating_str:
      continue
    try:
      rating_value = float(rating_str)
    except ValueError:
      continue
    models.append(model_name)
    ratings.append(rating_value)

  if not ratings:
    print('No se encontraron ratings válidos para esta marca.')
    return

  bar_chart_path = charts.generateBarChart(marca_input, models, ratings)
  pie_chart_path = charts.generatePieChart(marca_input, models, ratings)

  trend = calculate_rating_trend(models, ratings)

  print('\nGráficas generadas:')
  print(f' - {bar_chart_path}')
  print(f' - {pie_chart_path}')

  if trend is None:
    print('\nNo hay suficientes datos para producir una predicción de tendencia.')
    return

  trend_chart_path = charts.generateTrendChart(
      marca_input,
      trend.models,
      trend.ratings,
      trend.trend_values,
      trend.predicted_rating,
  )

  print(f"\nTendencia estimada para {marca_input}: {trend.direction}.")
  print(
      f"Próxima puntuación estimada: {trend.predicted_rating:.2f} "
      f"(R² del ajuste: {trend.r_squared:.2%})."
  )
  print(f' - {trend_chart_path}')


if __name__ == '__main__':
  run()
