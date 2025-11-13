# Project API Reference

This document describes every public module, function, and command-line entry point available in this repository. Each section covers:

- Purpose and behavior of the callable.
- Parameters and return values.
- Side effects or external dependencies.
- Examples demonstrating typical usage.

The project currently contains three areas of functionality:

1. A simple greeting script in `hello.py`.
2. An interactive rock–paper–scissors game under `game/`.
3. A small data-visualization toolkit under `projectCharts/` for generating smartphone performance charts based on a CSV data source.

> **Python version:** The code targets Python 3.9+ (type conversions rely on built-in behavior available since Python 3).  
> **Dependencies:** Only the `projectCharts/charts.py` module requires third-party packages (`matplotlib`). Install via `pip install matplotlib`.

---

## `hello.py`

### `print("Hello World and Python Pip learn to Platzi")`

This module has no public functions. Executing `python hello.py` prints a single greeting line to standard output and exits.

```bash
$ python hello.py
Hello World and Python Pip learn to Platzi
```

This script can be used as a smoke test to confirm the Python environment works.

---

## `game/main.py`

This module implements an interactive best-of-three rock–paper–scissors game.

### `choose_options() -> tuple[str | None, str | None]`

- **Description:** Prompts the user to choose `piedra`, `papel`, or `tijera` (Spanish for rock, paper, scissors). Randomly selects the computer's option.
- **Parameters:** None (takes console input).
- **Returns:** A tuple `(user_option, computer_option)`. If the user enters an invalid choice, both values are `None`.
- **Side effects:** Prints both selections to the console.

**Example**

```python
from game.main import choose_options

user_option, computer_option = choose_options()
if user_option is None:
    print("Try again with piedra/papel/tijera.")
```

### `check_rules(user_option: str, computer_option: str, user_wins: int, computer_wins: int) -> tuple[int, int]`

- **Description:** Compares the two options and updates the win counters.
- **Parameters:**
  - `user_option`: Expected to be `'piedra'`, `'papel'`, or `'tijera'`. Passing `None` leaves scores unchanged.
  - `computer_option`: Same domain as `user_option`.
  - `user_wins`: Current user score.
  - `computer_wins`: Current computer score.
- **Returns:** Updated `(user_wins, computer_wins)` counters.
- **Side effects:** Prints match outcome messages in Spanish.

**Example**

```python
from game.main import check_rules

user_wins, computer_wins = check_rules("papel", "piedra", user_wins=0, computer_wins=0)
print(user_wins)        # 1
print(computer_wins)    # 0
```

### `run_game() -> None`

- **Description:** Runs the full interactive loop until either player reaches two victories.
- **Parameters / Returns:** None.
- **Side effects:** Continuously reads from standard input and prints the scoreboard after each round.

`run_game()` is automatically executed when `game/main.py` is run as a script:

```bash
$ cd game
$ python3 main.py
**********
ROUND 1
**********
computer_wins 0
user_wins 0
piedra, papel o tijera =>
```

Programmatic invocation is also possible:

```python
from game.main import run_game

run_game()
```

> **Note:** Because `run_game()` uses an infinite loop with `input`, it should be called from a terminal session. It exits only after either side wins twice.

---

## `projectCharts/read_csv.py`

### `read_csv(path: str) -> list[dict[str, str]]`

- **Description:** Reads a CSV file where the first row contains headers. Produces a list of dictionaries mapping header names to row values (all strings).
- **Parameters:** `path` – filesystem path to the CSV file.
- **Returns:** List of dictionaries, one per row.
- **Side effects:** None.
- **Dependencies:** Standard library `csv`.

**Example**

```python
from projectCharts import read_csv

records = read_csv.read_csv("projectCharts/data.csv")
print(records[0]["brand_name"])
```

> **Tip:** Convert numeric fields manually (e.g., `int(float(row["rating"]))`) before performing calculations.

---

## `projectCharts/utils.py`

Helper functions for working with country population datasets (not used by the current smartphone workflow but available for reuse).

### `get_population(country_dict: dict[str, str]) -> tuple[dict_keys[str], dict_values[int]]`

- **Description:** Extracts population counts for selected census years and converts them to integers.
- **Parameters:** `country_dict` – a dictionary with keys `1970`–`2022 Population`.
- **Returns:** Two iterables `(labels, values)` containing the year strings and their corresponding integer populations.
- **Side effects:** None.

**Example**

```python
from projectCharts import utils

labels, values = utils.get_population({
    "2022 Population": "338289857",
    "2020 Population": "331002647",
    "2015 Population": "320878310",
    "2010 Population": "309327143",
    "2000 Population": "282398554",
    "1990 Population": "248083732",
    "1980 Population": "226545805",
    "1970 Population": "209513341",
})
print(list(labels))  # ['2022', '2020', ...]
print(list(values)[0])  # 338289857
```

### `population_by_country(data: list[dict[str, str]], country: str) -> list[dict[str, str]]`

- **Description:** Filters a collection of country records to those matching `country` based on the `Country/Territory` field.
- **Parameters:**
  - `data`: List of dictionaries (e.g., result of `read_csv`).
  - `country`: Country name to match.
- **Returns:** List of dictionaries with matching entries (empty if none found).
- **Side effects:** None.

**Example**

```python
from projectCharts import utils, read_csv

data = read_csv.read_csv("projectCharts/data.csv")
colombia = utils.population_by_country(data, "Colombia")
if colombia:
    labels, values = utils.get_population(colombia[0])
```

---

## `projectCharts/charts.py`

Provides chart-generation helpers built on `matplotlib`. Both functions save images to disk; make sure the target `img/` directory exists.

### `generateBarChart(name: str, labels: list[str], values: list[int | float]) -> None`

- **Description:** Produces a bar chart for the given data series and saves it as `./img/{name}_pieChart.png`.
- **Parameters:**
  - `name`: Base filename (a suffix `_pieChart` is added automatically).
  - `labels`: X-axis labels (e.g., product models).
  - `values`: Numeric heights for each bar.
- **Returns:** None.
- **Side effects:** Writes a PNG file; rotates X-axis labels by 40° for readability.

**Example**

```python
from projectCharts import charts

charts.generateBarChart(
    name="Samsung",
    labels=["Galaxy S24", "Galaxy S23", "Galaxy A55"],
    values=[92, 89, 78],
)
# File saved at ./img/Samsung_pieChart.png
```

### `generatePieChart(name: str, labels: list[str], values: list[int | float]) -> None`

- **Description:** Creates a pie chart for the given series and saves it as `./img/{name}_pieChart.png`.
- **Parameters:** Same as `generateBarChart`.
- **Returns:** None.
- **Side effects:** Writes a PNG file; ensures the chart has equal aspect ratio.

**Example**

```python
charts.generatePieChart(
    name="Samsung",
    labels=["Galaxy S24", "Galaxy S23", "Galaxy A55"],
    values=[92, 89, 78],
)
# File saved at ./img/Samsung_pieChart.png
```

> **Note:** Both chart functions currently write to the same filename pattern. Calling them sequentially with the same `name` will result in the pie chart overwriting the bar chart. Supply distinct names if you need both files.

---

## `projectCharts/main.py`

### `run() -> None`

- **Description:** Command-line entry point that reads `data.csv`, prompts the user for a smartphone brand, filters the dataset, and generates both bar and pie charts for the selected brand.
- **Parameters / Returns:** None.
- **Side effects:** Displays prompts, prints an error message if no brand matches, and writes charts to `./img/`.
- **Dependencies:** `projectCharts/read_csv`, `projectCharts/charts`, and a dataset formatted like `projectCharts/data.csv`.

**Interactive Usage**

```bash
$ cd projectCharts
$ python3 main.py
Ingrese Marca de Smartphone para graficar el rendimiento Modelo: Samsung
# Charts saved to projectCharts/img/Samsung_pieChart.png
```

**Programmatic Usage**

```python
from projectCharts import main

def export_brand(brand: str) -> None:
    # Ensures charts are regenerated without user input
    import builtins
    original_input = builtins.input
    try:
        builtins.input = lambda _: brand
        main.run()
    finally:
        builtins.input = original_input

export_brand("Samsung")
```

> **Prerequisites:** Ensure the `img/` directory exists at the project root (`mkdir -p projectCharts/img`). Without it, `matplotlib` raises a `FileNotFoundError` when saving charts.

When `projectCharts/main.py` is executed directly (`python3 projectCharts/main.py`), the `run()` function executes automatically thanks to the `if __name__ == '__main__':` guard.

---

## Running the Projects Together

- To play the game: `cd game && python3 main.py`
- To generate smartphone charts interactively: `cd projectCharts && python3 main.py`
- To reuse functions programmatically, import the relevant modules as shown in the examples above.

Consider creating a virtual environment and installing dependencies before running the charting scripts:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r projectCharts/requeriments.txt
```

This document should serve as the authoritative reference for all callable entry points in the repository. Update it whenever new modules or functions are added.
