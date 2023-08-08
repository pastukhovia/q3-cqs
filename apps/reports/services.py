import subprocess
from datetime import datetime
from reports.models import Status


class ReportReviewService:
    def __init__(self, report):
        self.report = report

    def _get_errors_list(self):
        var = subprocess.Popen(['flake8', f'./{self.report.file.file}'], stdout=subprocess.PIPE)
        errors_list = (var.communicate()[0].decode('utf-8').split('\n'))
        return errors_list

    def save_results(self):
        result = []
        errors_list = self._get_errors_list()
        for error in errors_list[:-1]:
            error = error.split(':')
            result.append(
                {
                    'line': error[1],
                    'column': error[2],
                    'error': ''.join(error[3:]),
                    'check_time': datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
                }
            )

        self.report.result = result
        self.report.status = Status.reviewed
        self.report.save()
