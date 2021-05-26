from Model.Tour import Tour
import matplotlib.pyplot as plt

def plot(tour, instances, velocity,graph_step_by_step):
    fig, ax = plt.subplots()
    x_1 = [tour_cities.get_coordinate()[1] for tour_cities in tour]
    y_1 = [tour_cities.get_coordinate()[0] for tour_cities in tour]
    ax.plot(x_1, y_1,'r-*')

    x = [city.get_coordinate()[1] for city in instances]
    y = [city.get_coordinate()[0] for city in instances]

    ax.plot(x, y, 'b*')
    ax.set(title='About as simple as it gets, folks')
    if graph_step_by_step:
        plt.show()
    else:
        plt.draw()
        plt.pause(velocity)
