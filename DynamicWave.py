import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import MySQL


class Scope(object):
    def __init__(self, ax, cur, rang=400, time=0):
        self.rang = rang
        self.ax = ax
        self.cur = cur
        self.time = time
        self.xdata = np.arange(self.rang)
        self.ydata = np.array(np.zeros(self.rang))
        self.line, = ax.plot(self.xdata, self.ydata)
        self.ax.set_xlim(0, self.rang)

    def update(self, y):
        self.ydata = self.ydata[1:]
        sql = 'select * from wavedata where time>%s limit 1' % (self.time)
        self.cur.execute(sql)
        data = self.cur.fetchall()[0]
        self.time = data[0]
        self.ydata = np.append(self.ydata, [data[1]], axis=0)
        self.ax.set_ylim(self.ydata.min(), self.ydata.max())
        self.line.set_ydata(self.ydata)
        return self.line,


def display():
    fig, ax = plt.subplots()
    plt.xticks([])
    cur = MySQL.MysqlInit()
    scope = Scope(ax, cur, 1000)
    ani = animation.FuncAnimation(fig, scope.update, interval=5, blit=True)
    plt.show()


if __name__ == '__main__':
    display()
