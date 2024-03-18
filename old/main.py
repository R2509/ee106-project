'''
Main file.
'''

if __name__ == '__main__':
    from argparse import Namespace
    from pathlib import Path

    from proc import summarise_file
    from simple_cli import SimpleCLI

    this_dir = dirpath = Path(__file__).resolve().parent

    def run(ns: Namespace):
        data = summarise_file(
            this_dir / 'small_dataset.csv',
            method = 1,
            time_range = ('2018-04-01', '2018-04-01'),
            sensor_range = (0, 5),
        )
        print(data)


    # """ cli = SimpleCLI()

    # cli.add_command('main', run, 'Test run.', [
    #     (['--time-start'], {'action': 'store'}),
    # ]) """

    # cli.start()

    data, time_taken = summarise_file(
        this_dir / 'small_dataset.csv',
        method = 1,
        time_range = ('2018-04-01 00:00:00', '2018-04-01 00:03:00'),
        sensor_range = (0, 1),
    )
    print(*data, sep='\n\n')
    print(f'Tasks took {time_taken:.2f} seconds.')
