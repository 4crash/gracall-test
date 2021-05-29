from settings import settings

PostLogic = getattr(__import__(
    settings.storage_type, fromlist=["PostLogic"]), "PostLogic")

