import pickle
import matplotlib.pyplot as plt


def main():
    with open('all_scores.tkl', 'r') as f:
        l = pickle.load(f)
    i = 0
    ptx, pty = [], []
    for pts in l:
        i += 1
        for y in pts:
            ptx.append(i)
            pty.append(y)
    plt.plot(ptx, pty, 'ro')
    plt.show()


if __name__ == "__main__":
    main()
