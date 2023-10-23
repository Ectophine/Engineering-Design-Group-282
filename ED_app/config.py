from datetime import datetime

# Global Configurations
timeline = ['Daily', 'Weekly', 'Monthly']
usage = ['Water Usage', 'Gas Usage', 'Both']
view = ['Amount', 'Cost']

no_data_text = ('The app is still calculating your baseline. Keep showering normally with the shower sensor attached, '
                'and check back later to track your usage! The dashboard will be available after 7 showers.')

last_update_time = datetime.now()