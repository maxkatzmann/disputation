from manim import Group, SurroundingRectangle


class Layout:
    @staticmethod
    def move_arranged_mobjects_to(*mobjects, target):
        """Given a set of mobjects, they are moved such that
        their bounding box is centered at the passed
        center, while their relative positions are kept
        intact.
        """
        group = Group(*mobjects)
        bounding_box = SurroundingRectangle(group)
        surrounding_group = Group(group, bounding_box)
        surrounding_group.move_to(target)

        return surrounding_group
