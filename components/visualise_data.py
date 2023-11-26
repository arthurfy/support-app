import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def draw_figure(canvas, figure):
  '''
  draw a figure for the graph

  PARAMETERS
  ----------
  canvas : tkinter canvas
  figure : matplotlib figure

  RETURN
  ------
  figure_canvas_agg : figure canvas
  '''

  figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
  figure_canvas_agg.draw()
  figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
  return figure_canvas_agg


def create_plot_graph(x_plot,
                      y_plot,
                      title: str = None,
                      x_label: str = None,
                      y_label: str = None):
  '''
  create a plot graph
  
  PARAMETERS
  ----------
  x_plot : list
  y_plot : list
  title : str
  x_label : str
  y_label : str

  RETURN
  ------
  fig : matplotlib figure
  '''
  plt.plot(x_plot, y_plot, color='red', marker='o')

  # if title is passed
  if title != None or title != "":
    plt.title(title, fontsize=14)

  if x_label != None or x_label != "":
    plt.xlabel(x_label, fontsize=14)

  if y_label != None or y_label != "":
    plt.ylabel(y_label, fontsize=14)

  plt.grid(True)
  return plt.gcf()


def create_scatter_graph(x_plot,
                         y_plot,
                         title: str = None,
                         x_label: str = None,
                         y_label: str = None):
  '''
  
  '''
  # if title is passed
  if title != None or title != "":
    plt.title(title, fontsize=14)

  if x_label != None or x_label != "":
    plt.xlabel(x_label, fontsize=14)

  if y_label != None or y_label != "":
    plt.ylabel(y_label, fontsize=14)

  plt.scatter(x_plot, y_plot)
  return plt.gcf()
