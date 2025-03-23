from __future__ import annotations

import json
import os
import shutil
from typing import Iterable, Sequence

from manim import (
    DOWN,
    LIGHT_GRAY,
    UP,
    Animation,
    Dot,
    FadeIn,
    FadeOut,
    Group,
    MovingCameraScene,
    Tex,
    Text,
    config,
)


class PresentationSlide(MovingCameraScene):
    def __init__(self, *args, **kwargs):
        self.output_folder = kwargs.pop("output_folder", "./presentation")
        super(PresentationSlide, self).__init__(*args, **kwargs)
        self.slides = list()
        self.current_slide = 1
        self.current_animation = 0
        self.loop_start_animation = None
        self.pause_start_animation = 0

    def play(self, *args, **kwargs):
        super(PresentationSlide, self).play(*args, **kwargs)
        self.current_animation += 1

    def pause(self):
        self.slides.append(
            dict(
                type="slide",
                start_animation=self.pause_start_animation,
                end_animation=self.current_animation,
                number=self.current_slide,
            )
        )
        self.current_slide += 1
        self.pause_start_animation = self.current_animation

    def start_loop(self):
        assert self.loop_start_animation is None, "You cant nest loops"
        self.loop_start_animation = self.current_animation

    def end_loop(self):
        assert (
            self.loop_start_animation is not None
        ), "You have to start a loop before ending it"
        self.slides.append(
            dict(
                type="loop",
                start_animation=self.loop_start_animation,
                end_animation=self.current_animation,
                number=self.current_slide,
            )
        )
        self.current_slide += 1
        self.loop_start_animation = None
        self.pause_start_animation = self.current_animation

    def render(self, *args, **kwargs):
        # We need to disable the caching limit since we rely on intermidiate files
        max_files_cached = config["max_files_cached"]
        config["max_files_cached"] = float("inf")

        super(PresentationSlide, self).render(*args, **kwargs)

        config["max_files_cached"] = max_files_cached

        if not os.path.exists(self.output_folder):
            os.mkdir(self.output_folder)

        files_folder = os.path.join(self.output_folder, "files")
        if not os.path.exists(files_folder):
            os.mkdir(files_folder)

        scene_name = type(self).__name__
        scene_files_folder = os.path.join(files_folder, scene_name)

        if os.path.exists(scene_files_folder):
            shutil.rmtree(scene_files_folder)

        if not os.path.exists(scene_files_folder):
            os.mkdir(scene_files_folder)

        files = list()
        for src_file in self.renderer.file_writer.partial_movie_files:
            dst_file = os.path.join(scene_files_folder, os.path.basename(src_file))
            shutil.copyfile(src_file, dst_file)
            files.append(dst_file)

        f = open(os.path.join(self.output_folder, "%s.json" % (scene_name,)), "w")
        json.dump(dict(slides=self.slides, files=files), f)
        f.close()


class DefaultSlide(PresentationSlide):
    subtitleScale = 0.66
    headerScale = 0.9
    contentScale = 0.66
    contentTexScale = 0.924
    sideNoteScale = 0.5
    sideNoteTexScale = 0.7

    instantAnimationRunTime = 0.1
    defaultAnimationRunTime = 1.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def content(self):
        print("Add content here...")

    # def click(self):
    #     self.pause()
    #     self.play(FadeIn(Dot(radius=0), run_time=0.01))

    # Plays the passed animations at once and inserts a pause afterwards.
    def click(self, *animations: Iterable[Animation]):
        if animations:
            self.play(*animations)

        self.pause()
        self.play(FadeIn(Dot(radius=0), run_time=0.01))

    # Deprecated.
    def click_object(self, obj):
        self.play(FadeIn(obj, run_time=1.0))
        self.click()

    def click_objects(self, objects):
        for obj in objects:
            self.click_object(obj)

    def add_title(self, title_lines, subtitle=None):
        title_texts = [Text(line) for line in title_lines]
        group = Group(*title_texts).arrange(DOWN)
        if subtitle is not None:
            subtitle_text = Text(subtitle).scale(DefaultSlide.subtitleScale)
            group = Group(*title_texts, subtitle_text).arrange(DOWN)

        self.play(FadeIn(group, run_time=0.1))

    def add_header(self, title, with_click=True, run_time=None):
        if run_time is None:
            run_time = DefaultSlide.defaultAnimationRunTime

        text = Text(title).scale(DefaultSlide.headerScale).shift(UP * 3)
        if with_click:
            self.click(FadeIn(text, run_time=run_time))

        return text

    def fade_out(self):
        self.play(
            *[FadeOut(mob, run_time=0.5) for mob in self.mobjects]
            # All mobjects in the screen are saved in self.mobjects
        )

    def construct(self):
        self.content()


class ContentText(Text):
    def __init__(self, *texts, **kwargs):
        super().__init__(*texts, **kwargs)
        self.scale(DefaultSlide.contentScale)


class ContentTex(Tex):
    def __init__(self, *texts, **kwargs):
        super().__init__(*texts, **kwargs)
        self.scale(DefaultSlide.contentTexScale)


class SideNoteText(Text):
    def __init__(self, *texts, **kwargs):
        super().__init__(*texts, color=LIGHT_GRAY, **kwargs)
        self.scale(DefaultSlide.sideNoteScale)


class SideNoteTex(Tex):
    def __init__(self, *texts, **kwargs):
        super().__init__(*texts, color=LIGHT_GRAY, **kwargs)
        self.scale(DefaultSlide.sideNoteTexScale)


class Bullet(Group):
    def __init__(self, text: ContentText, **kwargs):
        # The ghost ensures that the bullet has the maximum text height,
        # such that multiple bullets are aligned evenly.
        ghost = ContentText(
            "jI",
            stroke_opacity=0,
            fill_opacity=0,
        )
        text.align_to(ghost, UP)
        super().__init__(ghost, text, **kwargs)

    @staticmethod
    def group(*texts: Sequence[Text], **kwargs):
        bullets = [Bullet(text) for text in texts]
        bullet_group = Group(*bullets, **kwargs)
        bullet_group.arrange(DOWN)
        return bullet_group, bullets
