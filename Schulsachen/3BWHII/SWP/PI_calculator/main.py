import tkinter as tk
import random
import math

class MonteCarloPiApp_Typeshiiiit:
    def __init__(self, root, num_samples):
        self.root = root
        self.canvas_size = 400   # big screen
        self.inside_circle = 0   # point in
        self.total_points = 0   # point out
        self.num_samples = num_samples

        # Creat/pack the canvas
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg='white')
        self.canvas.pack()

        # Draw circle sqaue
        self.canvas.create_oval(0, 0, self.canvas_size, self.canvas_size, outline='blue')
        self.canvas.create_line(self.canvas_size / 2, 0, self.canvas_size / 2, self.canvas_size, fill='black')
        self.canvas.create_line(0, self.canvas_size / 2, self.canvas_size, self.canvas_size / 2, fill='black')

        # display label
        self.label = tk.Label(root, text="Estimated Pi: ")
        self.label.pack()

        # Run 
        self.run_simulation()

    def run_simulation(self):
        # Clear point
        self.canvas.delete("point")
        self.inside_circle = 0
        self.total_points = 0

        # Generate point and if in circle
        for _ in range(self.num_samples):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            distance = math.sqrt(x**2 + y**2)

            screen_x = (x + 1) * (self.canvas_size / 2)
            screen_y = (y + 1) * (self.canvas_size / 2)

            if distance <= 1:
                self.inside_circle += 1
                self.canvas.create_oval(screen_x, screen_y, screen_x + 2, screen_y + 2, fill='red', outline='red', tags="point")
            else:
                self.canvas.create_oval(screen_x, screen_y, screen_x + 2, screen_y + 2, fill='black', outline='black', tags="point")

            self.total_points += 1
            pi_estimate = (self.inside_circle / self.total_points) * 4
            self.label.config(text=f"Estimated Pi: {pi_estimate:.6f}")

            self.root.update_idletasks()
            self.root.update()

if __name__ == "__main__":
    num_samples = int(input("Enter the number of points to generate: "))
    root = tk.Tk()
    root.title("Monte Carlp shit")
    app = MonteCarloPiApp_Typeshiiiit(root, num_samples)
    root.mainloop()