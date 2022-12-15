from seaborn import lineplot

def likes_over_time(list_of_likes):
    x = list_of_likes[:][0]
    y = list_of_likes[:][1]
    plot = lineplot(x=x, y=y)
    return plot


