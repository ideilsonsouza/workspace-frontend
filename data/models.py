from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class System(models.Model):
    start_server_control = models.BooleanField(default=False, null=True, blank=True)
    start_send_backup = models.BooleanField(default=False, null=True, blank=True)
    error_upload_count = models.IntegerField(default=0,null=True, blank=True)
    error_upload_max = models.IntegerField(default=30,null=True, blank=True)
    error_server_count = models.IntegerField(default=0,null=True, blank=True)
    error_server_max = models.IntegerField(default=30,null=True, blank=True)
    
    def clean(self):
        # Verifica se é uma nova instância e se já existe um dispositivo
        if not self.pk and System.objects.exists():
            raise ValidationError('Only one Device instance is allowed.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Valida o objeto antes de salvar
        super(System, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Evita a exclusão se for o único objeto
        if System.objects.count() == 1:
            raise ValidationError('Cannot delete the only System instance.')
        super(System, self).delete(*args, **kwargs)
    

class Device(models.Model):
    company = models.BigIntegerField(null=True, blank=True)
    description = models.CharField(max_length=196, null=True, blank=True)
    enabled = models.BooleanField(default=False, null=True, blank=True)
    licensed = models.BooleanField(default=False, null=True, blank=True)
    license_key = models.TextField(null=True, blank=True)
    ssh_key = models.TextField(null=True, blank=True)
    expired = models.BooleanField(default=False, null=True, blank=True)

    sleep_boot = models.SmallIntegerField(default=60, null=True, blank=True)
    start_wifi = models.BooleanField(default=True, null=True, blank=True)
    
    sleep_readings = models.SmallIntegerField(default=60, null=True, blank=True)
    start_readings = models.BooleanField(default=False, null=True, blank=True)
     
    dns_main = models.CharField(max_length=230, null=True, blank=True)
    dns_main_token = models.CharField(max_length=230, null=True, blank=True)
    dns_main_token_type = models.CharField(max_length=60, null=True, blank=True)
    
    sleep_upload = models.SmallIntegerField(default=20, null=True, blank=True)
    start_upload = models.BooleanField(default=False, null=True, blank=True)
    dns_upload = models.CharField(max_length=230, null=True, blank=True)
    dns_upload_token = models.CharField(max_length=230, null=True, blank=True)
    dns_upload_token_type = models.CharField(max_length=60, null=True, blank=True)
    
    sleep_feedback = models.SmallIntegerField(default=600, null=True, blank=True)
    start_feedback = models.BooleanField(default=False, null=True, blank=True)
    dns_feedback = models.CharField(max_length=230, null=True, blank=True)
    dns_feedback_token = models.CharField(max_length=230, null=True, blank=True)
    dns_feedback_token_type = models.CharField(max_length=60, null=True, blank=True)

    ssh_remote_host = models.CharField(max_length=230,default='vps.zaimineracao.com.br',null=True, blank=True)
    ssh_port = models.IntegerField(default=22,null=True, blank=True)
    ssh_remote_user = models.CharField(max_length=100, default='zabe',null=True, blank=True)
    ssh_tunnel_port = models.IntegerField(default=2222,null=True, blank=True)
    ssh_tunnel = models.BooleanField(default=False, null=True, blank=True)

    license_check_at = models.DateField(null=True, blank=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Verifica se é uma nova instância e se já existe um dispositivo
        if not self.pk and Device.objects.exists():
            raise ValidationError('Only one Device instance is allowed.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Valida o objeto antes de salvar
        super(Device, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Evita a exclusão se for o único objeto
        if Device.objects.count() == 1:
            raise ValidationError('Cannot delete the only Device instance.')
        super(Device, self).delete(*args, **kwargs)


class Source(models.Model):
    name = models.CharField(max_length=196, default='new', null=True, blank=True)
    code = models.BigIntegerField(null=True, blank=True)
    protocol = models.CharField(max_length=30, default='modbus')
    settings = models.JSONField(default=dict, null=True, blank=True)
    last_reading = models.DateTimeField(null=True, blank=True)
    readings = models.JSONField(default=dict, null=True, blank=True)
    enabled = models.BooleanField(default=False, null=True, blank=True)
    connected = models.BooleanField(default=False, null=True, blank=True)
    count_error = models.IntegerField(default=0,null=True, blank=True)
    max_error = models.IntegerField(default=15,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    module = models.CharField(max_length=255)
    type = models.CharField(max_length=30, default='error')
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

class Reading(models.Model):
    reading_created_at = models.DateTimeField()
    values = models.JSONField(default=dict)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Summary(models.Model):
    company = models.BigIntegerField(null=True, blank=True)
    datetime = models.DateTimeField()
    readings = models.JSONField(default=tuple, null=True, blank=True)
    source = models.IntegerField()
    protocol = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SummaryHour(models.Model):
    company = models.BigIntegerField(null=True, blank=True)
    datetime = models.DateTimeField()
    readings = models.JSONField(default=tuple, null=True, blank=True)
    source = models.IntegerField()
    protocol = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LastReading(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    values = models.JSONField(default=dict)

class NetworkConfig(models.Model):
    ip_address = models.CharField(max_length=15)
    subnet_mask = models.CharField(max_length=15)
    gateway = models.CharField(max_length=15)
    dns = models.CharField(max_length=15)
    dhcp_enabled = models.BooleanField(default=True)
