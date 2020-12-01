from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import cv2 as cv
import tkinter
import tkinter.filedialog
from PIL import Image, ImageTk
import numpy as np



import argparse
import os.path
import re
import sys
import tarfile

import numpy as np
from six.moves import urllib
import tensorflow as tf

#界面设置
window = tkinter.Tk()
window.title('垃圾分类识别界面')
window.geometry('350x400')

#下面这个可以展开全屏
#window.state("zoomed")

#固定窗口，使界面不可放大或缩小
window.resizable(0, 0)
var1 = tkinter.StringVar()
#弄个花里花俏一点的界面增加视觉效果而已
#T = tkinter.Label(window, text="25+100=", textvariable=var1, bg="lightGreen", fg="DimGray", anchor="se")
#T.place(x=0, y=0, width=350, height=120)

#显示图片路径以及识别结果的窗口
tkinter.Label(window, text='图片地址为: ').place(x=50, y=150)
tkinter.Label(window, text='识别结果为: ').place(x=50, y=190)
var_user_name = tkinter.StringVar()
entry_user_name = tkinter.Entry(window, textvariable=var_user_name)
entry_user_name.place(x=120, y=150)
var_user_pd = tkinter.StringVar()
entry_user_pd = tkinter.Entry(window, textvariable=var_user_pd)
entry_user_pd.place(x=120, y=190)

FLAGS = None

# pylint: disable=line-too-long
DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'


# pylint: enable=line-too-long


class NodeLookup(object):
    """Converts integer node ID's to human readable labels."""

    def __init__(self,
                 uid_chinese_lookup_path,
                 model_dir,
                 label_lookup_path=None,
                 uid_lookup_path=None):
        if not label_lookup_path:
            label_lookup_path = os.path.join(
                model_dir, 'imagenet_2012_challenge_label_map_proto.pbtxt')
        if not uid_lookup_path:
            uid_lookup_path = os.path.join(
                model_dir, 'imagenet_synset_to_human_label_map.txt')
        # self.node_lookup = self.load(label_lookup_path, uid_lookup_path)
        self.node_lookup = self.load_chinese_map(uid_chinese_lookup_path)

    def load(self, label_lookup_path, uid_lookup_path):
        """Loads a human readable English name for each softmax node.
        Args:
          label_lookup_path: string UID to integer node ID.
          uid_lookup_path: string UID to human-readable string.
        Returns:
          dict from integer node ID to human-readable string.
        """
        if not tf.gfile.Exists(uid_lookup_path):
            tf.logging.fatal('File does not exist %s', uid_lookup_path)
        if not tf.gfile.Exists(label_lookup_path):
            tf.logging.fatal('File does not exist %s', label_lookup_path)

        # Loads mapping from string UID to human-readable string
        proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
        uid_to_human = {}
        # p = re.compile(r'[n\d]*[ \S,]*')
        p = re.compile(r'(n\d*)\t(.*)')
        for line in proto_as_ascii_lines:
            parsed_items = p.findall(line)
            print(parsed_items)
            uid = parsed_items[0]
            human_string = parsed_items[1]
            uid_to_human[uid] = human_string

        # Loads mapping from string UID to integer node ID.
        node_id_to_uid = {}
        proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
        for line in proto_as_ascii:
            if line.startswith('  target_class:'):
                target_class = int(line.split(': ')[1])
            if line.startswith('  target_class_string:'):
                target_class_string = line.split(': ')[1]
                node_id_to_uid[target_class] = target_class_string[1:-2]

        # Loads the final mapping of integer node ID to human-readable string
        node_id_to_name = {}
        for key, val in node_id_to_uid.items():
            if val not in uid_to_human:
                tf.logging.fatal('Failed to locate: %s', val)
            name = uid_to_human[val]
            node_id_to_name[key] = name

        return node_id_to_name

    def load_chinese_map(self, uid_chinese_lookup_path):
        # Loads mapping from string UID to human-readable string
        proto_as_ascii_lines = tf.gfile.GFile(uid_chinese_lookup_path).readlines()
        uid_to_human = {}
        p = re.compile(r'(\d*)\t(.*)')
        for line in proto_as_ascii_lines:
            parsed_items = p.findall(line)
            # print(parsed_items)
            uid = parsed_items[0][0]
            human_string = parsed_items[0][1]
            uid_to_human[int(uid)] = human_string

        return uid_to_human

    def id_to_string(self, node_id):
        if node_id not in self.node_lookup:
            return ''
        return self.node_lookup[node_id]


def create_graph(model_dir):
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(os.path.join(
            model_dir, 'classify_image_graph_def.pb'), 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(image):
    """Runs inference on an image.
    Args:
      image: Image file name.
    Returns:
      Nothing
    """
    if not tf.gfile.Exists(image):
        tf.logging.fatal('File does not exist %s', image)
    image_data = tf.gfile.FastGFile(image, 'rb').read()

    # Creates graph from saved GraphDef.
    create_graph(FLAGS.model_dir)

    with tf.Session() as sess:
        # Some useful tensors:
        # 'softmax:0': A tensor containing the normalized prediction across
        #   1000 labels.
        # 'pool_3:0': A tensor containing the next-to-last layer containing 2048
        #   float description of the image.
        # 'DecodeJpeg/contents:0': A tensor containing a string providing JPEG
        #   encoding of the image.
        # Runs the softmax tensor by feeding the image_data as input to the graph.
        softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        # Creates node ID --> chinese string lookup.
        node_lookup = NodeLookup(uid_chinese_lookup_path='./data/imagenet_2012_challenge_label_chinese_map.pbtxt', \
                                 model_dir=FLAGS.model_dir)

        top_k = predictions.argsort()[-FLAGS.num_top_predictions:][::-1]
        for node_id in top_k:
            human_string = node_lookup.id_to_string(node_id)
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))
            # print('node_id: %s' %(node_id))


def maybe_download_and_extract():
    """Download and extract model tar file."""
    dest_directory = FLAGS.model_dir
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
    filename = DATA_URL.split('/')[-1]
    filepath = os.path.join(dest_directory, filename)
    if not os.path.exists(filepath):
        def _progress(count, block_size, total_size):
            sys.stdout.write('\r>> Downloading %s %.1f%%' % (
                filename, float(count * block_size) / float(total_size) * 100.0))
            sys.stdout.flush()

        filepath, _ = urllib.request.urlretrieve(DATA_URL, filepath, _progress)
        print()
        statinfo = os.stat(filepath)
        print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')
    tarfile.open(filepath, 'r:gz').extractall(dest_directory)

#打开文件函数
def choose_fiel():
    selectFileName = tkinter.filedialog.askopenfilename(title='选择文件')  # 选择文件
    var_user_name.set(selectFileName)

#识别图片数字函数
def main(_):

    maybe_download_and_extract()
    image = (FLAGS.image_file if FLAGS.image_file else
                os.path.join(FLAGS.model_dir, 'C:/Users/luo/Desktop/rafuse_recognize/img/2.png'))  # cropped_panda.jpg
    run_inference_on_image(image)
    var_user_pd.set(result[0][0])

#清零函数，不过没啥意义，就想把界面弄的对称一点而已
def delete():      #删除函数
    content = var_user_pd.get()
    var_user_pd.set(content[0:len(content) - 1])

#显示所要识别的图片函数
def showImg(img1):
    #canvas = tkinter.Canvas(window, height=400, width=1000)
    load = Image.open(img1)
    render = ImageTk.PhotoImage(load)
    img = tkinter.Label(image=render)
    img.image = render
    #canvas.create_image(0, 0, anchor='nw', image=render)
    #canvas.pack(side='bottom')
    img.place(x=160, y=120)

#按钮
submit_button = tkinter.Button(window, text="选择文件", command=choose_fiel).place(x=50, y=250)
submit_button = tkinter.Button(window, text="清除数据", command=delete()).place(x=50, y=300)
submit_button = tkinter.Button(window, text="显示图片", command=lambda: showImg(entry_user_name.get())).place(x=219, y=250)
submit_button = tkinter.Button(window, text="开始识别", command=lambda: main(entry_user_name.get())).place(x=219, y=300)


window.mainloop()