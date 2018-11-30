class SqlBuilder:

    base_query = "Select {column} from logs where lower(resource_name) = lower('{resource_name}')"

    def build_query(self, column=None, resource_name=None, time_identifier=None):
        if column is None or resource_name is None:
            raise AssertionError('Column Name and resource name are mandatory')

        query = self.base_query.format(column=column, resource_name=resource_name)
        if time_identifier is not None:
            return query + self.from_time_identifier(self, time_identifier.upper())

        return query

    @staticmethod
    def from_time_identifier(self, time_identifier=None):
        if time_identifier == 'MORNING':
            return "and event_time::time BETWEEN '00:00:00'::time and '11:59:59'::time"
        if time_identifier == 'AFTERNOON':
            return "and event_time::time BETWEEN '12:00:00'::time and '16:00:00'::time"
        if time_identifier == 'EVENING':
            return "and event_time::time BETWEEN '16:00:01'::time and '20:00:00'::time"
        if time_identifier == 'NIGHT':
            return "and event_time::time BETWEEN '20:00:01'::time and '23:59:59'::time"