from datetime import datetime

class HelperUtil:
    def stringToDate(self, dateString):
        return datetime.strptime(dateString, '%Y-%m-%d').date()