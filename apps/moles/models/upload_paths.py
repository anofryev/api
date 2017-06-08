from skiniq.utils import generate_filename


def distant_photo_path(instance, filename):
    anatomical_site = instance.anatomical_site
    patient = instance.patient
    doctor = patient.doctor

    new_filename = generate_filename(
        filename,
        prefix='{0}_{1}_regional_photo'.format(
            instance.pk, anatomical_site.pk))

    return '/'.join([
        'users', str(doctor.pk),
        'patients', str(patient.pk),
        'anatomical_sites', str(instance.pk),
        'regional_photo', new_filename,
    ])


def mole_image_photo_path(instance, filename):
    mole_image = instance
    mole = mole_image.mole
    patient = mole.patient
    doctor = patient.doctor

    new_filename = generate_filename(
        filename,
        prefix='{0}_photo'.format(mole.pk))

    return '/'.join([
        'users', str(doctor.pk),
        'patients', str(patient.pk),
        'skin_images', str(mole.pk), new_filename,
    ])
