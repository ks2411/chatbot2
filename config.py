# config.py

# Определение используемых моделей
GPT_4_0 = "gpt-4o"
GPT_4_MINI = "gpt-4o-mini"
GPT_4_TURBO = "gpt-4-1106-preview"
GPT_35_TURBO = "gpt-3.5-turbo-1106"
MODEL = GPT_4_MINI  # Выбранная модель

# Настройки базы знаний
VECTOR_DB = ''
NUM_CHUNKS = 7
CHUNK_SIZE = 200
CHUNK_OVERLAP = 0
TEMP = 0
VERBOSE = 1

# URL базы знаний
KNOWLEDGE_DB_URL = 'https://docs.google.com/document/d/1o1wDpGLLRupCIsy7BLctJLxs9UHCZMZuCfMLH49VSg0/edit?usp=sharing'

# Переменные для хранения истории сообщений
history_chat = []
history_user = []
history_manager = []

# Переменные для хранения выделенных сущностей
needs_extractor = []
benefits_extractor = []
objection_detector = []
resolved_objection_detector = []
tariff_detector = []

# Основные переменные ответа
main_answer = ''
summarized_dialog = ''