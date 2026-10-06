"""Contratos de salida de un experimento. Los JSON Schema de esquemas/ se exportan desde aquí.

Un plan vive en experimentos/<H-NNN-nombre>/<ID>-<variante>.md y su salida en la carpeta espejo
resultados/<H-NNN-nombre>/<ID>-<variante>/ (motor.ruta_resultado):
- resumen.json     -> Resumen: identidad, evidencia, robustez, métricas, conclusiones y procedencia.
- equity.csv       -> una fila Sesion por sesión de la muestra.
- operaciones.csv  -> una fila Operacion por operación cerrada.
- ficha.md         -> lectura humana generada desde resumen.json.
- equity_100.csv, operaciones_100.csv -> la misma operativa al 100 % del capital (resumida en `referencia`).
- `sensibilidad`   -> opcional: rejilla de umbral y multiplicador del tamaño por serie (operativa por sesión, sesion.py).
- variantes.csv    -> opcional: una fila Variante por sesión y ventana alternativa, con las covariables para
                      filtrar o dimensionar en el dashboard (descrita en `variantes`; ver variantes.py).
`metricas` usa el tamaño del plan; `referencia`, el 100 % del capital (riesgo comparable entre experimentos).
resultados/indice.csv tiene una fila por experimento (con su `ruta`) e INDICE.md, en la raíz, lo mismo para leer
(motor.reconstruir_indice).

Garantías:
- Solo IS: Experimento rechaza otra muestra y fechas fuera de la IS de su mercado (proteccion.MUESTRAS),
  salvo OOS de un experimento base autorizado (proteccion.AUTORIZADAS_OOS) con su misma especificación.
- Contabilidad (motor.validar_contabilidad, al guardar y al cargar): la equity cubre la muestra,
  concilia sesión a sesión (anterior + pnl_bruto - coste) y cuadra con operaciones y costes por lado.
- Variantes (motor.validar_variantes): la ventana base reproduce, operación a operación, los precios del libro.
- Sin campos desconocidos, NaN ni infinitos; una métrica null necesita motivo; guardar no sobrescribe.
"""
from datetime import date
import json
import math
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .proteccion import exigir_muestra

VERSION = "2.4"  # 2.1: `referencia` (riesgo al 100 %); 2.2: `variantes`; 2.3: `sensibilidad`; 2.4: `experimento.variante`


class Modelo(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False, frozen=True)


class Sesion(Modelo):
    """Fila de equity.csv: valoración al cierre de cada sesión, incluidas las que no tienen posición."""
    fecha: date
    equity: float = Field(gt=0, description="Capital al cierre = anterior + pnl_bruto - coste")
    pnl_bruto: float = Field(description="Variación de valor de la posición en la sesión, antes de costes")
    coste: float = Field(ge=0, description="Costes cargados en la sesión (entradas y salidas)")
    nocional: float = Field(ge=0, description="Nocional negociado en la sesión, ambos lados")
    exposicion: float = Field(ge=0, le=1, description="Fracción de la sesión con posición abierta")


class Operacion(Modelo):
    """Fila de operaciones.csv."""
    id: str = Field(min_length=1)
    entrada: date
    salida: date
    pnl_bruto: float
    coste_entrada: float = Field(ge=0)
    coste_salida: float = Field(ge=0)
    pnl_neto: float = Field(description="pnl_bruto - coste_entrada - coste_salida")

    @model_validator(mode="after")
    def _coherente(self):
        if self.salida < self.entrada:
            raise ValueError("Salida anterior a la entrada")
        if not math.isclose(self.pnl_neto, self.pnl_bruto - self.coste_entrada - self.coste_salida, abs_tol=1e-9):
            raise ValueError("pnl_neto no cuadra con bruto menos costes")
        return self


class Variante(Modelo):
    """Fila de variantes.csv: una sesión en una ventana alternativa, con lo conocido al cierre de la sesión previa."""
    fecha: date = Field(description="Sesión de la operación (día de entrada y salida)")
    previa: date = Field(description="Sesión lun-vie anterior, de la que salen senal y serie")
    ventana: str = Field(min_length=1, description="Nombre de la ventana (clave de `variantes.ventanas`)")
    entrada: float = Field(gt=0, description="Precio a la hora de entrada")
    salida: float = Field(gt=0, description="Precio a la hora de salida")
    senal: Optional[float] = Field(description="Retorno de la sesión previa entre las horas de `variantes.senal`; null si falta una barra")
    serie: Optional[float] = Field(description="Valor de `variantes.serie` en la sesión previa; null si no hay dato")
    desfase: bool = Field(description="EE. UU. y Europa con distinto horario de verano ese día")


class Variantes(Modelo):
    """Describe variantes.csv. El dashboard combina en vivo filtros (senal < 0, serie > umbral, sin desfase) y tamaño."""
    ventanas: dict[str, list[str]] = Field(description="Nombre -> [hora de entrada, hora de salida], hora del dato")
    base: str = Field(description="Ventana que reproduce la operativa del experimento")
    senal: Optional[list[str]] = Field(description="[hora inicial, hora final] del retorno de la sesión previa")
    serie: Optional[str] = Field(description="Serie diaria de la columna serie (nombre del catálogo)")
    coste_lado: float = Field(ge=0, description="Coste por unidad y lado, en unidades de precio")
    filas: int = Field(ge=1)

    @model_validator(mode="after")
    def _base(self):
        if self.base not in self.ventanas or any(len(h) != 2 for h in self.ventanas.values()):
            raise ValueError("La base debe ser una de las ventanas y cada ventana, [entrada, salida]")
        return self


class Sensibilidad(Modelo):
    """Una combinación de umbral y multiplicador del tamaño por serie (operativa por sesión). Se informa, no se elige."""
    umbral: float
    multiplicador: float = Field(gt=0)
    operaciones_sobre_umbral: int = Field(ge=0, description="Operaciones con la serie por encima del umbral")
    diferencia: Optional[float] = Field(description="Retorno bruto medio por operación sobre el umbral menos el resto (pb); null si un lado está vacío")
    rentabilidad_total: float = Field(description="Al 100 % del capital por unidad de tamaño")
    max_drawdown: float = Field(description="Al 100 % del capital por unidad de tamaño")
    sharpe: Optional[float]


class Reglas(Modelo):
    entrada: str
    salida: str
    tamano: str
    costes: str


class Experimento(Modelo):
    id: str = Field(description="HNNN-IS-REAL-NNN, HNNN-OOS-REAL-NNN o HNNN-TOT-REAL-NNN")
    hipotesis: str = Field(description="H-NNN")
    version: str
    fecha: date = Field(description="Fecha de ejecución")
    sintetico: bool = Field(description="True solo en tests: nunca es evidencia")
    pregunta: str
    variante: Optional[str] = Field(default=None, description="Nombre corto de la variante (p. ej. 'OD+ BtD'); agrupa IS, OOS y Total en INDICE.md")
    muestra: Literal["IS", "OOS", "Total"]
    base: Optional[str] = Field(default=None, description="Experimento IS que se lleva a OOS o Total (misma especificación); solo en esas muestras")
    mercado: Literal["clasica", "cripto"] = Field(default="clasica", description="Qué IS aplica (proteccion.MUESTRAS)")
    inicio: date
    fin: date
    instrumento: str
    frecuencia: str
    moneda: str
    capital_inicial: float = Field(gt=0)
    reglas: Reglas
    receta: str = Field(description="Ruta de la receta en el repo")
    plan: str = Field(description="Ruta del plan fijado antes de calcular")
    fuente_datos: str

    @model_validator(mode="after")
    def _muestra_autorizada(self):
        if (self.muestra != "IS") != (self.base is not None):
            raise ValueError("`base` va solo y siempre con muestra OOS o Total")
        exigir_muestra(self.inicio, self.fin, self.muestra, self.mercado, self.hipotesis, self.base)
        return self


class Componente(Modelo):
    nombre: str
    valor: float
    unidad: str


class Evidencia(Modelo):
    """El contraste de la hipótesis: un estadístico y sus componentes descriptivos."""
    estadistico: str = Field(description="Nombre del estadístico, p. ej. 'media TOM − media resto'")
    unidad: str
    valor: float
    componentes: list[Componente] = Field(description="Cifras de las que sale el estadístico")
    desglose: dict[str, float] = Field(default={}, description="Retorno medio por etiqueta (hora, día del mes…), en la unidad del estadístico")


class Bootstrap(Modelo):
    metodo: Literal["bloques circulares"] = "bloques circulares"
    unidad: str = Field(description="Unidad remuestreada: sesión, semana, mes…")
    bloque: int = Field(ge=1, description="Unidades consecutivas por bloque")
    replicas: int = Field(ge=2)
    semilla: int
    nivel: float = Field(gt=0, lt=1)
    ic_inf: float
    ic_sup: float
    incluye_cero: bool
    motivo: str = Field(description="Por qué esa unidad y ese bloque")


class Robustez(Modelo):
    """Batería fija, igual para todas las hipótesis; cambian los parámetros."""
    bootstrap: Bootstrap
    por_anio: dict[str, float] = Field(description="Estadístico calculado en cada año")
    sin_cada_anio: dict[str, float] = Field(description="Estadístico excluyendo cada año")
    pnl_costes_x2: float = Field(description="PnL neto de la simulación con costes duplicados")


class Metricas(Modelo):
    """Métricas de la simulación de la operativa. Null si no son calculables (motivo en no_calculables)."""
    operaciones: int = Field(ge=0, description="Operaciones cerradas")
    pnl_neto: float = Field(description="Equity final - capital inicial")
    esperanza: Optional[float] = Field(description="Media del PnL neto por operación")
    tasa_acierto: Optional[float] = Field(description="Operaciones con PnL neto > 0 / todas")
    payoff: Optional[float] = Field(description="Ganancia neta media / |pérdida neta media|")
    profit_factor: Optional[float] = Field(description="Suma de ganancias netas / |suma de pérdidas netas|")
    rentabilidad_total: float = Field(description="Equity final / inicial - 1")
    rentabilidad_anual: Optional[float] = Field(description="(final / inicial)^(A / n) - 1; A = sesiones por año")
    sharpe: Optional[float] = Field(description="√A · media(r) / desv. típica muestral(r); r diaria de equity, rf = 0")
    sortino: Optional[float] = Field(description="√A · media(r) / √media(min(r, 0)²), sobre todas las sesiones")
    max_drawdown: float = Field(description="Máximo de 1 - equity / máximo acumulado, incluido el capital inicial")
    max_recuperacion: Optional[int] = Field(description="Mayor duración pico-recuperación, en sesiones")
    drawdown_abierto: int = Field(description="Sesiones desde el último pico si el drawdown sigue abierto")
    exposicion: float = Field(description="Media de la fracción de sesión con posición abierta")
    rotacion: float = Field(description="Σ nocional negociado / equity previa")
    costes: float = Field(description="Suma de costes de entrada y salida")
    peso_costes: Optional[float] = Field(description="Costes / Σ |PnL bruto por operación|")
    concentracion_anual: Optional[float] = Field(description="Máxima proporción de operaciones cerradas en un año")
    autocorrelacion: Optional[float] = Field(description="Correlación de r[t] con r[t-1]")


class Referencia(Modelo):
    """La misma operativa con el 99,9 % de la equity por operación (al 100 % no cabe la comisión de entrada),
    sin apalancamiento. Hace comparable el riesgo entre experimentos con tamaños distintos (1 unidad, 30 %…)."""
    fraccion: float = Field(gt=0, le=1)
    rentabilidad_total: float = Field(description="Equity final / inicial - 1")
    rentabilidad_anual: Optional[float] = Field(description="Null con menos de un año de sesiones")
    sharpe: Optional[float] = Field(description="Null con volatilidad cero")
    max_drawdown: float = Field(description="Máximo de 1 - equity / máximo acumulado")
    pico: date = Field(description="Máximo previo al drawdown máximo")
    valle: date = Field(description="Mínimo del drawdown máximo")
    recuperacion: Optional[date] = Field(description="Primera sesión que vuelve al pico; null si no vuelve en la muestra")
    sesiones_bajo_agua: int = Field(ge=0, description="Del pico a la recuperación, o al final de la muestra si no vuelve")
    motor_sha256: str = Field(description="Motor con el que se calculó (puede añadirse después de la ejecución)")


class Conclusiones(Modelo):
    estado: Literal["exploratoria"] = "exploratoria"
    lectura: str
    supuestos: list[str]
    limites: list[str]
    siguiente_comprobacion: str = Field(description="Propuesta, nunca ejecutada automáticamente")


class Procedencia(Modelo):
    motor_sha256: str
    datos_sha256: str
    plan_sha256: str = Field(description="SHA-256 del bloque TOML del plan (desde el esquema 2.4; antes, del fichero entero, recalculado en la migración del 2026-10-06)")
    periodos_por_anio: int = Field(ge=1)


class Intento(Modelo):
    id: str
    fecha: date
    cambio: str


class Ficheros(Modelo):
    equity: Literal["equity.csv"] = "equity.csv"
    operaciones: Literal["operaciones.csv"] = "operaciones.csv"
    ficha: Literal["ficha.md"] = "ficha.md"
    equity_100: Optional[Literal["equity_100.csv"]] = Field(default=None, description="Equity de la referencia; presente si hay `referencia`")
    operaciones_100: Optional[Literal["operaciones_100.csv"]] = Field(default=None, description="Operaciones de la referencia")
    variantes: Optional[Literal["variantes.csv"]] = Field(default=None, description="Tabla de variantes; presente si hay `variantes`")


class Resumen(Modelo):
    """resumen.json: todo lo necesario para leer, comparar o graficar un experimento sin abrir el código."""
    version_esquema: Literal["2.0", "2.1", "2.2", "2.3", "2.4"] = VERSION
    experimento: Experimento
    evidencia: Evidencia
    robustez: Robustez
    metricas: Metricas
    referencia: Optional[Referencia] = Field(default=None, description="Riesgo al 100 % del capital; null en experimentos previos al esquema 2.1 sin recalcular")
    variantes: Optional[Variantes] = Field(default=None, description="Tabla de variantes para el dashboard; null si el plan no la pide")
    sensibilidad: Optional[list[Sensibilidad]] = Field(default=None, description="Rejilla umbral × multiplicador del tamaño por serie; null si el plan no la pide")
    no_calculables: dict[str, str] = Field(description="Métrica -> motivo por el que es null")
    operaciones_por_anio: dict[str, int]
    conclusiones: Conclusiones
    procedencia: Procedencia
    historial: list[Intento] = Field(min_length=1, description="Intentos de esta hipótesis, en orden; el último es este")
    ficheros: Ficheros = Ficheros()

    @model_validator(mode="after")
    def _coherente(self):
        if (self.referencia is None) != (self.ficheros.equity_100 is None) or (self.ficheros.equity_100 is None) != (self.ficheros.operaciones_100 is None):
            raise ValueError("`referencia` va siempre con equity_100.csv y operaciones_100.csv")
        if (self.variantes is None) != (self.ficheros.variantes is None):
            raise ValueError("`variantes` va siempre con variantes.csv")
        if self.historial[-1].id != self.experimento.id:
            raise ValueError("El último intento debe ser este experimento")
        faltan = {k for k, v in self.metricas.model_dump().items() if v is None} - set(self.no_calculables)
        if faltan:
            raise ValueError(f"Métricas null sin motivo: {sorted(faltan)}")
        return self


ESQUEMAS = {"resumen": Resumen, "sesion": Sesion, "operacion": Operacion, "variante": Variante}


def exportar_esquemas(directorio):
    for nombre, modelo in ESQUEMAS.items():
        esquema = {"$schema": "https://json-schema.org/draft/2020-12/schema", **modelo.model_json_schema()}
        (Path(directorio) / f"{nombre}.schema.json").write_text(json.dumps(esquema, ensure_ascii=False, indent=2) + "\n")
