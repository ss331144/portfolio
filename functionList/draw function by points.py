##import matplotlib.pyplot as plt
##
### Data
##x_values = [1, 2, 3, 4, 5]
##y_values = [1, 4, 9, 16, 25]
##
### Create a figure and axis
##fig, ax = plt.subplots()
##
### Plot the data
##ax.plot(x_values, y_values)
##
### Set the title and axis labels
##ax.set_title("My Line Graph")
##ax.set_xlabel("X-axis Label")
##ax.set_ylabel("Y-axis Label")
##
### Show the graph
##plt.show()
import numpy as np
import matplotlib.pyplot as plt
import math


# Get 5 user input points
points=[]
i=0
print("Enter 000 for continue to Graph ")
num_input=int(input("How point do you have? "))
mon=-num_input-1
num_s=0
while num_s!=num_input :
    num_s+=1
    mon+=1
    x=mon
    #x = str(input(f"Enter x value for point {i+1}: "))
    y = str(input(f"Enter y value for point {i+1}: "))
    print()
    if x=="000" or y=="000" :
        break
    else: x=float(x); y=float(y)
    i+=1
    points.append((x, y))

# Create arrays for x and y values
x_values = [p[0] for p in points]
y_values = [p[1] for p in points]

# Generate curve points using numpy's polyfit function
z = np.polyfit(x_values, y_values, 4)
f = np.poly1d(z)
x_curve = np.linspace(min(x_values), max(x_values), 100)
y_curve = f(x_curve)

# Plot the points and curve
plt.plot(x_values, y_values, 'bo', label="User Points")
plt.plot(x_curve, y_curve, 'r-', label="Curve")
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.title("Curve from User Points")

# Display the plot
plt.show()

