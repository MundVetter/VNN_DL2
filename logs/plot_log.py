def main(args):
    import matplotlib.pyplot as plt

    # Read the log file
    with open(args.file, 'r') as f:
        lines = f.read().splitlines()

    # Parse the log file
    lines = [line for line in lines if 'Accuracy' in line]
    train_acc, test_acc = lines[::3], lines[1::3]

    # Plot the accuracy
    plt.plot(train_acc, label='Train Accuracy')
    plt.plot(test_acc, label='Test Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.title(args.title)
    if args.output:
        plt.savefig(args.output)
    plt.savefig(args.output + '.pdf')
    plt.show()

if __name__ == '__main__':
    # Get arguments from command line
    import argparse
    parser = argparse.ArgumentParser(description='Plot log file')
    parser.add_argument('-f', '--file', help='Log file to plot', required=True)
    parser.add_argument('-o', '--output', help='Output file (e.g. out.pdf)', required=False)
    parser.add_argument('-t', '--title', default='Model accuracy', help='Title of plot', required=True)
    args = parser.parse_args()
    main(args)