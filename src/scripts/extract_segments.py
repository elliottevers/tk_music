import sys
sys.path.insert(0, '/Users/elliottevers/Documents/git-repos.nosync/tk_music_py/src')
from information_retrieval import extraction as ir
from message import messenger as mes
import argparse
from preprocess import vamp as prep_vamp
from postprocess import music_xml as postp_mxl
from quantize import quantize
from utils import utils
import os
from convert import music_xml as convert_mxl
from i_o import exporter as io_exporter
from utils import musix_xml as utils_mxl
from analysis_discrete import music_xml as analysis_mxl


def main(args):

    messenger = mes.Messenger()

    use_warped = utils.b_use_warped()

    (
        s_beat_start,
        s_beat_end,
        tempo,
        beat_start,
        beat_end,
        length_beats,
        beatmap
    ) = utils.get_tuple_beats()

    messenger.message(['length_beats', str(length_beats)])

    representation = utils.parse_arg(args.representation)

    if representation == 'symbolic':

        filename_pickle = os.path.join(
            utils.get_dirname_score(),
            'melody',
            ''.join([utils._get_name_project_most_recent(), '.pkl'])
        )

        part_melody = utils_mxl.thaw_stream(
            filename_pickle
        )

        stream_segment = analysis_mxl.get_segments(
            part_melody
        )

    elif representation == 'numeric':

        data_segments = ir.extract_segments(
            os.path.join(
                utils.get_dirname_audio_warped() if use_warped else utils.get_dirname_audio(),
                utils._get_name_project_most_recent() + '.wav'
            )
        )

        df_segments = prep_vamp.segments_to_df(
            data_segments
        )

        segment_tree = quantize.get_interval_tree(
            df_segments,
            diff=False
        )

        data_quantized = quantize.quantize(
            beatmap,
            s_beat_start,
            s_beat_end,
            trees={
                'segment': segment_tree
            }
        )

        data_quantized_segments = data_quantized['segment']

        score = postp_mxl.df_grans_to_score(
            data_quantized_segments,
            parts=['segment']
        )

        stream_segment = postp_mxl.extract_part(
            score,
            'segment'
        )

    else:
        raise ' '.join(['representation', representation, 'does not exist'])

    utils.create_dir_score()

    utils.create_dir_segment()

    filename_pickle = os.path.join(
        utils.get_dirname_score(),
        'segment',
        ''.join(
            [
                utils._get_name_project_most_recent(),
                '.pkl'
            ]
        )
    )

    utils_mxl.freeze_stream(
        stream_segment,
        filename_pickle
    )

    notes_live = convert_mxl.to_notes_live(
        stream_segment,
        beatmap,
        s_beat_start,
        s_beat_end,
        tempo
    )

    exporter = io_exporter.Exporter()

    exporter.set_part(notes_live, 'segment')

    exporter.export(utils.get_file_json_comm())

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Segments')

    parser.add_argument('--representation', help='either symbolic or numeric')

    args = parser.parse_args()

    main(args)
