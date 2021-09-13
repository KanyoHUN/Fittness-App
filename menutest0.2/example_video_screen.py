from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.videoplayer import VideoPlayer
import config
from video_list import VideoScreen


class ExampleVideo(VideoScreen):

    def create_display(self):
        for child in self.children:
            if isinstance(child, BoxLayout):
                box = child
                video = VideoPlayer(id='video', allow_stretch=True)
                button = Button(id='back_button', text='Back to Editor', size_hint=(1, .2), disabled=True)
                button.on_press = self.on_back_to_videos_button_press
                box.add_widget(video)
                box.add_widget(button)

    def on_back_to_videos_button_press(self):
        self.manager.current = config.previous_screen
        self.removable = self.ids.video.source
        self.ids.video.source = ''
        self.ids.video.state = 'stop'
        self.delete_previous_video()
        self.ids.back_button.disabled = True
