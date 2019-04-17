from message import messenger as mes
import argparse
from utils import utils
import os


def main(args):

    messenger = mes.Messenger()

    _, _, _, _, length_beats, _ = utils.get_tuple_beats(
        os.path.join(
            utils.get_dirname_beat(),
            utils._get_name_project_most_recent() + '.pkl'
        )
    )

    messenger.message(['length_beats', str(length_beats)])

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get length of training data in beats')

    args = parser.parse_args()

    main(args)
