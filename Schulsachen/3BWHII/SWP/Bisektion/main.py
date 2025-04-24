import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Callable, Tuple, List, Optional, Dict
import json  # Add import for JSON handling

class EquationSolver:
    """Numerischer Solver für Nullstellenprobleme mit Bisektion und Newton-Raphson."""
    
    def __init__(self, function: str, tolerance: float = 1e-6, max_iter: int = 100):
        self.function_str = function
        self.tolerance = tolerance
        self.max_iter = max_iter
        self.history: List[Tuple[float, float, float]] = []
        self.errors: List[float] = []
        
    def _build_function(self) -> Callable[[float], float]:
        """Erstellt berechnete Funktion mit numpy Support."""
        return lambda x: eval(self.function_str, {'x': x, 'np': np, 'sinh': np.sinh, 'cosh': np.cosh})
    
    def bisection(self, a: float, b: float) -> float:
        """Bisektionsverfahren mit vollständiger History-Aufzeichnung."""
        f = self._build_function()
        self.history = []
        self.errors = []
        
        if f(a) * f(b) >= 0:
            raise ValueError("Funktion muss an den Intervallgrenzen unterschiedliche Vorzeichen haben.")
        
        for i in range(self.max_iter):
            c = (a + b) / 2
            self.history.append((a, b, c))
            error = abs(f(c))
            self.errors.append(error)
            
            if error < self.tolerance:
                return c
                
            if f(c) * f(a) < 0:
                b = c
            else:
                a = c
            
        return (a + b) / 2
    
    def newton_raphson(self, initial_guess: float) -> float:
        """Newton-Raphson Verfahren mit adaptiver Schrittweite."""
        f = self._build_function()
        self.history = []
        self.errors = []
        x = initial_guess
        
        for i in range(self.max_iter):
            # Numerische Ableitung mit adaptivem h
            h = max(1e-8, 1e-8 * abs(x))
            df = (f(x + h) - f(x - h)) / (2 * h)
            
            if abs(df) < 1e-12:
                break
                
            x_new = x - f(x)/df
            self.history.append((x, x_new, x_new))
            error = abs(f(x_new))
            self.errors.append(error)
            
            if error < self.tolerance:
                return x_new
                
            x = x_new
            
        return x

class SolutionVisualizer:
    """Interaktive Visualisierung des Lösungsprozesses."""
    
    def __init__(self, solver: EquationSolver, output_file: str = "animation_data.json"):
        self.solver = solver
        self.fig, self.axes = plt.subplots(3, 1, figsize=(10, 12))
        self.output_file = output_file  # File to save iteration data
        self._clear_output_file()  # Clear the file at the start
        self._setup_plots()
    
    def _clear_output_file(self):
        """Löscht den Inhalt der JSON-Datei zu Beginn."""
        with open(self.output_file, "w") as f:
            f.write("")  # Clear the file by writing an empty string
    
    def _setup_plots(self):
        """Initialisiert die drei Subplots."""
        titles = ['Funktionsverlauf', 'Fehlerentwicklung', 'Lösungskonvergenz']
        ylabels = ['f(x)', 'log10(Fehler)', 'x-Wert']
        
        for ax, title, ylabel in zip(self.axes, titles, ylabels):
            ax.clear()
            ax.set_title(title)
            ax.set_ylabel(ylabel)
            ax.grid(True)
        
        self.axes[1].set_yscale('log')
        self.axes[2].set_xlabel('Iteration')
        plt.tight_layout()
    
    def _save_iteration_data(self, frame: int):
        """Speichert die Iterationsdaten in eine JSON-Datei."""
        a, b, c = self.solver.history[frame]
        error = self.solver.errors[frame]
        data = {
            "iteration": frame + 1,
            "a": a,
            "b": b,
            "c": c,
            "error": error
        }
        with open(self.output_file, "a") as f:
            json.dump(data, f)
            f.write("\n")  # Add a newline for readability
    
    def animate(self):
        """Erzeugt die Animationssequenz."""
        f = self.solver._build_function()
        x_min = min(h[0] for h in self.solver.history)
        x_max = max(h[1] for h in self.solver.history)
        x_vals = np.linspace(x_min, x_max, 400)
        y_vals = [f(x) for x in x_vals]
        
        # Initiale Plot-Elemente
        self.axes[0].plot(x_vals, y_vals, 'b-')
        self.axes[0].axhline(0, color='grey', ls='--')
        self.axes[1].plot([], [], 'r-')
        self.axes[2].plot([], [], 'go-', markersize=4)
        
        def update(frame):
            a, b, c = self.solver.history[frame]
            
            # Aktualisiere alle Plots
            self.axes[0].clear()
            self.axes[0].plot(x_vals, y_vals, 'b-')
            self.axes[0].axhline(0, color='grey', ls='--')
            self.axes[0].scatter([a, b, c], [0, 0, 0], c=['red', 'blue', 'green'], s=50)
            
            self.axes[1].plot(self.solver.errors[:frame+1], 'r-')
            self.axes[1].set_yscale('log')
            
            solutions = [h[2] for h in self.solver.history[:frame+1]]
            self.axes[2].plot(solutions, 'go-', markersize=4)
            
            # Save iteration data to JSON
            self._save_iteration_data(frame)
            
            return self.axes
        
        anim = FuncAnimation(self.fig, update, frames=len(self.solver.history), interval=800, blit=False)
        self.animation = anim  # Assign to an instance variable to prevent garbage collection
        plt.show()  # Ensure the animation is displayed

class CatenarySolver:
    """Physikalisch exakte Lösung des Kettenlinienproblems."""
    
    def __init__(self):
        self.width = 100.0
        self.sag = 10.0
        self.a = None
        self.length = None
    
    def get_user_input(self):
        """Interaktive Parametererfassung."""
        print("\n=== Kettenlinienberechnung ===")
        self.width = float(input(f"Abstand zwischen Masten [m] (default: 100): ") or 100)
        self.sag = float(input(f"Maximaler Durchhang [m] (default: 10): ") or 10)
    
    def solve(self) -> Dict[str, float]:
        """Berechnet alle Parameter der Kettenlinie."""
        # Exakte Lösung für Krümmungsradius a
        solver = EquationSolver(f"x*cosh({self.width}/(2*x)) - x - {self.sag}")
        a_guess = self.width**2 / (8 * self.sag)  # Physikalisch sinnvolle Startschätzung
        self.a = solver.bisection(a_guess/10, a_guess*10)
        
        # Exakte Seillänge berechnen
        self.length = 2 * self.a * np.sinh(self.width/(2*self.a))
        
        # Position des Scheitelpunkts
        y0 = self.a * np.cosh(self.width/(2*self.a)) - self.a + self.sag
        
        return {
            'a': self.a,
            'length': self.length,
            'x0': self.width/2,
            'y0': y0,
            'iterations': len(solver.history)
        }
    
    def plot(self, params: Dict[str, float]):
        """Visualisierung der Kettenlinie mit allen Parametern."""
        x = np.linspace(0, self.width, 200)
        y = params['a'] * np.cosh((x - params['x0'])/params['a']) - params['a'] + params['y0']
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Kettenlinie
        ax.plot(x, y, 'b-', lw=2, label=f'Kettenlinie (L = {params["length"]:.2f}m)')
        
        # Masten
        ax.plot([0, 0], [0, y[0]], 'k-', lw=3)
        ax.plot([self.width, self.width], [0, y[-1]], 'k-', lw=3)
        
        # Durchhang5
        ax.plot([params['x0'], params['x0']], 
                [params['y0'] - params['a'], params['y0'] - params['a'] + self.sag], 
                'r--', label=f'Durchhang = {self.sag}m')
        
        # Scheitelpunkt
        ax.axhline(params['y0'] - params['a'], color='g', linestyle=':', label='Scheitelpunkt')
        
        ax.set_title(f'Kettenlinie: {self.width}m Spannweite, {self.sag}m Durchhang')
        ax.set_xlabel('Position [m]')
        ax.set_ylabel('Höhe [m]')
        ax.grid(True)
        ax.legend()
        ax.axis('equal')
        plt.show()

def run_bisection():
    """Interaktive Bisektionsberechnung."""
    print("\n=== Bisektionsverfahren ===")
    func = input("Funktion (z.B. 'x**2 - 25'): ") or "x**2 - 25"
    a = float(input("Linke Intervallgrenze: ") or 0)
    b = float(input("Rechte Intervallgrenze: ") or 2)
    
    solver = EquationSolver(func)
    root = solver.bisection(a, b)
    print(f"\nErgebnis: Nullstelle ≈ {root:.10f}")
    
    visualizer = SolutionVisualizer(solver)
    anim = visualizer.animate()
    plt.show()  # Animation anzeigen
    print(f"Animation-Daten gespeichert in animation_data.json")

def run_newton():
    """Interaktive Newton-Raphson Berechnung."""
    print("\n=== Newton-Raphson Verfahren ===")
    func = input("Funktion (z.B. 'x**2 - 25'): ") or "x**2 - 25"
    x0 = float(input("Startwert: ") or 2)
    
    solver = EquationSolver(func)
    root = solver.newton_raphson(x0)
    print(f"\nErgebnis: Nullstelle ≈ {root:.10f}")
    
    visualizer = SolutionVisualizer(solver)
    anim = visualizer.animate()
    plt.show()
    print(f"Animation-Daten gespeichert in animation_data.json")

def run_polynomial_test():
    """Genauigkeitstests für das Polynom aus Aufgabe 8."""
    print("\n=== Polynom-Genauigkeitstest ===")
    func = "2*x + x**2 + 3*x**3 - x**4"
    a = float(input("Linke Grenze (empfohlen 3): ") or 3)
    b = float(input("Rechte Grenze (empfohlen 4): ") or 4)
    
    for tol in [1e-2, 1e-5, 1e-8, 1e-12]:
        solver = EquationSolver(func, tolerance=tol)
        root = solver.bisection(a, b)
        print(f"Tol {tol:.0e}: Nullstelle = {root:.12f} ({len(solver.history)} Iterationen)")

def run_catenary():
    """Komplette Kettenlinienberechnung."""
    solver = CatenarySolver()
    solver.get_user_input()
    results = solver.solve()
    
    print("\n=== Ergebnisse ===")
    print(f"Krümmungsradius a: {results['a']:.6f} m")
    print(f"Exakte Seillänge: {results['length']:.6f} m")
    print(f"Scheitelpunkt (x0,y0): ({results['x0']:.2f}, {results['y0']:.6f})")
    print(f"Benötigte Iterationen: {results['iterations']}")
    
    solver.plot(results)

def main():
    """Hauptmenü der Anwendung."""
    while True:
        print("\n=== Numerische Methoden ===")
        print("1. Bisektionsverfahren")
        print("2. Newton-Raphson Verfahren")
        print("3. Polynom-Genauigkeitstest")
        print("4. Kettenlinienberechnung")
        print("5. Beenden")
        
        choice = input("Auswahl (1-5): ")
        
        if choice == "1":
            run_bisection()
        elif choice == "2":
            run_newton()
        elif choice == "3":
            run_polynomial_test()
        elif choice == "4":
            run_catenary()
        elif choice == "5":
            break
        else:
            print("Ungültige Eingabe!")

if __name__ == "__main__":
    main()