import os
from c3d import *
from classifier import *
from utils.visualization_util import *

def run_demo():
    name=0
    path, dirs, files = next(os.walk("E:\sih\AnomalyDetection_CVPR18\input"))
    file_count = len(files)

    while name<file_count:
      video_name = os.path.basename(cfg.sample_video_path+str(name)+'.mp4').split('.')[0]

      # read video
      video_clips, num_frames = get_video_clips(cfg.sample_video_path+str(name)+'.mp4')

      print("Number of clips in the video : ", len(video_clips))

      # build models
      feature_extractor = c3d_feature_extractor()
      classifier_model = build_classifier_model()

      print("Models initialized")

      # extract features
      rgb_features = []
      for i, clip in enumerate(video_clips):
          clip = np.array(clip)
          if len(clip) < params.frame_count:
              continue

          clip = preprocess_input(clip)
          rgb_feature = feature_extractor.predict(clip)[0]
          rgb_features.append(rgb_feature)

          print("Processed clip : ", i)

      rgb_features = np.array(rgb_features)

      # bag features
      rgb_feature_bag = interpolate(rgb_features, params.features_per_bag)

      # classify using the trained classifier model
      predictions = classifier_model.predict(rgb_feature_bag)

      predictions = np.array(predictions).squeeze()

      predictions = extrapolate(predictions, num_frames)

      save_path = os.path.join(cfg.output_folder, video_name + '.gif')
      # visualize predictions
      visualize_predictions(cfg.sample_video_path+str(name)+'.mp4', predictions, save_path, video_name)
      name = name + 1
if __name__ == '__main__':
    run_demo()