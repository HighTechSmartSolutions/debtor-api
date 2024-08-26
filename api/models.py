from django.db import models


class VerificationV(models.Model):
    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    persons_identity_card1 = models.TextField(blank=True, null=True)
    persons_identity_card2 = models.TextField(blank=True, null=True)
    application_date = models.DateTimeField(blank=True, null=True)
    phone_flag = models.IntegerField(blank=True, null=True)
    email_flag = models.IntegerField(blank=True, null=True)
    id1_flag = models.IntegerField(blank=True, null=True)
    id2_flag = models.IntegerField(blank=True, null=True)
    cases_num = models.IntegerField(blank=True, null=True)
    active_cases_num = models.IntegerField(blank=True, null=True)
    max_debtor_contact_date = models.DateTimeField(blank=True, null=True)
    min_debtor_contact_date = models.DateTimeField(blank=True, null=True)
    max_delivery_date = models.DateTimeField(blank=True, null=True)
    min_delivery_date = models.DateTimeField(blank=True, null=True)
    total_original_debt = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    total_actual_debt = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    max_hist_dpd = models.IntegerField(blank=True, null=True)
    fintech_max_cur_dpd = models.IntegerField(blank=True, null=True)
    max_payment_date = models.DateTimeField(blank=True, null=True)
    payments_number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'verification_v'


class ClientV(models.Model):
    client_id = models.IntegerField(primary_key=True)
    company_id = models.IntegerField(blank=True, null=True)
    descr = models.CharField(max_length=500, blank=True, null=True)
    return_limit = models.IntegerField(blank=True, null=True)
    ip = models.CharField(db_column='IP', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'client_v'
