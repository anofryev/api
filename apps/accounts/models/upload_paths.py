from skin.utils import generate_filename


def doctor_photo_path(instance, filename):
    doctor = instance
    new_filename = generate_filename(
        filename, prefix='{0}_profile_pic'.format(doctor.pk))

    return '/'.join([
        'users', str(doctor.pk),
        'profile_picture', new_filename])


def patient_photo_path(instance, filename):
    new_filename = generate_filename(
        filename, prefix='{0}_profile_pic'.format(instance.pk))

    return '/'.join([
        'patients', str(instance.pk),
        'profile_picture', new_filename])


def patient_consent_signature_path(instance, filename):
    consent = instance
    patient = instance.patient
    new_filename = generate_filename(
        filename, prefix='{0}_signature'.format(consent.pk))

    return '/'.join([
        'patients', str(patient.pk),
        'consent', new_filename])
