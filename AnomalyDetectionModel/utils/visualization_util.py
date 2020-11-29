import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils.video_util import *
from firebase_admin import credentials,firestore, messaging
import firebase_admin
import google.cloud
from datetime import datetime



def getCurrentTime():
    time = str(datetime.now().time()).split('.')[0].split(':')[:-1]
    date = str(datetime.now().date()).split('-')

    timej = "".join(t for t in time)
    datej = "".join(d for d in date)

    return datej + timej


cred = credentials.Certificate("./star.json")
app = firebase_admin.initialize_app(cred)
store = firestore.client()
doc_ref = store.collection(u'users').where(u'userAuthId', u'==','rish1234').stream()

docId = ""
docToken = ""
for doc in doc_ref:
    print(doc)
    docId = doc.id
    data = doc.to_dict()
    docToken = data['userToken']
    print(data['userName'])


def visualize_clip(clip, convert_bgr=False, save_gif=False, file_path=None):
    num_frames = len(clip)
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)

    def update(i):
        if convert_bgr:
            frame = cv2.cvtColor(clip[i], cv2.COLOR_BGR2RGB)
        else:
            frame = clip[i]
        plt.imshow(frame)
        return plt

    # FuncAnimation will call the 'update' function for each frame; here
    # animating over 10 frames, with an interval of 20ms between frames.
    anim = FuncAnimation(fig, update, frames=np.arange(0, num_frames), interval=1)
    if save_gif:
        anim.save(file_path, dpi=80, writer='imagemagick')
    else:
        # plt.show() will just loop the animation forever.
        plt.show()


def visualize_predictions(video_path, predictions, save_path, video_name):
    vid = 'http://192.168.137.1:5000/files/'+video_name+'.gif'

    frames = get_video_frames(video_path)
    assert len(frames) == len(predictions)

    fig, ax = plt.subplots(figsize=(5, 5))
    fig.set_tight_layout(True)

    fig_frame = plt.subplot(2, 1, 1)
    fig_prediction = plt.subplot(2, 1, 2)
    fig_prediction.set_xlim(0, len(frames))
    fig_prediction.set_ylim(0, 1.15)

    def update(i):
        flag=0
        start_time = 0
        end_time = 0
        frame = frames[i]
        x = range(0, i)
        y = predictions[0:i]
        fig_prediction.plot(x, y, '-')
        fig_frame.imshow(frame)
        if i>=len(frames)-40:
            for j in range(0,i):
                if(y[j]>0.7):
                    time = x[j]/29.63
                    print("predection = {} at frame = {} sec".format(y[j],x[j]/29.63))
                    if flag == 0:
                        start_time = time
                    else:
                        end_time = time
                    flag = 1
        if flag==1:

            camid = '69'
            currTime = getCurrentTime()
            print(currTime)
            id = currTime + '-' + camid

            data = {
                'eventId': id,
                'eventLatlng': '28.634598 , 77.447320',
                'eventStartTime': str(start_time),
                'eventGifUrl': vid,
                'eventEndTime': str(end_time)
            }

            message = messaging.Message(
                data=data,
                token=docToken
            )

            res = messaging.send(message)
            print("NOTIFICATION: " + res)

            print(docId)

            store.collection(u'users').document(u'{}'.format(docId)).collection(u'notifications').document(id).set(data)
            store.collection(u'cameras').document(camid).collection(u'history').document(currTime).set(data)




        return plt

    # FuncAnimation will call the 'update' function for each frame; here
    # animating over 10 frames, with an interval of 20ms between frames.

    anim = FuncAnimation(fig, update, frames=np.arange(0, len(frames), 40), interval=1, repeat=False)

    if save_path:
        anim.save(save_path, dpi=200, writer='imagemagick')
    else:
        plt.show()

    return


