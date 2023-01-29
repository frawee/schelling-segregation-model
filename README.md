# schelling-segregation-model

Show the Schelling segregation model process

Requires python 3

This project calculates a schelling segregation simulation show the emergence of segregation
even in the absence of strict preferences for a segregated society.
For more info, see https://en.wikipedia.org/wiki/Schelling%27s_model_of_segregation
For this purpose, agents of type A and B are randomly placed in a
grid of the size x_size * y_size. In each step, one agent evaluates his neighbors
and moves if the fraction of equal neighbors is less than T.

For displayed colors, the Colors class was taken from https://www.geeksforgeeks.org/print-colors-python-terminal/

In your run configuration, check "Emulate terminal in output console"

### Quickstart
To run the model, initalize an instance and call the run function.
Each call of run will update the last state, not re-initialize the grid.
You can decide how often to print updates.

```
 # initialize a schelling model
    schelling_model = SchellingModel(
        grid_size=(15, 15), n_agents=100, share_a=0.5, stay_threshold=0.5
    )

    # run and neatly print the result
    schelling_model.run(steps=2000, print_at_end=True, print_every=100)
```
# beside the grid state, you can also plot the share of agents that would not move if selected. 
```
    # plot the segregation over time
    schelling_model.plot_segregation_curve()
```
