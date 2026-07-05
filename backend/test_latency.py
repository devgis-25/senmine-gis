import time
from django.db import connection

t0 = time.time()
with connection.cursor() as cursor:
    cursor.execute("SELECT 1")
    cursor.fetchone()
print(f"Latence single query: {time.time()-t0:.3f}s")