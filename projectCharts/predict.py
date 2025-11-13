from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

import numpy as np


@dataclass
class RatingTrend:
  models: List[str]
  ratings: List[float]
  trend_values: List[float]
  predicted_rating: float
  slope: float
  r_squared: float
  direction: str


def _clean_series(models: Sequence[str], ratings: Sequence[float]) -> Tuple[List[str], List[float]]:
  cleaned_models: List[str] = []
  cleaned_ratings: List[float] = []

  for model, rating in zip(models, ratings):
    if rating is None:
      continue
    try:
      rating_value = float(rating)
    except (TypeError, ValueError):
      continue
    cleaned_models.append(model)
    cleaned_ratings.append(rating_value)

  return cleaned_models, cleaned_ratings


def _categorize_slope(slope: float, tolerance: float = 0.2) -> str:
  if slope > tolerance:
    return "al alza"
  if slope < -tolerance:
    return "a la baja"
  return "estable"


def calculate_rating_trend(models: Sequence[str], ratings: Sequence[float]) -> Optional[RatingTrend]:
  cleaned_models, cleaned_ratings = _clean_series(models, ratings)

  if len(cleaned_ratings) < 2:
    return None

  x_values = np.arange(len(cleaned_ratings), dtype=float)
  y_values = np.array(cleaned_ratings, dtype=float)

  slope, intercept = np.polyfit(x_values, y_values, 1)
  trend_values = (slope * x_values + intercept).tolist()

  next_index = float(len(cleaned_ratings))
  next_rating = slope * next_index + intercept
  next_rating_clipped = float(np.clip(next_rating, 0.0, 100.0))

  ss_total = float(np.sum((y_values - np.mean(y_values)) ** 2))
  ss_residual = float(np.sum((y_values - np.array(trend_values)) ** 2))
  r_squared = 0.0 if ss_total == 0 else 1 - ss_residual / ss_total

  direction = _categorize_slope(float(slope))

  return RatingTrend(
      models=cleaned_models,
      ratings=cleaned_ratings,
      trend_values=trend_values,
      predicted_rating=next_rating_clipped,
      slope=float(slope),
      r_squared=r_squared,
      direction=direction,
  )
