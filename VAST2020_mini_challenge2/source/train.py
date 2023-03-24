from nets.unet import mobilenet_unet
from keras.optimizers import Adam
from keras.callbacks import TensorBoard, ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from PIL import Image
import keras
from keras import backend as K
import numpy as np
from imgChange import get_random_data,rand,letterbox_image
import matplotlib.pyplot as plt

NCLASSES = 2
HEIGHT = 416
WIDTH = 416

def training_vis(hist):
    loss = hist.history['loss']
    val_loss = hist.history['val_loss']
    acc = hist.history['acc']  # new version => hist.history['accuracy']
    val_acc = hist.history['val_acc']  # => hist.history['val_accuracy']

    # make a figure
    fig = plt.figure(figsize=(8, 4))
    # subplot loss
    ax1 = fig.add_subplot(121)
    ax1.plot(loss, label='train_loss')
    ax1.plot(val_loss, label='val_loss')
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('Loss')
    ax1.set_title('Loss on Training and Validation Data')
    ax1.legend()
    # subplot acc
    ax2 = fig.add_subplot(122)
    ax2.plot(acc, label='train_acc')
    ax2.plot(val_acc, label='val_acc')
    ax2.set_xlabel('Epochs')
    ax2.set_ylabel('Accuracy')
    ax2.set_title('Accuracy  on Training and Validation Data')
    ax2.legend()
    plt.tight_layout()
    plt.show()

def generate_arrays_from_file(lines,batch_size,className):
    # 获取总长度
    n = len(lines)
    i = 0
    while 1:
        X_train = []
        Y_train = []
        # 获取一个batch_size大小的数据
        for _ in range(batch_size):
            if i==0:
                np.random.shuffle(lines)
            name = lines[i].split(',')[0]

            # 从文件中读取图像
            img = Image.open(r"C:\Users\FYC\Desktop\TNSCUI2020_train\TNSCUI2020_train\24IMAGE" + '/' + name)
            #进行边界填充，防止形变失真
            img, _, _ = letterbox_image(img, (WIDTH, HEIGHT), "jpg")

            img = img.resize((WIDTH,HEIGHT))
            img = np.array(img)
            img = img/255
            X_train.append(img)

            # 从文件中读取图像
            img = Image.open(r"C:\Users\FYC\Desktop\TNSCUI2020_train\TNSCUI2020_train\24MASK" + '/' + name)
            #进行边界填充，防止形变失真，填充皆为(0,0,0)
            img, _, _ = letterbox_image(img, (WIDTH, HEIGHT), "png")

            img = img.resize((int(WIDTH/2),int(HEIGHT/2)))
            img = np.array(img)
            seg_labels = np.zeros((int(HEIGHT/2),int(WIDTH/2),NCLASSES))
            for c in range(NCLASSES):
                seg_labels[: , : , c ] = (img[:,:,0] == c ).astype(int)
            seg_labels = np.reshape(seg_labels, (-1,NCLASSES))
            Y_train.append(seg_labels)

            # 读完一个周期后重新开始
            i = (i+1) % n
        yield (np.array(X_train),np.array(Y_train))

def loss(y_true, y_pred):
    loss = K.categorical_crossentropy(y_true,y_pred)
    return loss

def AllTrain():
    log_dir = "logs/"

    model = mobilenet_unet(n_classes=NCLASSES,input_height=HEIGHT, input_width=WIDTH)
    model.load_weights(".\models\mobilenet_1_0_224_tf_no_top.h5",by_name=True)

    with open(r"C:\Users\FYC\Desktop\allKinds.txt","r") as f:#训练所有类
        txtlines = f.readlines()
    for i in range(len(txtlines)):
        txtName = r".\dataset2/" + txtlines[i].strip() + ".txt"
        with open(txtName, "r") as f:
            lines = f.readlines()

        np.random.seed(10101)
        np.random.shuffle(lines)
        np.random.seed(None)

        # 90%用于训练，10%用于估计。
        num_val = int(len(lines) * 0.1)
        num_train = len(lines) - num_val

        # 保存的方式，5世代保存一次
        checkpoint_period = ModelCheckpoint(
            log_dir + 'ep{epoch:03d}-loss{loss:.3f}-val_loss{val_loss:.3f}.h5',
            monitor='val_loss',
            save_weights_only=True,
            save_best_only=True,
            period=5
        )
        # 学习率下降的方式，val_loss三次不下降就下降学习率继续训练
        reduce_lr = ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            verbose=1
        )
        # 是否需要早停，当val_loss一直不下降的时候意味着模型基本训练完毕，可以停止
        early_stopping = EarlyStopping(
            monitor='val_loss',
            min_delta=0,
            patience=10,
            verbose=1
        )

        # 交叉熵
        model.compile(loss=loss,
                      optimizer=Adam(lr=1e-3),
                      metrics=['accuracy'])
        batch_size = 4
        print('Train on {} samples, val on {} samples, with batch size {}.'.format(num_train, num_val, batch_size))

        # 开始训练
        hist = model.fit_generator(generate_arrays_from_file(lines[:num_train], batch_size, txtlines[i].strip()),
                            steps_per_epoch=max(1, num_train // batch_size),
                            validation_data=generate_arrays_from_file(lines[num_train:], batch_size, txtlines[i].strip()),
                            validation_steps=max(1, num_val // batch_size),
                            epochs=18,
                            initial_epoch=0,
                            callbacks=[checkpoint_period, reduce_lr])

        h5saveName = log_dir + txtlines[i].strip() + ".h5"
        model.save_weights(h5saveName)
    f.close()
        # training_vis(hist)
        # break


if __name__ == "__main__":
    # AllTrain()

    log_dir = "logs/"
    # 获取model
    model = mobilenet_unet(n_classes=NCLASSES,input_height=HEIGHT, input_width=WIDTH)
    # model.summary()
    model.load_weights(".\models\mobilenet_1_0_224_tf_no_top.h5",by_name=True)
    # model.summary()

    # 打开数据集的txt
    with open(r"C:\Users\FYC\Desktop\TNSCUI2020_train\TNSCUI2020_train\train1.txt","r") as f:
        lines = f.readlines()

    # 打乱行，这个txt主要用于帮助读取数据来训练
    # 打乱的数据更有利于训练
    np.random.seed(10101)
    np.random.shuffle(lines)
    np.random.seed(None)

    # 90%用于训练，10%用于估计。
    num_val = int(len(lines)*0.1)
    num_train = len(lines) - num_val

    # 保存的方式，1世代保存一次
    checkpoint_period = ModelCheckpoint(
                                    log_dir + 'ep{epoch:03d}-loss{loss:.3f}-val_loss{val_loss:.3f}.h5',
                                    monitor='val_loss',
                                    save_weights_only=True,
                                    save_best_only=True,
                                    period=1
                                )
    # 学习率下降的方式，val_loss三次不下降就下降学习率继续训练
    reduce_lr = ReduceLROnPlateau(
                            monitor='val_loss',
                            factor=0.5,
                            patience=3,
                            verbose=1
                        )
    # 是否需要早停，当val_loss一直不下降的时候意味着模型基本训练完毕，可以停止
    early_stopping = EarlyStopping(
                            monitor='val_loss',
                            min_delta=0,
                            patience=10,
                            verbose=1
                        )

    # 交叉熵
    model.compile(loss = loss,
            optimizer = Adam(lr=1e-3),
            metrics = ['accuracy'])
    batch_size = 3
    print('Train on {} samples, val on {} samples, with batch size {}.'.format(num_train, num_val, batch_size))

    # 开始训练
    hist = model.fit_generator(generate_arrays_from_file(lines[:num_train], batch_size,"birdCall"),
            steps_per_epoch=max(1, num_train//batch_size),
            validation_data=generate_arrays_from_file(lines[num_train:], batch_size,"birdCall"),
            validation_steps=max(1, num_val//batch_size),
            epochs=20,
            initial_epoch=0,
            callbacks=[checkpoint_period, reduce_lr])
    model.save_weights(log_dir+'CANCER.h5')
    training_vis(hist)
    f.close()