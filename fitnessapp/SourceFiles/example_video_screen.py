import config
from video_list import VideoScreen


class ExampleVideo(VideoScreen):

    def on_pre_enter(self, *args):
        self.ids.back_button.text = 'Back To Editor'

    def on_leave(self, *args):
        self.manager.remove_widget(self)
        del self

    def on_back_to_videos_button_press(self):
        self.manager.current = config.previous_screen
        self.removable = self.ids.video.source
        self.ids.video.source = ''
        self.ids.video.state = 'stop'
        self.delete_previous_video()
