


class LikedDislikedByMixin:
    """Provides liked/disliked checking methods for models that has related Like objects qs as likes"""

    def liked_by(self, user):
        if user.is_authenticated:
            return self.likes.filter(author=user, dislike=False).exists()
        return False

    def disliked_by(self, user):
        if user.is_authenticated:
            return self.likes.filter(author=user, dislike=True).exists()
        return False
