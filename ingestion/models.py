from django.db import models

class SensorData(models.Model):
    auto_id = models.AutoField(primary_key=True)  
    id = models.UUIDField(db_index=True) 
    type = models.UUIDField(db_index=True)
    subtype = models.UUIDField(db_index=True)
    reading = models.BigIntegerField(db_index=True)
    location = models.UUIDField(db_index=True)
    timestamp = models.DateTimeField(db_index=True)

    def __str__(self):
        return f"Sensor {self.id} - Type: {self.type}"
