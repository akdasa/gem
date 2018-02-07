from gem.db import comments, users


class CommentsWidget:
    """The widget to display a list of comments of specified proposal and stage."""

    def __init__(self, proposal_id, stage, anonymous=False):
        self.__comments = []
        self.__proposal_id = proposal_id
        self.__stage = stage
        self.__anonymous = anonymous
        self.update()

    def update(self):
        data = comments.of(self.__proposal_id, self.__stage)
        self.__comments = list(map(lambda x: self.__map(x), data))

    def view(self):
        return {
            "list": self.__comments,
            "stage": self.__stage
        }

    def __map(self, x):
        user = None
        if not self.__anonymous:
            user = users.get(x.user_id)
        return {
            "content": x.content,
            "type": x.type,
            "quote": x.quote,
            "user": user.name if user else None,
            "timestamp": x.get("timestamp", None),
            "role": user.role if user else None
        }