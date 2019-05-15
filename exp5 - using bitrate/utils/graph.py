"""
Classes para manipulação de graficos
"""
import numpy as np
import matplotlib.pyplot as plt


class Data:
    def __init__(self, x_leg: str, y_leg: str, x_axis: list, y_axis: list, y_stderr=(0,)):
        self.x_leg = x_leg
        self.y_leg = y_leg
        self.x_axis = list(x_axis)
        self.y_axis = list(y_axis)
        self.y_stderr = list(y_stderr)
        if y_stderr == 0:
            y_stderr *= len(x_axis)

    def __hash__(self):
        return hash((self.x_leg, self.y_leg, self.x_axis, self.y_axis))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__


class Line:
    def __init__(self, data: Data, label: str):
        self.data = data
        self.label = label

    def __hash__(self):
        return hash((self.label, self.data))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__


class Picture:
    def __init__(self, line: Line, title: str):
        self.line = [line]
        self.title = title

    def __hash__(self):
        return hash((self.line, self.title))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__

    def plot(self, graph_type='line', legend=True):

        plt.close()
        fig, ax = plt.subplots(1, 1, figsize=(8, 5))

        for line in self.line:
            if type in 'bar':
                w_bar = 0.2
                ax.bar(line.data.x_axis, line.data.y_axis, w_bar = w_bar, yerr=line.data.y_stderr)
            else:
                ax.plot(line.data.x_axis,
                        line.data.y_axis,
                        label=line.label)

            ax.set_xlabel(line.data.x_leg)
            ax.set_ylabel(line.data.y_leg)
            ax.set_title(self.title)
            ax.set_ylim(bottom=0)

            if legend:
                fig.legend()
