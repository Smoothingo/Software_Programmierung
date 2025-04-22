import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Callable, Dict, List, Tuple

class EquationSolver:
    """Allgemeiner Gleichungslöser mit Bisektionsverfahren"""
    
    def __init__(self, equation: str):
        self.equation = equation
        self.parameters: Dict[str, float] = {}
        self.history: List[Tuple[float, float, float]] = []
        self.errors: List[float] = []
        self.variables = self._parse_variables()

    def _parse_variables(self) -> List[str]:
        """Einfache Variablenanalyse der Gleichung"""
        variables = set()
        for part in self.equation.replace('math.', '').split():
            if part.isalpha() and part not in ['x', 'np'] and len(part) == 1:
                variables.add(part)
        return sorted(variables)

    def _build_function(self) -> Callable[[float], float]:
        """Erstellt die Lösungsfunktion dynamisch"""
        context = {
            'math': math,
            'np': np,
            '__builtins__': None,
            **self.parameters
        }
        return lambda x: eval(self.equation, {'__builtins__': {}}, {**context, 'x': x})

    def bisection(self, a: float, b: float, eps: float = 1e-8, max_iter: int = 100) -> float:
        """Implementierung des Bisektionsverfahrens"""
        f = self._build_function()
        
        if f(a) * f(b) >= 0:
            raise ValueError("Kein Vorzeichenwechsel im Intervall [a, b]")

        self.history.clear()
        self.errors.clear()

        for _ in range(max_iter):
            c = (a + b) / 2
            fc = f(c)
            
            self.history.append((a, b, c))
            self.errors.append(abs(fc))

            if abs(fc) < eps:
                return c

            if f(a) * fc < 0:
                b = c
            else:
                a = c

        return (a + b) / 2

class SolutionVisualizer:
    """Visualisierung des Lösungsprozesses"""
    
    def __init__(self, solver: EquationSolver):
        self.solver = solver
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(14, 6))
        self._setup_plots()

    def _setup_plots(self):
        """Initialisiert die Diagramme"""
        # Bestimme Plotbereich
        a_values = [h[0] for h in self.solver.history]
        b_values = [h[1] for h in self.solver.history]
        x_min = min(a_values) - 1
        x_max = max(b_values) + 1

        # Funktion plotten
        x = np.linspace(x_min, x_max, 400)
        f = self.solver._build_function()
        y = [f(xi) for xi in x]
        
        self.ax1.plot(x, y, 'b-', label='Funktion')
        self.ax1.axhline(0, color='gray', linestyle='--')
        self.ax1.set_title('Bisektionsverfahren')
        self.ax1.set_xlabel('x')
        self.ax1.set_ylabel('f(x)')
        self.ax1.grid(True)

        # Fehlerplot
        self.ax2.set_ylim(1e-10, 1e+3)
        self.ax2.set_yscale('log')
        self.ax2.set_title('Fehlerentwicklung')
        self.ax2.set_xlabel('Iteration')
        self.ax2.set_ylabel('Absoluter Fehler (log)')
        self.ax2.grid(True)

    def animate(self):
        """Erstellt die Animation"""
        def update(frame):
            # Lösche vorherige Punkte
            while self.ax1.collections:
                self.ax1.collections[-1].remove()
            
            # Aktuelle Iteration darstellen
            a, b, c = self.solver.history[frame]
            self.ax1.scatter([a, b, c], [0, 0, 0],
                           color=['red', 'blue', 'green'],
                           zorder=5,
                           label=f'Iteration {frame+1}')
            
            # Fehlerplot aktualisieren
            self.ax2.plot(self.solver.errors[:frame+1], 'r-')
            self.ax2.relim()
            self.ax2.autoscale_view()
            
            return self.ax1.collections + self.ax2.lines

        ani = FuncAnimation(self.fig,
                          update,
                          frames=len(self.solver.history),
                          interval=500,
                          blit=False,
                          repeat=False)
        plt.show()

def main():
    print("=== Numerischer Gleichungslöser ===")
    print("Geben Sie die Gleichung als Python-Ausdruck ein")
    print("Verfügbare Funktionen: math.*, np.*")
    print("Beispiel: x**2 - n\n")
    
    equation = input("Gleichung f(x) = ")
    solver = EquationSolver(equation)

    # Parameter eingeben
    for param in solver.variables:
        solver.parameters[param] = float(input(f"Wert für {param}: "))

    # Intervall eingeben
    while True:
        try:
            a = float(input("Linke Intervallgrenze a: "))
            b = float(input("Rechte Intervallgrenze b: "))
            break
        except ValueError:
            print("Ungültige Eingabe! Bitte Zahlen eingeben.")

    # Berechnung durchführen
    try:
        root = solver.bisection(a, b)
        print(f"\nErgebnis: {root:.10f}")
        print(f"Letzter Fehler: {solver.errors[-1]:.2e}")
        print(f"Benötigte Iterationen: {len(solver.history)}")

        # Visualisierung
        vis = SolutionVisualizer(solver)
        vis.animate()

    except ValueError as e:
        print(f"\nFehler: {str(e)}")
    except Exception as e:
        print(f"\nUnerwarteter Fehler: {str(e)}")

if __name__ == "__main__":
    main()