"""
Numerischer Gleichungslöser für Projekt Bisektion
Autor: [Ihr Name]
Klasse: [Ihre Klasse]
Datum: [Datum]
"""
# Set a non-interactive backend for matplotlib to avoid Qt issues
import matplotlib
matplotlib.use('TkAgg')

import math
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Callable, List, Tuple, Dict

# ================= KONFIGURATION =================
  # FORMEL FÜR IRGEND EINE AUFGABE SETZEN
HAUPTFORMEL = "a * math.cosh(50 / a) - (a + 10)" 
DEFAULT_EPS = 1e-8              # Standard-Genauigkeit
MAX_ITER = 100                  # Maximale Iterationen
PLOT_XLABEL = "x"               # X-Achsenbeschriftung
PLOT_YLABEL = "f(x)"            # Y-Achsenbeschriftung

# ================= LÖSUNGSKLASSE ================
class EquationSolver:
    """Numerischer Gleichungslöser mit Bisektion/Regula Falsi"""
    
    def __init__(self, equation: str):
        self.equation = equation
        self.parameters: Dict[str, float] = {}
        self.history: List[Tuple[float, float, float]] = []
        self.errors: List[float] = []
        self.variables = self._parse_variables()

    def _parse_variables(self) -> List[str]:
        """Erkennt Variablen mit Regex"""
        equation_clean = re.sub(r'\b(math\.|np\.)?', '', self.equation)
        return sorted(set(re.findall(r'\b([a-zA-Z])\b(?![\w.])', equation_clean)) - {'x'})

    def _build_function(self) -> Callable[[float], float]:
        """Erstellt die Lösungsfunktion sicher"""
        context = {'math': math, 'np': np, '__builtins__': None, **self.parameters, 'w': 100, 'h': 10}
        try:
            return lambda a: eval(self.equation, {'__builtins__': {}}, {**context, 'a': a})
        except Exception as e:
            raise ValueError(f"Ungültige Gleichung: {str(e)}") from e

    def bisection(self, a: float, b: float, eps: float = DEFAULT_EPS) -> float:
        """Implementierung des Bisektionsverfahrens (Aufgabe 5)"""
        if a > b: a, b = b, a
        f = self._build_function()
        self._validate_interval(f, a, b)
        
        self.history.clear()
        self.errors.clear()
        
        for _ in range(MAX_ITER):
            c = (a + b) / 2
            fc = f(c)
            self._update_history(a, b, c, fc)
            
            if abs(fc) < eps: 
                return c
            a, b = (a, c) if f(a)*fc < 0 else (c, b)
        
        return (a + b)/2

    def regula_falsi(self, a: float, b: float, eps: float = DEFAULT_EPS) -> float:
        """Regula Falsi Verfahren (Aufgabe 6)"""
        if a > b: a, b = b, a
        f = self._build_function()
        self._validate_interval(f, a, b)
        
        self.history.clear()
        self.errors.clear()
        
        for _ in range(MAX_ITER):
            fa, fb = f(a), f(b)
            c = b - fb*(b - a)/(fb - fa)
            fc = f(c)
            self._update_history(a, b, c, fc)
            
            if abs(fc) < eps: 
                return c
            a, b = (a, c) if f(a)*fc < 0 else (c, b)
        
        return c

    def _validate_interval(self, f: Callable, a: float, b: float):
        """Prüft Vorzeichenwechsel und gibt Debug-Informationen aus"""
        fa, fb = f(a), f(b)
        print(f"Debug: f({a}) = {fa}, f({b}) = {fb}")  # Debug-Ausgabe
        if fa * fb >= 0:
            raise ValueError("Kein Vorzeichenwechsel im Intervall [a, b]")

    def _update_history(self, a: float, b: float, c: float, fc: float):
        """Speichert Iterationsdaten"""
        self.history.append((a, b, c))
        self.errors.append(abs(fc))

# ================= VISUALISIERUNG ================
class SolutionVisualizer:
    """Visualisierungsklasse für Lösungsprozess (Aufgabe 7)"""
    
    def __init__(self, solver: EquationSolver):
        self.solver = solver
        self.fig = plt.figure(figsize=(16, 8))
        self._setup_plots()

    def _setup_plots(self):
        """Initialisiert die Diagramme"""
        # Layout-Anpassungen
        gs = self.fig.add_gridspec(2, 2)
        
        # Subplots erstellen
        self.ax1 = self.fig.add_subplot(gs[0, 0])  # Intervallentwicklung
        self.ax2 = self.fig.add_subplot(gs[0, 1])  # Fehlerkonvergenz
        self.ax3 = self.fig.add_subplot(gs[1, :])  # Lösungsannäherung (ganze Breite)

        # Initiale Plots
        self._draw_initial_plots()

    def _draw_initial_plots(self):
        """Zeichnet die initialen Diagrammelemente"""
        # Intervallentwicklung
        x_min = min(h[0] for h in self.solver.history) - 1
        x_max = max(h[1] for h in self.solver.history) + 1
        x = np.linspace(x_min, x_max, 400)
        f = self.solver._build_function()

        self.ax1.clear()
        self.ax1.plot(x, [f(xi) for xi in x], 'b-', label='Funktion')
        self.ax1.axhline(0, color='gray', linestyle='--')
        self.ax1.set_title('Intervallentwicklung', pad=15)
        self.ax1.set_xlabel(PLOT_XLABEL, labelpad=12)
        self.ax1.set_ylabel(PLOT_YLABEL, labelpad=12)
        self.ax1.grid(True)

        # Fehlerkonvergenz
        self.ax2.clear()
        self.ax2.set_yscale('log')
        self.ax2.set_title('Fehlerkonvergenz', pad=15)
        self.ax2.set_xlabel('Iterationen', labelpad=12)
        self.ax2.set_ylabel('Log. Fehler', labelpad=12)
        self.ax2.grid(True)

        # Lösungsannäherung
        self.ax3.clear()
        self.ax3.set_title('Lösungsannäherung', pad=15)
        self.ax3.set_xlabel('Iterationen', labelpad=12)
        self.ax3.set_ylabel('Lösung', labelpad=12)
        self.ax3.grid(True)

    def animate(self):
        """Erstellt Animationsframes"""
        def update(frame):
            # Update für alle Subplots
            a, b, c = self.solver.history[frame]
            
            # Intervallentwicklung aktualisieren
            self.ax1.clear()
            self._draw_initial_plots()
            self.ax1.scatter([a, b, c], [0, 0, 0], 
                            color=['red', 'blue', 'green'], 
                            marker='o',
                            s=100,
                            zorder=5)
            self.ax1.legend(['Funktion', 'Nullinie', 'a', 'b', 'c'], 
                           loc='upper right')

            # Fehlerkurve aktualisieren
            self.ax2.plot(self.solver.errors[:frame+1], 'r-', linewidth=2)
            self.ax2.set_ylim(top=max(self.solver.errors)*1.1)
            
            # Lösungsannäherung aktualisieren
            solutions = [h[2] for h in self.solver.history[:frame+1]]
            self.ax3.plot(solutions, 'g-', linewidth=2)
            self.ax3.set_xlim(0, len(self.solver.history))
            
            return self.ax1, self.ax2, self.ax3

        ani = FuncAnimation(self.fig, update, 
                           frames=len(self.solver.history), 
                           interval=800, 
                           repeat=False)
        plt.tight_layout()
        plt.show()
# ================= HAUPTPROGRAMM ================
def main():
    print("=== Numerischer Gleichungslöser ===")
    print(f"Aktive Formel: {HAUPTFORMEL}\n")

    # Solver initialisieren
    solver = EquationSolver(HAUPTFORMEL)

    # Intervall einlesen
    while True:
        try:
            a = float(input("Linke Grenze a: "))
            b = float(input("Rechte Grenze b: "))
            break
        except ValueError:
            print("Ungültige Eingabe!")

    # Verfahrenswahl
    method = input("Verfahren [Bisektion/Regula]: ").lower()

    try:
        # Berechnung durchführen
        if method.startswith('b'):
            root = solver.bisection(a, b)
        else:
            root = solver.regula_falsi(a, b)

        # Ergebnisse ausgeben
        print(f"\nErgebnis: {root:.10f}")
        print(f"Iterationen: {len(solver.history)}")
        print(f"Letzter Fehler: {solver.errors[-1]:.2e}")

        # Visualisierung
        if len(solver.history) > 0:
            vis = SolutionVisualizer(solver)
            vis.animate()

        # Aufgabe 9: Berechnung der Seillänge
        if HAUPTFORMEL == "a * math.cosh(50 / a) - (a + 10)":
            import math
            w = 100  # Abstand zwischen den Befestigungspunkten
            l = 2 * root * math.sinh(w / (2 * root))
            print(f"\nBerechneter Krümmungsradius a: {root:.10f}")
            print(f"Länge der Leitung l: {l:.10f} m")
        else:
            print("\nDie Seillänge wurde nicht berechnet, da die Formel nicht der Standardformel entspricht.")

    except ValueError as e:
        print(f"\nFehler: {str(e)}")

if __name__ == "__main__":
    main()