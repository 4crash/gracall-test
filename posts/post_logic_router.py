from settings import settings
# import PostLogic by settings directive settings.storage_type, save posts into list or Database
PostLogic = getattr(__import__(
    settings.storage_type, fromlist=["PostLogic"]), "PostLogic")

