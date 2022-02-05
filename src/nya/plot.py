import matplotlib.pyplot as plt
import json
import click

@click.command()
@click.argument('input_', metavar='INPUT', type=click.File())
def cli(input_):
    FF = []
    PP = []
    for line in input_:
        dat = json.loads(line)
        FF.append(dat['F']/1e6)
        PP.append(dat['P'])

    plt.plot(FF, PP)
    plt.xlabel('Frequency [MHz]')
    plt.ylabel('Power [dBm]')
    plt.show()
