import matplotlib.pyplot as plt

# Data for the x-axis
x = []
for i in range(20):
    x.append(i)

# Data for the y-axis
y = []

for i in x:
    y.append(i**2)

# Create a line plot
plt.plot(x, y)

# Add labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Simple Line Plot')

# Display the plot
plt.show()
