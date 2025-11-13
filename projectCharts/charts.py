import os
from typing import Iterable, List, Optional, Sequence

import matplotlib.pyplot as plt


_OUTPUT_DIR = "img"


def _ensure_output_dir() -> None:
  os.makedirs(_OUTPUT_DIR, exist_ok=True)


def _build_output_path(name: str, suffix: str) -> str:
  safe_slug = "".join(char if char.isalnum() else "_" for char in name.lower().strip())
  filename = f"{safe_slug}_{suffix}.png"
  return os.path.join(_OUTPUT_DIR, filename)


def _to_numeric(values: Iterable[float]) -> List[float]:
  return [float(value) for value in values]


def generateBarChart(name: str, labels: Sequence[str], values: Sequence[float]) -> str:
  _ensure_output_dir()
  numeric_values = _to_numeric(values)
  fig, ax = plt.subplots(figsize=(max(6, len(labels) * 0.7), 4.5))
  ax.bar(labels, numeric_values, color="#1f77b4")
  ax.set_ylabel("Rating")
  ax.set_title(f"Rating por modelo - {name}")
  ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.7)
  plt.xticks(rotation=40, ha="right")
  plt.tight_layout()
  output_path = _build_output_path(name, "bar_chart")
  plt.savefig(output_path)
  plt.close(fig)
  return output_path


def generatePieChart(name: str, labels: Sequence[str], values: Sequence[float]) -> str:
  _ensure_output_dir()
  numeric_values = _to_numeric(values)
  fig, ax = plt.subplots()
  ax.pie(numeric_values, labels=labels, autopct="%1.1f%%", startangle=140)
  ax.axis("equal")
  ax.set_title(f"Distribución de rating - {name}")
  output_path = _build_output_path(name, "pie_chart")
  plt.savefig(output_path)
  plt.close(fig)
  return output_path


def generateTrendChart(
    name: str,
    labels: Sequence[str],
    values: Sequence[float],
    trend_values: Sequence[float],
    predicted_value: Optional[float] = None,
) -> str:
  if len(labels) != len(values):
    raise ValueError("labels y values deben tener la misma longitud.")

  _ensure_output_dir()
  numeric_values = _to_numeric(values)
  numeric_trend = _to_numeric(trend_values)

  base_x = list(range(len(numeric_values)))
  fig, ax = plt.subplots(figsize=(max(6, len(labels) * 0.7), 4.5))

  ax.plot(base_x, numeric_values, marker="o", linewidth=2, label="Rating real")
  ax.plot(base_x, numeric_trend, linestyle="--", linewidth=1.5, label="Tendencia lineal")

  xticks = base_x[:]
  xtick_labels = list(labels)

  if predicted_value is not None:
    future_x = len(base_x)
    ax.scatter(future_x, predicted_value, color="#d62728", marker="o", label="Próxima predicción")
    if numeric_values:
      ax.plot(
          [base_x[-1], future_x],
          [numeric_values[-1], predicted_value],
          color="#d62728",
          linestyle=":",
      )
    xticks.append(future_x)
    xtick_labels.append("Predicción")

  ax.set_xticks(xticks)
  ax.set_xticklabels(xtick_labels, rotation=40, ha="right")
  ax.set_ylabel("Rating")
  ax.set_title(f"Tendencia de rating - {name}")
  ax.grid(axis="both", linestyle="--", linewidth=0.5, alpha=0.7)
  ax.legend()
  plt.tight_layout()

  output_path = _build_output_path(name, "trend_chart")
  plt.savefig(output_path)
  plt.close(fig)
  return output_path