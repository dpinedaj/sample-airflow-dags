from airflow.plugins_manager import AirflowPlugin

from .hooks import LivyBatchHook
from .operators import LivyBatchOperator
from .sensors import LivyBatchSensor






class LivyPlugin(AirflowPlugin):
    name = 'livy_plugin'
    hooks = [LivyBatchHook]
    operators = [LivyBatchOperator]
    sensors = [LivyBatchSensor]