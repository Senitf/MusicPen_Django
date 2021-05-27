import numpy
import os
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Bear in mind that the outlinks are integers, only valid within the same document.
# Therefore, we define a function per-document, not per-dataset.

# 전체 데이터 가져오기
def extract_notes_from_doc(cropobjects):

    _cropobj_dict = {c.objid: c for c in cropobjects}

    notes = []
    eight_notes = []
    sixteen_notes = []
    dot_notes = []
    dot_eight_notes = []
    dot_sixteen_notes = []
    for c in cropobjects:
        if (c.clsname == 'notehead-full') or (c.clsname == 'notehead-empty'):
            _has_stem = False
            _has_beam = False
            _has_8th_flag = False
            _has_16th_flag = False
            _has_dot = False
            stem_obj = None
            e_flag_obj = None
            s_flag_obj = None
            dot_obj = None
            for o in c.outlinks:
                _o_obj = _cropobj_dict[o]
                if _o_obj.clsname == 'stem':
                    _has_stem = True
                    stem_obj = _o_obj
                elif _o_obj.clsname == 'beam':
                    _has_beam = True
                elif _o_obj.clsname == '8th_flag':
                    _has_8th_flag = True
                    e_flag_obj = _o_obj
                elif _o_obj.clsname == '16th_flag':
                    _has_16th_flag = True
                    s_flag_obj = _o_obj
                elif _o_obj.clsname == 'duration-dot':
                    _has_dot = True
                    dot_obj = _o_obj
            if _has_stem and (not _has_beam):
                if len(stem_obj.inlinks) == 1:
                    if _has_dot:
                        if _has_8th_flag:
                            if _has_16th_flag:
                                dot_sixteen_notes.append((c, stem_obj, e_flag_obj, s_flag_obj, dot_obj))
                            else:
                                dot_eight_notes.append((c, stem_obj, e_flag_obj, dot_obj))
                        else:
                            dot_notes.append((c, stem_obj, dot_obj))
                    else:
                        if _has_8th_flag:
                            if _has_16th_flag:
                                sixteen_notes.append((c, stem_obj, e_flag_obj, s_flag_obj))
                            else:
                                eight_notes.append((c, stem_obj, e_flag_obj))
                        else:
                            notes.append((c, stem_obj))
    dot_quarter_notes = [(n, s, d) for n, s, d in dot_notes if n.clsname == 'notehead-full']
    dot_half_notes = [(n, s, d) for n, s, d in dot_notes if n.clsname == 'notehead-empty']
    quarter_notes = [(n, s) for n, s in notes if n.clsname == 'notehead-full']
    half_notes = [(n, s) for n, s in notes if n.clsname == 'notehead-empty']
    return quarter_notes, half_notes, eight_notes, sixteen_notes, dot_quarter_notes, dot_half_notes, dot_eight_notes, dot_sixteen_notes


def get_image(cropobjects, margin=1):
    """Paste the cropobjects' mask onto a shared canvas.
    There will be a given margin of background on the edges."""

    # Get the bounding box into which all the objects fit
    top = min([c.top for c in cropobjects])
    left = min([c.left for c in cropobjects])
    bottom = max([c.bottom for c in cropobjects])
    right = max([c.right for c in cropobjects])

    # Create the canvas onto which the masks will be pasted
    height = bottom - top + 2 * margin
    width = right - left + 2 * margin
    canvas = numpy.zeros((height, width), dtype='uint8')

    for c in cropobjects:
        # Get coordinates of upper left corner of the CropObject
        # relative to the canvas
        _pt = c.top - top + margin
        _pl = c.left - left + margin
        # We have to add the mask, so as not to overwrite
        # previous nonzeros when symbol bounding boxes overlap.
        canvas[_pt:_pt + c.height, _pl:_pl + c.width] += c.mask

    canvas[canvas > 0] = 1
    return canvas


def show_mask(mask):
    plt.imshow(mask, cmap='gray', interpolation='nearest')
    plt.show()


def show_masks(masks, row_length=5):
    n_masks = len(masks)
    n_rows = n_masks // row_length + 1
    n_cols = min(n_masks, row_length)
    fig = plt.figure()
    for i, mask in enumerate(masks):
        plt.subplot(n_rows, n_cols, i + 1)
        plt.imshow(mask, cmap='gray', interpolation='nearest')
    # Let's remove the axis labels, they clutter the image.
    for ax in fig.axes:
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_yticks([])
        ax.set_xticks([])
    plt.show()

def image_Augmentation(image, class_name, image_num):
    try:
        if not (os.path.isdir(class_name)):
            os.makedirs(os.path.join(class_name))
    except OSError as e:
        if e.errno != e.errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise

    aug = ImageDataGenerator(
        rotation_range=5,
        width_shift_range=0.05,
        height_shift_range=0.05,
        horizontal_flip=False,
        shear_range=0.05,
        zoom_range=0.05,
        fill_mode="nearest"
    )
    img = numpy.array(image).reshape(1, 200, 64, 1)
    imageGen = aug.flow(
        img,
        batch_size=1,
        save_format='png',
        save_to_dir='./' + class_name
    )

    total = 0
    for _ in imageGen:
        total += 1
        if total == image_num:
            break
