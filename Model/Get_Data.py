import os
import numpy as np
from muscima.io import parse_cropobject_list
import itertools
from Music_function import extract_notes_from_doc
from Music_function import get_image
from skimage.transform import resize


Q_LABEL = 0
H_LABEL = 1
E_LABEL = 2
S_LABEL = 3
D_Q_LABEL = 4
D_H_LABEL = 5
D_E_LABEL = 6
D_S_LABEL = 7

if __name__ == "__main__":
    # Change this to reflect wherever your MUSCIMA++ data lives
    CROPOBJECT_DIR = r'MUSCIMA-pp_v1.0/v1.0/data/cropobjects_manual'

    cropobject_fnames = [os.path.join(CROPOBJECT_DIR, f) for f in os.listdir(CROPOBJECT_DIR)]
    docs = [parse_cropobject_list(f) for f in cropobject_fnames]

    notes = [extract_notes_from_doc(cropobjects) for cropobjects in docs]

    qns = list(itertools.chain(*[qn for qn, hn, en, sn, d_qn, d_hn, d_en, d_sn in notes]))
    hns = list(itertools.chain(*[hn for qn, hn, en, sn, d_qn, d_hn, d_en, d_sn in notes]))
    ens = list(itertools.chain(*[en for qn, hn, en, sn, d_qn, d_hn, d_en, d_sn in notes]))
    sns = list(itertools.chain(*[sn for qn, hn, en, sn, d_qn, d_hn, d_en, d_sn in notes]))
    d_qns = list(itertools.chain(*[d_qn for qn, hn, en, sn, d_qn, d_hn, d_en, d_sn in notes]))
    d_hns = list(itertools.chain(*[d_hn for qn, hn, en, sn, d_qn, d_hn, d_en, d_sn in notes]))
    d_ens = list(itertools.chain(*[d_en for qn, hn, en, sn, d_qn, d_hn, d_en, d_sn in notes]))
    d_sns = list(itertools.chain(*[d_sn for qn, hn, en, sn, d_qn, d_hn, d_en, d_sn in notes]))

    qn_images = [get_image(qn) for qn in qns]
    hn_images = [get_image(hn) for hn in hns]
    en_images = [get_image(en) for en in ens]
    sn_images = [get_image(sn) for sn in sns]
    d_qn_images = [get_image(d_qn) for d_qn in d_qns]
    d_hn_images = [get_image(d_hn) for d_hn in d_hns]
    d_en_images = [get_image(d_en) for d_en in d_ens]
    d_sn_images = [get_image(d_sn) for d_sn in d_sns]

    qn_resized = [resize(qn, (200, 64)) for qn in qn_images]
    hn_resized = [resize(hn, (200, 64)) for hn in hn_images]
    en_resized = [resize(en, (200, 64)) for en in en_images]
    sn_resized = [resize(sn, (200, 64)) for sn in sn_images]
    d_qn_resized = [resize(d_qn, (200, 64)) for d_qn in d_qn_images]
    d_hn_resized = [resize(d_hn, (200, 64)) for d_hn in d_hn_images]
    d_en_resized = [resize(d_en, (200, 64)) for d_en in d_en_images]
    # d_sn_resized = [resize(d_sn, (200, 64)) for d_sn in d_sn_images]
    d_sn_resized = list(np.load('d_sn_resized.npy'))

    # And re-binarize, to compensate for interpolation effects
    for qn in qn_resized:
        qn[qn > 0] = 1
    for hn in hn_resized:
        hn[hn > 0] = 1
    for en in en_resized:
        en[en > 0] = 1
    for sn in sn_resized:
        sn[sn > 0] = 1

    for d_qn in d_qn_resized:
        d_qn[d_qn > 0] = 1
    for d_hn in d_hn_resized:
        d_hn[d_hn > 0] = 1
    for d_en in d_en_resized:
        d_en[d_en > 0] = 1
    for d_sn in d_sn_resized:
        d_sn[d_sn > 0] = 1

    qn_labels = [Q_LABEL for _ in qn_resized]
    hn_labels = [H_LABEL for _ in hn_resized]
    en_labels = [E_LABEL for _ in en_resized]
    sn_labels = [S_LABEL for _ in sn_resized]

    d_qn_labels = [D_Q_LABEL for _ in d_qn_resized]
    d_hn_labels = [D_H_LABEL for _ in d_hn_resized]
    d_en_labels = [D_E_LABEL for _ in d_en_resized]
    d_sn_labels = [D_S_LABEL for _ in d_sn_resized]

    notes = qn_resized + hn_resized + en_resized + sn_resized + d_qn_resized + d_hn_resized + d_en_resized + d_sn_resized
    labels = qn_labels + hn_labels + en_labels + sn_labels + d_qn_labels + d_hn_labels + d_en_labels + d_sn_labels

    np.save('Train_x.npy', np.array(notes))
    np.save('Train_y.npy', np.array(labels))
