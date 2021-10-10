from settings.settings import *


DEBUG = False
CELERY_TASK_ALWAYS_EAGER = True  # 全てのtaskが機能としてのみ動くようにする。テストなのでceleryを働かさない。
