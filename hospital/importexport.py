from import_export import resources
from django.dispatch import receiver
from import_export.signals import post_import
from import_export.results import RowResult

from hospital.models import Patient


class PatientResource(resources.ModelResource):
    def get_field_names(self):
        names = []
        for field in self.get_fields():
            names.append(self.get_field_name(field))
        return names

    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(PatientResource, self).import_row(
            row, instance_loader, **kwargs
        )

        if import_result.import_type == RowResult.IMPORT_TYPE_ERROR:
            import_result.diff = [
                row.get(name, '') for name in self.get_field_names()
            ]

            # Add a column with the error message
            import_result.diff.append(
                "Errors: {}".format(
                    [err.error for err in import_result.errors]
                )
            )
            # clear errors and mark the record to skip
            import_result.errors = []
            import_result.import_type = RowResult.IMPORT_TYPE_SKIP

        return import_result

    class Meta:
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        model = Patient


@receiver(post_import, sender=Patient)
def _post_import(sender, **kwargs):
    print('aaaaaaaaaaaaaaaaaaaaaaa')
